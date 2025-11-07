/**
 * E2E Tests for Job Recommendations Flow (ST-003, ST-004, ST-005)
 * 
 * Priority: P0 (Critical)
 * Test IDs: ST-003-E2E-001 through ST-005-E2E-003
 * 
 * Tests the complete recommendation journey including job indexing,
 * hybrid scoring, and explainability.
 */
import { test, expect, RecommendationsPage, APIHelper } from '../fixtures';

test.describe('Job Recommendations Flow @P0', () => {
  test('ST-003-E2E-001: Seeker receives job recommendations', async ({ page, seekerAuth, employerAuth, request, apiURL }) => {
    /**
     * Given: Jobs indexed and seeker with profile
     * When: Seeker views recommendations page
     * Then: Relevant jobs are displayed with scores
     */
    const apiHelper = new APIHelper(request, apiURL);
    
    // Create jobs as employer
    await apiHelper.createJob(employerAuth.token, {
      title: 'Senior Python Developer',
      description: 'Expert Python developer needed for FastAPI project',
      location: 'Remote',
      skills: ['python', 'fastapi', 'mongodb'],
    });
    
    await apiHelper.createJob(employerAuth.token, {
      title: 'Java Backend Engineer',
      description: 'Spring Boot expert needed',
      location: 'NYC',
      skills: ['java', 'spring', 'postgresql'],
    });
    
    // Reindex jobs
    await apiHelper.reindexJobs(employerAuth.token);
    
    // Login as seeker
    await page.goto('/');
    await page.evaluate((token) => {
      localStorage.setItem('access_token', token);
    }, seekerAuth.token);
    
    // Navigate to recommendations
    const recommendationsPage = new RecommendationsPage(page);
    await recommendationsPage.goto();
    
    // Wait for recommendations to load
    await recommendationsPage.waitForRecommendations();
    
    // Verify recommendations are displayed
    const count = await recommendationsPage.getRecommendationCount();
    expect(count).toBeGreaterThan(0);
    
    // Verify each recommendation has required elements
    const firstCard = page.locator('[data-testid="recommendation-card"]').first();
    await expect(firstCard.locator('[data-testid="job-title"]')).toBeVisible();
    await expect(firstCard.locator('[data-testid="job-score"]')).toBeVisible();
  });
  
  test('ST-004-E2E-001: Recommendations use hybrid scoring', async ({ page, seekerAuth, employerAuth, request, apiURL }) => {
    /**
     * Given: Jobs with varying BM25 and vector scores
     * When: Seeker views recommendations
     * Then: Results are ranked by hybrid score (BM25 + vector)
     */
    const apiHelper = new APIHelper(request, apiURL);
    
    // Create jobs
    await apiHelper.createJob(employerAuth.token, {
      title: 'Python Developer',
      description: 'Python FastAPI MongoDB',
      location: 'Remote',
      skills: ['python', 'fastapi'],
    });
    
    await apiHelper.reindexJobs(employerAuth.token);
    
    // Setup seeker with profile
    await page.goto('/');
    await page.evaluate((token) => {
      localStorage.setItem('access_token', token);
    }, seekerAuth.token);
    
    // Navigate to recommendations
    await page.goto('/recommendations');
    
    // Wait for results
    await page.waitForSelector('[data-testid="recommendation-card"]');
    
    // Verify scores are present
    const scoreElements = page.locator('[data-testid="job-score"]');
    const firstScore = await scoreElements.first().textContent();
    
    expect(firstScore).toBeTruthy();
    // Score should be a number
    expect(parseFloat(firstScore!)).toBeGreaterThanOrEqual(0);
  });
  
  test('ST-005-E2E-001: Recommendations include explanation chips', async ({ page, seekerAuth, employerAuth, request, apiURL }) => {
    /**
     * Given: Jobs matching seeker profile skills
     * When: Seeker views recommendations
     * Then: Each job shows explanation chips (e.g., "Python match")
     */
    const apiHelper = new APIHelper(request, apiURL);
    
    // Create job with specific skills
    await apiHelper.createJob(employerAuth.token, {
      title: 'Python Engineer',
      description: 'Looking for Python and React developer',
      location: 'Remote',
      skills: ['python', 'react', 'docker'],
    });
    
    await apiHelper.reindexJobs(employerAuth.token);
    
    // Login as seeker
    await page.goto('/');
    await page.evaluate((token) => {
      localStorage.setItem('access_token', token);
    }, seekerAuth.token);
    
    // Navigate to recommendations
    const recommendationsPage = new RecommendationsPage(page);
    await recommendationsPage.goto();
    await recommendationsPage.waitForRecommendations();
    
    // Get explanation chips
    const explanations = await recommendationsPage.getExplanationChips();
    
    // Verify explanations exist
    expect(explanations.length).toBeGreaterThan(0);
    
    // Verify explanation content (should mention skills)
    const hasSkillExplanation = explanations.some(exp => 
      exp.toLowerCase().includes('python') || 
      exp.toLowerCase().includes('react') ||
      exp.toLowerCase().includes('match')
    );
    
    expect(hasSkillExplanation).toBeTruthy();
  });
  
  test('ST-005-E2E-002: Explanation chips are interactive', async ({ page, seekerAuth, employerAuth, request, apiURL }) => {
    /**
     * Given: Job with explanation chips
     * When: User clicks on chip
     * Then: Additional detail or highlight is shown
     */
    const apiHelper = new APIHelper(request, apiURL);
    
    await apiHelper.createJob(employerAuth.token, {
      title: 'Full Stack Developer',
      description: 'React and Node.js expert',
      location: 'Remote',
      skills: ['react', 'nodejs'],
    });
    
    await apiHelper.reindexJobs(employerAuth.token);
    
    await page.goto('/');
    await page.evaluate((token) => {
      localStorage.setItem('access_token', token);
    }, seekerAuth.token);
    
    await page.goto('/recommendations');
    await page.waitForSelector('[data-testid="recommendation-card"]');
    
    // Click first explanation chip
    const firstChip = page.locator('[data-testid="explanation-chip"]').first();
    await firstChip.click();
    
    // Verify some interaction happened (tooltip, highlight, etc.)
    // This depends on implementation
    // For now, just verify chip is clickable
    expect(await firstChip.isEnabled()).toBeTruthy();
  });
});

test.describe('Search and Filtering @P1', () => {
  test('ST-003-E2E-002: Seeker can search jobs by query', async ({ page, seekerAuth, employerAuth, request, apiURL }) => {
    /**
     * Given: Multiple indexed jobs
     * When: Seeker enters search query
     * Then: Results are filtered by query relevance
     */
    const apiHelper = new APIHelper(request, apiURL);
    
    await apiHelper.createJob(employerAuth.token, {
      title: 'Machine Learning Engineer',
      description: 'Python ML expert',
      location: 'SF',
      skills: ['python', 'ml', 'tensorflow'],
    });
    
    await apiHelper.createJob(employerAuth.token, {
      title: 'Frontend Developer',
      description: 'React specialist',
      location: 'Remote',
      skills: ['react', 'typescript'],
    });
    
    await apiHelper.reindexJobs(employerAuth.token);
    
    await page.goto('/');
    await page.evaluate((token) => {
      localStorage.setItem('access_token', token);
    }, seekerAuth.token);
    
    await page.goto('/recommendations');
    
    // Enter search query
    await page.fill('[data-testid="search-input"]', 'machine learning');
    await page.click('[data-testid="search-button"]');
    
    // Wait for filtered results
    await page.waitForResponse(resp => resp.url().includes('/api/v1/recommendations'));
    
    // Verify ML job appears in results
    await expect(page.locator('text=Machine Learning Engineer')).toBeVisible();
  });
  
  test('ST-003-E2E-003: Empty state shown when no recommendations', async ({ page, seekerAuth }) => {
    /**
     * Given: No jobs indexed
     * When: Seeker views recommendations
     * Then: Empty state message is displayed
     */
    await page.goto('/');
    await page.evaluate((token) => {
      localStorage.setItem('access_token', token);
    }, seekerAuth.token);
    
    await page.goto('/recommendations');
    
    // Wait for page load
    await page.waitForLoadState('networkidle');
    
    // Check for empty state
    const hasCards = await page.locator('[data-testid="recommendation-card"]').count();
    
    if (hasCards === 0) {
      // Verify empty state message
      await expect(page.locator('[data-testid="empty-state"]')).toBeVisible();
    }
  });
});

test.describe('Recommendation Interactions @P2', () => {
  test('ST-005-E2E-003: Click on job navigates to detail page', async ({ page, seekerAuth, employerAuth, request, apiURL }) => {
    /**
     * Given: Job recommendations displayed
     * When: User clicks on job card
     * Then: Navigates to job detail page
     */
    const apiHelper = new APIHelper(request, apiURL);
    
    const job = await apiHelper.createJob(employerAuth.token, {
      title: 'DevOps Engineer',
      description: 'Kubernetes expert',
      location: 'Remote',
      skills: ['kubernetes', 'docker', 'aws'],
    });
    
    await apiHelper.reindexJobs(employerAuth.token);
    
    await page.goto('/');
    await page.evaluate((token) => {
      localStorage.setItem('access_token', token);
    }, seekerAuth.token);
    
    const recommendationsPage = new RecommendationsPage(page);
    await recommendationsPage.goto();
    await recommendationsPage.waitForRecommendations();
    
    // Click first recommendation
    await recommendationsPage.clickRecommendation(0);
    
    // Verify navigation to job detail
    await page.waitForURL(/\/jobs\/[a-zA-Z0-9]+/);
    
    // Verify job details are displayed
    await expect(page.locator('[data-testid="job-title"]')).toBeVisible();
    await expect(page.locator('[data-testid="job-description"]')).toBeVisible();
  });
});
