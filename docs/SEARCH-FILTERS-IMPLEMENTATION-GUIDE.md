# 🔍 Job Search & Filters - Implementation Guide

**Story**: ST-018  
**Sprint**: Sprint 3  
**Duration**: 4-5 days  
**Status**: Ready to implement

---

## 🎯 What We're Building

A Glassdoor-style job search interface with comprehensive filters, exactly like shown in your screenshots:

- **Search bar** with job title + location
- **Filter sidebar** with 12+ filter types
- **Active filters** display with remove chips
- **Real-time results** with pagination
- **URL persistence** for shareable searches

---

## 📋 Implementation Checklist

### ✅ Phase 1: Backend Setup (Day 1)

**Step 1.1: Update Job Model**
```bash
File: backend/app/models/job.py
```
- [ ] Add `work_type` enum (remote, hybrid, onsite)
- [ ] Add `job_type` enum (full_time, part_time, contract, internship)
- [ ] Add `experience_level` enum (entry, mid, senior, lead)
- [ ] Add salary fields (`salary_min`, `salary_max`, `salary_currency`)
- [ ] Add company fields (`company_name`, `company_rating`, `company_size`)
- [ ] Add location fields (`city`, `state`, `country`, `latitude`, `longitude`)
- [ ] Add `easy_apply` boolean flag
- [ ] Add `posted_at` datetime field
- [ ] Add database indexes for performance

**Step 1.2: Create Search API**
```bash
File: backend/app/api/v1/routes/search.py
```
- [ ] Create `/api/v1/jobs/search` GET endpoint
- [ ] Support query parameters:
  - `q` (keywords), `location` (city), `radius` (miles)
  - `easy_apply`, `remote_only` (booleans)
  - `salary_min`, `salary_max` (integers)
  - `posted_within` (24h, 7d, 30d, any)
  - `min_rating` (float 1-5)
  - `work_types[]`, `job_types[]`, `experience_levels[]` (arrays)
  - `cities[]`, `companies[]`, `company_sizes[]` (arrays)
  - `page`, `page_size`, `sort_by` (pagination/sort)
- [ ] Build MongoDB query from filters
- [ ] Return paginated results with metadata
- [ ] Add filter counts endpoint `/api/v1/jobs/filter-options`

**Step 1.3: Database Migration**
```bash
# Seed sample jobs with filter data
```
- [ ] Create migration script to add filter fields to existing jobs
- [ ] Seed 50+ sample jobs with varied data
- [ ] Add indexes: `posted_at`, `work_type`, `salary_min`, `city`

---

### ✅ Phase 2: Frontend Search Page (Day 2)

**Step 2.1: Create Search Page**
```bash
File: frontend/app/search/page.tsx
```
- [ ] Create `/search` route
- [ ] Parse URL query parameters
- [ ] Fetch jobs from API
- [ ] Display loading state
- [ ] Show "No results" state
- [ ] Implement pagination

**Step 2.2: Search Bar Component**
```bash
File: frontend/components/SearchBar.tsx
```
- [ ] Two input fields: Job title + Location
- [ ] Search button
- [ ] Auto-submit on Enter key
- [ ] Clear button
- [ ] Optional: Auto-complete suggestions

**Step 2.3: Active Filters Display**
```bash
File: frontend/components/ActiveFilters.tsx
```
- [ ] Show "X jobs found" count
- [ ] Display filter chips with × remove button
- [ ] "Clear all" button
- [ ] Update on filter changes

---

### ✅ Phase 3: Filter Panel (Day 3)

**Step 3.1: Main Filter Panel**
```bash
File: frontend/components/FilterPanel.tsx
```
- [ ] Scrollable sidebar (fixed position)
- [ ] Collapsible sections
- [ ] Apply/Clear buttons at bottom

**Step 3.2: Individual Filter Components**

**Toggle Filters:**
```bash
Files: frontend/components/filters/ToggleFilter.tsx
```
- [ ] Easy Apply only (checkbox)
- [ ] Remote only (checkbox)

**Salary Range Slider:**
```bash
File: frontend/components/filters/SalaryRangeSlider.tsx
```
- [ ] Dual-handle range slider
- [ ] Min/Max input fields
- [ ] Presets: $50-75k, $75-100k, $100-150k, $150k+
- [ ] Format with commas (e.g., $85,000)

**Radio Group Filters:**
```bash
File: frontend/components/filters/RadioFilter.tsx
```
- [ ] Date Posted: Last 24h, 7d, 30d, Any time
- [ ] Sort By: Relevance, Newest, Salary

**Select Dropdown:**
```bash
File: frontend/components/filters/SelectFilter.tsx
```
- [ ] Company Rating: Any, 3.0+, 3.5+, 4.0+, 4.5+

**Checkbox Group (Multi-select):**
```bash
File: frontend/components/filters/CheckboxGroup.tsx
```
- [ ] Work Types: Remote, Hybrid, On-site
- [ ] Job Types: Full-time, Part-time, Contract, Internship
- [ ] Experience Levels: Entry, Mid, Senior, Lead
- [ ] Show count per option (e.g., "Remote (247)")

**Expandable Sections:**
```bash
File: frontend/components/filters/ExpandableFilter.tsx
```
- [ ] Cities (multi-select with search)
- [ ] Companies (multi-select with search)
- [ ] Company Sizes (multi-select)
- [ ] Industries (multi-select)

---

### ✅ Phase 4: Job Results (Day 4)

**Step 4.1: Job Card Component**
```bash
File: frontend/components/JobCard.tsx
```
- [ ] Company logo
- [ ] Job title
- [ ] Company name + rating
- [ ] Location + work type badge
- [ ] Salary range (if available)
- [ ] Key skills (3-5 tags)
- [ ] Posted date ("2 days ago")
- [ ] Easy Apply badge
- [ ] Save/Bookmark button
- [ ] Click to view details

**Step 4.2: Results Layout**
```bash
File: frontend/components/JobResults.tsx
```
- [ ] Grid or list view
- [ ] Loading skeleton
- [ ] Empty state
- [ ] Pagination controls
- [ ] "Load more" option

**Step 4.3: Sort Options**
```bash
File: frontend/components/SortDropdown.tsx
```
- [ ] Most Relevant (default)
- [ ] Newest First
- [ ] Highest Salary

---

### ✅ Phase 5: Mobile & Polish (Day 5)

**Step 5.1: Mobile Responsive**
- [ ] Filter panel as bottom sheet/modal on mobile
- [ ] "Filters (5)" button with badge count
- [ ] Sticky search bar
- [ ] Touch-friendly controls
- [ ] Collapsible job cards

**Step 5.2: URL Persistence**
- [ ] Update URL on filter change
- [ ] Parse URL on page load
- [ ] Shareable search links
- [ ] Browser back/forward support

**Step 5.3: Polish & UX**
- [ ] Smooth animations
- [ ] Loading states
- [ ] Error messages
- [ ] Success notifications
- [ ] Analytics tracking

**Step 5.4: Testing**
- [ ] Unit tests for filter logic
- [ ] Integration tests for API
- [ ] E2E tests for user flows
- [ ] Cross-browser testing

---

## 🎨 UI/UX Specifications

### Design System

**Colors:**
- Primary: #2563eb (blue)
- Border: #e5e7eb (gray-200)
- Background: #f9fafb (gray-50)
- Text: #1f2937 (gray-800)

**Spacing:**
- Filter sections: 24px margin
- Items: 12px padding
- Chips: 8px padding

**Typography:**
- Page title: 24px, bold
- Section headers: 16px, semibold
- Labels: 14px, regular
- Small text: 12px, regular

---

## 📦 Required NPM Packages

```bash
# Frontend
npm install rc-slider          # Salary range slider
npm install @headlessui/react  # Accessible components
npm install react-icons        # Icons
npm install clsx              # Conditional classes

# Backend
pip install geopy             # Location geocoding (optional)
```

---

## 🔧 Configuration

### Environment Variables

```bash
# Backend .env
MONGODB_URI=mongodb://localhost:27017
DATABASE_NAME=job_portal

# Frontend .env.local
NEXT_PUBLIC_API_URL=http://localhost:8000
```

---

## 📊 Sample Data Structure

### Job Document Example:
```json
{
  "id": "job_123",
  "title": "Senior Software Engineer",
  "description": "We are seeking...",
  "company_name": "Tech Corp",
  "company_rating": 4.5,
  "company_size": "medium",
  "work_type": "remote",
  "job_type": "full_time",
  "experience_level": "senior",
  "salary_min": 120000,
  "salary_max": 160000,
  "salary_currency": "USD",
  "location": "San Francisco, CA",
  "city": "San Francisco",
  "state": "CA",
  "country": "USA",
  "skills": ["Python", "React", "AWS"],
  "easy_apply": true,
  "posted_at": "2025-11-05T10:00:00Z",
  "status": "active"
}
```

---

## 🚀 Quick Start Commands

### Start Development:
```bash
# Terminal 1: Backend
cd backend
source venv/bin/activate
uvicorn app.main:app --reload --port 8000

# Terminal 2: Frontend
cd frontend
npm run dev

# Terminal 3: MongoDB
docker start job-portal-mongo
```

### Test the Feature:
```bash
# Search endpoint
curl "http://localhost:8000/api/v1/jobs/search?q=engineer&remote_only=true"

# Filter options
curl "http://localhost:8000/api/v1/jobs/filter-options"
```

---

## ✅ Definition of Done

- [ ] All filters work individually and combined
- [ ] Results update in real-time
- [ ] URL parameters persist filters
- [ ] Mobile responsive (tested on iPhone/Android)
- [ ] 100+ sample jobs seeded
- [ ] Unit tests passing
- [ ] E2E test covers main user flow
- [ ] No console errors
- [ ] Page loads < 2 seconds
- [ ] Accessibility: Keyboard navigation works
- [ ] Code reviewed and approved

---

## 📚 Related Documentation

- Full Story: `docs/stories/story-018-advanced-job-filters.md`
- Feature README: `docs/ADVANCED-FILTERS-README.md`
- API Spec: (generate with `/docs` endpoint)

---

**Ready to start implementing? Follow the phases in order!** 🚀

Next step: **Phase 1.1 - Update the Job model**

