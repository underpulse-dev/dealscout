# DealScout — Roadmap

## Phase 1: Validate Demand (Current)
**Goal:** Prove people will pay for this before writing production code.
**Timeline:** 1-2 weeks

### Step 1: Sample Reports ✅ DONE
- 3 real-data reports across different industries
- Restaurant (Stinkin Crawfish), Auto Repair (35W), Pet Care (Woof Gang)

### Step 2: Landing Page ✅ DONE
- Professional page with value prop, pricing, sample reports
- Needs: deploy to live URL

### Step 3: Deploy Landing Page
- Push to GitHub Pages (or Hetzner if custom domain needed)
- Set up custom domain (dealscout.com or similar)
- Add analytics (Plausible or simple hit counter)
- **"Buy Report" button → email capture form** ("Launching soon — leave your email + the business you want researched")
- Track: page views, button clicks, email signups

### Step 4: Demand Test — Direct Outreach (Week 1)
Post in communities where buyers actively hang out:
- **SearchFunder** — primary audience, serious buyers
- **r/smallbusiness** — 1.5M members
- **r/Entrepreneur** — 3.3M members
- **BizBuySell forums**
- **Facebook groups** (Buying/Selling Small Businesses, etc.)

Format: value-first post sharing a sample report + link to landing page.
NOT a sales pitch — "here's what AI can do for due diligence, thoughts?"

### Step 5: Demand Test — Broker Outreach (Week 1-2)
- Find 20 active brokers on BizBuySell/LinkedIn
- Cold DM: "Would a $200 AI due diligence report help your buyers?"
- Offer free sample report for a listing they have
- Brokers = potential distribution channel (they send us buyers)

### Step 6: Evaluate Signal (End of Week 2)
**Go signals (build the product):**
- ≥5 people submit email + specific business they want researched
- ≥1 broker says "yes, I'd recommend this to buyers"
- ≥50 unique landing page visitors from community posts

**Kill signals (pivot or abandon):**
- <10 landing page visitors (nobody cares)
- Zero email signups (interest but no intent)
- Negative feedback from buyers ("I'd never pay for this")

**Pivot signals (adjust, don't kill):**
- Interest but price objection → test $99 instead of $200
- Interest but wrong audience → try different communities
- Interest but different use case → follow what people actually want

---

## Phase 2: Manual Fulfillment (2-4 weeks)
**Goal:** Deliver real reports to paying customers. Learn what matters.
**Trigger:** Phase 1 go signals met.

- Accept orders via landing page (Stripe checkout, $20 Quick Scan / $100 Full Report intro pricing)
- Generate reports semi-manually using sub-agent (proven process)
- Clawer handles: data collection, analysis, PDF generation via sub-sessions
- Target: 10-20 reports
- Gather feedback after every report (short survey or quick call)
- **Key learning:** What do buyers actually value most? What's missing?
- Iterate on report template based on feedback

---

## Phase 3: Build MVP (2-3 weeks)
**Goal:** Automate the pipeline. Self-serve report generation.
**Trigger:** 10+ reports delivered, clear product-market signal.

### Architecture: Deterministic Pipeline
```
Web form → Stripe payment → Data collection → LLM analysis → PDF → Email
```

### Build order:
1. **Data pipeline** — Yelp API, Census API, web search for competitors/news
2. **LLM analysis** — Single Claude Sonnet 4.5 call with collected data → structured JSON
3. **PDF generation** — WeasyPrint with Jinja2 templates
4. **Web frontend** — FastAPI + Tailwind, Stripe Checkout
5. **Email delivery** — SendGrid
6. **Deploy** — Hetzner

### Infrastructure:
- Python + FastAPI on Hetzner
- SQLite database
- Celery + Redis for async report generation
- Cloudflare R2 for PDF storage

---

## Phase 4: Growth (ongoing)
**Goal:** Scale acquisition channels.
**Trigger:** MVP live, reports generating automatically.

- **SEO landing pages** — city + industry pages ("Due diligence for restaurants in Austin TX")
- **Broker partnerships** — white-label or affiliate (20% commission)
- **Content marketing** — blog posts on due diligence topics
- **Google Ads** — targeted spend on high-intent keywords
- **Subscription tier** — $200/mo for brokers/active buyers (3 reports/mo)

---

## Current Status

| Phase | Status | 
|-------|--------|
| Phase 1: Validate | **IN PROGRESS** — Steps 1-2 done, Steps 3-6 next |
| Phase 2: Manual | Waiting on Phase 1 |
| Phase 3: Build MVP | Waiting on Phase 2 |
| Phase 4: Growth | Waiting on Phase 3 |

## Blockers
- Deploy landing page (need domain or GitHub Pages setup)
- Hetzner access token (Serg to provide)
