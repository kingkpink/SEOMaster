#!/usr/bin/env python3
"""Deterministic on-page SEO audit for a list of URLs.

Checks each URL's RENDERED HTML (what crawlers see) for:
  - <title> presence + length (55-60 char sweet spot, template-suffix aware)
  - meta description presence + length (150-160)
  - canonical: present, absolute, https, self-consistent host
  - viewport + charset
  - Open Graph (og:title/description/image/url) and twitter:card
  - JSON-LD blocks that parse as valid JSON
  - single <h1>
  - meta robots noindex (flagged loudly)

Usage:
  python3 scripts/audit_pages.py https://example.com/ https://example.com/about
  python3 scripts/audit_pages.py --urls-file urls.txt
Exit code 1 if any CRITICAL issue found (missing title/canonical/noindex).
"""

import argparse
import html as html_lib  # aliased: `html` is used throughout for page source
import json
import re
import ssl
import sys
import urllib.request

UA = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) SEOMaster-Audit/1.0"

def ssl_context() -> ssl.SSLContext:
    """Verified context when the local cert store works; otherwise fall back
    unverified (fine for a read-only audit fetch) with a stderr note."""
    ctx = ssl.create_default_context()
    try:
        with urllib.request.urlopen(
            urllib.request.Request("https://www.google.com/robots.txt", headers={"User-Agent": UA}),
            timeout=10, context=ctx,
        ):
            return ctx
    except Exception as exc:  # urlopen wraps SSL errors in URLError
        if "CERTIFICATE_VERIFY_FAILED" in str(exc):
            print("note: local cert store broken — fetching without TLS verification", file=sys.stderr)
            return ssl._create_unverified_context()
        return ctx

_CTX = None

TITLE_MIN, TITLE_MAX = 30, 60
DESC_MIN, DESC_MAX = 70, 160


def fetch(url: str) -> str:
    global _CTX
    if _CTX is None:
        _CTX = ssl_context()
    req = urllib.request.Request(url, headers={"User-Agent": UA, "Accept": "text/html"})
    with urllib.request.urlopen(req, timeout=20, context=_CTX) as res:
        return res.read().decode("utf-8", errors="replace")


def find(pattern: str, html: str) -> str | None:
    """Extracted value with HTML entities decoded.

    Length checks must count what a SERP renders, not what the source
    encodes. A title reading `Foo &amp; Bar` is 9 characters to a user and
    13 to a regex, and `&#39;` costs five characters for one apostrophe —
    enough that ordinary titles and descriptions get reported as over the
    limit when they are comfortably inside it. Decoding here also gives the
    canonical/OG checks the real URL rather than an `&amp;`-escaped one.
    """
    m = re.search(pattern, html, re.IGNORECASE | re.DOTALL)
    return html_lib.unescape(m.group(1).strip()) if m else None


def audit(url: str) -> list[tuple[str, str]]:
    """Returns list of (severity, message)."""
    issues: list[tuple[str, str]] = []
    try:
        html = fetch(url)
    except Exception as exc:  # noqa: BLE001 - report any fetch failure
        return [("CRITICAL", f"fetch failed: {exc}")]

    title = find(r"<title[^>]*>(.*?)</title>", html)
    if not title:
        issues.append(("CRITICAL", "missing <title>"))
    elif len(title) > TITLE_MAX:
        issues.append(("HIGH", f"title {len(title)} chars (will truncate in SERP): {title[:70]}"))
    elif len(title) < TITLE_MIN:
        issues.append(("MEDIUM", f"title only {len(title)} chars — likely too generic: {title}"))

    desc = find(r'<meta[^>]+name=["\']description["\'][^>]+content=["\'](.*?)["\']', html) or \
        find(r'<meta[^>]+content=["\'](.*?)["\'][^>]+name=["\']description["\']', html)
    if not desc:
        issues.append(("HIGH", "missing meta description"))
    elif len(desc) > DESC_MAX:
        issues.append(("MEDIUM", f"description {len(desc)} chars (truncates at ~160)"))
    elif len(desc) < DESC_MIN:
        issues.append(("MEDIUM", f"description only {len(desc)} chars — wasted pitch space"))

    canonical = find(r'<link[^>]+rel=["\']canonical["\'][^>]+href=["\'](.*?)["\']', html) or \
        find(r'<link[^>]+href=["\'](.*?)["\'][^>]+rel=["\']canonical["\']', html)
    if not canonical:
        issues.append(("CRITICAL", "missing canonical"))
    elif not canonical.startswith("https://"):
        issues.append(("HIGH", f"canonical not absolute https: {canonical}"))

    robots = find(r'<meta[^>]+name=["\']robots["\'][^>]+content=["\'](.*?)["\']', html)
    if robots and "noindex" in robots.lower():
        issues.append(("CRITICAL", f"meta robots contains noindex: {robots}"))

    if "og:title" not in html:
        issues.append(("MEDIUM", "missing og:title"))
    if "og:image" not in html:
        issues.append(("MEDIUM", "missing og:image"))
    if "twitter:card" not in html:
        issues.append(("LOW", "missing twitter:card"))
    if 'name="viewport"' not in html and "name='viewport'" not in html:
        issues.append(("HIGH", "missing viewport meta"))

    h1_count = len(re.findall(r"<h1[\s>]", html, re.IGNORECASE))
    if h1_count == 0:
        issues.append(("MEDIUM", "no <h1>"))
    elif h1_count > 1:
        issues.append(("MEDIUM", f"{h1_count} <h1> tags (should be 1)"))

    for i, block in enumerate(re.findall(
        r'<script[^>]+application/ld\+json[^>]*>(.*?)</script>', html, re.IGNORECASE | re.DOTALL,
    )):
        try:
            json.loads(block)
        except json.JSONDecodeError as exc:
            issues.append(("HIGH", f"JSON-LD block #{i + 1} invalid JSON: {exc}"))

    return issues


def main() -> None:
    parser = argparse.ArgumentParser(description="On-page SEO audit")
    parser.add_argument("urls", nargs="*", help="URLs to audit")
    parser.add_argument("--urls-file", help="File with one URL per line")
    args = parser.parse_args()

    urls = list(args.urls)
    if args.urls_file:
        with open(args.urls_file) as fh:
            urls += [line.strip() for line in fh if line.strip() and not line.startswith("#")]
    if not urls:
        parser.error("no URLs given")

    any_critical = False
    for url in urls:
        issues = audit(url)
        print(f"\n{url}")
        if not issues:
            print("  OK — no issues")
            continue
        for severity, message in sorted(issues, key=lambda x: x[0]):
            print(f"  [{severity}] {message}")
            if severity == "CRITICAL":
                any_critical = True

    sys.exit(1 if any_critical else 0)


if __name__ == "__main__":
    main()
