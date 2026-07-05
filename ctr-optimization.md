# CTR Optimization Playbook

> Referenced from SKILL.md Step 2b. Benchmarks and boost figures are field heuristics (as of 2026), not guarantees.

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

(Heuristic industry averages, as of 2026 — recalibrate against your own GSC data.)

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
8. **Account for framework title templates** — SSR frameworks auto-append a brand suffix to every page title (Next.js `title.template: '%s | Brand'`, Nuxt `titleTemplate`, SvelteKit layout `<svelte:head>`). The per-page title STRING you write is not the rendered `<title>`. A 75-char page title plus a ` | Heavy Metal Stats` suffix renders ~95 chars and gets truncated in SERPs. Write the per-page title to ~45-50 chars so the final tag lands at 55-60. Always verify the rendered `<title>` in "View Page Source" (or `curl … | grep '<title>'`), never the source string. To bypass the template on a page that needs full control, use the framework's absolute-title escape (Next.js `title: { absolute: '…' }`).

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
| Star Rating (`AggregateRating`) | +10-35% | Products, tools, services |
| Price (`Offer`) | +15-30% | Product/pricing pages |
| Breadcrumbs (`BreadcrumbList`) | +5-10% | All inner pages |
| Article date (`Article`) | +5-15% | Blog posts (shows publish date in SERP) |
| Sitelinks Search Box (`WebSite`) | +10% on branded | Homepage only |
| FAQ (`FAQPage`) | Google: restricted | See deprecation note below |
| How-To (`HowTo`) | Google: none | Deprecated — see note below |

**Google deprecation note (2023, still in effect):** Google restricted `FAQPage` rich results to well-known, authoritative government and health sites (Aug 2023) and retired `HowTo` rich results entirely (Sept 2023). Most sites will NOT get FAQ/HowTo rich snippets on Google anymore. The markup is still worth keeping where content genuinely matches: Bing still shows FAQ rich results, and Q&A markup helps AI answer engines (Copilot, AI Overviews) ground and cite your content — just don't promise a Google SERP CTR boost from it.

**Priority for data/analytics sites:**
1. `BreadcrumbList` on all pages (shows site hierarchy in SERP)
2. `Article` with `datePublished`/`dateModified` on blog posts (shows freshness)
3. `Dataset` schema on data pages (shows in Google Dataset Search)
4. `WebSite` with `SearchAction` on homepage (sitelinks search box)
5. `FAQPage` on learn/educational pages — for Bing rich results + AI answer grounding, not Google snippets (see deprecation note)

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
