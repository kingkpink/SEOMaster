# Structured Data Reference

JSON-LD implementation guide for all major schema.org types that enable Google rich results.

## Implementation Basics

Always use JSON-LD (Google recommended). Place in `<head>` or `<body>`.

```html
<script type="application/ld+json">
{
  "@context": "https://schema.org",
  "@type": "TypeName",
  ...properties
}
</script>
```

**Rules:**
- One or multiple JSON-LD blocks per page is fine
- Only mark up content visible on the page
- Required properties must be present for rich result eligibility
- Test with Google Rich Results Test before deploying
- Monitor with GSC Rich Results Status Reports after deployment

## Schema Types by Content

### WebSite (Homepage)

```json
{
  "@context": "https://schema.org",
  "@type": "WebSite",
  "name": "Your Site Name",
  "alternateName": "Alternate Name",
  "url": "https://example.com",
  "potentialAction": {
    "@type": "SearchAction",
    "target": {
      "@type": "EntryPoint",
      "urlTemplate": "https://example.com/search?q={search_term_string}"
    },
    "query-input": "required name=search_term_string"
  }
}
```

### Organization

```json
{
  "@context": "https://schema.org",
  "@type": "Organization",
  "name": "Company Name",
  "url": "https://example.com",
  "logo": "https://example.com/logo.png",
  "sameAs": [
    "https://twitter.com/company",
    "https://linkedin.com/company/company",
    "https://github.com/company"
  ],
  "contactPoint": {
    "@type": "ContactPoint",
    "telephone": "+1-555-555-5555",
    "contactType": "customer service"
  }
}
```

### Article / BlogPosting

```json
{
  "@context": "https://schema.org",
  "@type": "Article",
  "headline": "Article Title (max 110 chars)",
  "description": "Brief description",
  "image": ["https://example.com/image.jpg"],
  "datePublished": "2026-01-15T08:00:00+00:00",
  "dateModified": "2026-03-20T10:00:00+00:00",
  "author": {
    "@type": "Person",
    "name": "Author Name",
    "url": "https://example.com/author/name"
  },
  "publisher": {
    "@type": "Organization",
    "name": "Publisher Name",
    "logo": {
      "@type": "ImageObject",
      "url": "https://example.com/logo.png"
    }
  }
}
```

### BreadcrumbList

```json
{
  "@context": "https://schema.org",
  "@type": "BreadcrumbList",
  "itemListElement": [
    {
      "@type": "ListItem",
      "position": 1,
      "name": "Home",
      "item": "https://example.com/"
    },
    {
      "@type": "ListItem",
      "position": 2,
      "name": "Category",
      "item": "https://example.com/category/"
    },
    {
      "@type": "ListItem",
      "position": 3,
      "name": "Current Page"
    }
  ]
}
```

Note: The last item should NOT have an `item` URL (it's the current page).

### FAQPage

```json
{
  "@context": "https://schema.org",
  "@type": "FAQPage",
  "mainEntity": [
    {
      "@type": "Question",
      "name": "What is the question?",
      "acceptedAnswer": {
        "@type": "Answer",
        "text": "The answer text here. Can contain <a href='url'>HTML links</a>."
      }
    },
    {
      "@type": "Question",
      "name": "Second question?",
      "acceptedAnswer": {
        "@type": "Answer",
        "text": "Second answer."
      }
    }
  ]
}
```

### Product

```json
{
  "@context": "https://schema.org",
  "@type": "Product",
  "name": "Product Name",
  "image": ["https://example.com/product.jpg"],
  "description": "Product description",
  "sku": "SKU123",
  "brand": {
    "@type": "Brand",
    "name": "Brand Name"
  },
  "offers": {
    "@type": "Offer",
    "url": "https://example.com/product/",
    "priceCurrency": "USD",
    "price": "29.99",
    "availability": "https://schema.org/InStock",
    "seller": {
      "@type": "Organization",
      "name": "Seller Name"
    }
  },
  "aggregateRating": {
    "@type": "AggregateRating",
    "ratingValue": "4.5",
    "reviewCount": "123"
  }
}
```

### LocalBusiness

```json
{
  "@context": "https://schema.org",
  "@type": "LocalBusiness",
  "name": "Business Name",
  "image": "https://example.com/photo.jpg",
  "address": {
    "@type": "PostalAddress",
    "streetAddress": "123 Main St",
    "addressLocality": "City",
    "addressRegion": "ST",
    "postalCode": "12345",
    "addressCountry": "US"
  },
  "geo": {
    "@type": "GeoCoordinates",
    "latitude": 40.7128,
    "longitude": -74.0060
  },
  "telephone": "+1-555-555-5555",
  "openingHoursSpecification": [
    {
      "@type": "OpeningHoursSpecification",
      "dayOfWeek": ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"],
      "opens": "09:00",
      "closes": "17:00"
    }
  ]
}
```

### HowTo

```json
{
  "@context": "https://schema.org",
  "@type": "HowTo",
  "name": "How to Do Something",
  "description": "Brief description of the how-to",
  "totalTime": "PT30M",
  "estimatedCost": {
    "@type": "MonetaryAmount",
    "currency": "USD",
    "value": "0"
  },
  "step": [
    {
      "@type": "HowToStep",
      "name": "Step 1 Title",
      "text": "Step 1 instructions",
      "image": "https://example.com/step1.jpg"
    },
    {
      "@type": "HowToStep",
      "name": "Step 2 Title",
      "text": "Step 2 instructions"
    }
  ]
}
```

### Event

```json
{
  "@context": "https://schema.org",
  "@type": "Event",
  "name": "Event Name",
  "startDate": "2026-06-15T19:00:00-05:00",
  "endDate": "2026-06-15T23:00:00-05:00",
  "eventStatus": "https://schema.org/EventScheduled",
  "eventAttendanceMode": "https://schema.org/OfflineEventAttendanceMode",
  "location": {
    "@type": "Place",
    "name": "Venue Name",
    "address": {
      "@type": "PostalAddress",
      "streetAddress": "123 Main St",
      "addressLocality": "City",
      "addressRegion": "ST"
    }
  },
  "organizer": {
    "@type": "Organization",
    "name": "Organizer Name",
    "url": "https://example.com"
  }
}
```

### VideoObject

```json
{
  "@context": "https://schema.org",
  "@type": "VideoObject",
  "name": "Video Title",
  "description": "Video description",
  "thumbnailUrl": "https://example.com/thumb.jpg",
  "uploadDate": "2026-01-15T08:00:00+00:00",
  "duration": "PT5M30S",
  "contentUrl": "https://example.com/video.mp4",
  "embedUrl": "https://example.com/embed/video"
}
```

### SoftwareApplication

```json
{
  "@context": "https://schema.org",
  "@type": "SoftwareApplication",
  "name": "App Name",
  "operatingSystem": "Web",
  "applicationCategory": "FinanceApplication",
  "offers": {
    "@type": "Offer",
    "price": "0",
    "priceCurrency": "USD"
  },
  "aggregateRating": {
    "@type": "AggregateRating",
    "ratingValue": "4.8",
    "ratingCount": "500"
  }
}
```

### Review

```json
{
  "@context": "https://schema.org",
  "@type": "Review",
  "itemReviewed": {
    "@type": "Product",
    "name": "Product Name"
  },
  "reviewRating": {
    "@type": "Rating",
    "ratingValue": "4",
    "bestRating": "5"
  },
  "author": {
    "@type": "Person",
    "name": "Reviewer Name"
  }
}
```

## Combining Multiple Types

You can nest or use `@graph` to include multiple schema types on one page:

```json
{
  "@context": "https://schema.org",
  "@graph": [
    {
      "@type": "WebSite",
      "name": "Site Name",
      "url": "https://example.com"
    },
    {
      "@type": "BreadcrumbList",
      "itemListElement": [...]
    },
    {
      "@type": "Article",
      "headline": "..."
    }
  ]
}
```

## Multi-Engine Structured Data Notes

### Bing

- Bing supports JSON-LD, Microdata, and RDFa but recommends JSON-LD
- Structured data may support clearer **Copilot grounding** and citation accuracy
- Misleading structured data may be ignored and can affect trust/eligibility for enhanced features
- Bing has its own **Markup Validator** in Webmaster Tools (URL Inspection > Markup card)
- Bing's Copilot may use structured data to generate richer AI answers

### Yandex

- Yandex supports JSON-LD and Microdata
- Yandex has its own **Structured Data Validator**: `webmaster.yandex.com/tools/microtest/`
- Yandex supports additional types not common on Google:
  - `Recipe` with detailed cooking step markup
  - `SoftwareApplication` for app listings
  - Various commercial schema types for Yandex.Market integration
- Yandex may use structured data differently for its Turbo Pages feature

### Naver

Naver supports structured data for a specific subset of content types:
- Software applications
- Movies
- Restaurants
- Recipes
- FAQs
- Breadcrumbs
- Job postings

Use JSON-LD format. Validate through Naver Search Advisor's built-in tools.

### Baidu

- Baidu supports basic schema.org types but with limited documentation
- JSON-LD is supported but not as widely documented as Google's implementation
- Focus on Article, Product, and FAQ schemas for Baidu
- Test by checking how Baidu renders your pages in Baidu Webmaster Tools crawl diagnostics

## Validation Checklist

### Google

1. Paste JSON-LD into **Google Rich Results Test** (search.google.com/test/rich-results)
2. Verify all required properties are present (no errors)
3. Add recommended properties for richer results
4. Ensure data matches visible page content
5. Check GSC **Rich Results Status Reports** after deployment

### Bing

6. Use **Bing URL Inspection Tool** > Markup card to validate structured data
7. Check for errors in Bing's SEO Reports (Webmaster Tools)
8. Verify structured data supports Copilot grounding goals (accurate, matching visible content)

### Yandex

9. Test with **Yandex Structured Data Validator** (webmaster.yandex.com/tools/microtest/)
10. Check Yandex Webmaster for structured data processing errors

### General

11. Test with **Schema.org Validator** (validator.schema.org) for cross-engine validity
12. Ensure data matches visible page content across all validators
13. Monitor all webmaster tools for structured data warnings after deployment

## Common Mistakes

| Mistake | Impact | Fix |
|---------|--------|-----|
| Missing required properties | No rich result on any engine | Add all required fields per type |
| Marking up invisible content | Policy violation on Google/Bing, manual action possible | Only mark up visible content |
| Wrong date format | Dates not recognized | Use ISO 8601: `2026-01-15T08:00:00+00:00` |
| Relative image URLs | Images not loaded | Use absolute HTTPS URLs |
| Duplicate JSON-LD blocks | Conflicting signals | Merge into single `@graph` |
| Stale data (wrong price, old dates) | Rich result removal | Keep structured data in sync with page content |
| Only validating with Google | Missed errors on Bing/Yandex | Validate with all three tools |
| Misleading structured data | Bing may ignore and reduce trust; Google may issue manual action | Markup must accurately reflect visible content |
