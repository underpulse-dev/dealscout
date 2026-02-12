# DealScout — Email Collection Setup

We need to collect email signups from the landing page. Since the site is static (GitHub Pages), we'll use a free form service.

---

## Option 1: Google Forms (Recommended — Free, Simple)

### Step 1: Create the Form
1. Go to https://forms.google.com
2. Click "Blank form"
3. Title: "DealScout Waitlist"
4. Add one question:
   - Question type: "Short answer"
   - Question text: "Email Address"
   - Toggle "Required" ON
5. Click Settings (gear icon)
   - Disable "Limit to 1 response" (allow multiple submissions)
   - Enable "Collect email addresses" if you want double verification
6. Click "Send" → Get the form link
7. Copy the form URL (looks like: `https://docs.google.com/forms/d/e/[FORM_ID]/viewform`)

### Step 2: Embed in Landing Page
There are two ways:

**A) Redirect to Google Form (easiest):**
Update the landing page form to redirect:
```html
<form action="https://docs.google.com/forms/d/e/[YOUR_FORM_ID]/viewform" method="GET" target="_blank">
    <input type="email" name="emailAddress" required placeholder="you@example.com" class="...">
    <button type="submit">Join Waitlist</button>
</form>
```

**B) Embed iframe (cleaner UX):**
Google Forms provides an embed code. Replace the current form section with:
```html
<iframe src="https://docs.google.com/forms/d/e/[YOUR_FORM_ID]/viewform?embedded=true" width="640" height="400" frameborder="0" marginheight="0" marginwidth="0">Loading…</iframe>
```

### Step 3: View Responses
- Open the form in Google Forms
- Click "Responses" tab
- See all email signups in real-time
- Can export to Google Sheets for tracking

---

## Option 2: Tally.so (Cleaner, More Customizable)

### Step 1: Create Account
1. Go to https://tally.so
2. Sign up (free plan: unlimited forms, unlimited responses)
3. Create new form
4. Add "Email" field (mark required)
5. Customize design to match landing page
6. Publish form

### Step 2: Get Embed Code
1. Click "Share" in Tally
2. Choose "Embed"
3. Copy the embed code
4. Paste into landing page HTML

### Step 3: View Responses
- Tally dashboard shows all submissions
- Can export to CSV
- Can set up email notifications when someone signs up

---

## Option 3: Formspree (Developer-Friendly)

### Step 1: Create Account
1. Go to https://formspree.io
2. Sign up (free plan: 50 submissions/month)
3. Create new form
4. Get the form endpoint URL

### Step 2: Update Landing Page
Replace the current form with:
```html
<form action="https://formspree.io/f/[YOUR_FORM_ID]" method="POST">
    <input type="email" name="email" required placeholder="you@example.com" class="...">
    <input type="hidden" name="_subject" value="DealScout Waitlist Signup">
    <button type="submit">Join Waitlist</button>
</form>
```

### Step 3: View Responses
- Formspree dashboard shows submissions
- Also sends email notifications to you
- Can export data

---

## Option 4: Netlify Forms (If Moving to Netlify)

If we move from GitHub Pages to Netlify hosting:
```html
<form name="waitlist" method="POST" data-netlify="true">
    <input type="email" name="email" required placeholder="you@example.com" class="...">
    <button type="submit">Join Waitlist</button>
</form>
```
Netlify automatically handles form submissions (up to 100/month free).

---

## Recommended Approach

**For this validation test:** Use **Google Forms** (Option 1A — redirect method)

**Why:**
- ✅ Free, unlimited submissions
- ✅ Zero setup complexity
- ✅ Responses in Google Sheets (easy tracking)
- ✅ No account creation barriers
- ✅ Can set up in 5 minutes

**How to implement:**
1. Serg creates Google Form
2. Updates `tracks/dealscout/landing-page/index.html` with form action URL
3. Commits and pushes to gh-pages branch
4. Live in 30 seconds

---

## Adding UTM Tracking

To track which community posts drive signups, add a hidden field:

### Google Forms:
1. Add a new question: "Source"
2. Set type to "Short answer"
3. Make it required
4. In the landing page, append `?source=reddit` or `?source=searchfunder` to the URL
5. Use JavaScript to auto-fill the source field from URL params

### Simple JavaScript for Auto-Fill:
```html
<script>
// Get source from URL parameter
const urlParams = new URLSearchParams(window.location.search);
const source = urlParams.get('utm_source') || 'direct';

// If using redirect method, append source to form submission
document.querySelector('form').addEventListener('submit', function(e) {
    const input = document.createElement('input');
    input.type = 'hidden';
    input.name = 'source';
    input.value = source;
    this.appendChild(input);
});
</script>
```

---

## Analytics (Optional)

To track landing page visits:
1. **GitHub Pages built-in stats:** None available
2. **Google Analytics:** Add GA4 tag to landing page (free)
3. **Simple counter:** Add a free service like GoatCounter (https://goatcounter.com)
4. **Plausible Analytics:** Privacy-friendly, $9/month (or self-hosted free)

For validation test, **UTM parameters + form source tracking** is sufficient. Don't need full analytics yet.

---

## Implementation Checklist for Serg

- [ ] Create Google Form for email collection
- [ ] Get form URL
- [ ] Update `landing-page/index.html` with form action
- [ ] Test form submission (submit your own email)
- [ ] Verify email appears in Google Forms responses
- [ ] Commit and push to gh-pages branch
- [ ] Test live site: https://underpulse-dev.github.io/dealscout/
- [ ] Add UTM parameters to community post links
- [ ] Ready to distribute!

---

## What Happens After Someone Signs Up?

**Immediate:**
- Email appears in Google Forms responses
- Serg can manually respond if needed

**After validation test:**
- If we proceed to build → send "early access" email to all signups
- If we pivot/kill → send "thanks, decided to go a different direction" email

For now, no auto-responder needed. Manual follow-up is fine for <100 signups.
