# DealScout MVP — Architecture Plan

## Product Overview
**DealScout** generates AI-powered pre-acquisition intelligence reports for small business buyers ($100K-$5M deals). Input: business name + location. Output: comprehensive PDF report covering reputation, competitive landscape, demographics, customer sentiment, and risk signals.

## Value Proposition
- **For buyers:** Avoid catastrophic mistakes. Get unbiased intelligence before making a 6-figure bet.
- **Positioning:** "The Carfax for business acquisitions"
- **Differentiation:** Automated, affordable, comprehensive (most brokers don't provide this level of diligence)

---

## Technical Architecture

### Tech Stack
- **Backend:** Python 3.11+ with FastAPI
- **Data Collection:** Playwright (browser automation), httpx (API calls), BeautifulSoup4 (HTML parsing)
- **LLM Analysis:** Anthropic Claude (via anthropic SDK)
- **PDF Generation:** WeasyPrint (HTML→PDF with CSS support)
- **Frontend:** Jinja2 templates + Tailwind CSS (simple, fast, no React/Vue overhead for MVP)
- **Payment:** Stripe Checkout (no PCI compliance hassle)
- **Hosting:** DigitalOcean App Platform or Railway ($5-10/mo, auto-scaling)
- **Database:** SQLite for MVP (upgrade to PostgreSQL if we scale)
- **Email:** SendGrid free tier (100 emails/day)
- **Version Control:** GitHub

### System Architecture
```
User Input (web form)
    ↓
FastAPI endpoint
    ↓
Entity Resolution (Google Places API)
    ↓
Parallel Data Collection:
    - Yelp reviews/ratings
    - Google Trends (search interest)
    - Census/demographic data
    - Web scraping (news, BBB, etc.)
    ↓
LLM Analysis (Claude)
    - Sentiment analysis
    - Risk detection
    - Competitive insights
    ↓
Report Assembly (structured data)
    ↓
PDF Generation (WeasyPrint)
    ↓
Stripe Payment (if not paid yet)
    ↓
Email Delivery (SendGrid) + Download
```

---

## Data Sources & APIs

### Free/Low-Cost Services (under $200 total budget)

| Service | Purpose | Free Tier | Cost After | API Key Needed |
|---------|---------|-----------|------------|----------------|
| **Google Places API** | Entity resolution, basic business info | $200/mo credit | $0.032/call | YES (Serg) |
| **Yelp Fusion API** | Reviews, ratings, photos | 5000 calls/day | N/A | YES (free signup) |
| **Google Trends** | Search interest over time | Unlimited | Free | NO (pytrends) |
| **Census/ACS API** | Demographics by ZIP | Unlimited | Free | NO |
| **OpenStreetMap/Nominatim** | Geocoding backup | Unlimited | Free | NO |
| **Anthropic Claude** | LLM analysis | Pay-per-token | ~$0.50-2/report | YES (Serg) |
| **Stripe** | Payments | Free (2.9%+30¢) | N/A | YES (free signup) |
| **SendGrid** | Email delivery | 100/day | $0.0012/email | YES (free signup) |

**Budget Estimate:**
- Google Places: ~$0.03/report
- Yelp: $0 (free tier)
- Claude: ~$1-2/report (Full Report), ~$0.25 (Quick Scan)
- Stripe: 2.9% + $0.30 per transaction
- SendGrid: $0 (under 100/day)

**Total cost per Full Report:** ~$1-3 → **95%+ margin at $199 price point**

---

## Report Structure

### Quick Scan ($49)
1. **Business Overview** (name, address, type, hours)
2. **Online Reputation Summary** (Yelp/Google ratings, review count)
3. **Local Market Context** (population, income, competition density)
4. **Key Risk Flags** (if any major red flags detected)

**Delivery:** 2-3 pages, generated in <2 minutes

### Full Report ($199)
Everything in Quick Scan, plus:
5. **Competitive Landscape Analysis** (nearby competitors, market saturation)
6. **Customer Sentiment Deep-Dive** (sentiment trends, common complaints/praises)
7. **Demographic Insights** (target customer profile, spending power)
8. **Search Interest Trends** (Google Trends for business category)
9. **Risk Signal Analysis** (BBB complaints, news mentions, lawsuit searches)
10. **Acquisition Readiness Score** (0-100, based on all factors)

**Delivery:** 8-12 pages, generated in <5 minutes

---

## API Structure

### Endpoints

#### Public (unauthenticated)
- `GET /` → Landing page
- `GET /sample-report` → Sample PDF for marketing
- `POST /api/quick-scan` → Generate Quick Scan (requires payment)
- `POST /api/full-report` → Generate Full Report (requires payment)
- `POST /api/stripe-webhook` → Stripe payment confirmation

#### Internal (for testing)
- `GET /api/health` → Health check
- `POST /api/test-report` → Generate report without payment (dev only)

### Request Format
```json
{
  "business_name": "Joe's Pizza",
  "address": "123 Main St, Austin, TX 78701",
  "email": "buyer@example.com"
}
```

### Response Format
```json
{
  "status": "success",
  "report_id": "uuid",
  "pdf_url": "https://dealscout.com/reports/uuid.pdf",
  "message": "Report sent to buyer@example.com"
}
```

---

## Data Pipeline Details

### 1. Entity Resolution
**Goal:** Confirm the business exists and get canonical details (lat/long, hours, category)

**Method:**
- Google Places API: Search by name + address
- Fallback: Yelp Fusion search
- Store: name, address, lat/long, phone, category, hours

### 2. Review & Reputation Data
**Sources:**
- Yelp Fusion API: ratings, review count, price range, photos
- (Future: Google My Business scraping if needed)

**Extract:**
- Overall rating, review count, top reviews (positive & negative)
- Sentiment breakdown by time period

### 3. Competitive Analysis
**Method:**
- Yelp Fusion: Search businesses in same category within 1-mile radius
- Count competitors, compare ratings, identify market leader

**Output:**
- Competitor count, avg competitor rating, market share estimate

### 4. Demographics
**Source:** Census API (American Community Survey 5-year estimates)

**Extract by ZIP code:**
- Population, median income, age distribution, education level
- Foot traffic estimate (if retail location)

### 5. Search Interest
**Source:** Google Trends (pytrends library)

**Method:**
- Search for business category (e.g., "pizza restaurant") + geo
- Show 12-month trend

### 6. Risk Signals
**Sources (web scraping):**
- BBB.org: complaints, accreditation status
- Google News: mentions (filter for negative keywords: lawsuit, shutdown, health violation)
- (Future: court records if API available)

**Red Flags:**
- Unresolved BBB complaints
- Recent negative news
- Large rating drops

---

## LLM Analysis Strategy

### Claude Prompts (separate for each module)

**1. Sentiment Analysis**
- Input: Top 20 reviews (10 positive, 10 negative)
- Output: Summary of common themes, concerns, praises

**2. Risk Assessment**
- Input: All collected data (reviews, news, BBB)
- Output: List of risks (operational, reputational, financial) + severity (low/med/high)

**3. Competitive Positioning**
- Input: Business data + competitor data
- Output: Market position analysis, differentiation opportunities

**4. Acquisition Readiness Score**
- Input: All analysis results
- Output: 0-100 score + justification

**Token Budget per Report:**
- Quick Scan: ~5K tokens (~$0.25)
- Full Report: ~20K tokens (~$1.50)

---

## Project Structure

```
dealscout/
├── app/
│   ├── main.py                 # FastAPI app entry point
│   ├── api/
│   │   ├── routes.py           # API endpoints
│   │   └── webhooks.py         # Stripe webhooks
│   ├── services/
│   │   ├── entity_resolver.py  # Google Places lookup
│   │   ├── yelp_client.py      # Yelp API wrapper
│   │   ├── census_client.py    # Census data
│   │   ├── trends_client.py    # Google Trends
│   │   ├── scraper.py          # Web scraping (BBB, news)
│   │   └── llm_analyzer.py     # Claude analysis
│   ├── report/
│   │   ├── builder.py          # Report assembly logic
│   │   ├── pdf_generator.py    # WeasyPrint PDF creation
│   │   └── templates/          # HTML templates for reports
│   ├── payment/
│   │   └── stripe_client.py    # Stripe integration
│   └── models/
│       └── schemas.py          # Pydantic models
├── tests/
│   ├── test_entity_resolver.py
│   ├── test_yelp_client.py
│   └── test_report_builder.py
├── static/
│   ├── css/                    # Tailwind CSS
│   └── sample_report.pdf       # Marketing sample
├── templates/
│   ├── index.html              # Landing page
│   └── payment.html            # Stripe checkout
├── .env.example
├── pyproject.toml
├── Dockerfile
└── README.md
```

---

## Development Timeline (6 Sessions)

### Session 1: Planning (THIS SESSION)
- ✅ Create architecture plan
- ✅ Define API structure
- ✅ List data sources
- → Send to Serg for approval

### Session 2: Project Setup & Core Pipeline
**Time:** 1 hour
- Initialize Python project (FastAPI, pyproject.toml, Docker)
- Create GitHub repo (need token from Serg)
- Build entity resolver (Google Places API)
- Build Yelp client
- Unit tests for both
- Test with 3 real businesses

**Blockers:** Need Google Places API key, Yelp API key

### Session 3: Additional Data Sources
**Time:** 1 hour
- Census API integration
- Google Trends integration
- Basic web scraping (BBB)
- Test full data collection pipeline
- Error handling for missing data

### Session 4: LLM Analysis & Report Generation
**Time:** 1 hour
- Claude API integration
- Sentiment analysis module
- Risk detection module
- Competitive analysis module
- PDF generation (WeasyPrint)
- Test end-to-end report generation

**Blockers:** Need Anthropic API key

### Session 5: Web Frontend & Payments
**Time:** 1 hour
- Landing page (Tailwind CSS)
- Input form
- Stripe Checkout integration
- Email delivery (SendGrid)
- Sample report generation for marketing

**Blockers:** Need Stripe account, SendGrid API key

### Session 6: Testing & Launch Prep
**Time:** 1 hour
- End-to-end testing with 10+ businesses
- Edge case handling (business not found, API failures)
- Rate limiting
- Analytics setup (Plausible or Google Analytics)
- Deploy to DigitalOcean/Railway
- Create launch checklist

---

## Launch Strategy (Post-MVP)

### Initial Distribution Channels
1. **SearchFunder community** (actively looking for businesses)
2. **BizBuySell forums** (business buyers hang out here)
3. **Reddit:** r/smallbusiness, r/Entrepreneur
4. **Cold outreach:** Business brokers (offer affiliate deal: 20% commission)

### SEO Strategy
- Target keywords: "business due diligence report", "pre-acquisition intelligence", "business background check"
- Create landing pages for: by industry (restaurant, retail, etc.), by city (top 50 US cities)

### Growth Hacks
- **Free Quick Scan promotion:** First 100 users get Quick Scan free → build testimonials
- **Sample reports:** Generate reports for well-known businesses (Shake Shack, Chipotle) → show on homepage
- **Waitlist/early access:** If not ready to launch, capture emails

---

## Risk Mitigation

### Technical Risks
- **API rate limits:** Stay under free tiers for MVP, cache results, add retry logic
- **Data quality:** Some businesses may not have Yelp reviews → show "limited data" message
- **LLM hallucinations:** Use structured prompts, validate output, show confidence levels

### Business Risks
- **Low demand:** Mitigate with cheap validation (landing page + waitlist before building)
- **High CAC:** Focus on organic (SEO, communities) over paid ads initially
- **Churn:** Offer subscription tier ($99/mo unlimited scans) for brokers/active buyers

### Legal Risks
- **Data scraping:** Use APIs where possible, respect robots.txt, don't resell raw data
- **Liability:** Add disclaimer: "Report is for informational purposes only, not legal/financial advice"

---

## Success Metrics (First 30 Days)

- **10 paid reports** ($1,000+ revenue) → validates demand
- **50+ email signups** → audience building
- **5+ testimonials** → social proof for landing page
- **1+ broker partnership** → distribution channel

---

## Open Questions for Serg

1. **GitHub repo:** Do you want to create it, or should I create it once I have a token?
2. **API keys:** Do you already have Google Cloud (for Places API) and Anthropic accounts, or should I sign up during Session 2?
3. **Domain:** Do you have a domain preference (dealscout.com, getdealscout.com, etc.), or should I pick one?
4. **Priority:** Should I focus on speed-to-launch (bare-bones MVP in 6 sessions) or polish (better UX, more features, 8-10 sessions)?

---

## Next Steps

- ✅ Plan complete
- → Send to Serg for confirmation: `[🎯 DealScout] Phase 0 plan ready for review`
- → Wait for approval + API keys
- → Session 2: Start coding!
