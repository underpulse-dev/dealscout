# DealScout — Distribution Test Plan

**Objective:** Validate demand for DealScout before building production code.
**Success Criteria:** >50 email signups OR >5 purchase attempts in 2 weeks.
**Start Date:** TBD (when Serg posts)
**Duration:** 14 days from first post

---

## Tracking Metrics

Track daily in `tracks/dealscout/distribution-tracking.md`:

1. **Landing page visits** (check GitHub Pages analytics or add simple counter)
2. **Email signups** (waitlist form submissions)
3. **"Buy Report" button clicks** (if we add event tracking)
4. **Community engagement** (upvotes, comments, DMs)
5. **Conversion rate** (visitors → signups)

---

## Distribution Channels (Priority Order)

### 1. SearchFunder.com (PRIMARY TARGET)
**Why:** This is THE community for small business buyers. Highest intent audience.
**Account needed:** Yes (create free account)
**Post type:** Forum post in "Due Diligence" or "General Discussion"
**Sample report to include:** Stinkin Crawfish (Report #1) — shows what a DealScout report looks like
**Timing:** Post on a weekday morning (9-11am EST)
**Follow-up:** Engage with comments within first 6 hours

### 2. Reddit — r/smallbusiness
**Why:** 1.4M members, active community, entrepreneurial mindset
**Account needed:** Yes (use existing or create)
**Post type:** Text post (some subs ban direct links)
**Title:** "I built an AI tool to screen small business acquisitions (like Carfax for businesses) — feedback wanted"
**Body:** Share problem, show sample report, ask for feedback
**Timing:** Tuesday-Thursday, 8-10am EST (peak engagement)
**Subreddit rules:** Check if self-promotion is allowed (might need "feedback" framing)

### 3. Reddit — r/Entrepreneur
**Why:** 3.8M members, open to new business tools
**Account needed:** Same as above
**Post type:** Similar to r/smallbusiness
**Timing:** Same

### 4. BizBuySell Forums (if accessible)
**Why:** Buyers actively browsing businesses for sale
**Account needed:** Check if free accounts can post
**Post type:** Forum discussion
**Angle:** "Has anyone tried using AI to screen listings before DD?"

### 5. Facebook Groups (if Serg has access)
**Potential groups:**
- "Business Buying & Selling"
- "Small Business Acquisitions"
- "Entrepreneurs & Small Business Owners"
**Note:** Facebook groups often have anti-promotion rules. Frame as "I made this tool, looking for feedback" rather than selling.

### 6. Hacker News (Show HN)
**Why:** Tech-savvy audience, some may be interested in acquiring businesses
**Post type:** "Show HN: DealScout – AI reports for small business buyers (like Carfax for acquisitions)"
**Timing:** Best posting times: 8-10am EST on weekdays
**Note:** HN is hit-or-miss. Could get 500+ visits or nothing.

### 7. LinkedIn (Optional)
**Post type:** Personal post from Serg's account
**Angle:** "I'm building a tool to help business buyers screen acquisitions faster. Would this be useful?"
**Note:** LinkedIn engagement can be good for B2B tools.

---

## Post Templates

See `tracks/dealscout/post-templates.md` for ready-to-use templates for each platform.

---

## What To Do With Feedback

**If people ask questions:**
- Respond within 6 hours
- Be helpful, not salesy
- If they want to try it: "We're in beta — join the waitlist and I'll send you early access"

**If people criticize:**
- Listen and document feedback
- If it's a valid concern, acknowledge it
- Don't get defensive

**If people want to buy:**
- "We're in final testing — join the waitlist and I'll send you a discount code when we launch"
- Track these as high-intent leads

---

## Analytics Setup (Before Posting)

1. **Email form:** Use a simple Google Form or Tally.so (free) to collect emails
2. **Click tracking:** Add UTM parameters to links for each platform:
   - SearchFunder: `?utm_source=searchfunder&utm_medium=forum&utm_campaign=validation`
   - Reddit r/smallbusiness: `?utm_source=reddit&utm_medium=post&utm_campaign=rsmallbusiness`
   - Reddit r/Entrepreneur: `?utm_source=reddit&utm_medium=post&utm_campaign=rentrepreneur`
   - Hacker News: `?utm_source=hackernews&utm_medium=post&utm_campaign=showhn`
3. **GitHub Pages analytics:** Enable via repo settings or add simple JS counter

---

## Decision Timeline

**Day 7 checkpoint:** Review metrics. If <10 signups and low engagement, consider:
- Adjusting messaging
- Posting in additional communities
- Offering free first report to early testers

**Day 14 final evaluation:**
- If **>50 signups OR >5 purchase attempts**: PROCEED TO BUILD (Phase 2)
- If **20-49 signups**: Conditional proceed — build basic version, re-test with live product
- If **<20 signups**: PIVOT or KILL
  - Option A: Pivot positioning (e.g., target brokers instead of buyers)
  - Option B: Pivot product (different report focus)
  - Option C: Kill idea, move to next startup concept

---

## Serg's Action Items

1. Create accounts on SearchFunder, Reddit (if needed)
2. Set up email collection form (Google Form or Tally)
3. Add UTM tracking to landing page links
4. Post using templates in `post-templates.md`
5. Monitor and respond to comments daily
6. Log metrics in `distribution-tracking.md`
7. Report results to Clawer on Day 7 and Day 14

---

**Remember:** The goal is NOT to get sales. The goal is to validate INTEREST. Email signups = "I want this when it exists" = validated demand.
