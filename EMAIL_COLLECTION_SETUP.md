# DealScout — Email Collection Setup Guide

**Goal:** Capture waitlist signups from the landing page

**Current Status:** Landing page has a form, but it doesn't save emails anywhere yet.

---

## Quick Option: Google Forms (Recommended)

**Time:** 15-20 minutes  
**Cost:** Free  
**Pros:** Simple, no code, Google Sheets integration, email notifications  
**Cons:** Requires manual integration step

### Step 1: Create Google Form (5 min)

1. Go to https://forms.google.com
2. Click **+ Blank form**
3. Title: "DealScout Waitlist"
4. Add questions:
   - **Email Address**
     - Type: Short answer
     - Required: ✅
     - Validation: Email
   - **What business are you interested in?** (optional)
     - Type: Paragraph
     - Required: ❌
5. Click **Settings** → **Responses**
   - ✅ Collect email addresses
   - ✅ Limit to 1 response
6. Click **Send** → **Link** → Copy the form URL
   - Should look like: `https://docs.google.com/forms/d/e/[FORM_ID]/viewform`

### Step 2: Get the Form Submit URL (5 min)

1. In your Google Form, click **Preview** (eye icon)
2. Open browser DevTools (F12 or Cmd+Opt+I)
3. Go to **Network** tab
4. Submit the form with test data
5. Look for a POST request to `/formResponse`
6. Copy the URL — should look like:
   ```
   https://docs.google.com/forms/d/e/[FORM_ID]/formResponse
   ```
7. Right-click the request → **Copy** → **Copy as cURL**
8. Look for `entry.XXXXXX` field names (these are the form field IDs)
   - Email field will be something like `entry.123456789`
   - Optional field will be something like `entry.987654321`

### Step 3: Update Landing Page (10 min)

1. Clone the repo and switch to gh-pages branch:
   ```bash
   cd /path/to/dealscout
   git checkout gh-pages
   git pull origin gh-pages
   ```

2. Edit `index.html` — find the form section (around line 240-255):
   ```html
   <form id="waitlist-form" class="flex gap-4 max-w-md mx-auto">
   ```

3. Replace the form with:
   ```html
   <form 
       action="https://docs.google.com/forms/d/e/[YOUR_FORM_ID]/formResponse" 
       method="POST" 
       target="hidden_iframe"
       class="flex gap-4 max-w-md mx-auto"
       id="waitlist-form"
   >
       <input 
           type="email" 
           name="entry.[YOUR_EMAIL_FIELD_ID]"
           placeholder="your@email.com" 
           required
           class="flex-1 px-6 py-4 rounded-lg text-gray-900 focus:outline-none focus:ring-2 focus:ring-blue-300"
       />
       <button 
           type="submit"
           class="bg-white text-blue-600 px-8 py-4 rounded-lg font-bold hover:bg-gray-100 transition whitespace-nowrap"
       >
           Join Waitlist
       </button>
   </form>
   <iframe name="hidden_iframe" id="hidden_iframe" style="display:none;"></iframe>
   <p id="waitlist-message" class="mt-4 text-sm text-blue-100"></p>
   ```

4. Replace `[YOUR_FORM_ID]` with your form ID
5. Replace `[YOUR_EMAIL_FIELD_ID]` with the email entry number you found in DevTools

6. Update the JavaScript (around line 350):
   ```javascript
   document.getElementById('waitlist-form').addEventListener('submit', function(e) {
       setTimeout(function() {
           document.getElementById('waitlist-message').textContent = '✅ Thanks! Check your email to confirm.';
           document.getElementById('waitlist-form').reset();
       }, 500);
   });
   ```

7. Save, commit, and push:
   ```bash
   git add index.html
   git commit -m "Integrate Google Forms for email collection"
   git push origin gh-pages
   ```

8. Test: Visit https://underpulse-dev.github.io/dealscout/ and submit your email
9. Check Google Form responses — your email should appear

---

## Alternative: Formspree (Even Easier)

**Time:** 5 minutes  
**Cost:** Free (50 submissions/month), $10/mo for more  
**Pros:** No DevTools digging, cleaner integration, email notifications  
**Cons:** Costs money for >50 signups (but if you get >50, that's validation!)

### Setup

1. Go to https://formspree.io
2. Sign up (free account)
3. Create new form: "DealScout Waitlist"
4. Copy your form endpoint: `https://formspree.io/f/[YOUR_ID]`
5. Edit `index.html`:
   ```html
   <form 
       action="https://formspree.io/f/[YOUR_ID]" 
       method="POST"
       class="flex gap-4 max-w-md mx-auto"
       id="waitlist-form"
   >
       <input 
           type="email" 
           name="email"
           placeholder="your@email.com" 
           required
           class="flex-1 px-6 py-4 rounded-lg text-gray-900 focus:outline-none focus:ring-2 focus:ring-blue-300"
       />
       <button type="submit" class="bg-white text-blue-600 px-8 py-4 rounded-lg font-bold hover:bg-gray-100 transition whitespace-nowrap">
           Join Waitlist
       </button>
   </form>
   ```
6. Commit and push
7. Test: Submit your email, check Formspree dashboard

**Pros of Formspree:** You get email notifications for each signup, can export to CSV, no JavaScript needed.

---

## Alternative: Simple Google Sheets + Apps Script

**Time:** 20-30 minutes  
**Cost:** Free  
**Pros:** Full control, no third-party dependencies  
**Cons:** Requires writing a bit of Google Apps Script

### Setup

1. Create a Google Sheet: "DealScout Waitlist"
2. Headers: `Timestamp | Email | Interested In | IP`
3. **Tools** → **Script editor**
4. Paste this code:
   ```javascript
   function doPost(e) {
     var sheet = SpreadsheetApp.getActiveSpreadsheet().getActiveSheet();
     var timestamp = new Date();
     var email = e.parameter.email || '';
     var interest = e.parameter.interest || '';
     var ip = e.parameter.ip || '';
     
     sheet.appendRow([timestamp, email, interest, ip]);
     
     return ContentService.createTextOutput(JSON.stringify({success: true}))
       .setMimeType(ContentService.MimeType.JSON);
   }
   ```
5. **Deploy** → **New deployment**
   - Type: **Web app**
   - Execute as: **Me**
   - Who has access: **Anyone**
   - Deploy → Copy the URL
6. Update `index.html` to POST to that URL
7. Test: Submit email, check Google Sheet

---

## Which One Should You Use?

- **Google Forms** → Best for simplicity, no cost concerns
- **Formspree** → Best if you want email notifications and easy CSV export
- **Apps Script** → Best if you want full control and no third parties

For MVP validation, **Google Forms** is the sweet spot: free, reliable, and takes 20 minutes.

---

## After Setup: Testing Checklist

- [ ] Submit test email from landing page
- [ ] Verify email appears in Google Form / Formspree / Sheet
- [ ] Check that success message shows on landing page
- [ ] Test from mobile device
- [ ] Share with a friend to verify it works externally

---

## Tracking Signups

After setup, check daily:
- Google Forms: https://docs.google.com/forms → Your form → **Responses** tab
- Formspree: https://formspree.io → Dashboard → Your form
- Apps Script: Open your Google Sheet

Log daily counts in `distribution-tracking.md`

---

## Troubleshooting

**Form submits but emails don't appear:**
- Check that form action URL is correct (no typos)
- Verify entry field IDs match (for Google Forms)
- Check Formspree dashboard for errors

**Success message doesn't show:**
- Add `target="hidden_iframe"` to form tag
- Add invisible iframe: `<iframe name="hidden_iframe" style="display:none;"></iframe>`

**Getting CORS errors:**
- Google Forms: Use POST with `target="hidden_iframe"` (avoids CORS)
- Formspree: Already CORS-friendly
- Apps Script: Enable CORS in deployment settings

---

**Need help?** Message Clawer with `[🎯 DealScout] Email collection issue: [description]`
