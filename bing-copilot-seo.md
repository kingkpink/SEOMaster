# Bing, Copilot & Generative Engine Optimization (GEO)

Complete reference for Bing Webmaster Guidelines, Copilot/AI grounding controls, and Generative Engine Optimization. Based on Bing's official guidelines at bing.com/webmasters.

## Core Concept: SEO + GEO

Bing distinguishes two complementary practices:

- **SEO** — Technical quality, clarity, and accessibility to help Bing discover, understand, and evaluate content
- **GEO (Generative Engine Optimization)** — Content eligibility for grounding and reference in AI responses (Copilot)

Both rely on the same crawling, indexing, and ranking foundation. Neither guarantees rankings, traffic, or citations.

## Bing Webmaster Guidelines Summary

### 1. Discovery and Crawl Signals

Ensure Bing can reliably discover URLs using:

- **IndexNow** URL submission (preferred — instant notification)
- XML sitemaps with freshness signals
- Crawlable internal links with relevant anchor text
- External links from relevant websites

### 2. Sitemaps for Importance and Freshness

```xml
<!-- Bing sitemap requirements -->
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
  <url>
    <loc>https://example.com/page/</loc>
    <lastmod>2026-04-07</lastmod> <!-- Accurate lastmod is critical for Bing -->
  </url>
</urlset>
```

Sitemaps should:

- List only canonical URLs
- Reflect current site structure (remove deleted/redirected URLs promptly)
- Include accurate `lastmod` values — Bing uses these + ETags to detect content changes
- Be submitted to Bing Webmaster Tools at bing.com/webmaster

### 3. IndexNow: Instant Notification

Notify Bing when URLs are added, updated, or removed:

```bash
# Single URL submission
curl "https://www.bing.com/indexnow?url=https://example.com/page/&key=YOUR_KEY"

# Batch submission (up to 10,000 URLs)
curl -X POST "https://api.indexnow.org/indexnow" \
  -H "Content-Type: application/json" \
  -d '{
    "host": "example.com",
    "key": "YOUR_KEY",
    "urlList": [
      "https://example.com/page1/",
      "https://example.com/page2/"
    ]
  }'
```

**Bing-specific guidance:**
- Prefer **streaming** (submit as changes happen) over batch submissions
- Streaming provides faster updates, reduces server load, and improves indexing accuracy
- IndexNow URLs are shared across all participating engines: Bing, Yandex, Naver, Seznam.cz, Yep

### 4. Link Structure and Authority

- Every important URL must be reachable through crawlable internal links
- Use standard `<a href>` links (not JS click handlers)
- Include relevant anchor text or image alt attributes
- Strong internal + external linking supports discovery, authority, and grounding eligibility

### 5. Duplicate URL Consolidation

- Duplicate URLs dilute signals and reduce Bing's confidence in selecting a URL for grounding/citations
- Use canonical URLs, parameter controls, and consistent URL structures
- This is more impactful for Copilot than traditional search — Bing needs high confidence to cite a URL

### 6. URL Moves and Redirects

- **301** for permanent URL changes
- **302** only for very short-term changes (**less than 2 days** — Bing is more specific than Google here)
- **Use redirects instead of canonical tags** when possible (stronger signal for Bing)
- Proper redirects preserve visibility, traffic, and grounding continuity

### 7. Crawling and Rendering

Avoid:
- Blocking important URLs unnecessarily in robots.txt
- Hiding critical content behind client-side-only rendering
- Excessive/unnecessary HTTP requests to render content
- Outputting excessive low-value URLs (parameter variations, duplicates)

Content that cannot be reliably rendered may not be indexed or selected for grounding.

### 8. Clean URL Removal

When content is permanently removed:

- Return 404 status code
- Use Bing's **Content Removal tools** (Block URLs tool for temp 90-day hide, processed in <12 hours)
- Notify via IndexNow that the URL was deleted
- Prevents outdated URLs from appearing in search or being referenced in Copilot

### 9. robots.txt vs Meta Directives

| Directive | Controls | Effect on Copilot |
|-----------|----------|-------------------|
| `robots.txt Disallow` | Crawl access only | Does NOT prevent indexing |
| `noindex` | Indexing | Removes from Bing search AND Copilot |
| `noarchive` | Caching + AI | Blocks content from Copilot answers entirely |
| `nocache` | Caching + AI | Limits Copilot to URL/title/snippet only |
| `nosnippet` | Display | Prevents captions, may limit Copilot citation quality |
| `data-nosnippet` | Per-element display | Excludes specific elements from snippets and Copilot |
| `data-snippet` | Per-element display | Specifies text Bing may quote in Copilot |

### 10. Content Clarity

Content should:
- Fully satisfy user intent
- Be original and authoritative
- Be easy to understand without external context
- Thin, ad-heavy, or affiliate-only URLs may lose ranking and grounding visibility

### 11. Images and Video

Provide descriptive file names, alt text, captions, transcripts, or structured data. Images/video should reinforce primary text, not be the sole source of information.

### 12. HTML Structure

- Unique, non-duplicate `<title>` tags
- Compelling `<meta description>` tags
- Semantic HTML elements (`nav`, `main`, `article`, `section`)
- Logical heading hierarchy (h1 > h2 > h3)

Missing, duplicate, or overly short titles/descriptions reduce indexing reliability, ranking, and grounding eligibility.

### 13. Structured Data

Structured data may support clearer grounding but does not guarantee visibility. Markup must accurately reflect visible content. Misleading structured data may be ignored and affect trust.

### 14. Verifiable Content

URLs are more likely to be selected for grounding when:
- Facts and definitions are explicit (not implied)
- Key statements don't rely on context from other pages
- Important information is visible on the URL itself

### 15. Entity Definition

Use clear and consistent naming for people, organizations, products, and locations. Avoid ambiguous references. Clear entity definition improves grounding visibility and citation accuracy.

### 16. Single Topic Per URL

URLs focused on a primary topic are more likely to be selected for grounding:
- Avoid mixing unrelated concepts on a single URL
- Align titles, headings, and content intent

### 17. Key Information Placement

Place essential information near the top of the page. Avoid long introductions before addressing the main topic. Early clarity improves grounding visibility.

### 18. Content Freshness

- Update content when facts or guidance change
- Use freshness signals (lastmod, ETags) appropriately
- Remove or revise outdated information
- Notify IndexNow when content is added, updated, or deleted

### 19. URL Stability

Avoid unnecessary URL changes. Stable URLs support long-term visibility and grounding continuity. When changes are required, use proper redirects.

### 20. Crawl Efficiency

Excessive low-value URLs, duplication, or crawl waste can delay indexing and reduce grounding visibility. Best practices:
- Eliminate duplicate or low-value URLs
- Use canonicalization consistently
- Block unnecessary crawl paths with robots.txt
- Keep site structure logical and accessible

### 21. Measure Beyond Clicks

Content may surface across Bing experiences without traditional clicks. Monitor:
- Impressions
- Indexing status
- Grounding and citation eligibility (via Bing Webmaster Tools AI Dashboard)

A decline in clicks does not always indicate a loss of visibility — content may appear as citations in Copilot responses.

## Bing Meta Robots Directives — Complete Reference

All directives can be specified as `<meta>` tags or `X-Robots-Tag` HTTP headers. Replace `name="robots"` with `name="bingbot"` to target Bing only.

### Indexing Control

```html
<!-- Block indexing (same as Google) -->
<meta name="robots" content="noindex">
```

### AI Training Control

```html
<!-- Block content from training Microsoft's generative AI models -->
<meta name="robots" content="nocache">

<!-- Block content from Copilot answers AND AI training -->
<meta name="robots" content="noarchive">
```

### Snippet and Display Control

```html
<!-- No text snippet or preview thumbnail -->
<meta name="robots" content="nosnippet">

<!-- Limit snippet text length (characters) -->
<meta name="robots" content="max-snippet:400">

<!-- Limit image preview size: none | standard | large -->
<meta name="robots" content="max-image-preview:large">

<!-- Limit video preview length (seconds, -1 = unlimited) -->
<meta name="robots" content="max-video-preview:-1">
```

### HTML-Level Snippet Control

```html
<!-- Exclude specific elements from snippets and Copilot answers -->
<div data-nosnippet>
  <p>This content won't appear in Bing snippets or Copilot.</p>
</div>

<!-- Specify text Bing MAY quote in Copilot citations -->
<div data-snippet>
  <p>This is the preferred text for Bing to cite.</p>
</div>
```

### Copilot/AI Impact Matrix

| Tags Present | Bing Search | Copilot/Chat | AI Training |
|-------------|-------------|--------------|-------------|
| None | Full visibility | Full content in answers | Content used |
| `nocache` | Full visibility | URL/title/snippet only | URL/title/snippet only |
| `noarchive` | Full visibility | Excluded from answers | Not used |
| `nocache` + `noarchive` | Full visibility | URL/title/snippet only (treated as nocache) | URL/title/snippet only |
| `noindex` | Not indexed | Not available | Not available |

## Bing Content Removal Tools

### For Site Owners

| Method | Speed | Duration | Use Case |
|--------|-------|----------|----------|
| Block URLs tool | <12 hours | 90 days (temporary) | Quick hide while making permanent changes |
| 404/410 status code | Days | Permanent | Content permanently removed |
| `noindex` meta tag | Days | Permanent | Page exists but should not be indexed |
| `X-Robots-Tag: noindex` | Days | Permanent | Non-HTML files (PDFs, images) |

### For Non-Site Owners

Use Bing's Content Removal Tool at `bing.com/webmasters/tools/contentremoval` when:
- Content is no longer accessible but still showing in results
- Content was updated but Bing shows the old version

### Accelerating Removal

After making changes, notify Bing via IndexNow or updated XML sitemaps for faster re-crawling.

## Bing URL Inspection Tool

The URL Inspection tool provides four diagnostic cards:

### Index Card
- Shows discovery, crawling, and indexing status
- Displays specific errors if URL is not indexed
- Recommended actions: request indexing, edit robots.txt, contact support

### SEO Card
- SEO errors (red — high priority)
- SEO warnings (yellow — medium priority)
- SEO notices (blue — low priority)

### Markup Card
- Validates structured data on the page
- Shows errors in schema implementation

### Request Re-Indexing
- Available based on URL submission quota
- Use after making fixes to trigger re-crawl

## Bing Abuse Policies

The following result in reduced ranking, suppressed grounding, or delisting:

| Violation | Description |
|-----------|-------------|
| Cloaking | Different content for crawlers vs users |
| Link schemes | Buying links, link networks, artificial promotion |
| Duplicate content farming | Same content across multiple URLs |
| Scraped content | Copying without added value |
| Keyword stuffing | Unnatural keyword repetition |
| Auto-generated content at scale | Mass-produced without editorial oversight |
| Thin affiliate sites | Redirecting to retailers without original value |
| Malicious behavior | Phishing, malware distribution |
| Misleading structured data | Schema that doesn't match visible content |
| **Prompt injection** | Content designed to manipulate Copilot/AI models |

**Prompt injection** is a new violation category unique to Bing — hidden text or instructions attempting to influence AI responses can result in removal.

## Bing Webmaster Tools Setup

1. Go to `bing.com/webmaster`
2. Verify site ownership:
   ```html
   <meta name="msvalidate.01" content="YOUR_VERIFICATION_CODE">
   ```
3. Submit XML sitemap
4. Configure IndexNow API key
5. Monitor Index Coverage, SEO Reports, and AI Dashboard

## Quick Checklist: Bing + Copilot Optimization

```
- [ ] Site verified in Bing Webmaster Tools
- [ ] XML sitemap submitted with accurate lastmod values
- [ ] IndexNow configured and streaming URL changes
- [ ] No important URLs blocked by robots.txt
- [ ] Proper redirect strategy (301 permanent, 302 < 2 days only)
- [ ] Content is clear, focused, and verifiable
- [ ] Each URL covers a single primary topic
- [ ] Key information placed early on page
- [ ] Entities named clearly and consistently
- [ ] Structured data accurate and matching visible content
- [ ] AI/Copilot control directives set appropriately (nocache/noarchive)
- [ ] data-nosnippet used for sensitive sections
- [ ] data-snippet used for preferred citation text
- [ ] No prompt injection or AI manipulation in content
- [ ] Monitoring impressions and grounding citations, not just clicks
```
