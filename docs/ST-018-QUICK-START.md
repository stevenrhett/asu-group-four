# 🚀 ST-018 Quick Start Guide

## Advanced Job Search & Filters - Testing Instructions

---

## ⚡ Quick Setup (5 minutes)

### **Step 1: Seed Sample Data**

```bash
cd backend
source venv/bin/activate
python scripts/seed_jobs_with_filters.py
```

**Expected Output:**
```
🚀 Starting job seeding...
✅ Created 10 jobs...
✅ Created 20 jobs...
✅ Created 30 jobs...
✅ Created 40 jobs...
✅ Created 50 jobs...
✅ Created 60 jobs...

🎉 Successfully seeded 60 jobs!
```

---

### **Step 2: Start Backend**

```bash
cd backend
source venv/bin/activate
uvicorn app.main:app --reload --port 8000
```

**Verify:** Visit `http://localhost:8000/docs` to see API documentation

---

### **Step 3: Start Frontend**

```bash
cd frontend
npm run dev
```

**Access:** `http://localhost:3000/search`

---

## 🧪 Manual Testing Checklist

### **Test 1: Basic Search**
1. Go to `http://localhost:3000/search`
2. Enter "Python" in the job title field
3. Click **Search**
4. ✅ Should see jobs with "Python" in title/description

---

### **Test 2: Remote Filter**
1. Check the "Remote only" checkbox
2. ✅ URL should update: `?remote_only=true`
3. ✅ All job cards should show "Remote" badge
4. ✅ Active filter chip should appear at top

---

### **Test 3: Salary Range**
1. Scroll to "Salary Range" section
2. Enter Min: `100000`, Max: `150000`
3. Click **Apply**
4. ✅ URL should include `salary_min=100000&salary_max=150000`
5. ✅ Jobs should show salaries in that range

---

### **Test 4: Multiple Filters**
1. Check "Remote only"
2. Select "Senior" under Experience Level
3. Set salary min to `120000`
4. ✅ Should see jobs matching ALL criteria
5. ✅ Filter chips should show all 3 filters

---

### **Test 5: Remove Filters**
1. Apply multiple filters (from Test 4)
2. Click the **X** on one filter chip
3. ✅ That filter should be removed
4. ✅ Results should update
5. Click **Clear all**
6. ✅ All filters should reset

---

### **Test 6: Date Posted**
1. Select "Last 7 days" under Date Posted
2. ✅ Should only show recently posted jobs
3. ✅ "Posted X days ago" should be < 7 days

---

### **Test 7: Pagination**
1. If more than 20 jobs, pagination appears
2. Click **Next**
3. ✅ URL updates with `page=2`
4. ✅ Different jobs load
5. Click **Previous**
6. ✅ Returns to page 1

---

### **Test 8: URL Sharing**
1. Apply filters: Remote + Senior + Salary range
2. Copy the URL from browser
3. Open in new tab or incognito window
4. ✅ Same filters should be applied
5. ✅ Same results should appear

---

### **Test 9: Mobile View**
1. Open DevTools (F12)
2. Toggle device toolbar (Ctrl+Shift+M)
3. Select iPhone SE or similar
4. ✅ Search bar should be responsive
5. ✅ Filter panel hidden (can be enhanced with modal)
6. ✅ Job cards should stack vertically

---

### **Test 10: Job Card Display**
1. Scroll through results
2. Each card should show:
   - ✅ Job title
   - ✅ Company name and rating (if available)
   - ✅ Location or work type badge
   - ✅ Salary range (if available)
   - ✅ Skills (up to 5)
   - ✅ "Easy Apply" badge (if applicable)
   - ✅ Posted date ("X days ago")

---

## 🔬 API Testing

### **Test Search Endpoint**

```bash
# Basic search
curl "http://localhost:8000/api/v1/jobs/search?q=Python"

# Remote only
curl "http://localhost:8000/api/v1/jobs/search?remote_only=true"

# Salary range
curl "http://localhost:8000/api/v1/jobs/search?salary_min=100000&salary_max=150000"

# Multiple filters
curl "http://localhost:8000/api/v1/jobs/search?remote_only=true&experience_levels=senior&salary_min=120000"

# With pagination
curl "http://localhost:8000/api/v1/jobs/search?page=1&page_size=10"

# Get filter options
curl "http://localhost:8000/api/v1/jobs/filter-options"
```

**Expected Response:**
```json
{
  "jobs": [...],
  "pagination": {
    "page": 1,
    "page_size": 20,
    "total_results": 15,
    "total_pages": 1,
    "has_more": false
  },
  "filters_applied": {
    "remote_only": true
  }
}
```

---

## 🧬 Run Automated Tests

### **Backend Tests**

```bash
cd backend
pytest tests/test_job_search_filters.py -v
```

**Expected:** 13 tests passing ✅

---

### **Frontend E2E Tests**

```bash
cd frontend
npm run test:e2e
```

**Expected:** 17 tests passing ✅

---

## 🎯 Sample Search Scenarios

### **Scenario 1: Remote Senior Engineer**
```
1. Search: "Engineer"
2. Remote only: ✓
3. Experience: Senior
4. Salary: $120k - $180k
```

### **Scenario 2: Entry Level in San Francisco**
```
1. Location: "San Francisco"
2. Experience: Entry Level
3. Posted: Last 30 days
4. Easy Apply: ✓
```

### **Scenario 3: High-Paying Data Science**
```
1. Search: "Data Scientist"
2. Salary: $150k+
3. Company Rating: 4.0+ stars
4. Work Type: Remote, Hybrid
```

---

## 🐛 Troubleshooting

### **Issue: No jobs appear**
**Solution:**
1. Check if backend is running: `http://localhost:8000/health`
2. Re-run seed script: `python scripts/seed_jobs_with_filters.py`
3. Check MongoDB is running: `docker ps` or `mongosh`

### **Issue: Filters not working**
**Solution:**
1. Check browser console for errors (F12)
2. Verify API URL in `.env.local`: `NEXT_PUBLIC_API_URL=http://localhost:8000`
3. Clear browser cache and cookies

### **Issue: Tests failing**
**Solution:**
1. Ensure backend is running on port 8000
2. Ensure frontend is running on port 3000
3. Check database has seeded data
4. Run `pytest tests/conftest.py` to verify test setup

---

## 📊 Verify Implementation

### **✅ Backend Checklist**
- [ ] Job model has new filter fields
- [ ] `/api/v1/jobs/search` endpoint exists
- [ ] `/api/v1/jobs/filter-options` endpoint exists
- [ ] Seed script creates 60 jobs
- [ ] 13 backend tests pass

### **✅ Frontend Checklist**
- [ ] `/search` page loads
- [ ] Search bar functional
- [ ] Filter panel displays all 12+ filters
- [ ] Active filters show as chips
- [ ] Job cards display correctly
- [ ] Pagination works
- [ ] URL parameters persist filters
- [ ] 17 E2E tests pass

---

## 🎉 Success Criteria

If all of the following work, **ST-018 is complete**:

1. ✅ Search by keywords returns relevant jobs
2. ✅ Remote filter shows only remote jobs
3. ✅ Salary filter respects min/max range
4. ✅ Multiple filters work together (AND logic)
5. ✅ Pagination navigates through results
6. ✅ URL parameters can be shared
7. ✅ Active filters can be removed individually
8. ✅ Mobile view is responsive
9. ✅ All 30 tests pass (13 backend + 17 frontend)
10. ✅ No console errors

---

## 📚 Next Steps

After testing:

1. **User Acceptance Testing (UAT)**: Get feedback from real users
2. **Performance Testing**: Load test with 1000+ jobs
3. **A/B Testing**: Compare with/without filters
4. **Analytics**: Track which filters are most used
5. **Iterate**: Add V2 features based on feedback

---

## 🆘 Need Help?

- **API Docs**: `http://localhost:8000/docs`
- **Story Document**: `docs/stories/story-018-advanced-job-filters.md`
- **Implementation Summary**: `docs/ST-018-IMPLEMENTATION-SUMMARY.md`
- **Feature README**: `docs/ADVANCED-FILTERS-README.md`

---

**Happy Testing! 🚀**

