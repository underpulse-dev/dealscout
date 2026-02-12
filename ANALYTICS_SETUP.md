# DealScout — Analytics Setup Guide

**Goal:** Track visitors, engagement, and conversions during the 14-day distribution test

**Why this matters:** Without analytics, you won't know:
- How many people visited the landing page
- Which posts drove traffic
- Which sample reports people actually read
- How many clicked "Get Quick Scan" or "Get Full Report"
- What your conversion rate is (visitors → signups)

---

## Quick Setup: Google Analytics 4 (Recommended)

**Time:** 20 minutes  
**Cost:** Free  
**Complexity:** Low (copy-paste tracking code)

### Step 1: Create Google Analytics Property (5 min)

1. Go to https://analytics.google.com
2. **Admin** (gear icon) → **Create Property**
3. Property name: "DealScout Landing Page"
4. Time zone: Your timezone
5. Currency: USD
6. Click **Next**
7. Business details:
   - Industry: Technology
   - Size: Small (1-10)
   - Intended use: Measure customer engagement
8. Click **Create**
9. Accept Terms of Service

### Step 2: Set Up Data Stream (5 min)

1. Platform: **Web**
2. Website URL: `https://underpulse-dev.github.io`
3. Stream name: "DealScout GitHub Pages"
4. Enhanced measurement: ✅ (leave all enabled)
5. Click **Create stream**
6. Copy your **Measurement ID** (looks like `G-XXXXXXXXXX`)

### Step 3: Add Tracking Code to Landing Page (10 min)

1. Clone repo and checkout gh-pages:
   ```bash
   cd /path/to/dealscout
   git checkout gh-pages
   git pull origin gh-pages
   ```

2. Edit `index.html` — add this code in the `<head>` section (before `</head>`):
   ```html
   <!-- Google tag (gtag.js) -->
   <script async src="https://www.googletagmanager.com/gtag/js?id=G-XXXXXXXXXX"></script>
   <script>
     window.dataLayer = window.dataLayer || [];
     function gtag(){dataLayer.push(arguments);}
     gtag('js', new Date());
     gtag('config', 'G-XXXXXXXXXX');
   </script>
   ```
   Replace `G-XXXXXXXXXX` with your actual Measurement ID (twice)

3. Commit and push:
   ```bash
   git add index.html
   git commit -m "Add Google Analytics tracking"
   git push origin gh-pages
   ```

4. Wait 2-3 minutes for GitHub Pages to rebuild

5. **Test:** Visit https://underpulse-dev.github.io/dealscout/ and wait 30 seconds
6. Go to Google Analytics → **Reports** → **Realtime**
7. You should see "1 user right now" — that's you!

---

## Step 4: Set Up Custom Events (Advanced, Optional)

Track specific user actions beyond page views.

### Events to Track:
- Sample report views (which report is most interesting?)
- "Get Quick Scan" button clicks
- "Get Full Report" button clicks
- Waitlist form submissions
- Outbound links (if you add any)

### Implementation:

Edit `index.html` — add this JavaScript before the closing `</body>` tag:

```html
<script>
// Track sample report clicks
document.querySelectorAll('a[href*="sample-reports"]').forEach(function(link) {
  link.addEventListener('click', function(e) {
    var reportName = this.href.split('/').pop().replace('.html', '');
    gtag('event', 'view_sample_report', {
      'report_name': reportName
    });
  });
});

// Track pricing button clicks
document.querySelectorAll('a[href*="#pricing"]').forEach(function(button) {
  button.addEventListener('click', function() {
    gtag('event', 'pricing_interest', {
      'button_text': this.innerText
    });
  });
});

// Track waitlist form submission
var waitlistForm = document.getElementById('waitlist-form');
if (waitlistForm) {
  waitlistForm.addEventListener('submit', function() {
    gtag('event', 'waitlist_signup', {
      'form_location': 'landing_page'
    });
  });
}
</script>
```

Commit and push again:
```bash
git add index.html
git commit -m "Add custom event tracking for sample reports and CTAs"
git push origin gh-pages
```

---

## What You'll See in Google Analytics

### Real-Time Reports (check daily)
**Path:** Reports → Realtime

- Users right now
- Page views in last 30 minutes
- Traffic sources (where people came from)
- Pages being viewed

### Acquisition Reports (check Day 7, Day 14)
**Path:** Reports → Acquisition → Traffic acquisition

Shows where visitors came from:
- `reddit.com` → Your r/smallbusiness or r/Entrepreneur post
- `news.ycombinator.com` → Hacker News
- `searchfunder.com` → SearchFunder post
- `linkedin.com` → LinkedIn
- `(direct)` → Typed URL directly (unlikely)
- `t.co` or `facebook.com` → Twitter/Facebook shares

**Action:** Compare traffic sources to decide which platforms to focus on

### Engagement Reports (check Day 7, Day 14)
**Path:** Reports → Engagement → Pages and screens

- Which pages get the most views?
- How long do people spend on the landing page?
- Which sample reports get viewed most?

**Action:** If one sample report gets way more views, post that one in future communities

### Events Reports (if you added custom tracking)
**Path:** Reports → Engagement → Events

- How many `view_sample_report` events? (people reading reports)
- How many `waitlist_signup` events? (form submissions)
- How many `pricing_interest` events? (button clicks)

**Action:** Calculate conversion rate:
- `waitlist_signup` / `page_view` = Conversion rate %
- Industry average for cold traffic: 1-3%
- If you hit 5%+, that's strong validation

---

## Daily Tracking Routine (5 minutes)

**When:** Same time every day (e.g., 9am)

1. Open Google Analytics → **Realtime** → Check if anyone is currently browsing
2. **Reports** → **Realtime** → **Event count by Event name** (last 30 min)
3. **Reports** → **Acquisition** → **Traffic acquisition** → Last 7 days
   - Note which sources are sending traffic
4. **Reports** → **Engagement** → **Events** → Last 7 days
   - Count `waitlist_signup` events
5. Log in `distribution-tracking.md`:
   ```markdown
   ### Day 3 - Feb 15, 2026
   - Total visits: 47
   - Email signups: 3
   - Top traffic source: reddit.com (32 visits)
   - Sample report views: 18 (12 Stinkin Crawfish, 4 35W Auto, 2 Woof Gang)
   - Conversion rate: 6.4% (3/47)
   - Notes: r/smallbusiness post doing well, lots of engagement in comments
   ```

---

## Alternative: Simple Plausible Analytics

**Time:** 10 minutes  
**Cost:** $9/mo (but 30-day free trial)  
**Pros:** Privacy-friendly, simpler interface, no cookie consent needed, lightweight  
**Cons:** Costs money, less detailed than GA4

### Setup:

1. Sign up at https://plausible.io (free trial)
2. Add site: `underpulse-dev.github.io`
3. Copy the tracking script (1 line of code)
4. Paste in `<head>` of `index.html`
5. Commit and push
6. Done! Dashboard shows visitors, sources, pages

**When to use:** If Google Analytics feels overwhelming or you care about privacy compliance

---

## Alternative: No Analytics (Manual Tracking)

**Time:** 0 minutes  
**Cost:** Free  
**Pros:** Zero setup, privacy-friendly  
**Cons:** Very limited visibility

If you skip analytics, you can still track:
- **Email signups** (from Google Form)
- **Comments/engagement** on Reddit/HN/SearchFunder posts
- **DMs** from interested buyers
- **Upvotes/reactions** on posts

This is enough for basic validation, but you won't know:
- How many people visited but didn't sign up (conversion rate mystery)
- Which posts drove traffic
- Which sample reports people care about

**Verdict:** At minimum, add Google Analytics — it's free and takes 20 minutes

---

## Metrics That Matter (Day 14 Evaluation)

### Vanity Metrics (interesting but don't overweight):
- Total page views
- Time on page
- Bounce rate

### Validation Metrics (what actually matters):
- **Email signups** (>50 = strong signal)
- **"Buy now" attempts** (>5 = very strong signal)
- **Engaged comments** (questions about pricing, features, "when can I buy?")
- **Direct messages** from interested buyers
- **Conversion rate** (signups / visitors):
  - <1% = weak positioning
  - 1-3% = normal cold traffic
  - 3-5% = good product-market fit signal
  - 5%+ = strong validation

### Example Scenario:

**Scenario A: Strong Validation**
- 1,200 visitors
- 78 email signups
- 12 people clicked "Get Full Report" button
- Conversion rate: 6.5%
- 4 DMs asking "when can I actually buy this?"
- **Verdict:** BUILD IT

**Scenario B: Weak Validation**
- 800 visitors
- 8 email signups
- 2 button clicks
- Conversion rate: 1%
- Comments mostly "interesting idea" (not "I need this")
- **Verdict:** PIVOT positioning or move on

**Scenario C: Traffic Problem**
- 50 visitors total
- 5 email signups
- Conversion rate: 10%!
- 2 DMs saying "I'd buy this today"
- **Verdict:** Distribution failed, not the product. Try different channels or paid ads.

---

## Troubleshooting

**GA4 shows 0 users but I just visited:**
- Wait 5-10 minutes (data isn't instant)
- Check that Measurement ID is correct
- Check browser isn't blocking analytics (disable ad blockers)
- Open DevTools → Network tab → look for `collect?` requests to Google

**Events not showing up:**
- Custom events can take 24-48 hours to appear in reports
- Check **Realtime** → **Events** to see them immediately
- Verify JavaScript has no syntax errors (open DevTools Console)

**Tracking code in sample report HTML files:**
- Don't worry — each HTML file is standalone, so they won't trigger GA unless you add the code
- Only the main `index.html` needs tracking code for now
- Sample reports load in the same domain, so GA will track them as pageviews automatically

---

## Privacy & Legal

**Do you need a cookie banner?**
- Technically yes if you have EU visitors (GDPR)
- For a 2-week MVP test, most founders skip it
- If you want to be compliant, add a simple banner:
  - "We use Google Analytics to measure traffic. By using this site, you agree."
  - Link to a simple privacy policy

**Should you worry about GDPR/CCPA?**
- For a waitlist validation test with <1000 visitors, realistically no
- You're not selling data, not targeting EU citizens specifically
- Once you launch for real, add a privacy policy and cookie consent

**Quick privacy policy template:**
https://www.freeprivacypolicy.com/free-privacy-policy-generator/

---

## Next Steps After Setup

1. ✅ Add Google Analytics tracking code to `index.html`
2. ✅ Test in Realtime reports (visit the page, see yourself)
3. ✅ (Optional) Add custom event tracking for buttons and reports
4. ✅ Commit and push to gh-pages
5. ✅ Bookmark Google Analytics dashboard
6. ✅ Set a daily reminder to check analytics (same time every day)
7. ✅ Log metrics in `distribution-tracking.md`

**After Day 14:** Export all data before the trial period ends (if using paid tool)

---

## Summary: Why Analytics Matters

Without analytics:
- "I posted to Reddit, got some upvotes, 3 people signed up" ← Hard to evaluate

With analytics:
- "Posted to Reddit, got 342 visitors, 18 read sample reports, 12 clicked pricing, 3 signed up (0.9% conversion). Comments were positive but not buyer intent. Top sample report: 35W Auto (67% of views). Verdict: Good awareness, weak purchase intent." ← Actionable insights

Analytics turns validation from a guess into a decision.

---

**Questions? Message Clawer with [🎯 DealScout] Analytics issue: [description]**
