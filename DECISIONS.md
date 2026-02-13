# DealScout — Decisions

Active decisions for the project. Historical discussion removed — see git history for context.

---

## Strategy
- **Sell first, build later.** Validate demand before production code.
- Hand-craft sample reports → landing page → community posts → measure interest.
- Build only if validated: >50 signups OR >5 purchase attempts in 2 weeks.

## Positioning
- **Screening tool, not due diligence replacement.** Covers ~15-20% of full DD (public data layer).
- Helps buyers filter listings before committing $15-30K to professional DD.
- Value prop: "Know which businesses deserve your DD budget — and which ones don't."
- Reports must clearly state what we DON'T cover (financials, legal, environmental).
- Every report includes "What To Do Next" with actionable next steps.

## Tech Stack
- **Python + FastAPI** — best ecosystem for scraping, LLM, PDF, rapid iteration.
- **Claude Sonnet 4.5** — LLM for analysis. Best reasoning, structured output, 200K context. ~$0.25-1.50/report.
- **WeasyPrint** — PDF generation from HTML/CSS + Jinja2 templates.
- **SQLite** for MVP → PostgreSQL when scaling.
- **Playwright + stealth plugin** — browser automation for Cloudflare-protected sites.

## Hosting
- **Hetzner** — Serg will provide access token.

## Pricing
- **Intro (first report per customer):** Quick Scan $20 / Full Report $100
- **Regular:** Quick Scan $40 / Full Report $200
- Rationale: DealScout is a screening tool, not full DD. Low price = impulse buy for buyers browsing 10-50 listings. Screen 10 businesses for $200-400. Still 95%+ margin at $1-3 cost per report.

## Data Sources (priority order)
1. **Google Places API** — entity resolution, reviews (CRITICAL)
2. **Yelp Fusion API** — reviews, ratings, photos (CRITICAL)
3. **US Census API** — demographics, free & unlimited (HIGH)
4. **Google Trends** — market interest via pytrends (NICE TO HAVE)
5. **Web scraping** — BBB, news, social (BEST EFFORT)

## Report Types
- **Quick Scan:** 2-3 pages, basic reputation + risk flags. <2 min.
- **Full Report:** 8-12 pages, deep analysis across all dimensions. <5 min.

## Geographic Scope
- **US only** for MVP. Census data is US-specific. Expand later if demand.

## Frontend
- **Vanilla HTML/CSS/JS + Tailwind.** No React/Vue — overkill for MVP forms + landing page.

## Payments
- **Stripe Checkout.** Standard 2.9% + $0.30. Handles PCI compliance.

## Email
- **SendGrid free tier.** 100/day sufficient for MVP volume.

## Refund Policy
- 100% refund if report fails to generate.
- 50% refund within 48h if customer unsatisfied.
- No refunds after 48h or download.

## What We're NOT Building (MVP)
- User accounts / login
- Dashboard
- Report customization
- White-label for brokers
- International support
- Mobile app
- Partner API

## Budget
- **$200 cap** for external services during MVP development.
- Total cost per report: ~$1-3 → 95%+ margin.

## Competitive Landscape

### Direct Competitors (AI deal screening for SMB/search fund buyers)

**Skarp AI** — https://skarp.ai
- AI-powered M&A deal **sourcing** for search fund operators
- Core product: scans 27,000+ listings across top US brokers, matches against your acquisition criteria, sends alerts when new deals match
- Also building "Deal Navigator" module for CIM analysis (extracts financials from CIM packages into structured dashboard) — announced but unclear if shipped
- Pricing: **$85/month** subscription, 30-day free trial
- One testimonial (Jamie Gorman, Left Lane Ventures)
- Funded (1 round per Tracxn), competitors listed as Midaxo, Finquest, M&A Cloud
- **Overlap with DealScout:** LOW-MEDIUM. Skarp is primarily a **deal sourcing/matching** tool (find listings that match your criteria). Their Deal Navigator module is closer to DealScout but focuses on CIM document analysis (seller-provided data), not public data screening.
- **What Skarp does NOT do:** Generate standalone screening reports from public data for a specific listing. No reputation analysis, no local demographics, no competitor landscape, no risk flags from public sources. It matches listings to criteria — it doesn't deeply evaluate individual businesses.
- **Our differentiation:** DealScout evaluates a specific business using public data (reviews, demographics, competitors, market trends). Skarp finds you listings; DealScout tells you if a specific listing is worth pursuing. Complementary, not competing. Per-report pricing ($20-200) vs monthly subscription ($85/mo).

**Cerco AI** — cerco.ai
- AI-powered off-market deal sourcing (company & contact search)
- Comparable to Grata, SourceScrub, Inven
- $99/month subscription
- Posted on SearchFunder by co-founder
- **Overlap with DealScout:** Low. Cerco focuses on finding companies to acquire (sourcing), not evaluating specific listings (screening)

### Adjacent Competitors (enterprise/PE level)

**SESAMm Deal Screening Reports** — sesamm.com
- AI-powered "pre-commercial due diligence" reports for PE and M&A teams
- Claims to deliver "weeks of manual research in hours" — closest concept to DealScout
- Used by 7 of top 10 PE firms (Carlyle, Warburg)
- Enterprise pricing (not public), targets large PE deal teams
- **Overlap with DealScout:** CONCEPT is similar (pre-screening reports) but targets enterprise PE, not individual SMB buyers. Likely $1000s per report. Completely different market segment.

**V7 Go PE Screening Agent** — v7labs.com
- AI agent that reads CIMs, extracts financials (Revenue, EBITDA), scores against investment thesis
- Enterprise pricing (PE/VC firms, not individual buyers)
- **Overlap with DealScout:** Medium. Similar screening concept but targets PE firms with large deal flow, not individual SMB buyers looking at $100K-$5M businesses

**Grata / SourceScrub / Inven** — Deal sourcing platforms
- Company search & matching for PE/search funds
- $500-2000+/month range
- **Overlap with DealScout:** Low. Sourcing, not screening

### DIY Alternative
- Manual Google/Yelp/Census research: Free but takes 5-10 hours per listing
- ChatGPT/Claude direct prompting: Free but hallucination-prone, no structured format, no verify links
- **DealScout advantage:** Structured, verified, fast ($20 vs 5-10 hours of manual work)

### Key Takeaway
The gap DealScout fills: **pre-CIM screening from public data for individual SMB buyers ($100K-$5M)**. Competitors either require CIM access (Skarp), focus on sourcing not screening (Cerco, Grata), or target enterprise PE (V7). Nobody is doing cheap, one-off public-data screening reports for small buyers.

## Distribution (post-validation)
1. SearchFunder community (primary audience)
2. BizBuySell forums
3. Reddit: r/smallbusiness, r/Entrepreneur
4. Cold outreach to brokers (20% affiliate commission)
