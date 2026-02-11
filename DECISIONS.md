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

## Distribution (post-validation)
1. SearchFunder community (primary audience)
2. BizBuySell forums
3. Reddit: r/smallbusiness, r/Entrepreneur
4. Cold outreach to brokers (20% affiliate commission)
