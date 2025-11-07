# Job Portal - UX Design Specification

**Project:** asu-group-four  
**Designer:** UX Designer Agent (Sally)  
**Date:** 2025-11-04  
**Version:** 1.0  
**Status:** Draft

---

## Table of Contents
1. [Design Vision & Principles](#design-vision--principles)
2. [Design System Foundation](#design-system-foundation)
3. [User Flows & Journey Maps](#user-flows--journey-maps)
4. [Screen Specifications](#screen-specifications)
5. [Component Library](#component-library)
6. [Interaction Patterns](#interaction-patterns)
7. [Responsive Design Strategy](#responsive-design-strategy)
8. [Accessibility Guidelines](#accessibility-guidelines)

---

## Design Vision & Principles

### Vision Statement
Create a premium, efficient job marketplace experience that combines the professionalism of Apple's design language with futuristic glassmorphic aesthetics. The interface should feel lightweight, transparent, and intelligent while maintaining high productivity and clarity.

### Core Emotional Goals

**Job Seekers:**
- **PRIMARY:** Efficient and productive (zero wasted time on irrelevant jobs)
- **SUPPORTING:** Empowered through transparency, confident in opportunities, delighted by smart discoveries

**Employers:**
- **PRIMARY:** Efficient and productive (rapid, effective candidate review)
- **SUPPORTING:** Confident in hiring decisions, in control of pipeline, relieved by automation

### Design Principles

1. **Clarity Over Cleverness**
   - Every element serves a clear purpose
   - Information hierarchy is immediately apparent
   - No decorative elements that distract from core tasks

2. **Efficiency First**
   - Minimize clicks to complete core actions
   - Smart defaults reduce cognitive load
   - Keyboard shortcuts for power users

3. **Transparent Intelligence**
   - AI recommendations always explained
   - User understands "why" behind every suggestion
   - Build trust through visibility

4. **Premium Aesthetics**
   - Glassmorphic UI with frosted glass effects
   - Subtle animations that feel natural
   - Apple-level attention to detail

5. **Adaptive Experience**
   - Seamless light/dark mode support
   - Desktop-first, mobile-responsive
   - Respects system preferences

---

## Design System Foundation

### Color Palette

#### Light Mode
```css
/* Primary Colors */
--primary-500: #2563eb;        /* Main brand color - vibrant blue */
--primary-600: #1d4ed8;        /* Hover states */
--primary-700: #1e40af;        /* Active states */
--primary-50: #eff6ff;         /* Subtle backgrounds */
--primary-100: #dbeafe;        /* Light accents */

/* Neutral Colors */
--neutral-50: #f9fafb;         /* Page background */
--neutral-100: #f3f4f6;        /* Card backgrounds */
--neutral-200: #e5e7eb;        /* Borders */
--neutral-300: #d1d5db;        /* Disabled states */
--neutral-400: #9ca3af;        /* Placeholder text */
--neutral-500: #6b7280;        /* Secondary text */
--neutral-600: #4b5563;        /* Body text */
--neutral-700: #374151;        /* Headings */
--neutral-800: #1f2937;        /* Strong emphasis */
--neutral-900: #111827;        /* Maximum contrast */

/* Semantic Colors */
--success-500: #10b981;        /* Green for positive actions */
--success-50: #ecfdf5;
--warning-500: #f59e0b;        /* Orange for warnings */
--warning-50: #fffbeb;
--error-500: #ef4444;          /* Red for errors */
--error-50: #fef2f2;
--info-500: #3b82f6;           /* Blue for information */
--info-50: #eff6ff;

/* Glassmorphic Effects */
--glass-bg: rgba(255, 255, 255, 0.7);
--glass-border: rgba(255, 255, 255, 0.18);
--glass-shadow: 0 8px 32px 0 rgba(31, 38, 135, 0.15);
```

#### Dark Mode
```css
/* Primary Colors (brighter in dark mode) */
--primary-400: #60a5fa;        /* Main brand color */
--primary-500: #3b82f6;        /* Hover states */
--primary-600: #2563eb;        /* Active states */
--primary-900: #1e3a8a;        /* Subtle backgrounds */
--primary-800: #1e40af;        /* Light accents */

/* Neutral Colors */
--neutral-900: #0f1117;        /* Page background */
--neutral-800: #1a1d29;        /* Card backgrounds */
--neutral-700: #2d3142;        /* Borders */
--neutral-600: #4a5066;        /* Disabled states */
--neutral-500: #9ca3af;        /* Placeholder text */
--neutral-400: #c4c7d0;        /* Secondary text */
--neutral-300: #d1d5db;        /* Body text */
--neutral-200: #e5e7eb;        /* Headings */
--neutral-100: #f3f4f6;        /* Strong emphasis */
--neutral-50: #f9fafb;         /* Maximum contrast */

/* Semantic Colors (adjusted for dark) */
--success-400: #34d399;
--success-900: #064e3b;
--warning-400: #fbbf24;
--warning-900: #78350f;
--error-400: #f87171;
--error-900: #7f1d1d;
--info-400: #60a5fa;
--info-900: #1e3a8a;

/* Glassmorphic Effects (Dark) */
--glass-bg: rgba(26, 29, 41, 0.6);
--glass-border: rgba(255, 255, 255, 0.1);
--glass-shadow: 0 8px 32px 0 rgba(0, 0, 0, 0.37);
```

### Typography

#### Font Families
```css
/* Primary Font - Clean, modern, Apple-inspired */
--font-primary: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', system-ui, sans-serif;

/* Monospace for code/technical data */
--font-mono: 'JetBrains Mono', 'Fira Code', 'Monaco', 'Courier New', monospace;
```

#### Type Scale
```css
/* Headings */
--text-5xl: 3rem;      /* 48px - Hero headings */
--text-4xl: 2.25rem;   /* 36px - Page titles */
--text-3xl: 1.875rem;  /* 30px - Section headers */
--text-2xl: 1.5rem;    /* 24px - Card titles */
--text-xl: 1.25rem;    /* 20px - Subheadings */
--text-lg: 1.125rem;   /* 18px - Large body */
--text-base: 1rem;     /* 16px - Body text */
--text-sm: 0.875rem;   /* 14px - Small text */
--text-xs: 0.75rem;    /* 12px - Captions */

/* Font Weights */
--font-light: 300;
--font-regular: 400;
--font-medium: 500;
--font-semibold: 600;
--font-bold: 700;

/* Line Heights */
--leading-tight: 1.25;
--leading-normal: 1.5;
--leading-relaxed: 1.75;
```

### Spacing System
```css
/* Consistent 4px base unit */
--space-0: 0;
--space-1: 0.25rem;   /* 4px */
--space-2: 0.5rem;    /* 8px */
--space-3: 0.75rem;   /* 12px */
--space-4: 1rem;      /* 16px */
--space-5: 1.25rem;   /* 20px */
--space-6: 1.5rem;    /* 24px */
--space-8: 2rem;      /* 32px */
--space-10: 2.5rem;   /* 40px */
--space-12: 3rem;     /* 48px */
--space-16: 4rem;     /* 64px */
--space-20: 5rem;     /* 80px */
--space-24: 6rem;     /* 96px */
```

### Border Radius
```css
--radius-sm: 0.375rem;   /* 6px - Subtle rounding */
--radius-md: 0.5rem;     /* 8px - Default */
--radius-lg: 0.75rem;    /* 12px - Cards */
--radius-xl: 1rem;       /* 16px - Modals */
--radius-2xl: 1.5rem;    /* 24px - Hero elements */
--radius-full: 9999px;   /* Pill shapes */
```

### Shadows & Elevation
```css
/* Light Mode Shadows */
--shadow-sm: 0 1px 2px 0 rgba(0, 0, 0, 0.05);
--shadow-md: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
--shadow-lg: 0 10px 15px -3px rgba(0, 0, 0, 0.1);
--shadow-xl: 0 20px 25px -5px rgba(0, 0, 0, 0.1);
--shadow-2xl: 0 25px 50px -12px rgba(0, 0, 0, 0.25);

/* Dark Mode Shadows */
--shadow-sm-dark: 0 1px 2px 0 rgba(0, 0, 0, 0.3);
--shadow-md-dark: 0 4px 6px -1px rgba(0, 0, 0, 0.4);
--shadow-lg-dark: 0 10px 15px -3px rgba(0, 0, 0, 0.5);
--shadow-xl-dark: 0 20px 25px -5px rgba(0, 0, 0, 0.6);
--shadow-2xl-dark: 0 25px 50px -12px rgba(0, 0, 0, 0.7);

/* Glassmorphic Glow (Dark Mode) */
--glow-primary: 0 0 20px rgba(96, 165, 250, 0.3);
--glow-success: 0 0 20px rgba(52, 211, 153, 0.3);
```

### Animation & Transitions
```css
/* Duration */
--duration-fast: 150ms;
--duration-normal: 200ms;
--duration-slow: 300ms;
--duration-slower: 500ms;

/* Easing Functions */
--ease-in: cubic-bezier(0.4, 0, 1, 1);
--ease-out: cubic-bezier(0, 0, 0.2, 1);
--ease-in-out: cubic-bezier(0.4, 0, 0.2, 1);
--ease-spring: cubic-bezier(0.68, -0.55, 0.265, 1.55);

/* Common Transitions */
--transition-colors: color var(--duration-normal) var(--ease-out),
                     background-color var(--duration-normal) var(--ease-out),
                     border-color var(--duration-normal) var(--ease-out);
--transition-transform: transform var(--duration-normal) var(--ease-out);
--transition-all: all var(--duration-normal) var(--ease-out);
```

---

## User Flows & Journey Maps

### Job Seeker Journey

#### 1. Initial Onboarding Flow
```
Landing Page → Sign Up → Role Selection (Seeker) → 
Resume Upload → Profile Completion → Dashboard (First Recommendations)
```

**Key Touchpoints:**
1. **Landing Page** - Clear value proposition, prominent CTA
2. **Sign Up** - Minimal fields, social auth options
3. **Role Selection** - Clear visual choice between Seeker/Employer
4. **Resume Upload** - Drag-and-drop, instant parsing feedback
5. **Profile Completion** - Smart defaults from resume, optional enrichment
6. **Dashboard** - Immediate value with 5-10 personalized job recommendations

**Success Metrics:**
- Time to first recommendation: < 2 minutes
- Profile completion rate: > 80%
- First-session apply rate: > 15%

#### 2. Job Discovery & Application Flow
```
Dashboard → Browse Recommendations → Job Detail → 
One-Click Apply → Confirmation → Application Tracking
```

**Key Interactions:**
- **Recommendation Card**: Job title, company, location, salary, "Why recommended" badge
- **Quick Actions**: Save for later, not interested (improves future recommendations)
- **Job Detail**: Full description, requirements, explainability panel, apply button
- **One-Click Apply**: Auto-fill from profile, optional cover letter, instant submission
- **Status Tracking**: Real-time updates, email notifications

#### 3. Ongoing Engagement Loop
```
Email Notification → Return to Platform → New Recommendations → 
Review Application Status → Repeat
```

### Employer Journey

#### 1. Initial Onboarding Flow
```
Landing Page → Sign Up → Role Selection (Employer) → 
Company Profile → Post First Job → Smart Inbox Setup
```

**Key Touchpoints:**
1. **Landing Page** - Value proposition for hiring efficiency
2. **Sign Up** - Quick process, verify company email
3. **Company Profile** - Logo, description, culture details
4. **Post First Job** - Guided flow with smart templates
5. **Smart Inbox Setup** - Introduction to candidate triage features

#### 2. Job Posting Flow
```
Dashboard → Create Job Posting → Fill Details → 
Review → Publish → Activate Smart Inbox
```

**Key Interactions:**
- **Smart Templates**: Pre-filled job descriptions based on role
- **Skills Autocomplete**: Suggest relevant skills as you type
- **Salary Guidance**: Market data for transparency
- **Preview Mode**: See how job appears to seekers

#### 3. Candidate Review Flow
```
Smart Inbox → Filter/Sort Candidates → Review Candidate → 
Shortlist → Schedule Interview → Send Notification
```

**Key Features:**
- **Triage View**: Quick yes/no/maybe with keyboard shortcuts
- **Match Score**: AI-powered relevance with explanation
- **Bulk Actions**: Shortlist multiple, send batch updates
- **Calendar Integration**: ICS export for interview scheduling

---

## Screen Specifications

### 1. Authentication Screens

#### 1.1 Login Screen

**Layout:**
```
┌─────────────────────────────────────────────┐
│                                             │
│              [Logo]                         │
│                                             │
│         Welcome Back                        │
│     Sign in to your account                 │
│                                             │
│   ┌───────────────────────────────────┐    │
│   │ Email                             │    │
│   └───────────────────────────────────┘    │
│                                             │
│   ┌───────────────────────────────────┐    │
│   │ Password                   [👁]    │    │
│   └───────────────────────────────────┘    │
│                                             │
│   [x] Remember me      Forgot password?    │
│                                             │
│   ┌───────────────────────────────────┐    │
│   │        Sign In                    │    │
│   └───────────────────────────────────┘    │
│                                             │
│         ─── or continue with ───           │
│                                             │
│   [Google] [LinkedIn] [GitHub]             │
│                                             │
│   Don't have an account? Sign up           │
│                                             │
└─────────────────────────────────────────────┘
```

**Design Details:**
- **Background**: Subtle gradient with glassmorphic card overlay
- **Card**: Frosted glass effect (`backdrop-filter: blur(10px)`)
- **Inputs**: Clean, spacious, with floating labels
- **Primary Button**: Full-width, prominent, with hover lift effect
- **Social Auth**: Icon buttons in a row, equal spacing
- **Mobile**: Full-screen with adjusted spacing

**Interactions:**
- Email validation on blur
- Password show/hide toggle
- Enter key submits form
- Loading state on button during auth
- Error messages below relevant fields

#### 1.2 Sign Up Screen

**Additional Elements:**
- Role selection (Job Seeker / Employer) as prominent toggle
- Terms & conditions checkbox
- Password strength indicator
- Progressive disclosure for additional fields

---

### 2. Job Seeker Screens

#### 2.1 Resume Upload & Onboarding

**Layout:**
```
┌─────────────────────────────────────────────┐
│  [Progress: 1/3] Upload Resume              │
├─────────────────────────────────────────────┤
│                                             │
│        Let's get you started!               │
│   Upload your resume to get personalized    │
│         job recommendations                 │
│                                             │
│   ┌───────────────────────────────────┐    │
│   │                                   │    │
│   │         📄                        │    │
│   │                                   │    │
│   │   Drag & drop your resume here    │    │
│   │      or click to browse           │    │
│   │                                   │    │
│   │  Supported: PDF, DOCX (max 5MB)   │    │
│   │                                   │    │
│   └───────────────────────────────────┘    │
│                                             │
│   [Skip for now]          [Continue]        │
│                                             │
└─────────────────────────────────────────────┘
```

**Upload States:**
1. **Idle**: Dashed border, upload icon, instructional text
2. **Hover**: Border highlights, slight scale
3. **Uploading**: Progress bar, percentage, cancel option
4. **Processing**: Spinner, "Parsing your resume..." message
5. **Success**: Checkmark, preview of extracted data
6. **Error**: Red border, clear error message, retry option

**Extracted Data Preview:**
```
┌─────────────────────────────────────────────┐
│  [Progress: 2/3] Confirm Your Profile       │
├─────────────────────────────────────────────┤
│                                             │
│   Great! Here's what we found:              │
│                                             │
│   Name: [John Doe]              ✏️         │
│   Email: [john@example.com]     ✏️         │
│   Phone: [+1-555-0123]          ✏️         │
│                                             │
│   Skills (5):                               │
│   [Python] [React] [AWS] [SQL] [Docker]     │
│   + Add more                                │
│                                             │
│   Experience:                               │
│   • Senior Developer at TechCorp (3 years)  │
│   • Developer at StartupXYZ (2 years)       │
│                                             │
│   [Back]                    [Looks good!]   │
│                                             │
└─────────────────────────────────────────────┘
```

**Design Details:**
- Inline editing for all fields
- Skill tags with remove option
- Add missing skills with autocomplete
- Experience timeline visualization
- Smooth transitions between steps

#### 2.2 Job Seeker Dashboard

**Layout (Desktop):**
```
┌─────────────────────────────────────────────────────────────┐
│ [Logo]  Dashboard  Jobs  Applications  Profile    [🔔] [@]  │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  Welcome back, John! 👋                                     │
│  You have 12 new job recommendations                        │
│                                                             │
│  ┌─────────────────────────┐  Filters:                     │
│  │ 🎯 Recommended for You  │  [All] [Remote] [Hybrid]      │
│  └─────────────────────────┘  [Full-time] [Part-time]      │
│                                                             │
│  ┌────────────────────┐  ┌────────────────────┐            │
│  │ Senior Developer   │  │ Frontend Lead      │   ┌──...   │
│  │ TechCorp          │  │ StartupXYZ        │   │         │
│  │ San Francisco, CA │  │ Remote            │   │         │
│  │ $120k - $160k     │  │ $130k - $180k     │   │         │
│  │                   │  │                   │   │         │
│  │ 💡 Why recommended:│  │ 💡 Why recommended:│   │         │
│  │ Matches: Python,   │  │ Matches: React,    │   │         │
│  │ AWS, 5+ years exp │  │ Leadership exp    │   │         │
│  │                   │  │                   │   │         │
│  │ [💾] [👎] [Apply] │  │ [💾] [👎] [Apply] │   │         │
│  └────────────────────┘  └────────────────────┘   └──...   │
│                                                             │
│  [Load more recommendations]                                │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

**Job Card Components:**
1. **Header Section**
   - Job title (bold, prominent)
   - Company logo (if available)
   - Company name

2. **Details Section**
   - Location with icon
   - Salary range (transparent)
   - Employment type badge
   - Posted time (relative, e.g., "2 days ago")

3. **Explainability Panel**
   - "Why recommended" heading with lightbulb icon
   - Top 3 matching factors
   - Subtle background highlight
   - Tooltip with full explanation on hover

4. **Action Bar**
   - Save for later (bookmark icon)
   - Not interested (thumbs down)
   - Apply button (primary CTA)

**Glassmorphic Card Style:**
```css
.job-card {
  background: var(--glass-bg);
  backdrop-filter: blur(10px);
  border: 1px solid var(--glass-border);
  border-radius: var(--radius-lg);
  box-shadow: var(--shadow-md);
  padding: var(--space-6);
  transition: var(--transition-transform);
}

.job-card:hover {
  transform: translateY(-4px);
  box-shadow: var(--shadow-xl);
}
```

**Interactions:**
- Hover effect: Card lifts slightly
- Click card: Opens job detail modal/page
- Click "Not interested": Card fades out, shows undo option
- Click "Save": Bookmark fills, added to "Saved Jobs"
- Click "Apply": Opens application flow

#### 2.3 Job Detail View

**Layout:**
```
┌─────────────────────────────────────────────────────────────┐
│ ← Back to Jobs                                    [💾] [❌]  │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  Senior Full Stack Developer                                │
│  TechCorp  •  San Francisco, CA (Hybrid)                   │
│  Posted 2 days ago  •  15 applicants                       │
│                                                             │
│  ┌─────────────────────────────────────────────────────┐   │
│  │ 💡 Why this job matches you                         │   │
│  │                                                     │   │
│  │ • Your skills match 8/10 requirements (80%)        │   │
│  │ • You have 5+ years experience in similar roles    │   │
│  │ • Your Python and AWS expertise are key needs      │   │
│  │ • Salary aligns with your profile ($120k-$160k)    │   │
│  └─────────────────────────────────────────────────────┘   │
│                                                             │
│  ┌───────────────────────────────────────────────────┐     │
│  │                 [Apply Now]                       │     │
│  └───────────────────────────────────────────────────┘     │
│                                                             │
│  Job Description                                            │
│  ────────────────                                          │
│  We're seeking a talented Full Stack Developer...          │
│  [Full description text]                                    │
│                                                             │
│  Requirements                                               │
│  ────────────                                              │
│  ✓ 5+ years of software development experience             │
│  ✓ Strong proficiency in Python and JavaScript             │
│  ✓ Experience with AWS cloud services                      │
│  ○ Bachelor's degree in Computer Science (Preferred)       │
│                                                             │
│  About TechCorp                                             │
│  ────────────                                              │
│  [Company description]                                      │
│                                                             │
│  Benefits                                                   │
│  ────────────                                              │
│  • Health, dental, vision insurance                         │
│  • 401(k) matching                                          │
│  • Flexible work arrangements                               │
│  • Professional development budget                          │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

**Design Details:**
- Sticky header with action buttons
- Prominent "Why this matches" panel at top
- Requirements checklist with visual indicators (✓ you have, ○ nice-to-have)
- Rich text formatting for job description
- Fixed "Apply Now" button visible on scroll

**One-Click Apply Modal:**
```
┌─────────────────────────────────────────┐
│  Apply to Senior Full Stack Developer  │
│                                         │
│  Your profile will be submitted:        │
│  ✓ Resume: john-doe-resume.pdf          │
│  ✓ Experience: 5 years                  │
│  ✓ Skills: Python, React, AWS...        │
│                                         │
│  Cover Letter (Optional)                │
│  ┌─────────────────────────────────┐   │
│  │                                 │   │
│  │                                 │   │
│  │                                 │   │
│  └─────────────────────────────────┘   │
│                                         │
│  [Cancel]            [Submit Application]│
│                                         │
└─────────────────────────────────────────┘
```

#### 2.4 Application Tracking

**Layout:**
```
┌─────────────────────────────────────────────────────────────┐
│  My Applications (8)                    [All ▼] [Search 🔍] │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  Status: [All] [Pending] [Under Review] [Interview]        │
│          [Rejected] [Offered]                              │
│                                                             │
│  ┌─────────────────────────────────────────────────────┐   │
│  │ Senior Developer  •  TechCorp                       │   │
│  │ Applied 2 days ago                                  │   │
│  │ ●●●○○  Under Review                                │   │
│  │ "Your application is being reviewed by the team"    │   │
│  └─────────────────────────────────────────────────────┘   │
│                                                             │
│  ┌─────────────────────────────────────────────────────┐   │
│  │ Frontend Lead  •  StartupXYZ                        │   │
│  │ Applied 5 days ago                                  │   │
│  │ ●●●●○  Interview Scheduled                         │   │
│  │ "Interview: Nov 8, 2pm PST  [Add to Calendar]"     │   │
│  └─────────────────────────────────────────────────────┘   │
│                                                             │
│  ┌─────────────────────────────────────────────────────┐   │
│  │ Backend Engineer  •  DataCo                         │   │
│  │ Applied 1 week ago                                  │   │
│  │ ●●●●●  Offer Received! 🎉                          │   │
│  │ "Congratulations! Review your offer details"        │   │
│  └─────────────────────────────────────────────────────┘   │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

**Status Pipeline:**
1. Applied (●○○○○)
2. Under Review (●●○○○)
3. Interview Scheduled (●●●○○)
4. Final Review (●●●●○)
5. Offer/Rejection (●●●●●)

**Design Details:**
- Visual progress indicator for each application
- Color-coded status (blue=in-progress, green=offer, red=rejected)
- Expandable cards for more details
- Calendar integration for interviews
- Email notification badges

---

### 3. Employer Screens

#### 3.1 Employer Dashboard

**Layout:**
```
┌─────────────────────────────────────────────────────────────┐
│ [Logo]  Dashboard  Jobs  Candidates  Analytics    [🔔] [@]  │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  Welcome back, Sarah! 👋                                    │
│  You have 23 new applications across 3 active jobs          │
│                                                             │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐     │
│  │   Active     │  │    Total     │  │  Interviews  │     │
│  │    Jobs      │  │ Applications │  │  Scheduled   │     │
│  │      3       │  │     127      │  │      5       │     │
│  └──────────────┘  └──────────────┘  └──────────────┘     │
│                                                             │
│  Active Job Postings                    [+ Post New Job]   │
│  ────────────────────                                      │
│                                                             │
│  ┌─────────────────────────────────────────────────────┐   │
│  │ Senior Developer  •  Posted 3 days ago              │   │
│  │ 45 applications  •  8 shortlisted  •  2 interviewed │   │
│  │ [View Applications →]                               │   │
│  └─────────────────────────────────────────────────────┘   │
│                                                             │
│  ┌─────────────────────────────────────────────────────┐   │
│  │ Product Manager  •  Posted 1 week ago               │   │
│  │ 67 applications  •  12 shortlisted  •  3 interviewed│   │
│  │ [View Applications →]                               │   │
│  └─────────────────────────────────────────────────────┘   │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

#### 3.2 Job Posting Creation

**Layout (Multi-Step Form):**
```
┌─────────────────────────────────────────────────────────────┐
│  Create Job Posting                            [Save Draft] │
│  ●●○○  Step 2 of 4: Job Details                            │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  Basic Information                                          │
│  ──────────────────                                        │
│                                                             │
│  Job Title *                                                │
│  ┌─────────────────────────────────────────────────────┐   │
│  │ Senior Full Stack Developer                         │   │
│  └─────────────────────────────────────────────────────┘   │
│                                                             │
│  Department                  Location                       │
│  ┌─────────────────────┐    ┌───────────────────────┐     │
│  │ Engineering        ▼│    │ San Francisco, CA    ▼│     │
│  └─────────────────────┘    └───────────────────────┘     │
│                                                             │
│  Employment Type              Work Arrangement              │
│  ○ Full-time  ○ Part-time    ○ Remote  ● Hybrid  ○ On-site│
│  ○ Contract   ○ Internship                                 │
│                                                             │
│  Salary Range *                                             │
│  ┌───────────────┐  to  ┌───────────────┐  per year      │
│  │ $120,000      │      │ $160,000      │                 │
│  └───────────────┘      └───────────────┘                 │
│  💡 Market average: $135k - $155k for this role            │
│                                                             │
│  [← Previous]                           [Continue →]        │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

**Form Steps:**
1. **Basic Info** - Title, department, location, type
2. **Job Details** - Description, responsibilities, requirements
3. **Skills & Qualifications** - Required/preferred skills
4. **Review & Publish** - Preview, edit, publish

**Design Features:**
- Auto-save drafts every 30 seconds
- Smart suggestions as you type
- Market data for salary guidance
- Rich text editor for description
- Skills autocomplete with suggestions
- Preview mode shows candidate view

#### 3.3 Smart Inbox / Candidate Pipeline

**Layout:**
```
┌─────────────────────────────────────────────────────────────┐
│  Senior Developer Applications (45)          [Filters ▼]    │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  Pipeline: [New (23)] [Reviewed (14)] [Shortlisted (8)]    │
│            [Interviewed (2)] [Offered (1)] [Rejected (5)]   │
│                                                             │
│  Sort: [Best Match ▼]  Filters: [All Skills] [Any Location]│
│                                                             │
│  ┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓   │
│  ┃ ⭐ John Doe                                96% Match ┃   │
│  ┃ Senior Developer • 5 years exp                      ┃   │
│  ┃ San Francisco, CA • Applied 2 hours ago             ┃   │
│  ┃                                                      ┃   │
│  ┃ 💡 Top Match Because:                               ┃   │
│  ┃ • Has all 10 required skills (Python, AWS, React...) ┃   │
│  ┃ • 5+ years experience in similar roles               ┃   │
│  ┃ • Currently in target location                       ┃   │
│  ┃                                                      ┃   │
│  ┃ Key Skills: Python •  AWS • React • Docker • SQL    ┃   │
│  ┃                                                      ┃   │
│  ┃ [View Profile] [Shortlist] [Schedule Interview] [✕] ┃   │
│  ┗━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┛   │
│                                                             │
│  ┌─────────────────────────────────────────────────────┐   │
│  │ ⭐ Jane Smith                           88% Match   │   │
│  │ Full Stack Developer • 4 years exp                  │   │
│  │ Oakland, CA • Applied 5 hours ago                   │   │
│  │                                                     │   │
│  │ 💡 Strong Match Because:                            │   │
│  │ • Has 8/10 required skills                          │   │
│  │ • 4+ years relevant experience                      │   │
│  │ • Willing to relocate                               │   │
│  │                                                     │   │
│  │ Key Skills: Python • React • Node.js • PostgreSQL   │   │
│  │                                                     │   │
│  │ [View Profile] [Shortlist] [Schedule Interview] [✕] │   │
│  └─────────────────────────────────────────────────────┘   │
│                                                             │
│  [Select Multiple]  Bulk Actions: [Shortlist] [Reject]     │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

**Design Features:**
- **Match Score**: Prominent percentage with explanation
- **Visual Hierarchy**: Top matches highlighted with star/border
- **Quick Actions**: Inline buttons for common operations
- **Keyboard Shortcuts**: 
  - `j/k` - Navigate candidates
  - `s` - Shortlist
  - `r` - Reject
  - `v` - View full profile
  - `i` - Schedule interview
- **Bulk Operations**: Select multiple, apply actions
- **Filters & Sort**: Powerful filtering (skills, location, experience)
- **Pipeline Stages**: Drag-and-drop between stages (optional)

#### 3.4 Candidate Detail View

**Layout:**
```
┌─────────────────────────────────────────────────────────────┐
│ ← Back to Inbox                                             │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  John Doe                                      96% Match    │
│  Senior Developer • 5 years experience                      │
│  San Francisco, CA • john.doe@email.com                    │
│                                                             │
│  ┌─────────────────────────────────────────────────────┐   │
│  │ 💡 Why this candidate matches (96%)                 │   │
│  │                                                     │   │
│  │ Strengths:                                          │   │
│  │ ✓ Has all 10 required skills                        │   │
│  │ ✓ 5+ years in Python, AWS, React                    │   │
│  │ ✓ Led teams of 3-5 developers                       │   │
│  │ ✓ Currently in San Francisco (no relocation)        │   │
│  │                                                     │   │
│  │ Considerations:                                     │   │
│  │ • No GraphQL experience (nice-to-have)              │   │
│  └─────────────────────────────────────────────────────┘   │
│                                                             │
│  [Shortlist]  [Schedule Interview]  [Send Message]  [Reject]│
│                                                             │
│  ┌─────────────────────────────────────────────────────┐   │
│  │ Resume  |  Cover Letter  |  Portfolio  |  Notes    │   │
│  ├─────────────────────────────────────────────────────┤   │
│  │                                                     │   │
│  │ [Resume preview / download]                         │   │
│  │                                                     │   │
│  └─────────────────────────────────────────────────────┘   │
│                                                             │
│  Experience                                                 │
│  ──────────                                                │
│  Senior Developer @ TechCorp                  2020 - Present│
│  • Led team of 5 developers on cloud migration             │
│  • Built scalable APIs serving 1M+ requests/day            │
│  • Reduced infrastructure costs by 40%                      │
│                                                             │
│  Developer @ StartupXYZ                       2018 - 2020  │
│  • Full-stack development with React and Python             │
│  • Implemented real-time features using WebSockets          │
│                                                             │
│  Skills                                                     │
│  ──────                                                    │
│  ✓ Python (Expert)      ✓ AWS (Advanced)                  │
│  ✓ React (Advanced)     ✓ Docker (Intermediate)           │
│  ✓ SQL (Advanced)       ○ GraphQL (None listed)           │
│                                                             │
│  Education                                                  │
│  ─────────                                                 │
│  BS Computer Science, Stanford University (2018)            │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

**Interview Scheduling Modal:**
```
┌─────────────────────────────────────────┐
│  Schedule Interview with John Doe       │
│                                         │
│  Interview Type                         │
│  ● Phone Screen  ○ Technical  ○ Final   │
│                                         │
│  Date & Time                            │
│  ┌─────────────┐  ┌─────────────┐      │
│  │ Nov 8, 2025▼│  │ 2:00 PM    ▼│      │
│  └─────────────┘  └─────────────┘      │
│                                         │
│  Duration: [1 hour ▼]                   │
│                                         │
│  Interviewers                           │
│  [x] Sarah Chen (You)                   │
│  [ ] Mike Johnson (Tech Lead)           │
│  [ ] Amy Liu (Engineering Manager)      │
│                                         │
│  Meeting Link                           │
│  ○ Generate Zoom link                   │
│  ○ Use existing: [paste link]           │
│                                         │
│  Notes (Optional)                       │
│  ┌─────────────────────────────────┐   │
│  │ Prepare questions about AWS exp │   │
│  └─────────────────────────────────┘   │
│                                         │
│  [ ] Send calendar invite (.ics)        │
│  [x] Send email notification            │
│                                         │
│  [Cancel]           [Schedule Interview]│
│                                         │
└─────────────────────────────────────────┘
```

---

## Component Library

### Core Components

#### 1. Buttons

**Primary Button**
```jsx
<button class="btn btn-primary">
  Apply Now
</button>
```

**Variants:**
- `btn-primary` - Main actions (Apply, Submit, Save)
- `btn-secondary` - Secondary actions (Cancel, Go Back)
- `btn-ghost` - Tertiary actions (Skip, Learn More)
- `btn-danger` - Destructive actions (Delete, Reject)

**Sizes:**
- `btn-sm` - 32px height
- `btn-md` - 40px height (default)
- `btn-lg` - 48px height

**States:**
- Default
- Hover (lift + subtle glow in dark mode)
- Active (slight inset)
- Disabled (reduced opacity, no interaction)
- Loading (spinner, disabled interaction)

#### 2. Input Fields

**Text Input**
```jsx
<div class="input-group">
  <label for="email">Email</label>
  <input 
    type="email" 
    id="email" 
    class="input" 
    placeholder="you@example.com"
  />
</div>
```

**Variants:**
- Text, Email, Password, Number, URL
- Textarea (multiline)
- Select (dropdown)
- Date, Time pickers

**States:**
- Default
- Focus (border highlight, subtle glow)
- Error (red border, error message below)
- Disabled
- Success (green border, checkmark)

#### 3. Cards

**Job Card**
```jsx
<div class="card card-glass card-hover">
  <div class="card-header">
    <h3>Senior Developer</h3>
    <span class="badge">Remote</span>
  </div>
  <div class="card-body">
    <!-- Content -->
  </div>
  <div class="card-footer">
    <!-- Actions -->
  </div>
</div>
```

**Variants:**
- `card-glass` - Glassmorphic effect
- `card-elevated` - Stronger shadow
- `card-hover` - Lift on hover
- `card-bordered` - Solid border instead of shadow

#### 4. Badges & Tags

**Usage:**
```jsx
<span class="badge badge-primary">Full-time</span>
<span class="badge badge-success">Remote</span>
<span class="tag">Python</span>
```

**Types:**
- Status badges (primary, success, warning, error)
- Skill tags (removable, clickable)
- Count badges (notification counts)

#### 5. Modal / Dialog

**Structure:**
```jsx
<div class="modal-overlay" aria-modal="true">
  <div class="modal modal-glass">
    <div class="modal-header">
      <h2>Modal Title</h2>
      <button class="modal-close">&times;</button>
    </div>
    <div class="modal-body">
      <!-- Content -->
    </div>
    <div class="modal-footer">
      <button class="btn btn-secondary">Cancel</button>
      <button class="btn btn-primary">Confirm</button>
    </div>
  </div>
</div>
```

**Sizes:**
- `modal-sm` - 400px max width
- `modal-md` - 600px max width (default)
- `modal-lg` - 800px max width
- `modal-xl` - 1000px max width

#### 6. Navigation

**Top Navigation Bar**
```jsx
<nav class="navbar navbar-glass">
  <div class="navbar-brand">
    <img src="logo.svg" alt="Logo" />
  </div>
  <div class="navbar-menu">
    <a href="/dashboard" class="nav-link active">Dashboard</a>
    <a href="/jobs" class="nav-link">Jobs</a>
    <a href="/applications" class="nav-link">Applications</a>
  </div>
  <div class="navbar-actions">
    <button class="btn-icon"><NotificationIcon /></button>
    <button class="btn-icon"><ProfileIcon /></button>
  </div>
</nav>
```

**Features:**
- Fixed/sticky positioning
- Glassmorphic background
- Active state indication
- Mobile hamburger menu
- Notification badges

#### 7. Progress Indicators

**Linear Progress**
```jsx
<div class="progress-bar">
  <div class="progress-fill" style="width: 60%"></div>
</div>
```

**Step Progress**
```jsx
<div class="steps">
  <div class="step step-complete">1</div>
  <div class="step step-active">2</div>
  <div class="step">3</div>
</div>
```

**Loading Spinner**
```jsx
<div class="spinner"></div>
```

---

## Interaction Patterns

### 1. Micro-interactions

**Button Feedback**
- Hover: Lift 2px, add subtle shadow
- Active: Inset 1px
- Success: Checkmark animation, brief green flash
- Error: Shake animation, red flash

**Card Interactions**
- Hover: Lift 4px, enhance shadow
- Click: Slight scale down, then navigate
- Save/Unsave: Heart fill animation
- Dismiss: Swipe gesture (mobile), fade out

**Form Validation**
- Real-time: Validate on blur
- Success: Green checkmark appears
- Error: Red border, shake, error text
- Password strength: Animated bar

### 2. Page Transitions

**Route Changes**
- Fade out current page (150ms)
- Fade in new page (200ms)
- Maintain scroll position for back navigation

**Modal Animations**
- Overlay: Fade in (200ms)
- Modal: Fade + scale up (300ms ease-out)
- Close: Reverse animation

### 3. Loading States

**Skeleton Screens**
- Show content structure while loading
- Pulsing animation on placeholders
- Prevents layout shift

**Progressive Loading**
- Load above-the-fold content first
- Lazy load images and heavy content
- Show placeholders for pending data

**Empty States**
- Friendly illustration
- Clear message: "No applications yet"
- Actionable CTA: "Browse recommended jobs"

### 4. Notifications & Feedback

**Toast Notifications**
- Slide in from top-right
- Auto-dismiss after 5 seconds
- Manual dismiss option
- Stack multiple toasts

**Inline Feedback**
- Success messages near action
- Error messages contextual to field
- Warning banners for important info

---

## Responsive Design Strategy

### Breakpoints
```css
/* Mobile */
@media (max-width: 640px) { /* sm */ }

/* Tablet */
@media (min-width: 641px) and (max-width: 1024px) { /* md */ }

/* Desktop */
@media (min-width: 1025px) { /* lg */ }

/* Large Desktop */
@media (min-width: 1280px) { /* xl */ }
```

### Mobile Adaptations

**Navigation**
- Desktop: Horizontal nav bar
- Mobile: Hamburger menu, slide-in drawer

**Job Cards**
- Desktop: 2-3 column grid
- Tablet: 2 column grid
- Mobile: Single column, full width

**Forms**
- Desktop: Multi-column layouts
- Mobile: Single column, full width inputs

**Modals**
- Desktop: Centered with max-width
- Mobile: Full-screen overlay

**Tables (Candidate List)**
- Desktop: Full table
- Mobile: Card-based layout with key info

### Touch Interactions
- Minimum touch target: 44x44px
- Swipe gestures for dismissing cards
- Pull-to-refresh on lists
- Bottom sheet for mobile actions

---

## Accessibility Guidelines

### WCAG 2.1 AA Compliance

**Color Contrast**
- Text: Minimum 4.5:1 ratio
- Large text (18pt+): Minimum 3:1 ratio
- UI components: Minimum 3:1 ratio

**Keyboard Navigation**
- All interactive elements focusable
- Logical tab order
- Visible focus indicators
- Skip links for main content

**Screen Readers**
- Semantic HTML (headings, landmarks)
- Alt text for all images
- ARIA labels for icon-only buttons
- Live regions for dynamic content

**Forms**
- Associated labels for all inputs
- Error messages programmatically linked
- Required fields indicated
- Input purpose autocomplete attributes

**Motion & Animation**
- Respect `prefers-reduced-motion`
- Disable animations if user prefers
- No auto-playing videos/carousels

### Testing Checklist
- [ ] Keyboard-only navigation works
- [ ] Screen reader announces all content
- [ ] Color contrast meets AA standards
- [ ] Forms are fully accessible
- [ ] Focus indicators visible
- [ ] ARIA attributes correct
- [ ] Page titles descriptive
- [ ] Headings properly nested

---

## Implementation Notes

### Technology Stack Alignment

**Frontend (Next.js 14 + TypeScript)**
- Use Next.js App Router for page structure
- Implement components with TypeScript for type safety
- Use Tailwind CSS for styling (matches design system)
- Consider Radix UI or Headless UI for accessible primitives

**Glassmorphic Effects**
```css
/* Base glassmorphic card */
.glass {
  background: rgba(255, 255, 255, 0.7);
  backdrop-filter: blur(10px) saturate(180%);
  border: 1px solid rgba(255, 255, 255, 0.18);
  box-shadow: 0 8px 32px 0 rgba(31, 38, 135, 0.15);
}

/* Dark mode */
.dark .glass {
  background: rgba(26, 29, 41, 0.6);
  border: 1px solid rgba(255, 255, 255, 0.1);
  box-shadow: 0 8px 32px 0 rgba(0, 0, 0, 0.37);
}
```

**Theme Implementation**
- Use CSS variables for all colors
- `prefers-color-scheme` media query for default
- Local storage to persist user preference
- Toggle component in navigation

**Performance Optimization**
- Lazy load images with Next.js Image component
- Code split routes automatically with App Router
- Optimize glassmorphic effects (use will-change for animations)
- Consider reducing blur values on mobile for performance

### Design-to-Development Handoff

**Assets Needed:**
- Logo (SVG format, light/dark variants)
- Icons (use Heroicons or Lucide for consistency)
- Illustration for empty states
- Favicon and app icons

**Component Priority:**
1. Design system foundations (colors, typography, spacing)
2. Core components (buttons, inputs, cards)
3. Navigation and layout
4. Authentication screens
5. Dashboard and job cards
6. Application flows
7. Employer screens

**Design System Documentation:**
- Storybook or similar for component showcase
- Interactive examples of each component
- Code snippets for developers
- Accessibility notes for each component

---

## Next Steps

### 1. Design Review & Feedback
- Review this specification with stakeholders
- Gather feedback on visual direction
- Validate user flows with target users
- Prioritize any changes or additions

### 2. High-Fidelity Mockups (Optional)
- Create pixel-perfect designs in Figma
- Design key screens in both light/dark modes
- Create interactive prototype for user testing
- Include mobile responsive variants

### 3. Design System Setup
- Create Tailwind config with custom theme
- Build core component library
- Set up Storybook for documentation
- Establish naming conventions

### 4. Iterative Development
- Build and test components in isolation
- Implement screens incrementally
- Conduct accessibility audits
- Gather user feedback and iterate

---

## Appendix

### Inspiration References

**Job Platforms:**
- LinkedIn - Professional, clean interface
- Wellfound (AngelList) - Transparent, modern design
- Greenhouse - Enterprise ATS, clean pipelines

**Design Inspiration:**
- Apple.com - Premium aesthetics, attention to detail
- Stripe - Clean, professional, developer-friendly
- Linear - Keyboard shortcuts, efficiency focus

**Glassmorphic Examples:**
- macOS Big Sur - System UI elements
- iOS Control Center - Frosted glass effects
- Windows 11 Acrylic - Modern transparency

### Design Tools & Resources

**Prototyping:**
- Figma (recommended)
- Adobe XD
- Sketch

**Icons:**
- Heroicons (Tailwind official)
- Lucide Icons
- Feather Icons

**Fonts:**
- Inter (Google Fonts) - Free, similar to SF Pro
- SF Pro (Apple) - Requires license for web
- Manrope - Alternative geometric sans

**Color Tools:**
- Coolors.co - Palette generator
- Contrast Checker - WCAG compliance
- Tailwind Color Palette - Reference

---

**Document Status:** Ready for Review  
**Last Updated:** 2025-11-04  
**Next Review:** After stakeholder feedback

