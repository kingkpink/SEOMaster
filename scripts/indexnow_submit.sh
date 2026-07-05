#!/usr/bin/env bash
# Submit changed URLs to IndexNow (Bing, Yandex, Naver, Seznam.cz, Yep).
#
# Usage:
#   ./scripts/indexnow_submit.sh <KEY> <URL> [URL...]
#   ./scripts/indexnow_submit.sh <KEY> --file urls.txt
#
# Notes (see SKILL.md "IndexNow" section):
# - keyLocation is passed explicitly — required when the key file isn't at
#   the exact document root or multiple key files exist.
# - A 403 fetching your own key file through a WAF is a false alarm;
#   trust the api.indexnow.org status code (200/202 = accepted).
# - Google, Baidu and Apple do NOT support IndexNow.
set -euo pipefail

if [[ $# -lt 2 ]]; then
  grep '^#' "$0" | sed 's/^# \{0,1\}//' | head -12
  exit 1
fi

KEY="$1"; shift

urls=()
if [[ "$1" == "--file" ]]; then
  [[ $# -ge 2 ]] || { echo "--file needs a path" >&2; exit 1; }
  while IFS= read -r line; do
    [[ -n "$line" && "$line" != \#* ]] && urls+=("$line")
  done < "$2"
else
  urls=("$@")
fi

for url in "${urls[@]}"; do
  host=$(printf '%s' "$url" | sed -E 's#^https?://([^/]+).*#\1#')
  key_location="https://${host}/${KEY}.txt"
  status=$(curl -s -o /dev/null -w '%{http_code}' \
    "https://api.indexnow.org/indexnow?url=$(printf '%s' "$url" | sed 's/&/%26/g')&key=${KEY}&keyLocation=${key_location}")
  echo "${status}  ${url}"
done
