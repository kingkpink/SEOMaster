# Technical SEO Reference

Deep reference for crawling, rendering, indexing, and server-side SEO configuration.

## How Google Crawls and Indexes

### Three-Phase Process

1. **Crawling** — Googlebot fetches URLs, parses HTML, discovers links
2. **Rendering** — JavaScript pages queued for headless Chromium execution
3. **Indexing** — Rendered content analyzed, stored in search index

**Key facts:**
- Googlebot processes first **15MB** of any page
- Crawls primarily from **US IP addresses**
- Supports HTTP/1.1 and HTTP/2
- Supports gzip, deflate, and brotli compression
- Pages with non-200 status codes may skip rendering

### Crawl Budget Optimization

Crawl budget = how many pages Google will crawl on your site in a given time period.

**Increase crawl budget:**
- Fast server response times (< 200ms)
- No server errors (5xx)
- Avoid duplicate content (wastes crawl budget on duplicates)
- Use XML sitemap to prioritize important pages
- Strong internal linking structure
- Remove low-value pages (thin content, parameter variations)

**Reduce crawl waste:**
- Block crawling of faceted navigation / filter URLs with robots.txt
- Use `noindex` on paginated archive pages (or `rel="next"`/`rel="prev"`)
- Canonicalize parameter variations
- Return 404/410 for truly removed pages (not soft 404)

### HTTP Caching for Crawlers

Implement caching headers to optimize Googlebot crawl efficiency:

```
# Preferred: ETag-based caching
ETag: "abc123"
# Googlebot sends: If-None-Match: "abc123"
# Server returns 304 Not Modified if unchanged

# Alternative: Date-based caching
Last-Modified: Wed, 15 Jan 2026 10:00:00 GMT
# Googlebot sends: If-Modified-Since: Wed, 15 Jan 2026 10:00:00 GMT
```

Google recommends ETag over Last-Modified to avoid date formatting issues.

## robots.txt Deep Dive

### Syntax Reference

```
# Comment
User-agent: Googlebot
Disallow: /private/
Allow: /private/public-page.html

User-agent: *
Disallow: /api/
Disallow: /admin/
Disallow: /tmp/
Disallow: /*?sort=
Disallow: /*&filter=

Sitemap: https://example.com/sitemap.xml
```

### Pattern Matching

| Pattern | Matches | Example |
|---------|---------|---------|
| `/path/` | Exact directory | `/path/anything` |
| `/path` | Prefix match | `/path`, `/pathway` |
| `/*.pdf$` | Files ending in .pdf | `/docs/file.pdf` |
| `/*?` | URLs with parameters | `/page?id=1` |
| `/path/*/file` | Wildcard directory | `/path/sub/file` |

### Crawl-delay Directive

Not supported by Google, but respected by Bing and Yandex:

```
User-agent: Bingbot
Crawl-delay: 1

User-agent: Yandex
Crawl-delay: 2
```

For Google, adjust crawl rate in Search Console settings.

### Common robots.txt Mistakes

| Mistake | Problem | Fix |
|---------|---------|-----|
| `Disallow: /` for all agents | Blocks entire site | Be specific about what to block |
| Blocking CSS/JS files | Google can't render pages | Allow CSS/JS resources |
| Using robots.txt to hide pages | Pages can still appear in index (without snippet) | Use `noindex` instead |
| Forgetting trailing slash | `/admin` matches `/administrator` too | Use `/admin/` for directories |
| No Sitemap directive | Misses easy discovery signal | Add `Sitemap:` line |

## Meta Robots Tags

### Supported Directives

```html
<!-- Block indexing -->
<meta name="robots" content="noindex">

<!-- Block link following -->
<meta name="robots" content="nofollow">

<!-- Block both -->
<meta name="robots" content="noindex, nofollow">

<!-- Block caching/archiving -->
<meta name="robots" content="noarchive">

<!-- Block snippet in search results -->
<meta name="robots" content="nosnippet">

<!-- Limit snippet length -->
<meta name="robots" content="max-snippet:150">

<!-- Limit image preview size -->
<meta name="robots" content="max-image-preview:large">

<!-- Limit video preview -->
<meta name="robots" content="max-video-preview:30">

<!-- Prevent indexing after a date -->
<meta name="robots" content="unavailable_after: 2026-12-31T23:59:59+00:00">
```

### X-Robots-Tag HTTP Header

Same directives as meta tags but via HTTP headers (useful for PDFs, images, non-HTML):

```
X-Robots-Tag: noindex
X-Robots-Tag: noindex, nofollow
X-Robots-Tag: googlebot: noindex
```

### Directive Precedence

When conflicting directives exist, **the more restrictive one wins** (Google behavior):
- `index` + `noindex` = `noindex`
- `follow` + `nofollow` = `nofollow`

**Warning:** Yandex handles this differently — see Multi-Engine Directive Differences below.

### Multi-Engine Meta Directive Differences

Each search engine handles meta directives differently. These differences can cause a page to be indexed on one engine but blocked on another.

#### Directive Support Matrix

| Directive | Google | Bing | Yandex | Baidu | Applebot |
|-----------|--------|------|--------|-------|----------|
| `noindex` | Yes | Yes | Yes | **NO** | Yes |
| `nofollow` | Yes | Yes | Yes | Yes | Yes |
| `noarchive` | Yes | Yes (+ blocks Copilot) | Yes | Yes | No |
| `nocache` | No | **Yes** (Copilot: URL/title/snippet only) | No | No | No |
| `nosnippet` | Yes | Yes | No | No | Yes |
| `max-snippet` | Yes | Yes | No | No | No |
| `max-image-preview` | Yes | Yes | No | No | No |
| `max-video-preview` | Yes | Yes | No | No | No |
| `unavailable_after` | Yes | No | No | No | No |
| `data-nosnippet` attr | Yes | Yes | No | No | No |
| `data-snippet` attr | No | **Yes** | No | No | No |

#### Engine-Specific Targeting

Use `name` attribute to target specific engines:

```html
<!-- All engines -->
<meta name="robots" content="noindex">

<!-- Google only -->
<meta name="googlebot" content="noindex">

<!-- Bing only -->
<meta name="bingbot" content="noarchive">

<!-- Yandex only -->
<meta name="yandex" content="nofollow">

<!-- Baidu only (noindex NOT supported) -->
<meta name="baiduspider" content="noarchive">

<!-- Apple only -->
<meta name="applebot" content="nosnippet">
```

#### Critical Behavioral Differences

| Behavior | Google | Bing | Yandex | Baidu |
|----------|--------|------|--------|-------|
| Conflicting allow/deny | Restrictive wins | Restrictive wins | **Allow wins** | N/A |
| robots.txt vs meta tag | Independent | Independent | **robots.txt overrides meta** | robots.txt only for blocking |
| `keywords` meta tag | Ignored | Ignored | **Used for relevance** | Used (limited) |
| Applebot fallback | N/A | N/A | N/A | N/A |

**Applebot fallback behavior:** If robots.txt has no `User-agent: Applebot` section but has `User-agent: Googlebot`, Applebot follows Googlebot's rules.

#### Bing AI/Copilot-Specific Directives

Bing has unique directives for controlling content in AI-generated answers:

```html
<!-- Block content from Copilot answers AND AI training -->
<meta name="robots" content="noarchive">

<!-- Limit Copilot to URL/title/snippet only; limit AI training similarly -->
<meta name="robots" content="nocache">

<!-- Exclude specific elements from Copilot citations -->
<div data-nosnippet>Sensitive content here</div>

<!-- Specify preferred text for Copilot to cite -->
<div data-snippet>This is the text Bing should quote.</div>
```

See [bing-copilot-seo.md](bing-copilot-seo.md) for the complete AI/Copilot impact matrix.

#### Baidu: The noindex Problem

Baidu does not support `noindex` in meta tags or HTTP headers. The ONLY way to prevent Baidu from indexing a page:

```
# robots.txt — the only way to block Baidu indexing
User-agent: Baiduspider
Disallow: /private-page/
```

This means a page with `<meta name="robots" content="noindex">` will still be indexed by Baidu unless also blocked in robots.txt.

See [regional-engines.md](regional-engines.md) for full Baidu requirements.

#### Recommended Multi-Engine robots.txt Template

```
User-agent: *
Allow: /
Disallow: /api/
Disallow: /admin/
Disallow: /private/

# Google: adjust crawl rate in Search Console (Crawl-delay not supported)
User-agent: Googlebot
Allow: /

# Bing: Crawl-delay supported
User-agent: Bingbot
Crawl-delay: 1

# Yandex: Crawl-delay and Host supported
User-agent: Yandex
Crawl-delay: 2
Host: https://example.com

# Apple: allow search, block AI training
User-agent: Applebot
Allow: /

User-agent: Applebot-Extended
Disallow: /

# Baidu: remember noindex doesn't work — use Disallow for pages to hide
User-agent: Baiduspider
Allow: /
Disallow: /pages-to-hide-from-baidu/

Sitemap: https://example.com/sitemap.xml
```

## Canonical URL Implementation

### Methods (strongest to weakest)

1. **301 Redirect** — Strongest signal, use when removing a duplicate permanently
2. **`rel="canonical"` HTML tag** — Strong signal, use when both URLs must remain accessible
3. **`Link:` HTTP header** — Same as HTML tag, for non-HTML resources
4. **Sitemap inclusion** — Weak signal, supplementary only

### Implementation Rules

```html
<!-- CORRECT: Absolute HTTPS URL -->
<link rel="canonical" href="https://example.com/page/">

<!-- WRONG: Relative URL -->
<link rel="canonical" href="/page/">

<!-- WRONG: HTTP instead of HTTPS -->
<link rel="canonical" href="http://example.com/page/">
```

**Rules:**
- Always use absolute URLs with HTTPS
- Every page should have a self-referencing canonical (even if not a duplicate)
- Canonical target must return 200 status
- Canonical target should not be `noindex`
- Canonical target should not redirect
- Only one canonical tag per page
- Place in `<head>`, not in `<body>`
- If using JavaScript to inject canonical, ensure it's in initial server-rendered HTML

### Common Canonical Conflicts to Resolve

| Conflict | Resolution |
|----------|------------|
| `www` vs `non-www` | 301 redirect one to the other, canonical on preferred |
| `http` vs `https` | 301 redirect HTTP to HTTPS, canonical on HTTPS |
| Trailing slash vs no slash | Pick one, redirect the other, canonical on preferred |
| URL parameters (`?ref=`, `?utm_`) | Canonical to clean URL without parameters |
| Pagination (`/page/2/`) | Each page canonicalizes to itself (NOT to page 1) |
| AMP vs regular | AMP canonicalizes to regular version |

## JavaScript SEO

### Server-Side Rendering (SSR) Checklist

For frameworks like Next.js, Nuxt, SvelteKit, Astro, Remix:

1. `<title>` and `<meta name="description">` present in initial server HTML
2. `<link rel="canonical">` present in initial server HTML
3. Structured data (JSON-LD) present in initial server HTML
4. Main content text present in initial server HTML
5. Internal links are real `<a href="...">` tags (not JS click handlers)
6. Proper HTTP status codes (404 for missing pages, not client-side redirect)
7. `<meta name="robots">` directives in initial server HTML

### Dynamic Rendering

If full SSR isn't possible, use dynamic rendering to serve pre-rendered HTML to bots:

- Detect Googlebot user-agent at the server/CDN level
- Serve pre-rendered static HTML to crawlers
- Serve normal SPA to users
- Google officially supports this as a workaround (not cloaking)
- Tools: Rendertron, Prerender.io, Puppeteer-based solutions

### Common JS SEO Failures

| Problem | Symptom | Fix |
|---------|---------|-----|
| Client-only rendering | "Discovered not indexed" or "Indexed without content" | Implement SSR/SSG |
| Hash routing (`#/page`) | Only homepage indexed | Use History API routing |
| Lazy-loaded content | Content not in Google's index | Ensure content loads without user interaction |
| JS-injected canonical | Google ignores it | Put canonical in server-rendered HTML |
| Click-based navigation | Google can't discover pages | Use standard `<a href>` links |
| Infinite scroll only | Deep content never crawled | Add pagination with `<a>` links |

## International SEO (hreflang)

For multilingual or multi-regional sites:

```html
<link rel="alternate" hreflang="en" href="https://example.com/page/">
<link rel="alternate" hreflang="es" href="https://example.com/es/page/">
<link rel="alternate" hreflang="fr" href="https://example.com/fr/page/">
<link rel="alternate" hreflang="x-default" href="https://example.com/page/">
```

**Rules:**
- Every page must reference all alternate versions including itself
- `x-default` specifies the fallback for unmatched languages
- Use ISO 639-1 language codes, optionally with ISO 3166-1 region codes
- Can be implemented via HTML `<link>`, HTTP headers, or sitemap
- Canonical URL should be within the same language group

## HTTPS and Security

- All pages must be served over HTTPS (ranking signal)
- HTTP URLs should 301 redirect to HTTPS
- Use HSTS headers: `Strict-Transport-Security: max-age=31536000; includeSubDomains`
- Ensure SSL certificate is valid and covers all subdomains
- Mixed content (HTTP resources on HTTPS pages) can cause rendering issues

## URL Structure Best Practices

```
GOOD:
https://example.com/blog/seo-guide/
https://example.com/products/blue-widget/

BAD:
https://example.com/page?id=123&cat=4
https://example.com/blog/2026/01/15/post-title (unnecessary date in URL)
https://EXAMPLE.COM/Blog/SEO-Guide/ (mixed case)
```

**Rules:**
- Lowercase only
- Hyphens between words (not underscores)
- No unnecessary parameters
- Keep URLs short and descriptive
- Max 3 directory levels from root
- Trailing slash: pick one convention, be consistent
- Use HTTPS always
