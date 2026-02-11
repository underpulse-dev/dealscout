# DealScout Report Generation Guidelines

## Core Principle: Verifiable Data Only

Every data point in a DealScout report **MUST** be independently verifiable by a human reader. No fabricated, assumed, or simulated data.

## Verification Format

Every factual claim must include a verification reference:

```markdown
📎 Verify: [Brief description of what to check](URL) — What to look for on the page
```

**Example:**
```markdown
**Review Score:** 4.5/5.0 (347 reviews)  
📎 Verify: [Yelp listing](https://www.yelp.com/biz/example-business-city) — Check star rating and review count at top of page
```

## When Data Cannot Be Verified

If information cannot be independently confirmed, mark it clearly:

```markdown
⚠️ Unverifiable — sourced from [method/reason]
```

**Examples:**
- `⚠️ Unverifiable — sourced from verbal claim by listing broker`
- `⚠️ Unverifiable — estimated from industry averages`
- `⚠️ DATA NOT AVAILABLE — no public records found`

## Required Verification Sources by Category

### 1. Business Reviews
- **Primary:** Yelp listing URL (exact business page)
- **Secondary:** Google Maps/Business URL, TripAdvisor, specialized review sites
- **What to verify:** Star rating, review count, recent review sentiment
- **Example:** `📎 Verify: [Yelp reviews](https://yelp.com/biz/...) — See 4.5★ rating and 347 reviews`

### 2. Demographics & Market Data
- **Census data:** https://data.census.gov
- **DataUSA:** https://datausa.io/profile/geo/[city-state]
- **What to verify:** Population, median income, age distribution, employment
- **Example:** `📎 Verify: [DataUSA Inglewood profile](https://datausa.io/profile/geo/inglewood-ca) — Check median household income`

### 3. Competitor Analysis
- **Yelp category search:** Direct URL to search results
- **Google Maps search:** Link to map view with competitors
- **What to verify:** Number of competitors, their ratings, proximity
- **Example:** `📎 Verify: [Yelp seafood search Inglewood](https://yelp.com/search?find_desc=seafood&find_loc=Inglewood%2C+CA) — Count of competing restaurants`

### 4. Business Details
- **Website:** Direct link to business website (if available)
- **Broker listing:** BizBuySell, LoopNet, or broker page URL
- **BBB:** Better Business Bureau profile (if exists)
- **LinkedIn/Social:** Company pages
- **What to verify:** Asking price, years in operation, square footage, equipment details
- **Example:** `📎 Verify: [BizBuySell listing](https://bizbuysell.com/...) — See asking price $425K and 8 years established`

### 5. Location & Real Estate
- **Google Maps:** Pinned location with street view
- **Zillow/LoopNet:** Commercial real estate listings
- **What to verify:** Exact address, proximity to landmarks, visibility, parking
- **Example:** `📎 Verify: [Google Maps location](https://maps.google.com/?q=...) — See street view and parking lot`

### 6. Permits & Licenses
- **County/City records:** Direct link to permit portal or search result
- **State licensing databases:** Link to license lookup
- **What to verify:** Active licenses, health inspection scores, permit status
- **Example:** `📎 Verify: [LA County health inspection](https://ehservices.publichealth.lacounty.gov/...) — See latest inspection score`

## Report Structure Standards

### Header
- Business name
- Location (City, State)
- Report type (Full Report / Quick Scan)
- Date generated
- Data collection timestamp

### Executive Summary
- Brief 3-4 sentence overview
- Key opportunity/risk highlights
- Quick verdict (Strong Opportunity / Moderate / High Risk / Pass)

### Core Sections
1. **Business Overview** — What they do, how long operating, basic stats
2. **Financial Overview** — Asking price, revenue claims, verification status
3. **Market Position** — Reviews, reputation, customer sentiment
4. **Location Analysis** — Foot traffic, visibility, demographics
5. **Competitive Landscape** — Direct competitors, market saturation
6. **Opportunities** — Growth potential, underutilized assets
7. **Risks & Red Flags** — Concerns, challenges, unknowns
8. **Verdict** — Final assessment with confidence level

### Verification Appendix
At the end of each report, include:
```markdown
## Data Sources & Verification
All data points in this report can be independently verified using the 📎 Verify links throughout.

**Primary Sources:**
- Yelp: [URL]
- Demographics: [URL]
- Broker listing: [URL]
- [Additional sources]

**Data Collection:** [Date/Time]
**Unverifiable Claims:** [List any ⚠️ items or note "None"]
```

## Quality Checklist

Before finalizing a report, verify:
- [ ] Every factual claim has a 📎 Verify link OR ⚠️ Unverifiable tag
- [ ] All URLs are publicly accessible (no login required)
- [ ] URLs point to the EXACT page showing the data (not homepage)
- [ ] Review scores match what's currently on the linked page
- [ ] Demographic data includes the specific geographic area
- [ ] Competitor searches use the correct location parameters
- [ ] Financial claims cite the specific source (broker listing, etc.)
- [ ] No assumptions presented as facts

## Research Best Practices

### Web Search Strategy
1. **Business name + city + state** → Find official listings
2. **"Business name" reviews** → Aggregate review sentiment
3. **Business category + city** → Find competitors
4. **City + state + demographics** → Market data
5. **Business name + "for sale"** → Broker listings

### Rate Limiting
- Sleep 2 seconds between web_search calls to avoid API limits
- Batch searches where possible
- Cache results to avoid redundant calls

### Data Freshness
- Note the date when data was collected
- For time-sensitive data (reviews, prices), include "as of [date]"
- Flag outdated sources (>6 months old) when relevant

## Ethics & Disclaimers

Include at the end of every report:

```markdown
---
**Disclaimer:** This report is for informational purposes only and does not constitute financial, legal, or investment advice. All data points should be independently verified before making any business decisions. Review scores and demographics are snapshots from public sources and may change. DealScout is not responsible for the accuracy of third-party data sources.
```

---

**Remember:** Trust is built on verifiable facts. When in doubt, mark it as unverifiable or leave it out.
