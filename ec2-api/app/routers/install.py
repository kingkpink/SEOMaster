from fastapi import APIRouter
from fastapi.responses import PlainTextResponse

router = APIRouter(tags=["install"])

INSTALL_SCRIPT = r'''#!/usr/bin/env bash
# SEO Master CLI — tiny wrapper around the hosted API.
#
# USAGE
#   seo "Audit example.com for title tags"                  # ask a question
#   seo "Check structured data" --context "<html>...</html>" # pass raw context
#   echo "<html>..." | seo "Audit this HTML"                 # pipe anything in
#   seo "Full SEO audit" --dir .                             # scan a local project
#   seo "Full SEO audit" --dir /path/to/my-nextjs-app       # scan a specific folder
#
# The --dir flag collects key SEO-relevant files from a local project directory
# and sends them as context so the API can audit your source code, not just a live URL.

set -euo pipefail

API_URL="${SEO_API_URL:-__API_URL__}"
API_KEY="${SEO_API_KEY}"

if [ -z "$API_KEY" ]; then
  echo "Set your API key first:"
  echo "  export SEO_API_KEY=your-key-here"
  exit 1
fi

if [ -z "${1:-}" ]; then
  echo "Usage: seo \"your question\" [--context \"...\"] [--dir path/to/project]"
  exit 1
fi

MESSAGE="$1"
shift

CONTEXT=""
DIR=""

while [ $# -gt 0 ]; do
  case "$1" in
    --context) CONTEXT="$2"; shift 2 ;;
    --dir)     DIR="$2"; shift 2 ;;
    *)         shift ;;
  esac
done

# If no explicit --context or --dir, read from stdin (pipe)
if [ -z "$CONTEXT" ] && [ -z "$DIR" ] && [ ! -t 0 ]; then
  CONTEXT="$(cat)"
fi

# --dir: collect SEO-relevant files from a local project
if [ -n "$DIR" ]; then
  if [ ! -d "$DIR" ]; then
    echo "Error: $DIR is not a directory"
    exit 1
  fi

  echo "Scanning $DIR for SEO-relevant files..." >&2

  SNAPSHOT=""

  collect() {
    local label="$1" file="$2"
    if [ -f "$file" ]; then
      local size
      size=$(wc -c < "$file" | tr -d ' ')
      if [ "$size" -lt 50000 ]; then
        SNAPSHOT="$SNAPSHOT
--- $label ($file) ---
$(cat "$file")
"
      else
        SNAPSHOT="$SNAPSHOT
--- $label ($file) [truncated — ${size} bytes] ---
$(head -c 30000 "$file")
... (truncated)
"
      fi
    fi
  }

  # package.json / tech stack
  collect "package.json" "$DIR/package.json"
  collect "composer.json" "$DIR/composer.json"

  # Robots & sitemap (static)
  collect "robots.txt" "$DIR/public/robots.txt"
  collect "robots.txt" "$DIR/static/robots.txt"
  collect "sitemap.xml" "$DIR/public/sitemap.xml"

  # Next.js App Router
  for f in "$DIR"/app/layout.{tsx,jsx,ts,js}; do collect "app/layout" "$f"; done
  for f in "$DIR"/app/page.{tsx,jsx,ts,js}; do collect "app/page (homepage)" "$f"; done
  for f in "$DIR"/app/robots.{ts,js}; do collect "app/robots" "$f"; done
  for f in "$DIR"/app/sitemap.{ts,js}; do collect "app/sitemap" "$f"; done
  for f in "$DIR"/app/manifest.{ts,js}; do collect "app/manifest" "$f"; done

  # Next.js Pages Router
  for f in "$DIR"/pages/_app.{tsx,jsx,ts,js}; do collect "pages/_app" "$f"; done
  for f in "$DIR"/pages/_document.{tsx,jsx,ts,js}; do collect "pages/_document" "$f"; done
  for f in "$DIR"/pages/index.{tsx,jsx,ts,js}; do collect "pages/index (homepage)" "$f"; done

  # Nuxt
  for f in "$DIR"/nuxt.config.{ts,js}; do collect "nuxt.config" "$f"; done
  collect "app.vue" "$DIR/app.vue"

  # SvelteKit
  for f in "$DIR"/src/routes/+layout.{svelte,ts,js}; do collect "+layout" "$f"; done
  for f in "$DIR"/src/routes/+page.{svelte,ts,js}; do collect "+page (homepage)" "$f"; done

  # Astro
  collect "astro.config" "$DIR/astro.config.mjs"
  for f in "$DIR"/src/layouts/*.{astro,tsx}; do collect "layout" "$f" 2>/dev/null; done

  # HTML files at root or public
  for f in "$DIR"/index.html "$DIR"/public/index.html; do collect "index.html" "$f"; done

  # next.config / vite.config / svelte.config
  for f in "$DIR"/next.config.{ts,js,mjs}; do collect "next.config" "$f"; done
  for f in "$DIR"/vite.config.{ts,js}; do collect "vite.config" "$f"; done
  collect "svelte.config.js" "$DIR/svelte.config.js"

  # Head / SEO components (common names)
  for f in "$DIR"/components/Head.{tsx,jsx,vue,svelte} \
           "$DIR"/components/SEO.{tsx,jsx,vue,svelte} \
           "$DIR"/components/Meta.{tsx,jsx,vue,svelte} \
           "$DIR"/components/Seo.{tsx,jsx,vue,svelte}; do
    collect "SEO component" "$f" 2>/dev/null
  done

  if [ -z "$SNAPSHOT" ]; then
    echo "Warning: no SEO-relevant files found in $DIR" >&2
  else
    FILECOUNT=$(echo "$SNAPSHOT" | grep -c '^--- ' || true)
    echo "Collected $FILECOUNT file(s), sending to API..." >&2
    CONTEXT="Local project directory: $DIR
Tech stack detection: auto

$SNAPSHOT"
  fi
fi

PAYLOAD=$(jq -cn --arg m "$MESSAGE" --arg c "$CONTEXT" \
  '{message:$m,context:(if $c=="" then null else $c end)}')

curl -sS "$API_URL/v1/seo" \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $API_KEY" \
  -d "$PAYLOAD" | jq -r '.reply // .detail // .'
'''


@router.get("/install", response_class=PlainTextResponse)
def install_script() -> str:
    from app.config import get_settings
    settings = get_settings()
    api_url = getattr(settings, "public_url", "").strip()
    if not api_url:
        api_url = "http://YOUR_API_HOST:8000"
    return INSTALL_SCRIPT.replace("__API_URL__", api_url)
