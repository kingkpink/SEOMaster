---
name: seo-master
description: Performs comprehensive SEO audits, CTR optimization, and indexing error resolution for web projects. Analyzes HTML pages for proper meta tags, canonical URLs, structured data (JSON-LD), sitemaps, robots.txt, Open Graph, Core Web Vitals, and internal linking. Optimizes click-through rate (CTR) using Google Search Console data — rewrites title tags, meta descriptions, adds dynamic dates for time-sensitive content, fixes www/non-www duplication, and recommends structured data for rich snippets. Diagnoses and fixes indexing errors across Google Search Console, Bing Webmaster Tools, Yandex Webmaster, and Apple (Applebot). Covers Bing Copilot/AI grounding (GEO), regional engines (Baidu, Naver, Seznam.cz), and IndexNow protocol. Use when the user mentions SEO, search rankings, CTR, click-through rate, indexing, Search Console errors, page not indexed, structured data, sitemaps, Copilot optimization, or wants to improve search engine visibility.
---

# SEO Master

Comprehensive SEO auditing, optimization, and indexing error resolution for web projects across all major search engines.

## Quick Start Workflow

Copy this checklist and track progress:

```
SEO Audit Progress:
- [ ] Step 1: Discover project structure and tech stack
- [ ] Step 2: Audit HTML head tags (title, meta, canonical, OG)
- [ ] Step 2b: Audit and optimize click-through rate (CTR)
- [ ] Step 3: Audit robots.txt and sitemap.xml
- [ ] Step 4: Audit structured data (JSON-LD / schema.org)
- [ ] Step 5: Audit internal linking and URL structure
- [ ] Step 6: Audit Core Web Vitals and performance signals
- [ ] Step 7: Audit JavaScript SEO (if SPA/SSR)
- [ ] Step 8: Audit multi-engine compatibility (Bing/Copilot, Yandex, Apple, Baidu, Naver, Seznam)
- [ ] Step 9: Fix all discovered issues
- [ ] Step 10: Validate fixes
```

## Step 1: Discover Project Structure

Identify the tech stack and page generation method:

- **Static HTML**: Check each `.html` file directly
- **SSR frameworks** (Next.js, Nuxt, SvelteKit, Astro, Remix): Check layout files, head components, metadata config
- **SPA** (React, Vue, Angular): Check for SSR/prerendering setup — SPAs without prerendering have major SEO issues
- **CMS** (WordPress, etc.): Check theme templates, SEO plugin config

Search for:
```
# Find HTML files
**/*.html

# Find head/meta configuration
grep -r "<title" "<meta" "canonical" "og:" "json-ld" "schema.org"

# Find robots.txt and sitemap
robots.txt, sitemap.xml, sitemap*.xml

# Find layout/head files (framework-specific)
_app.*, layout.*, _document.*, app.html, +layout.*, head.*
```

## Step 2: Audit HTML Head Tags

Every indexable page MUST have these elements in `<head>`:

### Required Tags

```html
<!-- Unique, descriptive title (50-60 chars) -->
<title>Primary Keyword - Secondary Keyword | Brand Name</title>

<!-- Unique meta description (150-160 chars) -->
<meta name="description" content="Compelling description with primary keyword that encourages clicks.">

<!-- Self-referencing canonical URL (absolute, HTTPS) -->
<link rel="canonical" href="https://example.com/current-page/">

<!-- Viewport for mobile -->
<meta name="viewport" content="width=device-width, initial-scale=1">

<!-- Charset -->
<meta charset="utf-8">
```

### Open Graph (Facebook, LinkedIn, Discord, etc.)

```html
<meta property="og:title" content="Page Title">
<meta property="og:description" content="Page description">
<meta property="og:image" content="https://example.com/image.jpg">
<meta property="og:url" content="https://example.com/page/">
<meta property="og:type" content="website">
<meta property="og:site_name" content="Brand Name">
```

### Twitter Card

```html
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:title" content="Page Title">
<meta name="twitter:description" content="Page description">
<meta name="twitter:image" content="https://example.com/image.jpg">
```

### Common Mistakes to Fix

| Issue | Impact | Fix |
|-------|--------|-----|
| Missing `<title>` | Critical — no ranking signal | Add unique title per page |
| Duplicate titles across pages | Dilutes rankings | Make each title unique |
| Missing canonical | Duplicate content risk | Add self-referencing canonical |
| Relative canonical URL | Google may ignore it | Use absolute HTTPS URL |
| Missing meta description | Lower CTR | Add compelling description |
| Missing viewport meta | Mobile ranking penalty | Add viewport tag |
| Multiple `<h1>` tags | Confuses hierarchy | Use single `<h1>` per page |

## Step 2b: Click-Through Rate (CTR) Optimization

CTR is the ratio of clicks to impressions in search results. Even with good rankings, poor CTR means wasted visibility. This step audits and fixes CTR across all pages.

### CTR Audit Process

1. **Get GSC data** — Ask the user for their Google Search Console Performance export (CSV or XLSX), or ask them to share top queries/pages with impressions, clicks, CTR, and position.
2. **Identify CTR problems** using the benchmarks below.
3. **Diagnose root causes** (title, description, rich snippets, intent mismatch).
4. **Fix titles and descriptions** using the patterns below.
5. **Add structured data** to earn rich snippets.
6. **Monitor** — CTR changes take 2-4 weeks to appear in GSC data.

### CTR Benchmarks by Position

Expected CTR varies by position. Pages significantly below these benchmarks have CTR problems:

| Position | Expected CTR | Action threshold |
|----------|-------------|-----------------|
| 1 | 25-35% | Investigate if < 20% |
| 2 | 12-18% | Investigate if < 10% |
| 3 | 8-12% | Investigate if < 6% |
| 4-5 | 4-8% | Investigate if < 3% |
| 6-10 | 1-4% | Investigate if < 1% |
| 11-20 | 0.5-1.5% | Focus on ranking improvement first |

### CTR Problem Diagnosis

When CTR is below benchmark, diagnose using this priority list:

| Symptom | Likely Cause | Fix |
|---------|-------------|-----|
| High impressions, 0% CTR | Title doesn't match search intent | Rewrite title to match what users are searching for |
| Many date-specific queries with 0 clicks | Title/description lack freshness signals | Add dynamic dates, "Updated [Month Year]", "Latest" to title |
| CTR < 1% at position 1-5 | Title is generic or doesn't differentiate | Add power words, numbers, specificity |
| Branded queries have low CTR | Sitelinks or knowledge panel stealing clicks | Optimize sitelink titles, add structured data |
| Informational queries, low CTR | No rich snippet (FAQ, table, how-to) | Add structured data for rich results |
| Duplicate www/non-www pages | Clicks split across duplicate URLs | Enforce canonical domain via redirects |
| Product/comparison queries, low CTR | No star ratings or price in SERP | Add `Product`, `AggregateRating` structured data |

### Title Tag Formulas for High CTR

Generic titles kill CTR. Use these proven formulas:

**Data/Stats pages:**
```
[Metric Name] — [Current Value] (Updated [Month Year]) | [Brand]
```
Example: `COMEX Silver Inventory — 298M oz (Updated April 2026) | HeavyMetalStats`

**Live data pages:**
```
[Data Type] Today: [Live Value] — [Trend] | [Brand]
```
Example: `COMEX Gold Inventory Today: 18.2M oz — Down 3.1% | HeavyMetalStats`

**Blog/analysis pages:**
```
[Compelling Claim or Question] — [Data Point or Year] | [Brand]
```
Example: `Silver Bottomed Out? 3 Charts Say Yes (2026 Analysis) | HeavyMetalStats`

**How-to/guide pages:**
```
How to [Action]: [Specific Detail] ([Year] Guide) | [Brand]
```
Example: `How to Buy Physical Silver: Dealer Comparison & Premiums (2026 Guide) | HeavyMetalStats`

**Comparison/list pages:**
```
[Number] Best [Things] in [Year] (Ranked by [Criteria]) | [Brand]
```

### Title Tag Rules

1. **Front-load the primary keyword** — Google bolds matching words, which draws the eye
2. **Include current date/year** for time-sensitive queries (CRITICAL for financial data)
3. **Add a number or data point** — "298M oz" outperforms "Latest Data"
4. **Use separators** — em dash (—) or pipe (|) to visually break sections
5. **50-60 characters max** — truncated titles hurt CTR
6. **Never duplicate titles** across pages — each page must have unique title
7. **Match search intent exactly** — if users search "COMEX silver inventory February 2026", the title must contain those words

### Meta Description Rules for CTR

Descriptions don't affect ranking but directly affect CTR. Google bolds keyword matches.

1. **150-160 characters** — truncation wastes your pitch
2. **Start with the answer** — "COMEX silver registered inventory is 298.1M oz as of April 15, 2026" not "Welcome to our site where we track..."
3. **Include a call-to-action** — "See live chart", "Compare dealers", "Track daily changes"
4. **Include the primary keyword** — Google bolds it in results
5. **Add differentiators** — "Updated daily", "Free", "No signup required", "With interactive charts"
6. **Use numbers** — "Track 5 metals across 3 exchanges" > "Track precious metals"

**Template for data pages:**
```
[Current data point with date]. [What the page offers]. [Differentiator]. [CTA].
```
Example: `COMEX silver registered inventory: 298.1M oz (Apr 15, 2026). Daily updates with interactive charts. Free, no signup. See live data →`

**Template for blog/analysis:**
```
[Key finding or claim]. [Supporting data point]. [What reader will learn]. [CTA].
```

### Dynamic Titles and Descriptions (for Data Sites)

For sites showing live/frequently-updated data, titles and descriptions should update automatically:

**Next.js App Router pattern:**
```typescript
// app/precious-metals/page.tsx
export async function generateMetadata(): Promise<Metadata> {
  const data = await getLatestInventory();
  const date = new Date().toLocaleDateString('en-US', { month: 'long', year: 'numeric' });

  return {
    title: `COMEX Silver Inventory — ${data.total} (Updated ${date})`,
    description: `COMEX silver registered inventory is ${data.registered} as of ${data.date}. Track daily changes with interactive charts. Free, updated daily.`,
  };
}
```

This ensures title tags always match date-specific searches (e.g., "COMEX silver inventory April 2026").

### Fixing Date-Specific Query CTR

When GSC shows many impressions for date-stamped queries (e.g., "COMEX silver inventory February 2026") with 0% CTR:

1. **Root cause**: Title tag lacks the date, so users don't see freshness confirmation in SERP
2. **Fix**: Add dynamic date to title using `generateMetadata()` or equivalent
3. **Verify**: Title in "View Page Source" contains current month/year
4. **Monitor**: Request re-indexing in GSC after deploying, check CTR in 2-4 weeks

### Fixing Duplicate URL CTR Dilution

When both `www.example.com` and `example.com` appear in GSC Pages report:

1. **Root cause**: Missing or misconfigured canonical / redirect
2. **Impact**: Clicks and impressions split between two URLs, halving effective CTR
3. **Fix**:
   - Pick one canonical domain (www or non-www)
   - Add 301 redirect from non-canonical to canonical in middleware or hosting config
   - Ensure all `<link rel="canonical">` tags use the canonical domain
   - Update sitemap to only include canonical domain URLs
4. **Verify**: After redirect is live, check GSC for the non-canonical domain — impressions should drop to zero over weeks

### Rich Snippets for CTR

Rich results (stars, FAQs, tables, prices) dramatically increase CTR by making your result visually larger and more informative.

| Rich Result Type | CTR Boost | When to Use |
|-----------------|-----------|------------|
| FAQ (`FAQPage`) | +15-25% | Pages with Q&A sections |
| How-To (`HowTo`) | +10-20% | Step-by-step guides |
| Star Rating (`AggregateRating`) | +10-35% | Products, tools, services |
| Price (`Offer`) | +15-30% | Product/pricing pages |
| Breadcrumbs (`BreadcrumbList`) | +5-10% | All inner pages |
| Article date (`Article`) | +5-15% | Blog posts (shows publish date in SERP) |
| Sitelinks Search Box (`WebSite`) | +10% on branded | Homepage only |

**Priority for data/analytics sites:**
1. `BreadcrumbList` on all pages (shows site hierarchy in SERP)
2. `Article` with `datePublished`/`dateModified` on blog posts (shows freshness)
3. `FAQPage` on learn/educational pages (expands SERP real estate)
4. `WebSite` with `SearchAction` on homepage (sitelinks search box)
5. `Dataset` schema on data pages (shows in Google Dataset Search)

### CTR Optimization Checklist

After analyzing GSC data, output this customized checklist:

```
## CTR Optimization Plan

### Immediate Fixes (deploy this week)
- [ ] Rewrite title tags for pages with CTR below benchmark
- [ ] Add dynamic dates to titles for time-sensitive data pages
- [ ] Write compelling meta descriptions for top-20 impression pages
- [ ] Fix www/non-www duplicate if present (add 301 redirect)
- [ ] Add canonical tags pointing to preferred domain

### Structured Data (deploy within 2 weeks)
- [ ] Add BreadcrumbList to all inner pages
- [ ] Add Article schema with dateModified to blog posts
- [ ] Add FAQPage schema to educational pages
- [ ] Add Dataset schema to data/chart pages
- [ ] Test all structured data with Rich Results Test

### Monitor (check after 4 weeks)
- [ ] Compare CTR for rewritten title pages vs baseline
- [ ] Check Search Appearance in GSC for new rich result types
- [ ] Verify www/non-www consolidation in Pages report
- [ ] Re-audit any pages still below CTR benchmarks
```

## Step 3: Audit robots.txt and Sitemap

### robots.txt

Must exist at site root. Check for:

```
# Good baseline
User-agent: *
Allow: /
Disallow: /api/
Disallow: /admin/
Disallow: /private/

# Point to sitemap
Sitemap: https://example.com/sitemap.xml

# Bing-specific (optional)
User-agent: Bingbot
Crawl-delay: 1

# Yandex-specific (optional)
User-agent: Yandex
Crawl-delay: 2
Host: https://example.com
```

**Critical rules:**
- NEVER block CSS/JS resources Google needs to render pages
- `Disallow` does NOT prevent indexing — use `noindex` meta tag instead
- Verify with Google's robots.txt Tester in Search Console
- **AI crawlers**: Block training bots (`GPTBot`, `Google-Extended`, `ClaudeBot`, `CCBot`, etc.) while allowing AI search bots (`OAI-SearchBot`, `PerplexityBot`) that cite sources with links back. See [technical-seo.md → AI Crawler Management](technical-seo.md#ai-crawler-management-training-vs-search) for the full bot reference table and templates.

### XML Sitemap

Must include all canonical, indexable pages:

```xml
<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
  <url>
    <loc>https://example.com/page/</loc>
    <lastmod>2026-01-15</lastmod>
    <changefreq>weekly</changefreq>
    <priority>0.8</priority>
  </url>
</urlset>
```

**Rules:**
- Max 50,000 URLs or 50MB per sitemap file
- Use sitemap index for larger sites
- Only include canonical URLs (not redirects, not noindexed pages)
- `<loc>` must use absolute HTTPS URLs matching canonicals
- `<lastmod>` must reflect actual content change dates
- Reference sitemap in robots.txt
- Submit to Google Search Console, Bing Webmaster Tools, and Yandex Webmaster

### Bing-Specific: IndexNow

For instant indexing on Bing, Yandex, DuckDuckGo:

```bash
# Notify search engines of new/updated URLs instantly
curl "https://api.indexnow.org/indexnow?url=https://example.com/page/&key=YOUR_API_KEY"
```

Create a key file at `https://example.com/YOUR_API_KEY.txt` containing the key.

## Step 4: Audit Structured Data

Use JSON-LD format (Google recommended). Place in `<head>` or `<body>`.

### Website + Organization (homepage)

```json
{
  "@context": "https://schema.org",
  "@type": "WebSite",
  "name": "Site Name",
  "url": "https://example.com",
  "potentialAction": {
    "@type": "SearchAction",
    "target": "https://example.com/search?q={search_term_string}",
    "query-input": "required name=search_term_string"
  }
}
```

### Breadcrumbs (all inner pages)

```json
{
  "@context": "https://schema.org",
  "@type": "BreadcrumbList",
  "itemListElement": [
    {"@type": "ListItem", "position": 1, "name": "Home", "item": "https://example.com/"},
    {"@type": "ListItem", "position": 2, "name": "Category", "item": "https://example.com/category/"}
  ]
}
```

### Common Schema Types

Choose based on content type. For detailed implementation, see [structured-data.md](structured-data.md).

| Content Type | Schema Type |
|-------------|-------------|
| Articles/Blog | `Article`, `BlogPosting` |
| Products | `Product` with `Offer` |
| Local Business | `LocalBusiness` |
| FAQ pages | `FAQPage` with `Question` |
| How-to guides | `HowTo` |
| Events | `Event` |
| Recipes | `Recipe` |
| Videos | `VideoObject` |
| Reviews | `Review`, `AggregateRating` |
| Software/App | `SoftwareApplication` |

**Validation:** Test with Google Rich Results Test and Schema.org Validator.

## Step 5: Audit Internal Linking and URL Structure

- Use descriptive, keyword-rich anchor text (not "click here")
- Ensure flat URL hierarchy (max 3 levels deep from root)
- Use hyphens in URLs, not underscores
- Lowercase URLs only
- Avoid URL parameters when possible; use clean paths
- Every important page should be reachable within 3 clicks from homepage
- Add breadcrumb navigation matching structured data
- Check for orphan pages (no internal links pointing to them)

## Step 6: Core Web Vitals

Check and optimize these metrics:

| Metric | Target | What It Measures |
|--------|--------|-----------------|
| LCP | < 2.5s | Largest Contentful Paint (loading speed) |
| INP | < 200ms | Interaction to Next Paint (responsiveness) |
| CLS | < 0.1 | Cumulative Layout Shift (visual stability) |

**Common fixes:**
- LCP: Optimize images (WebP/AVIF, lazy-load below fold, preload hero image), minimize render-blocking CSS/JS
- INP: Break up long tasks, use `requestIdleCallback`, defer non-critical JS
- CLS: Set explicit `width`/`height` on images/videos, avoid injecting content above existing content

## Step 7: JavaScript SEO (SPA/SSR)

If the project uses client-side rendering:

1. **Verify SSR/SSG is enabled** — Pure client-side rendering is an SEO blocker
2. **Check that meta tags render server-side** — Not just injected by JS after load
3. **Use History API for routing** — Not hash fragments (`#/page`)
4. **Ensure canonical tags are in initial HTML** — Not dynamically added
5. **Return proper HTTP status codes** — 404 for missing pages, not soft 404
6. **Test with "View Page Source"** — If content isn't in source, Google may not see it

For detailed JS SEO guidance, see [technical-seo.md](technical-seo.md).

## Step 8: Multi-Engine Compatibility

### Bing + Copilot (GEO)

Bing now powers both traditional search and AI-generated Copilot answers. SEO and GEO (Generative Engine Optimization) share the same crawling/indexing foundation.

- Submit sitemap at bing.com/webmaster
- Add `<meta name="msvalidate.01" content="VERIFICATION_CODE">` for ownership
- **Configure IndexNow** — Bing prefers streaming submissions over batch for faster indexing
- **AI/Copilot control directives**:
  - `noarchive` — blocks content from Copilot answers entirely
  - `nocache` — limits Copilot to URL/title/snippet only
  - `data-nosnippet` — excludes specific HTML elements from snippets and Copilot
  - `data-snippet` — specifies text Bing may quote in Copilot citations
- **302 redirects** — Bing says use only for changes lasting <2 days (stricter than Google)
- **Prompt injection** — Hidden text designed to manipulate AI models results in delisting
- For full Bing/Copilot reference, see [bing-copilot-seo.md](bing-copilot-seo.md)

### Yandex Webmaster

- Submit sitemap at webmaster.yandex.com
- Add `<meta name="yandex-verification" content="VERIFICATION_CODE">`
- `Host` directive in robots.txt for preferred domain (Yandex-only feature)
- `Crawl-delay` in robots.txt for Yandex bot
- **`keywords` meta tag matters** — Yandex actually considers it for relevance (Google ignores it)
- **Allow directives take priority** over deny when conflicting — opposite of Google
- **robots.txt overrides meta tags** — if robots.txt blocks a page, `noindex` is ignored
- **10 MB document size limit** (Google is 15 MB)
- **Original Texts tool** — submit original content before publication to establish authorship
- **Indexes iframe/frame content** — unlike most engines
- For Yandex-specific error types, see [multi-engine-errors.md](multi-engine-errors.md)

### Apple (Applebot)

Powers Spotlight, Siri, and Safari search across all Apple devices:

- **Two user agents** with distinct purposes:
  - `Applebot` — search crawling (allow this for search visibility)
  - `Applebot-Extended` — AI training data; block to opt out without losing search
- **Falls back to Googlebot rules** if no Applebot section in robots.txt
- Renders pages in a browser — don't block CSS/JS
- Supports `noindex`, `nosnippet`, `nofollow`, `none`, `all` directives
- Verify traffic via reverse DNS (`*.applebot.apple.com`) or IP list at `search.developer.apple.com/applebot.json`

```
# robots.txt — allow search, block AI training
User-agent: Applebot
Allow: /

User-agent: Applebot-Extended
Disallow: /
```

### DuckDuckGo

- Sources results from Bing — optimizing for Bing covers DuckDuckGo
- Supports IndexNow protocol
- Respects standard robots.txt and meta robots tags

### Regional Engines (Baidu, Naver, Seznam.cz)

Critical for projects targeting specific markets. Key gotchas:

- **Baidu (China)** — Cannot render JavaScript; does NOT support `noindex` meta tag; requires ICP License and mainland China hosting; .CN domain preferred
- **Naver (South Korea)** — Registration-first discovery; indexing takes up to 14 days; supports IndexNow
- **Seznam.cz (Czech Republic)** — Crawls much slower than Google; prefers server-rendered HTML; 100/day manual URL submission limit

For full regional engine requirements, see [regional-engines.md](regional-engines.md).

### IndexNow Protocol (Multi-Engine Instant Notification)

Single submission notifies all participating engines: Bing, Yandex, Naver, Seznam.cz, Yep.

```bash
# Submit URL change (shared to all IndexNow engines)
curl "https://api.indexnow.org/indexnow?url=https://example.com/page/&key=YOUR_API_KEY"
```

**Not supported by**: Google, Baidu, Apple — use their native submission tools.

### Engine-Specific Gotchas

| Gotcha | Engine | Impact |
|--------|--------|--------|
| `noindex` meta tag ignored | Baidu | Must use robots.txt to block pages |
| No JavaScript rendering | Baidu | All content must be server-rendered |
| `keywords` meta tag used for ranking | Yandex | Add relevant keywords (others ignore it) |
| Allow overrides Deny in meta directives | Yandex | Opposite of Google's "restrictive wins" |
| Falls back to Googlebot rules | Applebot | Your Google robots.txt rules affect Apple |
| `noarchive` blocks AI answers | Bing | Prevents content from appearing in Copilot |
| 302 must be <2 days | Bing | Stricter than Google's 302 guidance |
| Indexing takes up to 14 days | Naver | Much slower than Google |
| ICP License legally required | Baidu | Cannot host in China without it |

### General Multi-Engine Rules

- Use standard HTML meta tags (all engines understand them)
- Structured data benefits all engines — validate with multiple tools
- Valid XML sitemap works across all engines
- Clean, semantic HTML is universally beneficial
- Server-side rendering is mandatory for Baidu, strongly preferred by Seznam.cz
- Configure IndexNow alongside Google's native submission tools

## Step 9: Fixing Issues

When issues are found, fix them in priority order:

1. **Critical** (blocks indexing): Missing pages, server errors, redirect loops, noindex on important pages, blocked by robots.txt
2. **High** (hurts rankings): Missing titles/descriptions, duplicate content, broken canonical tags, missing structured data
3. **Medium** (limits potential): Poor Core Web Vitals, missing Open Graph, weak internal linking
4. **Low** (polish): Missing alt text on non-critical images, minor schema improvements

For Google Search Console indexing error resolution, see [indexing-errors.md](indexing-errors.md).
For Bing and Yandex indexing errors, see [multi-engine-errors.md](multi-engine-errors.md).

## Step 10: Validate Fixes

After applying fixes:

1. Check HTML validity with W3C validator
2. Test structured data with Google Rich Results Test, Bing Markup Validator, and Schema.org Validator
3. Test mobile-friendliness with Google Mobile-Friendly Test
4. Verify robots.txt with Google's robots.txt Tester
5. Validate sitemap XML structure
6. Use Google Search Console URL Inspection tool to request re-indexing
7. Use Bing URL Inspection tool to request re-indexing and check SEO card
8. Submit updated sitemap to all search engine webmaster tools (Google, Bing, Yandex, Baidu, Naver)
9. Submit URL changes via IndexNow for Bing, Yandex, Naver, Seznam.cz
10. Verify Applebot can access pages (check robots.txt fallback to Googlebot rules)

## Step 11: Post-Deploy Manual Actions

After pushing code fixes, the user/administrator MUST complete these steps manually in each search engine console. **Always output this checklist to the user after making SEO changes**, customized to the specific fixes that were applied.

### Google Search Console (search.google.com/search-console)

1. **Test robots.txt** (if robots.txt was changed)
   - Settings > robots.txt > click "Check"
   - Verify blocked/allowed paths are correct

2. **Resubmit sitemap** (if sitemap was changed)
   - Indexing > Sitemaps > enter `sitemap.xml` > Submit
   - This clears stale entries (e.g. removed URLs) from Google's copy

3. **Request re-indexing of changed pages** (URL Inspection tool)
   - Paste each changed URL into the search bar, click "Request Indexing"
   - Prioritize: pages with new structured data, new/changed canonical, new meta tags
   - Rate limit: ~10 URLs per day max

4. **Check Page Indexing report for existing errors**
   - Indexing > Pages > review "Why pages aren't indexed" table
   - Look for errors that should now be fixed (e.g. "Submitted URL blocked by robots.txt" after removing contradictory sitemap entries)
   - Click "Validate Fix" on any error categories that were addressed

5. **Validate structured data**
   - Enhancements > check for new rich result types
   - Or use Rich Results Test (search.google.com/test/rich-results) to test individual URLs

6. **Verify site ownership** (if verification meta tag was added/changed)
   - Settings > Ownership verification > confirm HTML tag method shows "Verified"

### Bing Webmaster Tools (bing.com/webmaster)

7. **Resubmit sitemap** (if sitemap changed)
   - Sitemaps > resubmit URL

8. **Submit URLs via IndexNow** (fastest method for Bing/Yandex/DuckDuckGo)
   - If the project has an IndexNow endpoint, trigger it for all changed URLs
   - Otherwise: `curl "https://api.indexnow.org/indexnow?url=<URL>&key=<KEY>"`

9. **Check URL Inspection** for changed pages
   - Enter changed URLs > review SEO tab for warnings

### Yandex Webmaster (webmaster.yandex.com)

10. **Set up Yandex Webmaster** (if not already done)
    - Add site, verify via HTML meta tag (add `yandex-verification` to layout verification config)
    - Submit sitemap

11. **Recheck indexing** (if robots.txt or sitemap changed)
    - Indexing > Sitemap files > resubmit
    - Check "Pages in search" for error counts

### Template for User Output

When presenting post-deploy steps to the user, customize this template based on what was actually changed:

```
## After You Push — Manual Steps

### Google Search Console
- [ ] Resubmit sitemap (Indexing > Sitemaps > Submit)
- [ ] Request re-indexing for: [list specific changed URLs]
- [ ] Validate fix for: [list specific GSC error categories that were fixed]
- [ ] Test structured data on: [list pages with new/changed JSON-LD]

### Bing Webmaster Tools
- [ ] Resubmit sitemap
- [ ] Submit changed URLs via IndexNow

### Yandex Webmaster
- [ ] Resubmit sitemap (if set up)
```

## Additional Resources

- For all GSC indexing error types and fixes: [indexing-errors.md](indexing-errors.md)
- For Bing and Yandex indexing errors: [multi-engine-errors.md](multi-engine-errors.md)
- For Bing Copilot/AI grounding and GEO: [bing-copilot-seo.md](bing-copilot-seo.md)
- For Baidu, Naver, and Seznam.cz: [regional-engines.md](regional-engines.md)
- For technical crawling/rendering details: [technical-seo.md](technical-seo.md)
- For structured data implementation: [structured-data.md](structured-data.md)
- For full audit checklist: [audit-checklist.md](audit-checklist.md)
