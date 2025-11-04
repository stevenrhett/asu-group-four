import { test, expect } from '@playwright/test';

test.describe('Authentication Flow', () => {
  test.beforeEach(async ({ page }) => {
    await page.goto('http://localhost:3000');
  });

  test('should display auth form with visible text', async ({ page }) => {
    // Check if the page loads
    await expect(page).toHaveTitle(/Job Portal/);
    
    // Check for the Create Account heading
    const heading = page.locator('h2').first();
    await expect(heading).toBeVisible();
    
    // Get the computed color
    const color = await heading.evaluate((el) => {
      return window.getComputedStyle(el).color;
    });
    console.log('Heading color:', color);
    
    // Check if form inputs are visible
    await expect(page.locator('input[type="email"]')).toBeVisible();
    await expect(page.locator('input[type="password"]')).toBeVisible();
  });

  test('should attempt to register a new user', async ({ page }) => {
    // Wait for page to load
    await page.waitForLoadState('networkidle');
    
    // Check if we're on register mode (default)
    const createButton = page.locator('button:has-text("Create Account")');
    await expect(createButton).toBeVisible();
    
    // Select Job Seeker role
    await page.locator('button:has-text("Job Seeker")').click();
    
    // Fill in the form
    await page.locator('input[type="email"]').fill('test@example.com');
    await page.locator('input[type="password"]').fill('testpassword123');
    
    // Listen for network requests
    const responsePromise = page.waitForResponse(
      response => response.url().includes('/auth/register'),
      { timeout: 10000 }
    );
    
    // Submit the form
    await createButton.click();
    
    try {
      const response = await responsePromise;
      const status = response.status();
      const body = await response.json().catch(() => null);
      
      console.log('Register Response Status:', status);
      console.log('Register Response Body:', body);
      
      if (status !== 200 && status !== 201) {
        console.log('Registration failed with status:', status);
        console.log('Error details:', body);
      }
    } catch (error) {
      console.log('Network error during registration:', error);
      
      // Check if there's an error message displayed
      const errorMessage = await page.locator('text=/error|failed|unable/i').first().textContent().catch(() => null);
      console.log('Error message on page:', errorMessage);
    }
    
    // Take a screenshot for debugging
    await page.screenshot({ path: 'auth-test-result.png', fullPage: true });
  });

  test('should check backend connectivity', async ({ page }) => {
    // Try to ping the backend directly
    const backendHealthCheck = await page.evaluate(async () => {
      try {
        const response = await fetch('http://localhost:8000/api/v1/health').catch(() => null);
        return {
          reachable: !!response,
          status: response?.status,
          ok: response?.ok
        };
      } catch (error) {
        return {
          reachable: false,
          error: String(error)
        };
      }
    });
    
    console.log('Backend health check:', backendHealthCheck);
  });
});
