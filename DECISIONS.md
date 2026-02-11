# DealScout — Decision Log

## 2026-02-10 Session 1: Phase 0 Architecture Decisions

### Tech Stack
- **Python + FastAPI** chosen over Java for prototype
- Reason: vastly better ecosystem for web scraping (BeautifulSoup, Playwright), LLM integration (anthropic SDK), PDF generation (weasyprint), and rapid iteration
- Can rewrite in Java for production if product takes off

### Database: PostgreSQL
- **Why:** Mature, JSONB support for flexible data storage, excellent with FastAPI
- Alternative considered: MongoDB (rejected: less structured, overkill for MVP)
- Railway.app provides managed PostgreSQL in free tier

### PDF Generation: WeasyPrint
- **Why:** Renders HTML/CSS directly to PDF, easy templating with Jinja2, beautiful output
- Alternative considered: ReportLab (rejected: too low-level, harder to design)
- Alternative considered: Playwright PDF export (rejected: heavier, requires browser)

### Task Queue: Celery + Redis
- **Why:** Battle-tested for async jobs, good monitoring, scales well
- Alternative considered: FastAPI BackgroundTasks (rejected: no persistence, lost on restart)
- Redis serves dual purpose: cache + task queue backend

### LLM: Claude 3.5 Sonnet (Anthropic)
- **Why:** Best reasoning for nuanced analysis, 200K context, strong at structured output
- Cost: ~$0.50-1.50 per report (well within margins)
- Alternative considered: GPT-4 (rejected: more expensive, less reliable structured output)
- Alternative considered: Open source (rejected: quality concerns, hosting costs)

### Hosting: Railway.app (initially)
- **Why:** $5/mo credit, easy setup, includes PostgreSQL + Redis, great DX
- Alternative: Render.com (equivalent, slightly different pricing)
- Migration path: Can move to AWS/GCP later if scaling requires

### Payment: Stripe
- **Why:** Industry standard, excellent API, handles compliance
- 2.9% + $0.30 per transaction is standard (not negotiable at MVP stage)

### Email: SendGrid (free tier)
- **Why:** 100 emails/day free tier sufficient for MVP
- Alternative: Postmark (equivalent free tier, similar quality)

### Frontend: Vanilla HTML/CSS/JS + Tailwind
- **Why:** Fastest to build, no build step, easy to iterate
- Avoid React/Vue for MVP: overkill for simple forms and landing page
- Can upgrade later if dashboard needed

### Geographic Scope: US Only (MVP)
- **Why:** Census data is US-specific, simplifies entity resolution
- Can expand to Canada/UK/Australia later if demand exists
- International would require different demographic data sources

### Data Sources Priority:
1. **Google Places** (entity resolution, reviews) — CRITICAL
2. **Yelp Fusion** (reviews, ratings, photos) — CRITICAL
3. **US Census** (demographics) — HIGH VALUE
4. **Google Trends** (market trends) — NICE TO HAVE
5. **Web scraping** (BBB, social, news) — BEST EFFORT

Rationale: Focus on highest-signal data first, add supplementary sources as time allows

### Report Types:
- **Quick Scan:** $49 (basic metrics, sentiment, 2-page summary)
- **Full Report:** $199 (comprehensive 7-page analysis)
- **Subscription:** $99/mo (3 reports + updates)

Decision: Offer tiered pricing to capture price-sensitive buyers, test demand

### Refund Policy:
- 100% refund if report generation fails
- 50% refund within 48h if customer unsatisfied
- No refunds after 48h or download (standard digital goods policy)

### MVP Success Criteria (First 30 Days):
- 10 paid reports (validates willingness to pay)
- <5% refund rate (validates quality)
- 5+ pieces of feedback (validates iteration direction)
- <10min report generation (validates technical feasibility)

### Launch Strategy:
1. Soft launch: SearchFunder community post (target audience)
2. Offer: 50% discount to first 20 customers
3. Gather feedback aggressively, iterate on quality
4. Expand to BizBuySell forum after refining

### What We're NOT Building in MVP:
- ❌ User accounts / login (email-based delivery only)
- ❌ Dashboard (just landing page + checkout + download)
- ❌ Report customization (one template fits all)
- ❌ White-label for brokers (maybe Phase 6 if demand)
- ❌ International support (US only)
- ❌ Mobile app (responsive web only)
- ❌ API for partners (maybe later)

Rationale: Stay laser-focused on core value prop: "Enter business → Get great report"

## 2026-02-10: Two-Tier Pricing Model
- **Quick Scan ($49):** 2-3 pages, basic reputation + risk flags
- **Full Report ($199):** 8-12 pages, deep competitive/sentiment/demographic analysis
- Reason: Lowers barrier to entry, captures impulse buyers, upsell path to full report
- Quick Scan = lead magnet with value; Full Report = serious buyer tool

## 2026-02-10: Data Sources (Free Tier First)
- **Google Places API:** Entity resolution ($200/mo credit = ~6000 reports free)
- **Yelp Fusion API:** Reviews/ratings (5000 calls/day free)
- **Census API:** Demographics (unlimited, free, no key)
- **Google Trends:** Search interest (unlimited via pytrends)
- **Web scraping:** BBB, news (free but rate-limited)
- Reason: Stay under $200 total budget for MVP, validate demand before paying for premium APIs

## 2026-02-10: WeasyPrint for PDF Generation
- Chose **WeasyPrint** over ReportLab
- Reason: HTML/CSS-based (easier to design/iterate), better fonts/styling, open-source
- Trade-off: Slightly slower than ReportLab, but speed not critical for MVP

## 2026-02-10: Claude for LLM Analysis
- Using **Claude Sonnet** for sentiment/risk/competitive analysis
- Token budget: ~5K (Quick Scan), ~20K (Full Report)
- Cost: ~$0.25-1.50/report → maintains 95%+ margin
- Reason: Best at structured analysis, reliable, Serg already has API access

## 2026-02-10: SQLite for MVP Database
- Starting with **SQLite**, upgrade to PostgreSQL if needed
- Reason: Zero config, embedded, sufficient for <1000 reports/mo
- Migration path clear if we scale

## 2026-02-10: 6-Session Timeline
- Phase 0: Planning (✅)
- Phase 1-2: Data pipeline + entity resolution
- Phase 3-4: LLM analysis + report generation
- Phase 5: Frontend + payments
- Phase 6: Testing + launch prep
- Reason: Breaks work into manageable 1-hour chunks, each session delivers testable progress

## 2026-02-10: PIVOT — Sell First, Build Later
- **Overrides** the 6-session build timeline above
- Validate demand BEFORE writing production code
- Hand-craft 2-3 sample reports from real BizBuySell listings
- Landing page + community posts to measure interest
- Build only if validated (>50 signups OR >5 purchase attempts in 2 weeks)
- Reason: the #1 startup mistake is building before validating. Manual reports also reveal what data actually matters to buyers.

## 2026-02-10: Pricing — Go High
- **Beta (first 20 customers):** Quick Scan $50 / Full Report $200
- **Full price:** Quick Scan $100 / Full Report $400 / Subscription $200/mo
- Reason: buyer is making a $100K-$5M decision. $400 is 0.08% of a $500K deal.
- Higher price = quality signal + filters for serious buyers + fewer customers needed for revenue
- $1K MRR = just 3 full reports at $400
- Can always discount but can never easily raise from cheap
- At $400, reports must feel genuinely worth it — good discipline for quality
