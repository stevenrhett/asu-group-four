/**
 * E2E tests for the Advanced Job Search feature (ST-018)
 * 
 * Tests the job search page, filters, and results display.
 */
import { test, expect } from '@playwright/test';

const API_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000';
const BASE_URL = 'http://localhost:3000';

test.describe('Job Search Page', () => {
  test.beforeEach(async ({ page }) => {
    await page.goto(`${BASE_URL}/search`);
  });

  test('should display search page with search bar', async ({ page }) => {
    // Check that search bar is visible
    await expect(page.locator('input[placeholder*="Job title"]')).toBeVisible();
    await expect(page.locator('input[placeholder*="City"]')).toBeVisible();
    await expect(page.locator('button:has-text("Search")')).toBeVisible();
  });

  test('should display filter panel', async ({ page }) => {
    // Check for filter panel
    await expect(page.locator('text=Filter Jobs')).toBeVisible();
    await expect(page.locator('text=Easy Apply only')).toBeVisible();
    await expect(page.locator('text=Remote only')).toBeVisible();
    await expect(page.locator('text=Salary Range')).toBeVisible();
  });

  test('should search by keywords', async ({ page }) => {
    // Enter search term
    await page.locator('input[placeholder*="Job title"]').fill('Python');
    await page.locator('button:has-text("Search")').click();
    
    // Wait for results
    await page.waitForTimeout(1000);
    
    // Check URL updated
    expect(page.url()).toContain('q=Python');
    
    // Check results are displayed
    const jobCards = page.locator('.bg-white.border.border-gray-200.rounded-lg');
    await expect(jobCards.first()).toBeVisible();
  });

  test('should filter by remote only', async ({ page }) => {
    // Click remote only checkbox
    await page.locator('text=Remote only').click();
    
    // Wait for results
    await page.waitForTimeout(1000);
    
    // Check URL updated
    expect(page.url()).toContain('remote_only=true');
    
    // Check that Remote badges are displayed
    await expect(page.locator('text=Remote').first()).toBeVisible();
  });

  test('should filter by salary range', async ({ page }) => {
    // Set salary range
    await page.locator('input[placeholder*="$0"]').fill('100000');
    await page.locator('input[placeholder*="$300,000"]').fill('150000');
    await page.locator('button:has-text("Apply")').click();
    
    // Wait for results
    await page.waitForTimeout(1000);
    
    // Check URL updated
    expect(page.url()).toContain('salary_min=100000');
    expect(page.url()).toContain('salary_max=150000');
  });

  test('should filter by date posted', async ({ page }) => {
    // Select "Last 7 days"
    await page.locator('text=Last 7 days').click();
    
    // Wait for results
    await page.waitForTimeout(1000);
    
    // Check URL updated
    expect(page.url()).toContain('posted_within=7d');
  });

  test('should filter by work type', async ({ page }) => {
    // Select Remote and Hybrid
    await page.locator('text=Work Type').click();
    await page.locator('label:has-text("Remote") input[type="checkbox"]').check();
    
    // Wait for results
    await page.waitForTimeout(1000);
    
    // Check URL updated
    expect(page.url()).toContain('work_types');
  });

  test('should filter by experience level', async ({ page }) => {
    // Select Senior level
    await page.locator('label:has-text("Senior") input[type="checkbox"]').check();
    
    // Wait for results
    await page.waitForTimeout(1000);
    
    // Check URL updated
    expect(page.url()).toContain('experience_levels');
  });

  test('should display active filters', async ({ page }) => {
    // Apply multiple filters
    await page.locator('text=Remote only').click();
    await page.locator('input[placeholder*="Job title"]').fill('Engineer');
    await page.locator('button:has-text("Search")').click();
    
    // Wait for results
    await page.waitForTimeout(1000);
    
    // Check active filters are displayed
    await expect(page.locator('text=jobs matching your filters')).toBeVisible();
    await expect(page.locator('text=Keywords: Engineer')).toBeVisible();
    await expect(page.locator('text=Remote Only')).toBeVisible();
  });

  test('should remove individual filters', async ({ page }) => {
    // Apply a filter
    await page.locator('text=Remote only').click();
    await page.waitForTimeout(1000);
    
    // Check filter chip is displayed
    await expect(page.locator('text=Remote Only')).toBeVisible();
    
    // Remove the filter by clicking X
    await page.locator('text=Remote Only').locator('..').locator('button').click();
    
    // Wait for update
    await page.waitForTimeout(1000);
    
    // Check filter is removed from URL
    expect(page.url()).not.toContain('remote_only=true');
  });

  test('should clear all filters', async ({ page }) => {
    // Apply multiple filters
    await page.locator('text=Remote only').click();
    await page.locator('text=Easy Apply only').click();
    await page.waitForTimeout(1000);
    
    // Click "Clear all"
    await page.locator('button:has-text("Clear all")').click();
    
    // Wait for update
    await page.waitForTimeout(1000);
    
    // Check URL is reset
    expect(page.url()).toBe(`${BASE_URL}/search`);
  });

  test('should display job cards with correct information', async ({ page }) => {
    // Wait for jobs to load
    await page.waitForTimeout(1000);
    
    // Check first job card has required elements
    const firstCard = page.locator('.bg-white.border.border-gray-200.rounded-lg').first();
    
    // Should have title
    await expect(firstCard.locator('h3')).toBeVisible();
    
    // Should have location or work type badge
    await expect(firstCard.locator('text=/Remote|Hybrid|On-site/')).toBeVisible();
    
    // Should have posted date
    await expect(firstCard.locator('text=/ago|hours|days|weeks/')).toBeVisible();
  });

  test('should handle pagination', async ({ page }) => {
    // Wait for initial results
    await page.waitForTimeout(1000);
    
    // Check if pagination exists (only if there are enough results)
    const nextButton = page.locator('button:has-text("Next")');
    const isVisible = await nextButton.isVisible();
    
    if (isVisible && !(await nextButton.isDisabled())) {
      // Click next page
      await nextButton.click();
      await page.waitForTimeout(1000);
      
      // Check URL updated with page number
      expect(page.url()).toContain('page=2');
      
      // Check previous button is now enabled
      await expect(page.locator('button:has-text("Previous")')).toBeEnabled();
    }
  });

  test('should persist filters in URL', async ({ page }) => {
    // Apply filters
    await page.locator('text=Remote only').click();
    await page.locator('input[placeholder*="Job title"]').fill('Developer');
    await page.locator('button:has-text("Search")').click();
    
    await page.waitForTimeout(1000);
    
    // Get the URL with filters
    const urlWithFilters = page.url();
    
    // Navigate away and back
    await page.goto(`${BASE_URL}`);
    await page.goto(urlWithFilters);
    
    // Check filters are still applied
    expect(page.url()).toContain('remote_only=true');
    expect(page.url()).toContain('q=Developer');
    
    // Check UI reflects the filters
    const remoteCheckbox = page.locator('label:has-text("Remote only") input[type="checkbox"]');
    await expect(remoteCheckbox).toBeChecked();
  });

  test('should show no results message when no jobs match', async ({ page }) => {
    // Search for something that definitely won't exist
    await page.locator('input[placeholder*="Job title"]').fill('xyzabc123impossible');
    await page.locator('button:has-text("Search")').click();
    
    await page.waitForTimeout(1000);
    
    // Check no results message
    await expect(page.locator('text=No jobs found')).toBeVisible();
    await expect(page.locator('text=Try adjusting your filters')).toBeVisible();
  });

  test('should clear search with clear button', async ({ page }) => {
    // Enter search terms
    await page.locator('input[placeholder*="Job title"]').fill('Python');
    await page.locator('input[placeholder*="City"]').fill('San Francisco');
    
    // Check clear button appears
    const clearButton = page.locator('button[title="Clear search"]');
    await expect(clearButton).toBeVisible();
    
    // Click clear
    await clearButton.click();
    
    // Check inputs are cleared
    await expect(page.locator('input[placeholder*="Job title"]')).toHaveValue('');
    await expect(page.locator('input[placeholder*="City"]')).toHaveValue('');
  });
});

test.describe('Job Search Mobile View', () => {
  test.use({
    viewport: { width: 375, height: 667 } // iPhone SE
  });

  test('should display search page on mobile', async ({ page }) => {
    await page.goto(`${BASE_URL}/search`);
    
    // Check search bar is visible and functional on mobile
    await expect(page.locator('input[placeholder*="Job title"]')).toBeVisible();
    await expect(page.locator('button:has-text("Search")')).toBeVisible();
  });

  test('should handle filters on mobile', async ({ page }) => {
    await page.goto(`${BASE_URL}/search`);
    
    // Note: Filter panel may be hidden on mobile by default (in a modal/drawer)
    // This test checks if the basic search functionality works on mobile
    await page.locator('input[placeholder*="Job title"]').fill('Engineer');
    await page.locator('button:has-text("Search")').click();
    
    await page.waitForTimeout(1000);
    
    // Check results are displayed
    await expect(page.locator('.bg-white.border.border-gray-200.rounded-lg').first()).toBeVisible();
  });
});

