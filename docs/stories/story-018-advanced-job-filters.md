# Story: Advanced Job Search & Filters

**ID**: ST-018  
**Epic**: Job Seeker Experience Enhancement  
**Owner**: TBD  
**Status**: in-progress  
**Priority**: HIGH  
**Estimated Effort**: 4-5 days

---

## 📋 User Story

**As a** job seeker  
**I want to** manually search for jobs with advanced filters  
**So that** I can quickly find relevant opportunities that match my preferences

---

## 🎯 Problem Statement

Currently, the job portal only shows AI-recommended jobs. Users cannot:
- Manually search by keywords and location
- Filter by salary range
- Filter by work type (remote/hybrid/on-site)
- Filter by company rating
- Filter by date posted
- Filter by experience level, job type, or company size

This limits user control and makes it hard to find specific opportunities.

---

## ✨ Proposed Solution

Implement a comprehensive search and filter system similar to Glassdoor with:

### **1. Search Bar**
- Job title/keyword search
- Location search with radius
- Real-time search suggestions

### **2. Filter Panel (Sidebar)**
- **Easy Apply only** - Toggle for quick applications
- **Remote only** - Toggle for remote jobs
- **Salary range** - Dual slider ($85k - $275k)
- **Company rating** - Minimum rating filter
- **Date posted** - Last 24h, 7d, 30d, any time
- **Job types** - Full-time, Part-time, Contract, Internship
- **Distance** - Radius from location
- **Cities** - Multi-select city filter
- **Industries** - Filter by industry
- **Job functions** - Engineering, Design, etc.
- **Seniority levels** - Entry, Mid, Senior, Lead
- **Companies** - Filter by specific companies
- **Company sizes** - Startup, SMB, Enterprise

### **3. Active Filters Display**
- Show applied filters as chips
- Quick remove individual filters
- "Clear all" option

### **4. Results Display**
- Job count display
- Sort options (Most relevant, Newest, Salary)
- Pagination

---

## ✅ Acceptance Criteria

### AC1: Search Bar Functionality
**Given** a job seeker is on the search page  
**When** they enter a job title and location  
**Then** they should see:
- Real-time search results as they type
- Auto-complete suggestions
- Results matching the search criteria
- Result count (e.g., "473 jobs found")

### AC2: Filter Panel Display
**Given** a job seeker views the search results  
**When** they open the filter panel  
**Then** they should see:
- All filter categories collapsed/expanded
- Current filter selections highlighted
- Apply and Clear buttons
- Filter counts (e.g., "Remote (247)")

### AC3: Salary Range Filter
**Given** a job seeker wants to filter by salary  
**When** they adjust the salary slider  
**Then** they should:
- See min/max values update in real-time
- See results filter immediately (or on "Apply")
- Be able to type exact salary amounts
- See jobs within or above the range

### AC4: Remote/Work Type Filter
**Given** a job seeker wants remote work  
**When** they toggle "Remote only"  
**Then** they should:
- See only 100% remote positions
- Have option to also filter hybrid/on-site
- See work type badges on job cards

### AC5: Multiple Filters Combined
**Given** a job seeker applies multiple filters  
**When** they select: Remote + $100k-$150k + Last 7 days  
**Then** they should see:
- Only jobs matching ALL criteria
- Active filter chips displayed
- Updated result count
- Ability to remove individual filters

### AC6: Filter Persistence
**Given** a job seeker applies filters  
**When** they navigate away and return  
**Then** their filters should:
- Be saved in URL parameters
- Persist across page refreshes
- Be shareable via URL

### AC7: Mobile Responsiveness
**Given** a job seeker on mobile device  
**When** they access the search page  
**Then** they should see:
- Filters in a slide-up modal
- Filter count badge on button
- Easy-to-use touch controls
- Responsive layout

---

## 🏗️ Technical Implementation

### **Backend Changes**

#### 1. Enhanced Job Model
```python
# backend/app/models/job.py
from enum import Enum
from typing import Optional, List
from datetime import datetime

class WorkType(str, Enum):
    REMOTE = "remote"
    HYBRID = "hybrid"
    ONSITE = "onsite"

class JobType(str, Enum):
    FULL_TIME = "full_time"
    PART_TIME = "part_time"
    CONTRACT = "contract"
    INTERNSHIP = "internship"

class ExperienceLevel(str, Enum):
    ENTRY = "entry"
    MID = "mid"
    SENIOR = "senior"
    LEAD = "lead"

class Job(Document):
    # Existing fields
    title: str
    description: str
    skills: List[str]
    employer_id: str
    
    # NEW FIELDS FOR FILTERS
    location: str
    work_type: WorkType = WorkType.ONSITE
    job_type: JobType = JobType.FULL_TIME
    experience_level: ExperienceLevel = ExperienceLevel.MID
    
    salary_min: Optional[int] = None
    salary_max: Optional[int] = None
    salary_currency: str = "USD"
    
    company_name: str
    company_rating: Optional[float] = None
    company_size: Optional[str] = None
    
    posted_at: datetime = Field(default_factory=datetime.utcnow)
    easy_apply: bool = False
    
    # Geolocation
    city: Optional[str] = None
    state: Optional[str] = None
    country: str = "USA"
    latitude: Optional[float] = None
    longitude: Optional[float] = None
    
    class Settings:
        name = "jobs"
        indexes = [
            "posted_at",
            "work_type",
            "salary_min",
            "company_rating",
            "city",
            "experience_level"
        ]
```

#### 2. Search & Filter API Endpoint
```python
# backend/app/api/v1/routes/search.py
from fastapi import APIRouter, Query
from typing import Optional, List
from datetime import datetime, timedelta

router = APIRouter()

@router.get("/jobs/search")
async def search_jobs(
    # Search
    q: Optional[str] = Query(None, description="Job title or keywords"),
    location: Optional[str] = Query(None, description="City or location"),
    radius: Optional[int] = Query(50, description="Search radius in miles"),
    
    # Toggles
    easy_apply: bool = Query(False),
    remote_only: bool = Query(False),
    
    # Salary
    salary_min: Optional[int] = Query(None, ge=0),
    salary_max: Optional[int] = Query(None, ge=0),
    
    # Date posted
    posted_within: Optional[str] = Query(
        None, 
        regex="^(24h|7d|30d|any)$"
    ),
    
    # Company
    min_rating: Optional[float] = Query(None, ge=1.0, le=5.0),
    company_sizes: Optional[List[str]] = Query(None),
    companies: Optional[List[str]] = Query(None),
    
    # Job details
    work_types: Optional[List[WorkType]] = Query(None),
    job_types: Optional[List[JobType]] = Query(None),
    experience_levels: Optional[List[ExperienceLevel]] = Query(None),
    
    # Location
    cities: Optional[List[str]] = Query(None),
    
    # Pagination
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=100),
    
    # Sort
    sort_by: str = Query("relevance", regex="^(relevance|newest|salary)$")
):
    """
    Advanced job search with comprehensive filters
    """
    # Build query
    query = {"status": "active"}
    
    # Keyword search
    if q:
        query["$or"] = [
            {"title": {"$regex": q, "$options": "i"}},
            {"description": {"$regex": q, "$options": "i"}},
            {"skills": {"$in": [q]}}
        ]
    
    # Location search
    if location:
        query["$or"] = [
            {"location": {"$regex": location, "$options": "i"}},
            {"city": {"$regex": location, "$options": "i"}}
        ]
    
    # Easy apply filter
    if easy_apply:
        query["easy_apply"] = True
    
    # Remote filter
    if remote_only:
        query["work_type"] = WorkType.REMOTE
    elif work_types:
        query["work_type"] = {"$in": work_types}
    
    # Salary filter
    if salary_min or salary_max:
        salary_conditions = []
        if salary_min:
            salary_conditions.append({"salary_max": {"$gte": salary_min}})
        if salary_max:
            salary_conditions.append({"salary_min": {"$lte": salary_max}})
        if salary_conditions:
            query["$and"] = salary_conditions
    
    # Date posted filter
    if posted_within and posted_within != "any":
        hours_map = {"24h": 24, "7d": 168, "30d": 720}
        hours = hours_map.get(posted_within, 720)
        cutoff = datetime.utcnow() - timedelta(hours=hours)
        query["posted_at"] = {"$gte": cutoff}
    
    # Company rating
    if min_rating:
        query["company_rating"] = {"$gte": min_rating}
    
    # Experience level
    if experience_levels:
        query["experience_level"] = {"$in": experience_levels}
    
    # Job types
    if job_types:
        query["job_type"] = {"$in": job_types}
    
    # Cities
    if cities:
        query["city"] = {"$in": cities}
    
    # Companies
    if companies:
        query["company_name"] = {"$in": companies}
    
    # Company sizes
    if company_sizes:
        query["company_size"] = {"$in": company_sizes}
    
    # Execute query with pagination
    skip = (page - 1) * page_size
    
    # Sorting
    sort_options = {
        "relevance": [("_id", -1)],  # Default
        "newest": [("posted_at", -1)],
        "salary": [("salary_max", -1)]
    }
    sort = sort_options.get(sort_by, [("_id", -1)])
    
    total_count = await Job.find(query).count()
    jobs = await Job.find(query).sort(sort).skip(skip).limit(page_size).to_list()
    
    return {
        "jobs": jobs,
        "pagination": {
            "page": page,
            "page_size": page_size,
            "total_results": total_count,
            "total_pages": (total_count + page_size - 1) // page_size
        },
        "filters_applied": {
            "q": q,
            "location": location,
            "easy_apply": easy_apply,
            "remote_only": remote_only,
            "salary_range": f"${salary_min}-${salary_max}" if salary_min or salary_max else None,
            "posted_within": posted_within
        }
    }

@router.get("/jobs/filter-options")
async def get_filter_options():
    """
    Get available filter options with counts
    """
    # Aggregate to get counts
    work_type_counts = await Job.aggregate([
        {"$match": {"status": "active"}},
        {"$group": {"_id": "$work_type", "count": {"$sum": 1}}}
    ]).to_list()
    
    return {
        "work_types": [
            {"value": wt["_id"], "count": wt["count"]} 
            for wt in work_type_counts
        ],
        "salary_ranges": [
            {"min": 0, "max": 75000, "label": "$0-$75k"},
            {"min": 75000, "max": 100000, "label": "$75k-$100k"},
            {"min": 100000, "max": 150000, "label": "$100k-$150k"},
            {"min": 150000, "max": None, "label": "$150k+"}
        ]
    }
```

### **Frontend Components**

#### 1. Search Page with Filters
```typescript
// frontend/app/search/page.tsx
'use client';

import { useState, useEffect } from 'react';
import { useSearchParams, useRouter } from 'next/navigation';
import { SearchBar } from '@/components/SearchBar';
import { FilterPanel } from '@/components/FilterPanel';
import { JobCard } from '@/components/JobCard';
import { ActiveFilters } from '@/components/ActiveFilters';

export default function SearchPage() {
  const router = useRouter();
  const searchParams = useSearchParams();
  
  const [jobs, setJobs] = useState([]);
  const [loading, setLoading] = useState(false);
  const [totalResults, setTotalResults] = useState(0);
  
  // Parse filters from URL
  const [filters, setFilters] = useState({
    q: searchParams.get('q') || '',
    location: searchParams.get('location') || '',
    remote_only: searchParams.get('remote_only') === 'true',
    easy_apply: searchParams.get('easy_apply') === 'true',
    salary_min: parseInt(searchParams.get('salary_min') || '0'),
    salary_max: parseInt(searchParams.get('salary_max') || '300000'),
    posted_within: searchParams.get('posted_within') || 'any',
    min_rating: parseFloat(searchParams.get('min_rating') || '0'),
    page: parseInt(searchParams.get('page') || '1')
  });

  // Fetch jobs when filters change
  useEffect(() => {
    fetchJobs();
  }, [filters]);

  const fetchJobs = async () => {
    setLoading(true);
    try {
      const queryParams = new URLSearchParams(
        Object.entries(filters)
          .filter(([_, v]) => v)
          .map(([k, v]) => [k, String(v)])
      );
      
      const response = await fetch(
        `http://localhost:8000/api/v1/jobs/search?${queryParams}`
      );
      const data = await response.json();
      
      setJobs(data.jobs);
      setTotalResults(data.pagination.total_results);
    } catch (error) {
      console.error('Search failed:', error);
    } finally {
      setLoading(false);
    }
  };

  const handleFilterChange = (newFilters) => {
    setFilters({ ...filters, ...newFilters, page: 1 });
    
    // Update URL
    const params = new URLSearchParams(
      Object.entries({ ...filters, ...newFilters })
        .filter(([_, v]) => v)
        .map(([k, v]) => [k, String(v)])
    );
    router.push(`/search?${params.toString()}`);
  };

  const handleRemoveFilter = (filterKey) => {
    const newFilters = { ...filters };
    delete newFilters[filterKey];
    setFilters(newFilters);
  };

  return (
    <div className="search-page">
      <SearchBar
        initialQuery={filters.q}
        initialLocation={filters.location}
        onSearch={(q, location) => handleFilterChange({ q, location })}
      />
      
      <div className="search-content">
        <aside className="filter-sidebar">
          <FilterPanel
            filters={filters}
            onChange={handleFilterChange}
          />
        </aside>
        
        <main className="results-section">
          <ActiveFilters
            filters={filters}
            totalResults={totalResults}
            onRemove={handleRemoveFilter}
            onClearAll={() => setFilters({})}
          />
          
          {loading ? (
            <div>Loading...</div>
          ) : (
            <div className="job-results">
              {jobs.map((job) => (
                <JobCard key={job.id} job={job} />
              ))}
            </div>
          )}
        </main>
      </div>
    </div>
  );
}
```

#### 2. Filter Panel Component
```typescript
// frontend/components/FilterPanel.tsx
import { useState } from 'react';
import { SalaryRangeSlider } from './SalaryRangeSlider';

interface FilterPanelProps {
  filters: any;
  onChange: (filters: any) => void;
}

export function FilterPanel({ filters, onChange }: FilterPanelProps) {
  return (
    <div className="filter-panel">
      <h3>Filter jobs</h3>
      
      {/* Easy Apply Toggle */}
      <div className="filter-item">
        <label>
          <input
            type="checkbox"
            checked={filters.easy_apply}
            onChange={(e) => onChange({ easy_apply: e.target.checked })}
          />
          Easy Apply only
        </label>
      </div>
      
      {/* Remote Only Toggle */}
      <div className="filter-item">
        <label>
          <input
            type="checkbox"
            checked={filters.remote_only}
            onChange={(e) => onChange({ remote_only: e.target.checked })}
          />
          Remote only
        </label>
      </div>
      
      {/* Salary Range */}
      <div className="filter-section">
        <h4>Salary range</h4>
        <SalaryRangeSlider
          min={filters.salary_min}
          max={filters.salary_max}
          onChange={(min, max) => onChange({ salary_min: min, salary_max: max })}
        />
      </div>
      
      {/* Company Rating */}
      <div className="filter-section">
        <h4>Company rating</h4>
        <select
          value={filters.min_rating}
          onChange={(e) => onChange({ min_rating: parseFloat(e.target.value) })}
        >
          <option value="0">Any rating</option>
          <option value="3.0">3.0+</option>
          <option value="3.5">3.5+</option>
          <option value="4.0">4.0+</option>
          <option value="4.5">4.5+</option>
        </select>
      </div>
      
      {/* Date Posted */}
      <div className="filter-section">
        <h4>Date posted</h4>
        <div className="radio-group">
          {['24h', '7d', '30d', 'any'].map((option) => (
            <label key={option}>
              <input
                type="radio"
                name="posted_within"
                value={option}
                checked={filters.posted_within === option}
                onChange={(e) => onChange({ posted_within: e.target.value })}
              />
              {option === '24h' ? 'Last 24 hours' :
               option === '7d' ? 'Last 7 days' :
               option === '30d' ? 'Last 30 days' : 'Any time'}
            </label>
          ))}
        </div>
      </div>
      
      {/* Action Buttons */}
      <div className="filter-actions">
        <button onClick={() => onChange({})}>Clear</button>
        <button className="primary">Apply filters</button>
      </div>
    </div>
  );
}
```

---

## 📊 Success Metrics

- **80%+** of users use at least one filter
- **60%** reduction in time to find relevant jobs
- **45%** increase in application rate
- **4.5/5** user satisfaction with search

---

## 🔗 Dependencies

- ✅ ST-001: Auth & JWT
- ✅ ST-003: Job Index
- ⚠️ Need to add filter fields to Job model

---

## 🧪 Testing Strategy

### Unit Tests
- Filter query builder logic
- Salary range validation
- Date range calculations

### Integration Tests
- Search with multiple filters
- Filter persistence in URL
- Pagination with filters

### E2E Tests
- User applies filters and sees results
- User removes filters
- User shares filtered search URL

---

## 📝 Tasks

### Phase 1: Backend (2 days)
- [ ] Update Job model with filter fields
- [ ] Create search/filter API endpoint
- [ ] Add database indexes
- [ ] Write unit tests

### Phase 2: Frontend (2 days)
- [ ] Create SearchPage component
- [ ] Build FilterPanel component
- [ ] Implement SalaryRangeSlider
- [ ] Add ActiveFilters display
- [ ] URL parameter persistence

### Phase 3: Polish (1 day)
- [ ] Mobile responsive design
- [ ] Loading states
- [ ] Error handling
- [ ] Analytics tracking

---

**Estimated Total Effort**: 4-5 days  
**Priority**: HIGH  
**Status**: Ready to Start

---

_Last Updated: 2025-11-06_  
_Author: Development Team_

