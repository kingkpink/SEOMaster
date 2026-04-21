# Google Search Console Indexing Errors — Complete Reference

Every status type from the GSC Page Indexing Report with root causes, diagnostic steps, and fixes.

## Error Statuses (Blocks Indexing)

### 1. Server Error (5xx)

**What it means:** Googlebot received a 5xx status code when trying to crawl the URL.

**Common causes:**
- Server overloaded or crashed during crawl
- Application error (uncaught exception, database connection failure)
- CDN/reverse proxy misconfiguration
- Rate limiting blocking Googlebot
- Timeout (page takes too long to respond)

**How to fix:**
1. Check server logs for the exact error at the time of Googlebot's visit
2. Use GSC URL Inspection tool to test the URL live
3. Verify the page loads correctly in a browser
4. Check server resources (CPU, memory, disk) — scale if needed
5. Ensure Googlebot is not rate-limited (check WAF/CDN rules)
6. If intermittent, increase server timeout and optimize slow database queries
7. After fixing, request re-indexing via URL Inspection tool

**Prevention:**
- Monitor server uptime and error rates
- Set up alerting for 5xx spikes
- Ensure hosting can handle Googlebot crawl volume

---

### 2. Redirect Error

**What it means:** The URL has a redirect problem Google cannot follow.

**Common causes:**
- Redirect loop (A -> B -> A)
- Redirect chain too long (A -> B -> C -> D -> E...)
- Redirect to a URL that also errors
- Empty or malformed redirect target
- Mixed HTTP/HTTPS redirect issues

**How to fix:**
1. Trace the full redirect chain: `curl -I -L <url>`
2. Fix redirect loops — ensure no circular references
3. Shorten chains to a single redirect (A -> final destination)
4. Ensure all redirects use 301 (permanent) not 302 (temporary) for SEO
5. Verify HTTPS redirects: `http://` should 301 to `https://`
6. Check `.htaccess`, nginx config, or framework routing for conflicts

**Prevention:**
- Audit redirects regularly
- Use a redirect mapping spreadsheet during site migrations
- Never chain more than 2 redirects

#### multiple_redirects (GSC-specific)

**What it means:** Google followed more than 5 redirect hops before reaching (or failing to reach) the final URL. GSC reports this as a distinct subtype of "Redirect Error" in the Page Indexing report.

**How to identify:**
```bash
curl -sIL --max-redirs 20 <url> 2>&1 | grep -E "^HTTP|^Location"
```
Count the `Location:` lines — more than 5 = `multiple_redirects`.

**Common chains that trigger this:**
- `http://www.` → `https://www.` → `https://non-www.` → another redirect → error
- Old migration leftovers: stale redirect rules compounding CMS or CDN redirects
- www/non-www + HTTP/HTTPS combined: up to 3 hops before even reaching the page

**How to fix:**
1. Trace every hop: `curl -sIL --max-redirs 20 <url> | grep -E "^HTTP|^Location"`
2. Update internal links and sitemap entries to point directly to the final canonical URL — skip all intermediate hops
3. Collapse the redirect chain server-side: `A → B → C → D` becomes `A → D` (one hop)
4. Remove stale redirect rules from `.htaccess`, nginx, CDN, or framework routing
5. Ensure the final destination returns 200, not another redirect or error (a chain ending in 403 is a redirect error even with fewer than 5 hops)

**robots.txt and multiple_redirects:**

Google fetches `robots.txt` before crawling. If `robots.txt` itself exceeds 5 redirect hops, Google abandons the fetch and **assumes no crawl restrictions** — silently bypassing all your `Disallow` rules.

Requirements:
- `https://yourdomain.com/robots.txt` must return **200 directly**
- `http://` → `https://` for robots.txt is fine (1 hop, within limit)
- `www` and non-www versions should serve **identical robots.txt content**, or `www/robots.txt` should 301 to non-www in a single hop — never chain `www → https → non-www → robots.txt`
- If both `www` and non-www independently return 200 for robots.txt, their content must match exactly — Google may fetch either

**Diagnose robots.txt redirect chains:**
```bash
# Check all four variants
curl -sI http://example.com/robots.txt | grep -E "^HTTP|^Location"
curl -sI https://example.com/robots.txt | grep -E "^HTTP|^Location"
curl -sI http://www.example.com/robots.txt | grep -E "^HTTP|^Location"
curl -sI https://www.example.com/robots.txt | grep -E "^HTTP|^Location"

# Verify www and non-www serve identical content
diff <(curl -s https://example.com/robots.txt) <(curl -s https://www.example.com/robots.txt)
# Empty output = consistent. Any diff = fix required.
```

---

### 3. Submitted URL Has Crawl Issue

**What it means:** A URL in your sitemap had an unspecified crawl problem.

**How to fix:**
1. Use URL Inspection tool to see the specific crawl error
2. Check if the URL is accessible from a different network/IP
3. Verify DNS resolution is working
4. Check for connection resets or timeouts
5. Remove the URL from sitemap if it's no longer valid

---

### 4. Submitted URL Not Found (404)

**What it means:** A URL listed in your sitemap returns a 404 status.

**How to fix:**
1. If the page was removed intentionally: remove the URL from sitemap.xml
2. If the page should exist: restore it or fix the URL path
3. If the page moved: add a 301 redirect to the new URL AND update the sitemap
4. Regenerate the sitemap to remove stale URLs

---

### 5. Submitted URL Blocked by robots.txt

**What it means:** A URL in your sitemap is also blocked by robots.txt — contradictory signals.

**How to fix:**
1. Decide: should this page be indexed or not?
2. If YES: remove the `Disallow` rule from robots.txt
3. If NO: remove the URL from the sitemap AND add a `noindex` meta tag
4. Never submit URLs in sitemap that are blocked by robots.txt

---

### 6. Submitted URL Marked 'noindex'

**What it means:** A URL in your sitemap has a `noindex` directive — contradictory signals.

**How to fix:**
1. If the page should be indexed: remove the `noindex` meta tag or HTTP header
2. If the page should NOT be indexed: remove the URL from the sitemap
3. Check for `noindex` in: `<meta name="robots" content="noindex">`, `X-Robots-Tag: noindex` HTTP header, or framework-level config

---

## Excluded Statuses (Not Indexed by Design or Decision)

### 7. Excluded by 'noindex' Tag

**What it means:** Google found a `noindex` directive and is respecting it.

**When this is a problem:**
- If you WANT the page indexed, you have an unintentional `noindex`

**How to fix (if unintentional):**
1. Search codebase for `noindex`: meta tags, HTTP headers, framework config
2. Check for CMS SEO plugins adding `noindex` (common in WordPress with Yoast/RankMath)
3. Check HTTP response headers: `curl -I <url> | grep -i robots`
4. Remove the directive and request re-indexing

**Common accidental sources:**
- Development/staging `noindex` leaked to production
- CMS SEO plugin default settings
- Framework SSR config (Next.js `robots` metadata)
- CDN/edge function injecting headers

---

### 8. Blocked by robots.txt

**What it means:** Google cannot crawl the page because robots.txt disallows it.

**Important:** This does NOT prevent indexing if other sites link to the URL. Google may index the URL without content (showing just the URL in results).

**How to fix (if unintentional):**
1. Review robots.txt `Disallow` rules
2. Check for overly broad patterns: `Disallow: /` blocks everything
3. Test specific URLs with Google's robots.txt Tester
4. If you want to prevent indexing (not just crawling), use `noindex` instead

---

### 9. Blocked Due to Unauthorized Request (401)

**What it means:** Googlebot received a 401 status requiring authentication.

**How to fix:**
1. If the page is public: fix the authentication middleware to not require auth for Googlebot (or for anyone accessing the public URL)
2. If the page requires login: this is expected — no action needed
3. Check for basic auth on staging environments accidentally applied to production
4. Verify CDN/WAF is not challenging Googlebot with auth

---

### 10. Blocked Due to Access Forbidden (403)

**What it means:** The server explicitly denied Googlebot access.

**How to fix:**
1. Check server/CDN firewall rules for IP-based blocking
2. Verify WAF (Cloudflare, AWS WAF) is not blocking Googlebot user-agent
3. Check file permissions on the server
4. Ensure geographic restrictions don't block Google (crawls primarily from US IPs)
5. Whitelist Googlebot IPs or user-agent in firewall rules

---

### 11. Blocked Due to Other 4xx Issue

**What it means:** A non-standard 4xx error (not 401, 403, or 404).

**How to fix:**
1. Use URL Inspection tool to see the exact status code
2. Common codes: 410 (Gone), 429 (Too Many Requests), 451 (Legal)
3. For 410: intentional removal — no action needed unless unintentional
4. For 429: Googlebot is being rate-limited — increase rate limits or adjust crawl rate in GSC
5. Fix the underlying server configuration returning the error

---

### 12. Not Found (404)

**What it means:** URL returns 404. Google discovered it via links (not sitemap).

**How to fix:**
1. If the page was removed: ensure internal links are also removed/updated
2. If the URL never existed: find and fix the broken link source
3. If the page moved: add a 301 redirect
4. Clean up internal links pointing to 404 pages

---

### 13. Soft 404

**What it means:** The page returns HTTP 200 but Google detects it has no useful content (appears to be an error page).

**Common causes:**
- Empty pages or pages with only boilerplate/navigation
- Search results pages with zero results
- Product pages for out-of-stock items with no content
- Pages with "Page not found" text but 200 status code
- Thin content pages with just headers/footers

**How to fix:**
1. If the page has no content: return a proper 404 or 410 status code
2. If the page should have content: add substantial, unique content
3. For zero-result search pages: add `noindex` or return 404
4. For out-of-stock products: show alternative products or return 404
5. Ensure error pages return proper 404 status codes, not 200

---

### 14. Crawled — Currently Not Indexed

**What it means:** Google crawled the page but decided not to index it. This is a quality signal — Google doesn't think the page adds value to its index.

**Common causes:**
- Thin or low-quality content
- Content too similar to other indexed pages
- Page provides little unique value
- Poor E-E-A-T signals (Experience, Expertise, Authoritativeness, Trustworthiness)
- New/low-authority site

**How to fix:**
1. Improve content quality — add unique, in-depth, expert information
2. Ensure the page offers value not found elsewhere on your site or the web
3. Add internal links from high-authority pages on your site
4. Improve the page's E-E-A-T signals (author bios, citations, credentials)
5. Ensure proper meta tags, title, and structured data are present
6. Build external backlinks to the page
7. Request re-indexing after improvements via URL Inspection tool

---

### 15. Discovered — Currently Not Indexed

**What it means:** Google knows the URL exists but hasn't crawled it yet. This is a crawl budget issue.

**Common causes:**
- Site has too many URLs relative to its crawl budget
- Server is too slow, limiting crawl rate
- Low-priority pages (Google decides what to crawl first)
- New pages on a new/low-authority site

**How to fix:**
1. Improve server response time (under 200ms ideal)
2. Reduce total URL count by removing low-value pages
3. Improve internal linking to important uncrawled pages
4. Submit the URL directly via URL Inspection tool
5. Ensure the URL is in your sitemap
6. Build external links to improve site authority and crawl budget

---

### 16. Duplicate Without User-Selected Canonical

**What it means:** Google found duplicate pages and you didn't specify which is canonical. Google chose one on its own.

**How to fix:**
1. Add `<link rel="canonical" href="...">` to specify the preferred version
2. Use absolute HTTPS URLs in canonical tags
3. Ensure the canonical page is the most complete version
4. Add 301 redirects from duplicate URLs to the canonical
5. Update internal links to point to canonical URLs only

---

### 17. Duplicate, Google Chose Different Canonical Than User

**What it means:** You specified a canonical URL, but Google disagrees and chose a different one.

**Common causes:**
- Canonical points to a page with less content than the duplicate
- Canonical URL returns errors or redirects
- Internal links predominantly point to the non-canonical version
- Sitemap includes the non-canonical version
- Inconsistent signals (hreflang, internal links, sitemap all disagree)

**How to fix:**
1. Ensure canonical URL is the best, most complete version of the content
2. Make internal links consistent — all point to the canonical URL
3. Include only canonical URLs in sitemap
4. Verify canonical URL returns 200 and is accessible
5. Check for `hreflang` conflicts
6. Use 301 redirects from duplicates to canonical where possible
7. Remove `www` vs `non-www` and `http` vs `https` duplicates with redirects

---

### 18. Duplicate, Submitted URL Not Selected as Canonical

**What it means:** A URL in your sitemap is a duplicate, and Google chose a different URL as canonical.

**How to fix:**
1. Same fixes as #17 above
2. Additionally: update your sitemap to include only the canonical URL, not the duplicate

---

### 19. Alternate Page with Proper Canonical Tag

**What it means:** This page correctly declares itself as an alternate version pointing to a canonical. This is working as intended.

**When this is a problem:** Only if the page should be the canonical version itself.

**How to fix (if wrong):**
1. Change the canonical tag to be self-referencing
2. Update the other page's canonical to point here if this is the preferred version

---

### 20. Page with Redirect

**What it means:** This URL redirects to another URL. Redirected pages are not indexed (the destination is indexed instead).

**When this is a problem:** Only if the page shouldn't be redirecting.

**How to fix (if unintentional):**
1. Remove the redirect if the page should serve content directly
2. Check `.htaccess`, nginx config, or application routing

---

### 21. Page Removed Because of Legal Complaint

**What it means:** A DMCA or other legal takedown request removed this page from the index.

**How to fix:**
1. If the complaint is invalid: file a counter-notice through Google's legal tools
2. If the complaint is valid: remove the infringing content

---

### 22. Page Indexed Without Content

**What it means:** Google indexed the URL but could not extract any meaningful content.

**How to fix:**
1. Ensure the page has visible, crawlable text content
2. Check if content is loaded entirely via JavaScript that Googlebot can't render
3. Verify content isn't hidden behind login walls or paywalls without proper markup
4. Test with URL Inspection tool's "View Rendered Page" feature
5. If content is JS-rendered, implement SSR or prerendering

---

## Diagnostic Workflow for Any Indexing Error

```
1. Open GSC > Indexing > Pages
2. Click on the specific error/status type
3. Review sample affected URLs
4. For each URL:
   a. Use URL Inspection tool > "Test Live URL"
   b. Check "View Crawled Page" to see what Google sees
   c. Check HTTP response code, canonical, robots directives
   d. Compare rendered HTML vs source HTML
5. Identify the root cause from the categories above
6. Apply the fix
7. Click "Validate Fix" in GSC to trigger re-crawl
8. Monitor the status over 1-2 weeks
```

## Quick Reference: Error-to-Fix Matrix

| Error | Most Common Fix |
|-------|----------------|
| Server error (5xx) | Fix server/hosting, check logs |
| Redirect error | Break redirect loops, shorten chains |
| multiple_redirects | Collapse chain to 1 hop; update links/sitemap to final canonical URL |
| Crawl issue | Check DNS, server connectivity |
| Submitted 404 | Remove from sitemap or restore page |
| Submitted blocked by robots | Remove Disallow or remove from sitemap |
| Submitted noindex | Remove noindex or remove from sitemap |
| Noindex tag | Remove unintentional noindex |
| Blocked by robots.txt | Update Disallow rules |
| 401 Unauthorized | Fix auth middleware |
| 403 Forbidden | Fix firewall/WAF rules |
| Other 4xx | Check specific status code |
| 404 Not found | Redirect or fix broken links |
| Soft 404 | Add content or return real 404 |
| Crawled not indexed | Improve content quality |
| Discovered not indexed | Improve crawl budget/server speed |
| Duplicate no canonical | Add canonical tags |
| Google chose different canonical | Align all signals to one canonical |
| Duplicate submitted not canonical | Update sitemap to canonical URLs |
| Alternate with canonical | Working correctly (usually) |
| Page with redirect | Expected for redirected URLs |
| Indexed without content | Fix JS rendering or add content |
