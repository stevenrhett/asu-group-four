# Job Portal - Interactive Prototypes

## Overview

This directory contains interactive HTML prototypes demonstrating the Job Portal platform's user interface and key features. These prototypes are designed for presentation and demonstration purposes.

## Files

### 1. **employer-dashboard.html** - Employer Smart Inbox View
A fully interactive prototype showing the employer's perspective with:
- 📊 **Smart Inbox** with AI-ranked applicants
- 🎯 **Match Scores** with detailed explainability breakdowns
- 🔍 **Filtering System** (skills, experience, status)
- ⚡ **Quick Actions** (shortlist, reject, schedule interview)
- 📈 **Application Statistics**
- 💡 **Match Reasoning** showing why each candidate fits

### 2. **job-seeker-dashboard.html** - Job Seeker Recommendations View
An interactive prototype showing the job seeker's experience with:
- 🎯 **Personalized Job Recommendations** with match scores
- 💡 **Explainability** showing why jobs are recommended
- 📋 **Application Tracking** with status updates
- 🚀 **Quick Apply** functionality
- 📊 **Profile Statistics**
- ✅ **Matched Skills** highlighting

## How to Use for Presentation

### Option 1: Open Directly in Browser (Recommended)

1. Navigate to the `docs/prototypes/` directory
2. Double-click the HTML file you want to show
3. It will open in your default web browser
4. Use during your presentation demo

### Option 2: Open from Command Line

```bash
# Mac/Linux
open docs/prototypes/employer-dashboard.html
open docs/prototypes/job-seeker-dashboard.html

# Windows
start docs/prototypes/employer-dashboard.html

# Linux alternative
xdg-open docs/prototypes/employer-dashboard.html
```

### Option 3: Serve with Python

If you need to serve from a local server:

```bash
cd docs/prototypes
python3 -m http.server 8080
```

Then open:
- http://localhost:8080/employer-dashboard.html
- http://localhost:8080/job-seeker-dashboard.html

## Presentation Flow Recommendations

### For Speaker 2 (Solution & Features)
Use **job-seeker-dashboard.html** to show:
- How job seekers see personalized recommendations
- The explainability feature ("Why this job matches you")
- Quick apply functionality

### For Speaker 5 (Demo & Results)
Use **both prototypes** to demonstrate:

**Part 1: Job Seeker Experience (2 minutes)**
1. Show the job seeker dashboard
2. Click on a recommended job
3. Point out the 92% match score
4. Highlight the "Why this job matches you" section
5. Explain skill matching (green tags = matched)
6. Show application tracking table

**Part 2: Employer Experience (2 minutes)**
1. Switch to employer dashboard
2. Show the Smart Inbox with ranked applicants
3. Point out Sarah Johnson (92% match) at the top
4. Expand the match breakdown bars
5. Demonstrate filtering capabilities (sidebar)
6. Show quick action buttons (shortlist, schedule interview)
7. Point out different application statuses

## Interactive Features

### Employer Dashboard
- ✅ **Clickable Applicant Cards** - Cards highlight on hover
- ✅ **Action Buttons** - Shortlist, reject, schedule buttons show alerts
- ✅ **Filters** - Sidebar filtering controls (visual only)
- ✅ **Status Badges** - Color-coded application statuses

### Job Seeker Dashboard
- ✅ **Job Cards** - Hover effects on recommendations
- ✅ **Quick Apply Button** - Shows alert when clicked
- ✅ **Tab Navigation** - Filter applications by status
- ✅ **Match Scores** - Visual percentage badges

## Key Features to Highlight During Demo

### 1. Explainability (★ Main Differentiator)
**Employer View:**
- Match breakdown bars (Skills: 95%, Experience: 90%, Title: 88%)
- Matched skills highlighted in green
- Clear percentage scores

**Job Seeker View:**
- "Why this job matches you" box with bullet points
- Specific reasons for recommendations
- Skill alignment visualization

### 2. AI-Powered Ranking
**Employer View:**
- Applicants sorted by match score (92%, 89%, 87%, 84%)
- Top candidates appear first
- Different status stages shown

### 3. Smart Filtering
**Employer View:**
- Filter by status, experience, skills, match score
- Quick access to candidate segments

### 4. Application Tracking
**Job Seeker View:**
- Complete application history
- Status progression (Applied → Viewed → Interview)
- Interview scheduling shown for David Kim

## Customization for Your Team

### Update Team Names
Replace "TechCorp Inc." in the employer view with your preferred company name.

### Add Team Member Names
Replace applicant names (Sarah Johnson, Michael Chen, etc.) with team member names for a more personal demo.

### Adjust Match Scores
Edit the percentages in the HTML if you want different demo values.

## Tips for a Great Demo

### Before the Presentation
1. ✅ Test both prototypes in your browser
2. ✅ Zoom browser to 110-125% for better visibility
3. ✅ Close unnecessary browser tabs
4. ✅ Turn off notifications
5. ✅ Bookmark both files for quick access

### During the Presentation
1. 🎯 **Start with context**: "Let me show you what a job seeker sees..."
2. 💡 **Highlight explainability**: "Notice the 'Why this matches you' section - this is our key differentiator"
3. 📊 **Show the data**: "The 92% match is broken down into skills, experience, and title similarity"
4. ⚡ **Demonstrate actions**: Click buttons to show interactivity
5. 🔄 **Switch views**: "Now let's see what employers experience..."

### What to Say

**For Job Seeker View:**
> "Here's what Sarah sees when she logs in. She immediately gets personalized recommendations with clear explanations. Notice how the system tells her exactly WHY each job is a good match - this transparency builds trust."

**For Employer View:**
> "Now from the employer's perspective - this is our Smart Inbox. Candidates are automatically ranked by how well they match the job requirements. The employer can see at a glance that Sarah Johnson is a 92% match, and they can dig into exactly what makes her a great fit."

## Technical Details

### Technologies Used in Prototypes
- Pure HTML5
- CSS3 (Flexbox, Grid, Gradients)
- Vanilla JavaScript (minimal interactivity)
- No external dependencies (fully self-contained)

### Browser Compatibility
- ✅ Chrome/Edge (recommended)
- ✅ Firefox
- ✅ Safari
- ✅ Opera

### Responsive Design
Both prototypes are responsive and will work on:
- Desktop (1920x1080 and above) - Optimal
- Laptop (1366x768 and above) - Good
- Tablet (768px and above) - Acceptable
- Mobile - Basic support

**Recommendation:** Present on desktop/laptop for best experience.

## Backup Plan

If you can't open the HTML files during presentation:

1. **Take Screenshots**: Capture key screens beforehand
2. **Use Slides**: Reference the wireframes in your slide deck
3. **Describe Verbally**: Walk through the features from memory
4. **Show Code**: Display the actual application if it's running

## After the Presentation

### Share with Audience
If asked, you can:
1. Share the GitHub repository link
2. Email the HTML files directly
3. Host on GitHub Pages for live demo

### GitHub Pages Deployment (Optional)
To make these accessible online:

```bash
# These files are already in docs/prototypes/
# GitHub Pages will automatically serve them at:
# https://stevenrhett.github.io/asu-group-four/prototypes/employer-dashboard.html
```

Enable GitHub Pages in repository settings → Pages → Source: main branch → /docs folder

## Troubleshooting

### Issue: HTML files won't open
**Solution:** Right-click → Open With → Choose your browser

### Issue: Styles not showing
**Solution:** Ensure you opened the HTML file directly (not viewing source code)

### Issue: Buttons don't work
**Solution:** JavaScript might be disabled. Check browser settings.

### Issue: Layout looks broken
**Solution:** Zoom out (Ctrl/Cmd + -) or use a different browser

## Contact

For questions about these prototypes or the presentation:

**Team 4 - Arizona State University**
- Andre Exilien
- David Nwankwo
- Muhammad Zahid
- Steven Johnson

**Repository:** https://github.com/stevenrhett/asu-group-four

---

**Good luck with your presentation!** 🚀

*Last updated: November 2025*
