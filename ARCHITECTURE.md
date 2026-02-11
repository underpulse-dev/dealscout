# DealScout — Architecture

## Product

**DealScout** generates AI-powered pre-acquisition intelligence reports for small business buyers ($100K-$5M deals).

- **Input:** Business name + location
- **Output:** Comprehensive PDF report (reputation, competition, demographics, risks)
- **Value prop:** Screen business acquisitions in 5 minutes. Know which ones deserve your DD budget.
- **Positioning:** "The Carfax for business acquisitions" — pre-screening, not full DD

---

## Tech Stack

| Layer | Choice | Rationale |
|-------|--------|-----------|
| **Language** | Python 3.11+ | Best ecosystem for scraping, LLM, PDF generation |
| **Framework** | FastAPI | Async, fast, great docs |
| **LLM** | Anthropic Claude Sonnet 4.5 | Best reasoning for structured analysis, 200K context |
| **PDF** | WeasyPrint | HTML/CSS → PDF, Jinja2 templates, beautiful output |
| **Frontend** | HTML/CSS/JS + Tailwind | No framework overhead for MVP |
| **Payments** | Stripe Checkout | Industry standard, handles PCI compliance |
| **Database** | SQLite (MVP) → PostgreSQL | Zero config to start, clear migration path |
| **Hosting** | Hetzner | Cost-effective, Serg provides access |
| **Email** | SendGrid (free tier) | 100/day sufficient for MVP |
| **Browser automation** | Playwright + stealth | For scraping behind Cloudflare/JS walls |
| **Task queue** | Celery + Redis | Async report generation, retry logic |
| **Storage** | Cloudflare R2 (free 10GB) | PDF storage |

---

## System Flow (Deterministic Pipeline)

```
User Input (web form)
    ↓
Stripe Payment
    ↓
Entity Resolution (Google Places API)
    ↓
Parallel Data Collection (fixed steps, no agent):
    ├─ Yelp reviews/ratings
    ├─ Google Trends (search interest)
    ├─ Census/demographic data (free API)
    ├─ Web scraping (BBB, news, social)
    └─ Competitor discovery (nearby same-category)
    ↓
Single LLM Call (Claude Sonnet 4.5):
    → All collected data in → Structured analysis JSON out
    → Sentiment, risks, competition, readiness score
    ↓
Report Assembly → PDF (WeasyPrint + Jinja2)
    ↓
Email Delivery (SendGrid) + Download Link
```

**Why deterministic, not agentic:** Predictable cost/latency, easier to debug, sufficient for MVP. Agentic approach is a potential Phase 4+ upgrade once revenue justifies the engineering.

---

## Data Sources

| Source | Purpose | Free Tier | Key Needed |
|--------|---------|-----------|------------|
| Google Places API | Entity resolution, reviews | $200/mo credit | YES |
| Yelp Fusion API | Reviews, ratings, photos | 5,000 calls/day | YES (free) |
| US Census API | Demographics by ZIP | Unlimited | NO |
| Google Trends | Search interest trends | Unlimited (pytrends) | NO |
| Web scraping | BBB, news, social media | Free (rate-limited) | NO |
| Anthropic Claude | LLM analysis | Pay-per-token | YES |

**Cost per report:** ~$1-3 (API calls + LLM tokens) → **95%+ margin**

---

## Report Types

### Quick Scan ($20 intro / $40 regular)
- Business overview + online reputation summary
- Local market context + competition density
- Key risk flags
- Go / No-Go recommendation
- **2-3 pages, <2 min generation**

### Full Report ($100 intro / $200 regular)
Everything in Quick Scan, plus:
- Competitive landscape deep-dive
- Customer sentiment analysis (themes, trends)
- Demographic insights + target customer profile
- Search interest trends
- Risk signal analysis (BBB, news, legal)
- Screening score (0-100)
- "What To Do Next" — actionable next steps + questions for seller
- **8-12 pages, <5 min generation**

**Note:** DealScout is a pre-screening tool, not a due diligence replacement. Reports cover publicly available data only. Every report includes a clear disclaimer and recommendations for professional DD services.

---

## API Endpoints

```
POST /api/reports/create     → Start report generation (after payment)
GET  /api/reports/:id/status → Poll progress
GET  /api/reports/:id/download → Get PDF
POST /api/payments/checkout  → Create Stripe session
POST /api/webhooks/stripe    → Payment confirmation
GET  /health                 → Health check
```

---

## Project Structure

```
dealscout/
├── app/
│   ├── main.py                 # FastAPI entry point
│   ├── api/
│   │   ├── routes.py           # Report + payment endpoints
│   │   └── webhooks.py         # Stripe webhooks
│   ├── services/
│   │   ├── entity_resolver.py  # Google Places lookup
│   │   ├── yelp_client.py      # Yelp API
│   │   ├── census_client.py    # Demographics
│   │   ├── trends_client.py    # Google Trends
│   │   ├── scraper.py          # BBB, news, social
│   │   └── llm_analyzer.py     # Claude analysis
│   ├── report/
│   │   ├── builder.py          # Report assembly
│   │   ├── pdf_generator.py    # WeasyPrint rendering
│   │   └── templates/          # Jinja2 HTML templates
│   ├── payment/
│   │   └── stripe_client.py
│   └── models/
│       └── schemas.py          # Pydantic models
├── tests/
├── static/                     # Landing page assets
├── templates/                  # Web page templates
├── .env.example
├── pyproject.toml
├── Dockerfile
└── README.md
```

---

## Database Schema (MVP)

```sql
CREATE TABLE reports (
  id TEXT PRIMARY KEY,
  business_name TEXT NOT NULL,
  location TEXT NOT NULL,
  report_type TEXT NOT NULL,        -- 'quick' | 'full'
  status TEXT NOT NULL,             -- 'pending' | 'processing' | 'complete' | 'failed'
  payment_status TEXT NOT NULL,     -- 'pending' | 'paid' | 'refunded'
  stripe_payment_intent_id TEXT,
  raw_data JSON,
  analysis_results JSON,
  pdf_url TEXT,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  completed_at TIMESTAMP,
  error_message TEXT
);

CREATE TABLE api_cache (
  cache_key TEXT PRIMARY KEY,
  service TEXT NOT NULL,
  response_data JSON NOT NULL,
  cached_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  expires_at TIMESTAMP NOT NULL
);
```

---

## LLM Analysis Strategy

Four separate Claude calls per Full Report (chained, not one mega-prompt):

1. **Sentiment Analysis** — Input: top 20 reviews → themes, trends, pain points
2. **Risk Assessment** — Input: all data → categorized risks with severity
3. **Competitive Positioning** — Input: business + competitors → market position
4. **Acquisition Readiness** — Input: all analysis → 0-100 score + justification

Token budget: ~5K (Quick Scan), ~20K (Full Report) → $0.25-1.50/report

---

## Error Handling

- **Critical source fails** (Google Places, Yelp): Retry 3x with backoff → fail + refund
- **Non-critical fails** (Trends, BBB): Continue with disclaimer in report
- **LLM errors**: Retry once, fallback to simpler prompt
- **Rate limits**: Respect all API limits, cache aggressively (24h for reviews, 7d for demographics)

---

## Security

- All API keys in environment variables (never in git)
- No PII stored beyond email (for delivery)
- Stripe handles payment data (PCI compliant)
- SSL/TLS everywhere
- Rate limiting: 10 req/min per IP (public), 100 req/hr (authenticated)
- Reports auto-deleted after 30 days

---

## MVP Scope

**Building:**
- Landing page + checkout flow
- Data pipeline (5 sources)
- LLM analysis (4 modules)
- PDF report generation
- Email delivery

**NOT building (yet):**
- User accounts / login
- Dashboard
- Report customization
- White-label for brokers
- International support
- Mobile app
- Partner API

---

## Success Metrics (First 30 Days)

- 10 paid reports → validates demand
- <5% refund rate → validates quality
- <5 min report generation → validates technical
- 5+ testimonials → social proof
