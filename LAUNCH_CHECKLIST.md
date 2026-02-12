# DealScout — Distribution Test Launch Checklist

**Status:** Landing page is LIVE at https://underpulse-dev.github.io/dealscout/
**Next:** Set up email collection and post to communities

---

## ✅ Completed
- [x] Phase 1 Step 1: Created 3 sample reports with real data
- [x] Phase 1 Step 2: Created professional landing page
- [x] Phase 1 Step 3: Deployed to GitHub Pages (site is live)

---

## 📋 What Serg Needs To Do (2-3 hours total)

### 1. Set Up Email Collection (30 min)
**Goal:** Capture waitlist signups from landing page

- [ ] Create Google Form for email collection
  - Go to https://forms.google.com → New form
  - Title: "DealScout Waitlist"
  - Add email field (required)
  - Add short answer field "What business are you interested in?" (optional)
  - Copy form URL
- [ ] Clone the repo and update landing page:
  ```bash
  cd /path/to/dealscout
  git checkout gh-pages
  # Edit index.html: Update form action with Google Form URL
  # Line ~120: <form action="[PASTE_GOOGLE_FORM_URL]" method="GET" target="_blank">
  git add index.html
  git commit -m "Add Google Form integration for waitlist"
  git push origin gh-pages
  ```
- [ ] Test: Submit your own email, verify it appears in Google Form responses

**Full instructions:** See `EMAIL_COLLECTION_SETUP.md`

---

### 2. Create Community Accounts (15 min)
**Goal:** Get access to post in target communities

- [ ] SearchFunder.com — Create free account (if don't have one)
- [ ] Reddit — Use existing account or create new
- [ ] Hacker News — Create account (needs email verification)
- [ ] LinkedIn — Use existing account
- [ ] Facebook — Check if you have access to business buying groups

---

### 3. Post to Communities (1 hour)
**Goal:** Drive traffic to landing page, measure interest

**Order of priority:**
1. [ ] **SearchFunder** (highest priority — actual buyers)
   - Copy template from `post-templates.md` → SearchFunder section
   - Post in "Due Diligence" or "General Discussion" forum
   - Best time: Tuesday-Thursday, 9-11am EST
   - Link to sample report #1 (Stinkin Crawfish)
2. [ ] **Reddit r/smallbusiness**
   - Copy template from `post-templates.md` → r/smallbusiness section
   - Post as text (not link post)
   - Best time: Tuesday-Thursday, 8-10am EST
3. [ ] **Reddit r/Entrepreneur**
   - Similar to r/smallbusiness
   - Same timing
4. [ ] **Hacker News** (Show HN)
   - Title: "Show HN: DealScout – AI reports for small business buyers"
   - URL: https://underpulse-dev.github.io/dealscout/
   - Best time: 8-10am EST on weekdays
5. [ ] **LinkedIn** (optional)
   - Personal post from your profile
   - Template in `post-templates.md` → LinkedIn section

**Important:**
- Don't post to all platforms on the same day (space them out)
- Respond to comments within 6 hours
- Be helpful, not salesy
- Track which post performs best

**Templates:** See `post-templates.md` for ready-to-use posts for each platform

---

### 4. Track Metrics Daily (5 min/day)
**Goal:** Measure validation signal

- [ ] Open `distribution-tracking.md`
- [ ] Log daily:
  - Landing page visits (if you set up analytics)
  - Email signups (check Google Form responses)
  - Comments/engagement on posts
  - Any DMs or direct inquiries
- [ ] Update daily for 14 days

**Full tracking template:** See `distribution-tracking.md`

---

### 5. Day 7 Checkpoint (30 min)
**Goal:** Evaluate if adjustments are needed

- [ ] Review metrics in `distribution-tracking.md`
- [ ] If <10 signups → consider:
  - Posting in additional communities
  - Adjusting messaging
  - Offering free first report to early testers
- [ ] If 10+ signups → continue as planned
- [ ] Notify Clawer of results: `[🎯 DealScout] Day 7 checkpoint: [status]`

---

### 6. Day 14 Final Evaluation (1 hour)
**Goal:** Decide if we build the product

- [ ] Review all metrics
- [ ] Make go/no-go decision:
  - **PROCEED TO BUILD:** >50 signups OR >5 purchase attempts
  - **CONDITIONAL PROCEED:** 20-49 signups (build basic version, re-test)
  - **PIVOT:** <20 signups, but promising feedback (adjust positioning)
  - **KILL:** <20 signups, no traction (move to next idea)
- [ ] Notify Clawer: `[🎯 DealScout] Final validation results: [decision]`
- [ ] Update `STATE.md` with decision

**Full evaluation criteria:** See `DISTRIBUTION_PLAN.md`

---

## 📚 Reference Documents

| Document | Purpose |
|----------|---------|
| `DISTRIBUTION_PLAN.md` | Full strategy, evaluation criteria |
| `post-templates.md` | Ready-to-use posts for each platform |
| `distribution-tracking.md` | Daily metrics log |
| `EMAIL_COLLECTION_SETUP.md` | Step-by-step email form setup |
| `STATE.md` | Current project status |
| `ROADMAP.md` | Full product roadmap |

---

## ⏱️ Time Estimate

- Email setup: 30 min
- Account creation: 15 min
- Writing & posting: 1 hour
- Daily tracking (14 days): 5 min/day = 70 min total
- Checkpoints: 30 min + 1 hour
- **Total time commitment:** ~4 hours over 2 weeks

---

## 🚨 What If I Get Stuck?

Message Clawer with `[🎯 DealScout]` prefix:
- Technical issues with GitHub/forms
- Questions about which communities to prioritize
- How to respond to specific feedback
- Any blockers

---

## 🎯 Success Looks Like

**By Day 14:**
- 50+ email signups → Strong signal, build the product
- 5+ people asking "when can I buy?" → Very strong signal
- Active discussions in comments → People care about the problem
- Specific feedback on features/pricing → Validation + product direction

**If we don't hit targets:**
- It's not a failure — it's data
- We learned demand is weak OR positioning is wrong
- We pivot or move to the next idea
- No time wasted building something nobody wants

---

## 📢 Reminder: This Is A Test, Not A Launch

- Don't stress if numbers are low in first few days
- Engagement > raw traffic (10 interested people > 100 drive-bys)
- Feedback is as valuable as signups
- The goal is to learn, not to sell

---

**Questions? Ping Clawer with [🎯 DealScout] prefix**
