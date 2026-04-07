from fastapi import APIRouter
from fastapi.responses import PlainTextResponse

router = APIRouter(tags=["install"])

INSTALL_SCRIPT = r'''#!/usr/bin/env bash
# SEO Master CLI — tiny wrapper around the hosted API.
# Usage:
#   seo "Audit example.com for title tags"
#   seo "Check structured data" --context "<html>...</html>"
#   echo "<html>...</html>" | seo "Audit this HTML"

API_URL="${SEO_API_URL:-__API_URL__}"
API_KEY="${SEO_API_KEY}"

if [ -z "$API_KEY" ]; then
  echo "Set your API key first:"
  echo "  export SEO_API_KEY=your-key-here"
  exit 1
fi

MESSAGE="$1"
shift

CONTEXT=""
if [ "$1" = "--context" ]; then
  CONTEXT="$2"
elif [ ! -t 0 ]; then
  CONTEXT="$(cat)"
fi

PAYLOAD=$(jq -cn --arg m "$MESSAGE" --arg c "$CONTEXT" '{message:$m,context:(if $c=="" then null else $c end)}')

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
