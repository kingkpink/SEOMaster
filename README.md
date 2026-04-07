# SEO Master — Cursor AI Skill for Web Developers

An AI-powered SEO auditing and optimization skill for [Cursor](https://cursor.com). Drop it into your project and let your AI coding assistant handle technical SEO across **Google, Bing/Copilot, Yandex, Apple, Baidu, Naver, and Seznam.cz** — so you can focus on building.

## What This Is

SEO Master is a **Cursor Agent Skill** — a set of structured markdown files that give Cursor's AI agent deep domain knowledge about search engine optimization. When attached to a conversation, the agent can audit your codebase, identify SEO issues, and fix them directly in your source files.

Think of it as giving your AI assistant the equivalent of a senior SEO engineer's knowledge base, covering every major search engine's documentation.

## What It Does

When you trigger the skill (mention SEO, indexing errors, search rankings, sitemaps, etc.), the agent follows a **10-step audit workflow**:

1. **Discovers your tech stack** — Static HTML, Next.js, Nuxt, SvelteKit, Astro, React SPA, WordPress, etc.
2. **Audits HTML head tags** — title, meta description, canonical URLs, Open Graph, Twitter Cards
3. **Audits robots.txt and sitemaps** — validates structure, checks for blocking issues, verifies IndexNow setup
4. **Audits structured data** — JSON-LD schema.org markup for rich results (Articles, Products, FAQs, Events, etc.)
5. **Audits internal linking and URL structure** — anchor text, hierarchy depth, orphan pages
6. **Audits Core Web Vitals** — LCP, INP, CLS with specific fix recommendations
7. **Audits JavaScript SEO** — SSR/SSG verification, client-side rendering detection
8. **Audits multi-engine compatibility** — engine-specific directive differences, AI grounding controls, regional requirements
9. **Fixes issues** in priority order — Critical > High > Medium > Low
10. **Validates fixes** across all engines and provides post-deploy manual steps

The agent doesn't just tell you what's wrong — it edits your code to fix it, then tells you what manual steps remain (like submitting sitemaps in Google Search Console).

## Search Engine Coverage

| Engine | Coverage |
|--------|----------|
| **Google** | Full — GSC indexing errors (22 types), crawl/render/index pipeline, structured data, Core Web Vitals |
| **Bing / Copilot** | Full — 22 webmaster guidelines, AI grounding directives, GEO (Generative Engine Optimization), `data-nosnippet`/`data-snippet` controls |
| **Yandex** | Full — 25-type error taxonomy, Original Texts tool, `keywords` meta tag handling, Host directive, 10MB limits |
| **Apple (Applebot)** | Covered — Applebot vs Applebot-Extended, Googlebot fallback behavior, Siri/Spotlight/Safari optimization |
| **Baidu** | Covered — ICP License requirements, no-JS rendering, `noindex` not supported, mainland China hosting |
| **Naver** | Covered — Registration-first discovery, 14-day indexing, supported structured data types |
| **Seznam.cz** | Covered — SeznamBot behavior, server-rendered HTML preference, manual submission limits |
| **DuckDuckGo** | Covered via Bing (sources results from Bing index) |
| **IndexNow** | Full — cross-engine instant notification protocol (Bing, Yandex, Naver, Seznam, Yep) |

## File Structure

```
seo-master/
├── SKILL.md                 # Main skill — 10-step audit workflow and quick reference
├── bing-copilot-seo.md      # Bing's 22 guidelines, Copilot/AI grounding, GEO concepts
├── multi-engine-errors.md   # Indexing error types for Bing, Yandex, and Apple (alongside Google)
├── regional-engines.md      # Baidu, Naver, Seznam.cz technical requirements
├── indexing-errors.md       # Google Search Console — all 22 indexing error types with fixes
├── technical-seo.md         # Crawling, rendering, meta directives, multi-engine robots.txt
├── structured-data.md       # JSON-LD implementation for all schema.org types
├── audit-checklist.md       # Comprehensive audit checklist (13 sections + monitoring)
└── README.md
```

## Installation

### For Cursor Users

Copy the `seo-master/` folder into your Cursor skills directory:

```bash
# Clone the repo
git clone https://github.com/kingkpink/SEOMaster.git

# Copy into your Cursor skills directory
cp -r SEOMaster/ ~/.cursor/skills/seo-master/
```

Then mention SEO in any Cursor conversation, or attach the skill manually with `/seo-master`.

### As a Reference

Even without Cursor, the markdown files serve as a standalone technical SEO reference. Each file is self-contained and covers its topic with actionable fix steps and code examples.

## Usage Examples

Once installed, just describe what you need in Cursor:

- *"Audit this site for SEO issues"* — Runs the full 10-step workflow
- *"Fix my Google Search Console indexing errors"* — Diagnoses and resolves specific GSC issues
- *"Add structured data to my product pages"* — Implements JSON-LD Product schema
- *"Set up robots.txt for all search engines"* — Generates a multi-engine robots.txt
- *"Optimize this Next.js app for Bing Copilot"* — Applies GEO best practices and AI grounding directives
- *"Make this site work for Baidu"* — Identifies China-specific blockers (JS rendering, ICP, hosting)

## Key Highlights for Developers

**Engine-specific gotchas that break real projects:**

| Gotcha | Engine | What Happens If You Miss It |
|--------|--------|-----------------------------|
| `noindex` meta tag is ignored | Baidu | Pages you want hidden appear in Chinese search results |
| No JavaScript rendering | Baidu | Your entire SPA is invisible to 70% of China's search traffic |
| `noarchive` blocks AI answers | Bing | Content disappears from Copilot citations |
| Applebot falls back to Googlebot rules | Apple | Your Google-specific blocks accidentally hide you from Siri/Spotlight |
| Allow overrides Deny | Yandex | Pages you blocked are actually accessible to Yandex |
| `keywords` meta tag used for ranking | Yandex | Missing an easy ranking signal that other engines ignore |
| ICP License legally required | Baidu | Your site gets blocked by the Great Firewall |

**Multi-engine meta directive support:**

| Directive | Google | Bing | Yandex | Baidu | Apple |
|-----------|--------|------|--------|-------|-------|
| `noindex` | Yes | Yes | Yes | **No** | Yes |
| `noarchive` | Yes | Yes (blocks Copilot) | Yes | Yes | No |
| `nocache` | No | **Yes** (Copilot control) | No | No | No |
| `data-nosnippet` | Yes | Yes | No | No | No |
| `data-snippet` | No | **Yes** | No | No | No |

## Contributing

Found an error, or a search engine updated their docs? PRs welcome. Each file is self-contained — edit the relevant markdown file and submit.

## License

MIT
