# Regional Search Engines — Baidu, Naver, Seznam.cz

Technical SEO requirements for regional search engines with significant market share in their respective countries. These engines have critical differences from Google/Bing that can completely block indexing if not addressed.

---

## Baidu (China — 70%+ Market Share)

Baidu is the dominant search engine in mainland China. It has the most restrictive technical requirements of any major engine.

### Critical Differences from Google

| Requirement | Google | Baidu |
|-------------|--------|-------|
| JavaScript rendering | Full Chromium rendering | **No JS rendering at all** |
| `noindex` meta tag | Supported | **Not supported** — must use robots.txt |
| Hosting location | Anywhere | **Mainland China required** |
| ICP License | Not required | **Legally required** |
| Domain preference | Any TLD | **.CN strongly preferred** |
| Account registration | Email | **Chinese mobile number required** |

### Hosting and Legal Requirements

1. **ICP License (Internet Content Provider)** — Legally mandatory to host a website in mainland China. Without it, your site may be blocked by the Great Firewall.

2. **Mainland China hosting** — Required for acceptable load times. Hong Kong, Macau, and Taiwan hosting does NOT count. Foreign hosting loads too slowly behind the Great Firewall for Baiduspider to crawl reliably.

3. **.CN domain** — Strong ranking signal. While not strictly required, sites with `.cn` domains rank significantly better.

4. **Chinese mobile number** — Required to register a Baidu Webmaster Tools account and complete real-name verification (using Chinese ID or passport).

### JavaScript: Complete Blocker

**Baiduspider cannot execute JavaScript at all.** This is the single most critical difference from Google.

- All content must be in the initial server-rendered HTML
- Client-side rendering (React SPA, Vue SPA, Angular SPA) is completely invisible to Baidu
- SSR/SSG is not optional — it's mandatory
- Test with `curl` or "View Page Source" — if content isn't there, Baidu won't see it
- Even `<noscript>` fallbacks are insufficient — full SSR is required

### Meta Tags: No noindex Support

**Baidu does NOT support the `noindex` meta tag.** This is a critical gotcha.

Supported:
```html
<!-- These work on Baidu -->
<meta name="robots" content="nofollow">
<meta name="robots" content="noarchive">
<meta name="baiduspider" content="noarchive">
<meta name="baiduspider" content="nofollow">
```

Not supported:
```html
<!-- This does NOTHING on Baidu -->
<meta name="robots" content="noindex">
<meta name="baiduspider" content="noindex">
```

To prevent Baidu from indexing a page, you must use robots.txt:
```
User-agent: Baiduspider
Disallow: /private-page/
```

### Baiduspider User Agents

Baidu uses multiple crawlers for different content types:

| User Agent | Purpose |
|-----------|---------|
| `Baiduspider` | General web crawling |
| `Baiduspider-image` | Image search |
| `Baiduspider-video` | Video search |
| `Baiduspider-news` | News search |
| `Baiduspider-mobile` | Mobile search |

Verify Baiduspider via reverse DNS against `*.baidu.com`.

### Baidu Webmaster Tools Setup

1. Go to `ziyuan.baidu.com`
2. Register with Chinese mobile number
3. Complete real-name verification
4. Verify site ownership:
   - HTML file upload to site root, OR
   - HTML meta tag in homepage `<head>`
   - (CNAME no longer supported)
5. Submit sitemap (XML or TXT format, <10MB or <50,000 URLs)

### Baidu-Specific Optimization

- **Submit dead links proactively** — Baidu has a dead link submission tool; using it improves crawl efficiency
- **Use API push for active sites** — Real-time URL submission API for new/updated pages
- **Sitemaps as baseline** — Supplement API push, not replace it
- **Check crawl/index status weekly** — Baidu's crawl rate is slower than Google
- **Mobile adaptation is critical** — Baidu heavily emphasizes mobile-friendly design
- **Page load target: ≤2 seconds** — Use HTTP/2, CDN, responsive design
- **Use "website revision" tool** for domain migrations or major URL changes

### Baidu Sitemap Format

Baidu supports XML and plain TXT sitemaps:

```
# TXT format (one URL per line)
https://example.cn/page1/
https://example.cn/page2/
https://example.cn/page3/
```

Submit at `ziyuan.baidu.com` under Data Submission.

### Quick Checklist: Baidu

```
- [ ] ICP License obtained
- [ ] Hosted in mainland China
- [ ] .CN domain (or at minimum, Chinese-hosted)
- [ ] All content server-rendered (zero JS dependency)
- [ ] No reliance on noindex meta tag (use robots.txt instead)
- [ ] Chinese mobile number registered for Webmaster Tools
- [ ] Site verified in Baidu Webmaster Tools
- [ ] Sitemap submitted (XML or TXT)
- [ ] Dead links submitted proactively
- [ ] Mobile-optimized (responsive or dedicated mobile)
- [ ] Page load time ≤2 seconds
- [ ] robots.txt configured for Baiduspider
```

---

## Naver (South Korea — Major Market Share)

Naver is South Korea's dominant search platform, functioning as both a search engine and content ecosystem. It operates very differently from Google.

### Key Differences from Google

| Feature | Google | Naver |
|---------|--------|-------|
| Content discovery | Crawl-first | **Registration-first** |
| Indexing speed | Hours to days | **Up to 14 days** |
| Webmaster tool | Search Console | **Naver Search Advisor** |
| Content ecosystem | Open web | **Naver Blog, Cafe, Knowledge preferred** |
| Structured data | Broad support | **Specific types only** |

### Naver Search Advisor Setup

1. Go to `searchadvisor.naver.com`
2. Register/login with Naver account
3. Verify site ownership via HTML meta tag:
   ```html
   <meta name="naver-site-verification" content="YOUR_VERIFICATION_CODE">
   ```
4. Submit sitemap
5. Submit RSS feed (if applicable)

### Indexing Requirements

- **Registration is essential** — Unlike Google, Naver doesn't aggressively discover sites. You must register through Search Advisor.
- **Indexing takes up to 14 days** — Much slower than Google
- **Submit both sitemap AND RSS** — Naver supports both for content discovery
- **Request crawl** through Search Advisor for specific URLs

### Supported Structured Data Types

Naver supports structured data for specific content categories:

- Software applications
- Movies
- Restaurants
- Recipes
- FAQs
- Breadcrumbs
- Job postings

Use JSON-LD format (same as Google). Test with Naver's own validation tools in Search Advisor.

### Naver SEO Reports

Search Advisor provides:

- **Site status** — Overall health metrics
- **Crawl metrics** — How often Naver visits your site
- **Optimization analysis** — SEO improvement suggestions
- **Diagnostics** — Technical issues detected
- **Content exposure/click tracking** — Performance metrics

### Naver-Specific Optimization

- **Naver Blog integration** — Content on Naver Blog ranks preferentially in Naver search. Consider cross-posting or maintaining a Naver Blog presence.
- **Clean, semantic HTML** — Naver crawlers prefer well-structured HTML
- **Mobile optimization** — Critical for Naver rankings
- **Korean language content** — Content must be in Korean for Korean search results
- **robots.txt** — Naver respects standard robots.txt directives

### IndexNow Support

Naver participates in the IndexNow protocol. Submit URL changes for faster discovery:

```bash
curl "https://searchadvisor.naver.com/indexnow?url=https://example.com/page/&key=YOUR_KEY"
```

### Quick Checklist: Naver

```
- [ ] Site registered in Naver Search Advisor
- [ ] HTML verification meta tag added
- [ ] Sitemap submitted
- [ ] RSS feed submitted (if applicable)
- [ ] Structured data for supported types (FAQ, breadcrumbs, recipes, etc.)
- [ ] Mobile-optimized design
- [ ] Korean language content for Korean market
- [ ] IndexNow configured for faster discovery
- [ ] Crawl requests submitted for key pages
- [ ] Monitoring Search Advisor reports weekly
```

---

## Seznam.cz (Czech Republic — 10-20% Market Share)

Seznam is a Czech search engine that remains widely used for Czech-language queries, especially among older demographics and default browser users.

### Key Differences from Google

| Feature | Google | Seznam |
|---------|--------|--------|
| Crawler speed | Fast, continuous | **Significantly slower — days to weeks** |
| JS rendering | Full Chromium | **Prefers server-rendered HTML** |
| URL submission | Instant via API | **Manual, 100/day limit** |
| URL inspection | Full tool | **Not available** |
| IndexNow | Not supported | **Supported** |

### SeznamBot Crawler

**User agent:** `Mozilla/5.0 (compatible; SeznamBot/3.2; +http://fulltext.sblog.cz/)`

Characteristics:
- Crawls significantly slower than Googlebot — new content may take days or weeks to appear
- Prefers clean, server-rendered HTML over JavaScript frameworks
- Respects robots.txt, canonical tags, and XML sitemaps
- Does not guarantee re-crawls after sitemap updates

### Seznam Webmaster Tools Setup

1. Go to `reporter.seznam.cz/wm/`
2. Verify site ownership:
   - Meta tag on homepage, OR
   - Verification file upload
3. Submit sitemap
4. Monitor crawl statistics and error reports

### Getting Indexed on Seznam

1. **Submit sitemap** — Critical for new sites or after structural changes
2. **Manual URL submission** — Request indexing for individual URLs (limit: 100/day)
3. **Use IndexNow** — Seznam participates in IndexNow for faster URL discovery
4. **Clean internal linking** — Ensure SeznamBot can discover pages through links
5. **Don't block SeznamBot** — Check robots.txt for unintentional blocks

### Seznam-Specific Technical Notes

- **Server-side rendering preferred** — SeznamBot handles client-side JS poorly
- **No URL inspection tool** — Unlike Google/Bing, you can't inspect how Seznam sees a URL
- **No API-based indexing** — No equivalent to Google's Indexing API
- **Crawl statistics available** — Webmaster tools show pages with errors, redirects, and bot visit frequency
- **Czech language focus** — Primarily indexes Czech-language content

### Quick Checklist: Seznam

```
- [ ] Site verified in Seznam Webmaster Tools
- [ ] Sitemap submitted
- [ ] IndexNow configured for faster discovery
- [ ] Content server-rendered (not JS-dependent)
- [ ] SeznamBot not blocked in robots.txt
- [ ] Canonical tags present on all pages
- [ ] Czech language content for Czech market
- [ ] Monitoring crawl statistics regularly
```

---

## IndexNow Cross-Engine Coverage

IndexNow allows instant notification across multiple engines with a single submission:

| Engine | IndexNow Support | Native URL Submission |
|--------|-----------------|----------------------|
| Bing | Yes (primary) | IndexNow, Sitemap, URL Inspection |
| Yandex | Yes | Reindex Pages tool, Sitemap |
| Naver | Yes | Search Advisor crawl request |
| Seznam.cz | Yes | Manual (100/day), Sitemap |
| Yep | Yes | IndexNow only |
| Google | **No** | Indexing API, URL Inspection, Sitemap |
| Baidu | **No** | API push, Sitemap, Manual |
| Apple | **No** | No submission tools |

When IndexNow is configured, submitting to any participating engine shares the URL with all others.

### IndexNow Implementation

```bash
# 1. Generate API key (8-128 chars, alphanumeric + hyphens)
# 2. Host key file at site root
echo "YOUR_API_KEY" > /path/to/public/YOUR_API_KEY.txt

# 3. Submit URL changes (shared to all IndexNow engines)
curl "https://api.indexnow.org/indexnow?url=https://example.com/page/&key=YOUR_API_KEY"

# 4. Batch submit (up to 10,000 URLs)
curl -X POST "https://api.indexnow.org/indexnow" \
  -H "Content-Type: application/json" \
  -d '{
    "host": "example.com",
    "key": "YOUR_API_KEY",
    "keyLocation": "https://example.com/YOUR_API_KEY.txt",
    "urlList": [
      "https://example.com/new-page/",
      "https://example.com/updated-page/",
      "https://example.com/deleted-page/"
    ]
  }'
```

---

## Regional Engine Decision Matrix

Use this to determine which engines matter for your project:

| Target Market | Must Optimize For | Should Consider |
|--------------|-------------------|-----------------|
| Global (English) | Google, Bing | Apple (Spotlight/Siri) |
| United States | Google, Bing | Apple |
| China | **Baidu** (mandatory) | Google (blocked but some access) |
| South Korea | Google, **Naver** | Bing |
| Czech Republic | Google, **Seznam** | Bing |
| Russia/CIS | Google, **Yandex** | Bing |
| Japan | Google, Yahoo Japan (uses Google) | Bing |
| Global + AI | Google, Bing (Copilot) | Apple (Siri) |
