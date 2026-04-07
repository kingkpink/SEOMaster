# Multi-Engine Indexing Errors Reference

Indexing error types and fixes for Bing, Yandex, and Apple alongside Google. Each engine has its own error taxonomy, diagnostic tools, and resolution workflows.

For Google Search Console errors specifically, see [indexing-errors.md](indexing-errors.md).

---

## Bing Webmaster Tools — Crawl Errors and Indexing Issues

### Diagnostic Tools

- **URL Inspection Tool** — Check index status, crawl status, SEO errors, and markup validation per URL
- **Crawl Error Alerts** — Automated notifications when Bingbot encounters errors
- **SEO Reports** — Site-wide SEO errors prioritized by severity (red/yellow/blue)

### HTTP Status Code Errors

| Status Code | Error | Common Cause | Fix |
|-------------|-------|--------------|-----|
| 401 | Unauthorized | Password-protected pages, auth middleware blocking Bingbot | Remove auth requirements for public pages; whitelist Bingbot user-agent |
| 403 | Forbidden | Firewall/WAF blocking Bingbot, IP restrictions, geo-blocking | Whitelist Bingbot IPs/user-agent in WAF; remove geographic restrictions for crawlers |
| 404 | Not Found | Page removed, broken URL | Redirect to new URL (301) or remove from sitemap; notify via IndexNow |
| 500 | Internal Server Error | Application crash, uncaught exception | Check server logs, fix application errors, increase error handling |
| 503 | Service Unavailable | Server overloaded, maintenance mode | Scale infrastructure; use `Retry-After` header during planned maintenance |
| 509 | Bandwidth Exceeded | Hosting plan bandwidth limits reached | Upgrade hosting plan; optimize bandwidth usage |

### Indexing Exclusion Reasons

| Reason | Description | Fix |
|--------|-------------|-----|
| Blocked by robots.txt | URL disallowed in robots.txt | Remove Disallow rule if page should be indexed |
| Blocked by meta tag | `noindex` directive present | Remove noindex if page should be indexed |
| Blocked by webmaster | Manual block via Bing Webmaster Tools | Remove block in Webmaster Tools |
| Duplicate content | Bing identified URL as duplicate of another | Set canonical tag; use 301 redirect to preferred URL |
| Low page quality | Content doesn't meet Bing quality thresholds | Improve content depth, uniqueness, and E-E-A-T signals |

### Bing SEO Card Severity Levels

| Level | Color | Action Required |
|-------|-------|-----------------|
| Error | Red | Critical — fix immediately, blocks or severely hurts indexing |
| Warning | Yellow | Important — may reduce ranking or grounding eligibility |
| Notice | Blue | Informational — optimization opportunity |

### Bing-Specific Resolution Workflow

```
1. Open Bing Webmaster Tools > URL Inspection
2. Enter the affected URL
3. Review Index card (crawl/index status) and SEO card (errors/warnings)
4. Check Markup card for structured data issues
5. Apply fix based on error type
6. Click "Request Indexing" to trigger re-crawl
7. Alternatively, submit URL change via IndexNow for faster processing
8. Monitor status — Bing typically processes within hours to days
```

---

## Yandex Webmaster — Indexing Error Taxonomy

Yandex categorizes indexing problems into two distinct groups: **Download Errors** (robot couldn't fetch the document) and **Processing Errors** (document fetched but couldn't be processed).

### Diagnostic Tools

- **Indexing Status** — Shows total pages indexed, excluded, and error breakdown
- **Server Response Check** — Test how Yandex's robot sees a specific URL
- **Reindex Pages** — Request re-crawl of specific URLs (processing takes up to 3 days)
- **Removing Pages** — Remove URLs from Yandex search results
- **Site Diagnostics** — Automated detection of common problems

### Download Errors (Robot Failed to Fetch)

These occur when Yandex's robot cannot retrieve the document from the server.

| Error | Description | Fix |
|-------|-------------|-----|
| Connection failure | TCP connection to server failed | Check server uptime; verify Yandex IPs aren't firewalled |
| DNS error | Domain name could not be resolved | Verify DNS records; check nameserver configuration |
| Connection could not be established | Server refused connection | Check server is running; verify port accessibility |
| Invalid HTTP status code | Server returned unexpected status | Fix server configuration to return proper 200/301/404 codes |
| Invalid HTTP header | Malformed HTTP response headers | Fix server/framework configuration; validate headers |
| Invalid message length | HTTP content-length mismatch | Fix server response encoding; check compression settings |
| Invalid data amount transferred | Transfer interrupted or corrupted | Check server stability; verify no connection timeouts |
| Maximum HTTP header length exceeded | HTTP headers too large | Reduce cookie sizes; trim unnecessary headers |
| Maximum URL length exceeded | URL longer than 1024 bytes | Shorten URLs; reduce parameter count |
| Text size limit exceeded | Document larger than 10 MB | Split content across pages; optimize page size |
| Document blocked in robots.txt | Disallow rule prevents crawling | Remove Disallow if page should be indexed |
| Invalid document address | Malformed or unreachable URL | Fix URL structure; ensure proper encoding |
| Document format not supported | File type Yandex can't process | Convert to supported format (HTML, PDF, DOC, XLS, PPT, RTF, TXT) |
| Wrong encoding | Character encoding issues during download | Declare correct encoding in HTTP headers and `<meta charset>` |

### Processing Errors (Document Fetched but Cannot Be Processed)

These occur when the document downloads successfully but Yandex cannot extract useful content.

| Error | Description | Fix |
|-------|-------------|-----|
| Document contains `noindex` | Meta robots noindex directive found | Remove noindex if page should be indexed |
| Wrong encoding | Characters don't match declared encoding | Fix `<meta charset>` to match actual encoding; use UTF-8 |
| Encoding not recognized | Yandex can't determine character encoding | Add explicit `<meta charset="utf-8">` |
| Document recognized as server log | Content looks like raw log output | Ensure page serves actual HTML content, not debug output |
| Invalid document format | Downloaded file can't be parsed | Ensure valid HTML structure; fix syntax errors |
| Language not supported | Document in a language Yandex doesn't index | Typically not fixable; consider if Yandex is right market for this content |
| Document does not contain text | Page has no extractable text content | Add visible text content; don't rely on images/Flash for all content |
| Too many links on page | Excessive number of links on single page | Reduce links; use pagination for large lists |
| Extraction error | GZIP/DEFLATE decompression failed | Fix server compression configuration; test with `curl --compressed` |
| Empty server response | Server returned 200 but no body | Fix server/application to return actual content |
| Document is not canonical | Page points to different canonical URL | Expected behavior — check that the canonical target is correct |

### Yandex-Specific Limits

| Limit | Value |
|-------|-------|
| Maximum document size | 10 MB (Google: 15 MB) |
| Maximum URL length | 1024 bytes |
| Re-indexing time | Up to 3 days after request |
| Supported formats | HTML, PDF, DOC/DOCX, XLS/XLSX, PPT/PPTX, OpenOffice, RTF, TXT, SWF |

### Yandex-Specific Resolution Workflow

```
1. Open Yandex Webmaster > Indexing > Pages in Search
2. Review excluded pages and error categories
3. For each error:
   a. Use Server Response Check to see what Yandex's robot receives
   b. Check HTTP status code, headers, encoding, and content
   c. Compare with what browsers see
4. Apply fix based on error type above
5. Use Reindex Pages tool to request re-crawl
6. Monitor — processing takes up to 3 days
7. If pages still don't appear after 2 weeks, use Yandex support form
```

### Key Differences: Yandex vs Google Error Handling

| Behavior | Google | Yandex |
|----------|--------|--------|
| Max document size | 15 MB | 10 MB |
| `robots.txt` vs meta tag conflict | Both processed independently | robots.txt blocks override meta tags entirely |
| Conflicting allow/deny directives | Restrictive wins | **Allow takes priority** |
| `keywords` meta tag | Ignored | Considered for relevance |
| iframe/frame content | Generally not indexed | **Indexed and linked to source** |
| Re-indexing request time | Hours to days | Up to 3 days |
| Non-HTML format support | Limited | PDF, DOC, XLS, PPT, OpenOffice, RTF, TXT, SWF |

---

## Apple (Applebot) — Indexing Issues

### Diagnostic Approach

Apple does not provide webmaster tools. Diagnosis relies on server log analysis and robots.txt testing.

### Common Applebot Issues

| Issue | Symptom | Fix |
|-------|---------|-----|
| No Applebot rules, no Googlebot rules | Applebot follows generic `*` rules | Add specific Applebot rules or ensure `*` rules are permissive |
| Googlebot rules block content | Applebot follows Googlebot rules as fallback | Add explicit `User-agent: Applebot` section in robots.txt |
| CSS/JS blocked | Applebot can't render page properly | Allow CSS/JS resources for Applebot |
| Content behind JavaScript | Applebot may not see JS-rendered content | Ensure SSR/SSG or graceful degradation |

### Applebot robots.txt Configuration

```
User-agent: Applebot
Allow: /

# Optionally block AI training while keeping search visibility
User-agent: Applebot-Extended
Disallow: /
```

### Identifying Applebot Traffic

- Reverse DNS: `*.applebot.apple.com`
- IP CIDR list: `search.developer.apple.com/applebot.json`
- User-agent contains `Applebot/` in the string

---

## Cross-Engine Error Comparison Matrix

| Error Category | Google (GSC) | Bing (WMT) | Yandex (WM) |
|---------------|-------------|-------------|-------------|
| Server errors | Server Error (5xx) | 500, 503, 509 alerts | Connection failure, Invalid HTTP status |
| Auth blocks | 401, 403 statuses | 401, 403 alerts | Connection could not be established |
| Not found | 404, Soft 404 | 404 | Invalid document address |
| Redirect issues | Redirect Error | 3xx status class | (Counted under HTTP status errors) |
| robots.txt blocked | Blocked by robots.txt | Blocked by robots.txt | Document blocked in robots.txt |
| noindex | Excluded by noindex | Blocked by meta tag | Document contains noindex |
| Duplicate content | 3 duplicate statuses | Duplicate content | Document is not canonical |
| Quality issues | Crawled not indexed | Low page quality | (No direct equivalent) |
| Crawl budget | Discovered not indexed | (No direct equivalent) | (No direct equivalent) |
| Size limits | (15 MB implicit) | (No documented limit) | Text size limit exceeded (10 MB) |
| Encoding issues | (Rare) | (Rare) | Wrong encoding, Encoding not recognized |
| Content issues | Indexed without content | (No direct equivalent) | Document does not contain text, Empty server response |
| URL length | (No documented limit) | (No documented limit) | Maximum URL length exceeded (1024 bytes) |

---

## Unified Resolution Priority

When a URL has errors across multiple engines, fix in this order:

1. **Server errors** (5xx) — Affects all engines simultaneously
2. **robots.txt blocks** — Affects all engines that respect it
3. **Auth/firewall blocks** (401/403) — May affect engines differently based on IP ranges
4. **Meta directive conflicts** — Different engines handle conflicts differently
5. **Content quality** — Each engine has its own quality threshold
6. **Encoding/format issues** — Yandex is stricter than Google here
7. **Size/length limits** — Yandex has lower thresholds than Google
