# Presentation Materials - README

## Overview

This directory contains comprehensive presentation materials for a 20-minute team presentation with 5 speakers.

## Files

### 📊 Slide Deck
- **`slides.md`** - Marp-formatted slides (recommended for presenting)
  - 35+ slides optimized for 16:9 format
  - Ready to convert to PDF, PowerPoint, or HTML
  - Includes all content structured for 5 speakers

### 📖 Supporting Documents
- **`presentation.md`** - Detailed presentation content with full speaker notes
- **`speaker-guide.md`** - Quick reference guide for each speaker
- **`presentation-summary.md`** - One-page handout for audience

## How to Use the Slides

### Option 1: Marp (Recommended)

**Install Marp CLI:**
```bash
npm install -g @marp-team/marp-cli
```

**Generate PDF:**
```bash
cd docs
marp slides.md --pdf
```

**Generate PowerPoint:**
```bash
marp slides.md --pptx
```

**Generate HTML (for web presentation):**
```bash
marp slides.md --html
```

**Live Preview:**
```bash
marp slides.md --preview
```

### Option 2: Marp for VS Code

1. Install the "Marp for VS Code" extension
2. Open `slides.md` in VS Code
3. Click the preview icon or press `Ctrl+Shift+V` (Windows/Linux) or `Cmd+Shift+V` (Mac)
4. Export to PDF/PPTX from the preview window

### Option 3: Online Marp Editor

1. Go to https://web.marp.app/
2. Copy and paste the content from `slides.md`
3. Export to your preferred format

### Option 4: Manual Conversion

Copy the content from `slides.md` and paste into:
- **PowerPoint** - Each `---` separator indicates a new slide
- **Google Slides** - Same as PowerPoint
- **Keynote** - Same as PowerPoint

## Slide Structure

### Timing (20 minutes total)

| Speaker | Section | Duration | Slides |
|---------|---------|----------|--------|
| **Speaker 1** | Introduction & Problem | 4 min | Slides 1-5 |
| **Speaker 2** | Solution & Features | 4 min | Slides 6-10 |
| **Speaker 3** | Technical Architecture | 4 min | Slides 11-16 |
| **Speaker 4** | Development Process | 4 min | Slides 17-21 |
| **Speaker 5** | Demo & Future | 4 min | Slides 22-27 |

### Speaker Transitions

The slides are marked with speaker sections:
- Look for `<!-- _class: lead -->` headers indicating new speaker
- Each speaker section has a title slide
- Smooth transitions built into the content

## Presentation Tips

### Before Presenting

1. **Practice with timing** - Each speaker should rehearse their 4-minute section
2. **Test the demo** - Speaker 5 should ensure the app runs locally
3. **Review Q&A prep** - See `speaker-guide.md` for common questions
4. **Export slides early** - Generate PDF/PPTX at least 1 day before

### During Presentation

1. **Speaker 1**: Set the problem clearly - this hooks the audience
2. **Speaker 2**: Focus on benefits, not just features
3. **Speaker 3**: Don't get too technical - balance is key
4. **Speaker 4**: Show that you followed a professional process
5. **Speaker 5**: Demo is your proof - practice it until smooth

### Technical Setup

- **Resolution**: Slides are 16:9 format (1920x1080)
- **Fonts**: Use default fonts for compatibility
- **Demo**: Have screenshots as backup if live demo fails
- **Timing**: Keep a timer visible to all speakers

## Customization

### To Edit Slides

1. Open `slides.md` in any text editor
2. Each slide is separated by `---`
3. Use markdown formatting:
   - `#` for titles
   - `##` for headings
   - `-` for bullet points
   - Code blocks with triple backticks
   - Tables with `|` separators

### To Add Your Names

The title slide shows:
```markdown
Andre Exilien • David Nwankwo • Muhammad Zahid • Steven Johnson
```

Update this if needed, or assign specific speakers to sections.

### To Change Branding

Edit the frontmatter at the top of `slides.md`:
```yaml
header: 'Your Header Here'
footer: 'Your Footer Here'
theme: default  # or gaia, uncover, etc.
```

## Additional Resources

### Marp Documentation
- Official docs: https://marpit.marp.app/
- Theme gallery: https://github.com/marp-team/marp-core/tree/main/themes

### Presentation Best Practices
- Keep slides simple (6 bullets max, 6 words per bullet)
- Use visuals over text when possible
- Maintain eye contact with audience
- Practice transitions between speakers

## Demo Setup

For **Speaker 5's demo**, ensure:

```bash
# Terminal 1: Start MongoDB
docker run -d --name job-portal-mongo -p 27017:27017 mongo:latest

# Terminal 2: Start backend
cd backend
source venv/bin/activate
uvicorn app.main:app --reload

# Terminal 3: Start frontend
cd frontend
npm run dev
```

**Access:**
- Frontend: http://localhost:3000
- API Docs: http://localhost:8000/docs

**Demo Flow:**
1. Show registration page
2. Upload a sample resume (have one ready)
3. Show recommendations with explainability
4. Show employer inbox (have test data seeded)

## Backup Plan

If technical issues occur:
1. Use screenshots from `/docs/screenshots/` (if you create them)
2. Describe the functionality verbally
3. Show code snippets from the presentation
4. Direct audience to GitHub repo for later exploration

## Questions & Answers

Common questions and answers are in `speaker-guide.md`. Key points:

**Q: How is this different from LinkedIn?**
A: Explainability, hybrid AI, two-sided focus

**Q: What about security?**
A: JWT auth, bcrypt hashing, input validation

**Q: Can it scale?**
A: Yes - async architecture, horizontal scaling ready

## Contact

**Team 4 - Arizona State University**
- Andre Exilien
- David Nwankwo
- Muhammad Zahid
- Steven Johnson

**Repository:** https://github.com/stevenrhett/asu-group-four

---

**Good luck with your presentation!** 🚀

*Last updated: November 2025*
