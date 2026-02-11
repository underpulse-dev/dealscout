# DealScout MVP — Architecture & Technical Plan

**Version:** 1.0  
**Date:** 2026-02-10  
**Status:** Draft (Awaiting Approval)

---

## Executive Summary

DealScout generates AI-powered pre-acquisition intelligence reports for small business buyers. Input: business name + location. Output: comprehensive PDF report covering reputation, competitive landscape, demographics, customer sentiment, and risk signals.

**Core Value Prop:** Turn 20+ hours of due diligence research into a 5-minute AI report.

**Target Market:** Individual buyers acquiring small businesses ($100K-$5M range).

**Business Model:** 
- Quick Scan: $49 (basic overview)
- Full Report: $199 (comprehensive analysis)
- Subscription: $99/mo (3 reports/month + updates)

**Unit Economics:**
- Cost per report: $1-3 (API calls, compute)
- Gross margin: 95%+
- Budget cap: $200 total for external services during MVP

---

## System Architecture

### High-Level Flow

```
User Input (Web Form)
    ↓
Payment (Stripe)
    ↓
Entity Resolution (Google Places API)
    ↓
Data Collection Pipeline (parallel fetching)
    ├─ Yelp Reviews & Ratings
    ├─ Google Trends
    ├─ Census/Demographics Data
    ├─ Web Scraping (BBB, social media, news)
    └─ Competitor Discovery
    ↓
LLM Analysis Layer (Claude)
    ├─ Sentiment Analysis
    ├─ Risk Detection
    ├─ Competitive Positioning
    └─ Market Opportunity Assessment
    ↓
Report Generation (PDF)
    ↓
Delivery (Email + Download Link)
```

### Tech Stack

**Backend:**
- **Language:** Python 3.11+
- **Framework:** FastAPI (async, high performance, excellent docs)
- **Task Queue:** Celery + Redis (async report generation)
- **Database:** PostgreSQL (storing reports, user data, cache)
- **Caching:** Redis (API responses, intermediate data)

**Frontend:**
- **Framework:** Simple HTML/CSS/JS (no React/Vue for MVP — keep it lean)
- **Styling:** Tailwind CSS (via CDN for speed)
- **Form handling:** HTMX for dynamic interactions without heavy JS

**Infrastructure:**
- **Hosting:** Railway.app or Render.com (free tier initially, easy scaling)
- **Database:** Railway PostgreSQL or Supabase (generous free tier)
- **Redis:** Railway Redis or Upstash (free tier)
- **Storage:** S3-compatible (Cloudflare R2 free tier: 10GB)

**Deployment:**
- **Containerization:** Docker + docker-compose
- **CI/CD:** GitHub Actions (free for public repos)

---

## Data Collection Pipeline

### 1. Entity Resolution
**Goal:** Convert "Joe's Pizza, Brooklyn NY" → verified business entity with address, phone, website

**Tool:** Google Places API
- **Free tier:** $200/month credit (~40,000 requests)
- **Fallback:** Yelp Fusion API (can also resolve entities)

**Output:** Canonical business data
```json
{
  "name": "Joe's Pizza",
  "address": "123 Main St, Brooklyn, NY 11201",
  "phone": "+1-718-555-0123",
  "website": "https://joespizza.com",
  "place_id": "ChIJ...",
  "coordinates": {"lat": 40.7128, "lng": -73.9352},
  "category": "Restaurant - Pizza",
  "hours": {...}
}
```

### 2. Review & Reputation Data
**Source:** Yelp Fusion API
- **Free tier:** 5,000 calls/day (plenty for MVP)
- **Data collected:**
  - Average rating & review count
  - Recent reviews (last 3 months)
  - Response rate to reviews
  - Common keywords in reviews

**Backup/Supplementary:** 
- Google Places reviews (via Places API)
- BBB rating (web scraping if available)

### 3. Market & Demographics
**Source:** US Census Bureau API (free, no key required)
- **Data points:**
  - Population density & trends
  - Median household income
  - Age distribution
  - Education levels
  - Industry employment stats

**Supplementary:** 
- Google Trends (pytrends library, free)
  - Interest over time for business category
  - Regional interest comparison
  - Related queries

### 4. Competitive Landscape
**Approach:** 
- Use Google Places API to find similar businesses in radius
- Calculate competitive density
- Compare ratings/review counts
- Identify market gaps

**Metrics:**
- Number of competitors within 1mi/5mi/10mi
- Average competitor rating
- Market saturation index
- Unique positioning opportunities

### 5. Web Presence & Risk Signals
**Scraping targets (respect robots.txt):**
- Business website (if exists):
  - Tech stack analysis
  - SSL certificate validity
  - Social media links
  - Contact info consistency
- News mentions (Google News search)
- Legal records (if publicly available)
- Social media presence (follower counts, engagement)

**Risk signals to detect:**
- BBB complaints or unresolved issues
- Negative news coverage
- Inconsistent information across platforms
- Recent management changes
- Legal disputes mentioned in reviews

---

## LLM Analysis Layer

### Model Choice: Claude 3.5 Sonnet (or Claude 4 Sonnet if available)
**Reasoning:**
- Best reasoning capabilities for nuanced analysis
- 200K context window (can fit all collected data)
- Strong at extracting insights from unstructured text
- Anthropic SDK well-maintained for Python

**Cost:** ~$0.50-1.50 per report (well within margin)

### Analysis Modules

#### 1. Sentiment Analysis
**Input:** Reviews, social comments, news articles  
**Output:**
- Overall sentiment score (-1 to +1)
- Sentiment trends over time
- Key themes (positive/negative)
- Customer pain points
- Standout strengths

**Prompt strategy:** Few-shot examples with structured output (JSON)

#### 2. Risk Assessment
**Input:** All collected data  
**Output:**
- Risk score (1-10)
- Categorized risks:
  - Financial (declining reviews, location issues)
  - Operational (owner-dependent, key person risk)
  - Legal/Regulatory (violations, complaints)
  - Market (high competition, declining trends)
- Red flags with severity ratings

#### 3. Competitive Position Analysis
**Input:** Competitor data, market trends, business data  
**Output:**
- Market positioning summary
- Competitive advantages
- Vulnerabilities vs competitors
- Pricing position
- Differentiation opportunities

#### 4. Market Opportunity
**Input:** Demographics, trends, competitive density  
**Output:**
- Growth potential score
- Demographic fit analysis
- Untapped opportunities
- Market timing assessment

### Prompt Architecture
- Use structured prompts with XML tags
- Request JSON output for programmatic parsing
- Include examples in system prompt
- Chain multiple specialized prompts rather than one mega-prompt
- Cache static context (prompt templates) to reduce costs

---

## Report Generation

### PDF Structure

**Page 1: Executive Summary**
- Business overview (1-2 paragraphs)
- Key metrics dashboard (ratings, reviews, competitors)
- Overall assessment score (A-F grade)
- 3-5 key findings (bullet points)

**Page 2-3: Reputation & Customer Sentiment**
- Review analysis (charts: rating over time, sentiment distribution)
- Common themes from customers
- Response quality assessment
- Comparison to local competitors

**Page 4: Market & Demographics**
- Location demographics summary
- Trends in the area
- Customer base analysis
- Foot traffic indicators (if applicable)

**Page 5: Competitive Landscape**
- Map of competitors
- Competitive density metrics
- Positioning matrix
- Market gaps & opportunities

**Page 6: Risk Assessment**
- Risk score with breakdown
- Detailed risk factors
- Red flags (if any)
- Mitigation recommendations

**Page 7: Appendix**
- Data sources & methodology
- Limitations & disclaimers
- Recommended next steps

### PDF Generation Tool: **WeasyPrint**
**Why WeasyPrint:**
- Renders HTML/CSS to beautiful PDFs
- Full CSS support (unlike ReportLab)
- Easy templating with Jinja2
- Free & open source

**Alternative:** Playwright (headless browser screenshot to PDF)

**Template approach:**
- Jinja2 HTML templates
- Tailwind CSS for styling
- Chart.js or Plotly for data visualization
- Professional design (reference Carfax/credit reports)

---

## API Structure

### REST API Endpoints

```
POST /api/reports/create
Body: {
  "business_name": "Joe's Pizza",
  "location": "Brooklyn, NY",
  "report_type": "full" | "quick",
  "email": "buyer@example.com"
}
Response: {
  "report_id": "rpt_abc123",
  "status": "processing",
  "estimated_time": 180
}

GET /api/reports/{report_id}/status
Response: {
  "report_id": "rpt_abc123",
  "status": "processing" | "complete" | "failed",
  "progress": 65,
  "estimated_time_remaining": 60
}

GET /api/reports/{report_id}/download
Response: PDF file or redirect to S3 URL

POST /api/payments/checkout
Body: {
  "report_type": "full",
  "business_name": "...",
  "location": "..."
}
Response: {
  "checkout_url": "https://checkout.stripe.com/..."
}

POST /api/webhooks/stripe
(Stripe webhook handler to trigger report generation after payment)
```

### Internal Service Layer

```python
# services/entity_resolver.py
async def resolve_business(name: str, location: str) -> BusinessEntity

# services/data_collector.py
async def collect_reviews(business: BusinessEntity) -> ReviewData
async def collect_demographics(business: BusinessEntity) -> DemographicsData
async def collect_competitors(business: BusinessEntity) -> CompetitorData
async def collect_web_data(business: BusinessEntity) -> WebData

# services/analyzer.py
async def analyze_sentiment(reviews: ReviewData) -> SentimentAnalysis
async def assess_risks(all_data: CollectedData) -> RiskAssessment
async def analyze_competition(competitors: CompetitorData, business: BusinessEntity) -> CompetitiveAnalysis
async def assess_opportunity(all_data: CollectedData) -> OpportunityAssessment

# services/report_generator.py
async def generate_report(analysis_results: AnalysisResults) -> bytes  # PDF
```

---

## External Services & Free Tier Limits

| Service | Purpose | Free Tier | Cost After | MVP Strategy |
|---------|---------|-----------|------------|--------------|
| **Google Places API** | Entity resolution, reviews | $200/mo credit (~40K requests) | $17/1000 after credit | Cache aggressively, use $200 credit |
| **Yelp Fusion API** | Reviews, business data | 5,000 calls/day | N/A (no paid tier) | Primary review source |
| **US Census API** | Demographics | Unlimited, free | Free | Use freely |
| **Google Trends** | Market trends | Unlimited via pytrends | Free | Use freely |
| **Anthropic Claude API** | LLM analysis | Pay-as-you-go, ~$3/1M tokens | ~$0.50-1.50/report | Only cost that scales with reports |
| **Stripe** | Payments | Free + 2.9% + $0.30 per transaction | Same | Standard payment processing |
| **Railway.app** | Hosting (backend + DB + Redis) | $5/mo credit | $0.000463/GB-hour | Start here, migrate if needed |
| **Cloudflare R2** | PDF storage | 10GB free | $0.015/GB/mo | Plenty for MVP |
| **Postmark/SendGrid** | Email delivery | 100/day (Postmark) / 100/day (SendGrid) | ~$15/mo for 40K | Start with SendGrid free |

**Total estimated monthly cost (first 100 reports):**
- API calls: ~$0 (within free tiers)
- LLM analysis: ~$75 (100 reports × $0.75 avg)
- Hosting: ~$5 (Railway credit covers)
- Email: ~$0 (within free tier)
- **Total: ~$80/mo** well under budget

**At $199/report × 100 reports = $19,900 revenue**  
**Margins: 99.6%** (excluding payment processing)

---

## Database Schema

```sql
-- Users (future: for subscriptions)
CREATE TABLE users (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  email VARCHAR(255) UNIQUE NOT NULL,
  created_at TIMESTAMP DEFAULT NOW(),
  stripe_customer_id VARCHAR(255)
);

-- Reports
CREATE TABLE reports (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  user_id UUID REFERENCES users(id),
  business_name VARCHAR(255) NOT NULL,
  location VARCHAR(255) NOT NULL,
  report_type VARCHAR(20) NOT NULL, -- 'quick' or 'full'
  status VARCHAR(20) NOT NULL, -- 'pending', 'processing', 'complete', 'failed'
  payment_status VARCHAR(20) NOT NULL, -- 'pending', 'paid', 'refunded'
  stripe_payment_intent_id VARCHAR(255),
  
  -- Collected data (JSONB for flexibility)
  raw_data JSONB,
  analysis_results JSONB,
  
  -- Generated report
  pdf_url TEXT,
  pdf_size_bytes INTEGER,
  
  -- Metadata
  created_at TIMESTAMP DEFAULT NOW(),
  completed_at TIMESTAMP,
  processing_time_seconds INTEGER,
  error_message TEXT,
  
  -- Cost tracking
  api_cost_cents INTEGER,
  llm_cost_cents INTEGER
);

-- API call cache (avoid redundant external API calls)
CREATE TABLE api_cache (
  cache_key VARCHAR(255) PRIMARY KEY,
  service VARCHAR(50) NOT NULL, -- 'google_places', 'yelp', etc.
  request_params JSONB NOT NULL,
  response_data JSONB NOT NULL,
  cached_at TIMESTAMP DEFAULT NOW(),
  expires_at TIMESTAMP NOT NULL
);

CREATE INDEX idx_api_cache_expires ON api_cache(expires_at);
CREATE INDEX idx_reports_status ON reports(status, created_at);
CREATE INDEX idx_reports_user ON reports(user_id, created_at);
```

---

## Security & Compliance

### Data Privacy
- **No PII storage beyond email** (required for delivery)
- Reports deleted after 30 days (configurable)
- Stripe handles payment data (PCI compliant)
- SSL/TLS for all connections

### Rate Limiting
- **Public API:** 10 requests/min per IP
- **Authenticated:** 100 requests/hour per user
- Use Redis for rate limit tracking

### Input Validation
- Sanitize all user inputs
- Validate business names (no SQL injection, XSS)
- Limit location to US initially (Census data availability)

### API Key Security
- Store all keys in environment variables
- Use Railway/Render secret management
- Never commit keys to Git
- Rotate keys periodically

---

## Error Handling & Resilience

### Graceful Degradation
If a data source fails:
- **Critical (Google Places, Yelp):** Retry 3x with exponential backoff, then fail report with refund
- **Non-critical (Trends, some demographics):** Continue report with disclaimer
- **Scraping failures:** Note in report, don't fail entire process

### Monitoring & Alerts
- **Health checks:** `/health` endpoint for uptime monitoring
- **Error tracking:** Sentry (free tier: 5K events/mo)
- **Logging:** Structured logs (JSON) to stdout, captured by Railway
- **Alerts:** Email on critical failures (report failure rate >10%)

### Retry Strategy
- Use Celery with exponential backoff for task retries
- Max 3 retries for external API calls
- DLQ (dead letter queue) for failed reports

---

## Development Workflow

### Phase-by-Phase Timeline

**Phase 1: Core Pipeline (Sessions 1-2, ~2 hours)**
- Initialize project structure
- Set up FastAPI + Docker
- Implement entity resolution (Google Places)
- Implement Yelp integration
- Implement Census data fetching
- Unit tests for each data source
- Test with 5 real businesses

**Phase 2: LLM Analysis (Sessions 3-4, ~2 hours)**
- Design prompt templates
- Implement sentiment analysis
- Implement risk assessment
- Implement competitive analysis
- Implement opportunity assessment
- Test end-to-end pipeline with real data

**Phase 3: Report Generation (Session 5, ~1 hour)**
- Design PDF template (HTML/CSS)
- Implement WeasyPrint rendering
- Generate sample reports
- Refine design for readability

**Phase 4: Web Frontend & Payment (Sessions 6-7, ~2 hours)**
- Build landing page (conversion-optimized)
- Input form with validation
- Stripe Checkout integration
- Webhook handler for payment confirmation
- Email delivery (SendGrid)
- Order confirmation page with download

**Phase 5: Polish & Launch (Sessions 8-9, ~2 hours)**
- End-to-end testing (10+ businesses)
- Error handling refinement
- Sample report for marketing
- Deploy to production
- Set up monitoring
- Soft launch (SearchFunder post)

**Total: ~9-10 hours of focused work**

### Git Strategy
- **Repo name:** `dealscout-mvp`
- **Branches:** 
  - `main` (production)
  - `dev` (active development)
  - Feature branches as needed
- **Commit frequency:** Every logical unit of work (~30min)
- **Commit message format:** `[Phase X] Brief description`

### Testing Strategy
- **Unit tests:** pytest for individual services
- **Integration tests:** Test full pipeline with mocked APIs
- **E2E tests:** Test with real businesses (manual initially)
- **Coverage goal:** 70%+ for core services

---

## Go-to-Market Strategy (Post-Launch)

### Initial Distribution Channels
1. **SearchFunder community** (primary audience)
   - Post: "We built an AI tool to automate pre-acquisition due diligence"
   - Offer 50% discount to first 20 customers ($99 instead of $199)
   - Gather feedback aggressively

2. **BizBuySell forum**
   - Similar approach to SearchFunder
   - Value-first content: share sample report

3. **SEO Content**
   - Blog: "How to evaluate a small business before buying"
   - "10 red flags when buying a restaurant"
   - "Competitive analysis for [city] [industry]"

4. **Cold outreach to brokers**
   - Offer white-label reports
   - Revenue share: $50/report they sell

### Success Metrics (First 30 Days)
- **10 paid reports** (validation)
- **5+ pieces of qualitative feedback**
- **<5% refund rate**
- **<10min average report generation time**

### Pricing Validation
- Test $149 vs $199 for full report
- Offer "Quick Scan" at $49 to capture price-sensitive buyers
- Subscription at $99/mo if demand exists

---

## Open Questions / Decisions Needed

1. **Should we support non-US businesses in MVP?**
   - Leaning NO: Census data is US-only, complicates entity resolution
   - Can add later if demand exists

2. **Report update frequency for subscribers?**
   - Proposal: Weekly for active deals, monthly otherwise
   - Track changes in reviews, trends, competitors

3. **Refund policy?**
   - Proposal: 100% refund if report fails to generate
   - 50% refund if customer unsatisfied (within 48 hours)
   - No refunds after 48 hours or if report downloaded

4. **Sample report availability?**
   - YES: Generate 2-3 sample reports for different business types
   - Use for landing page, social proof, SEO

5. **Branding: DealScout vs other names?**
   - DealScout is solid (available .com for $12/year)
   - Alternative: BizIntel, AcquisitionIQ, DueDilligenceAI
   - Decision: Stick with DealScout unless Serg objects

---

## Risk Mitigation

### Technical Risks
- **API rate limits:** Implement aggressive caching, monitor usage
- **LLM hallucinations:** Use structured prompts, validate outputs, include disclaimers
- **Report generation failures:** Graceful degradation, clear error messages, refunds

### Business Risks
- **Low conversion:** Offer free Quick Scan, improve landing page copy
- **High refund rate:** Improve report quality, set clear expectations
- **Negative feedback:** Iterate quickly, over-deliver on support

### Financial Risks
- **Unexpected API costs:** Set hard spending limits, monitor daily
- **Payment fraud:** Use Stripe Radar (included), require email verification

---

## Next Steps (Pending Approval)

Once this plan is approved:
1. Create GitHub repo: `dealscout-mvp`
2. Initialize Python project structure
3. Set up development environment (Docker, pre-commit hooks)
4. Begin Phase 1: Entity resolution + Yelp integration
5. Request API keys from Serg (Google Places, Yelp, Anthropic)

**Estimated time to first working prototype:** 2-3 sessions (~3 hours)  
**Estimated time to soft launch:** 8-9 sessions (~9 hours)

---

## Appendix: Directory Structure

```
dealscout-mvp/
├── .github/
│   └── workflows/
│       └── ci.yml
├── src/
│   ├── api/
│   │   ├── __init__.py
│   │   ├── main.py              # FastAPI app
│   │   ├── routes/
│   │   │   ├── reports.py
│   │   │   ├── payments.py
│   │   │   └── webhooks.py
│   │   └── dependencies.py
│   ├── services/
│   │   ├── entity_resolver.py
│   │   ├── data_collector.py
│   │   ├── analyzer.py
│   │   └── report_generator.py
│   ├── models/
│   │   ├── business.py
│   │   ├── report.py
│   │   └── analysis.py
│   ├── integrations/
│   │   ├── google_places.py
│   │   ├── yelp.py
│   │   ├── census.py
│   │   ├── trends.py
│   │   └── anthropic_client.py
│   ├── templates/
│   │   └── report.html          # Jinja2 template for PDF
│   └── utils/
│       ├── cache.py
│       ├── logger.py
│       └── validators.py
├── tests/
│   ├── unit/
│   ├── integration/
│   └── fixtures/
├── frontend/
│   ├── index.html               # Landing page
│   ├── styles.css
│   └── app.js
├── docker-compose.yml
├── Dockerfile
├── pyproject.toml
├── README.md
└── .env.example
```

---

**END OF ARCHITECTURE DOCUMENT**

Questions? Concerns? Modifications needed? Reply with feedback and I'll iterate before starting Phase 1.
