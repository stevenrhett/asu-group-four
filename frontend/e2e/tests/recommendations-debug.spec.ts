import { test, expect } from '@playwright/test';

test.describe('Recommendations Debug', () => {
  test('should check recommendations API after login', async ({ page }) => {
    // Setup request interception
    page.on('response', async (response) => {
      if (response.url().includes('/recommendations')) {
        console.log('Recommendations API Response:', {
          status: response.status(),
          url: response.url(),
          headers: response.headers(),
        });
        try {
          const body = await response.json();
          console.log('Response body:', JSON.stringify(body, null, 2));
        } catch (e) {
          console.log('Could not parse response body');
        }
      }
      if (response.url().includes('/upload')) {
        console.log('Upload API Response:', {
          status: response.status(),
          url: response.url(),
        });
        try {
          const body = await response.json();
          console.log('Upload response:', JSON.stringify(body, null, 2));
        } catch (e) {
          console.log('Could not parse upload response');
        }
      }
    });

    page.on('request', (request) => {
      if (request.url().includes('/recommendations') || request.url().includes('/upload')) {
        console.log('API Request:', {
          method: request.method(),
          url: request.url(),
          headers: request.headers(),
        });
      }
    });

    // Go to the page
    await page.goto('http://localhost:3000');
    
    // Login as existing user (andre@a2.com)
    await page.waitForLoadState('networkidle');
    
    // Switch to Login mode
    const loginToggle = page.locator('button:has-text("Log In")');
    await loginToggle.click();
    
    // Select Job Seeker role
    await page.locator('button:has-text("Job Seeker")').click();
    
    // Fill in credentials
    await page.locator('input[type="email"]').fill('andre@a2.com');
    await page.locator('input[type="password"]').fill('password');
    
    // Submit login
    await page.locator('button:has-text("Log In")').last().click();
    
    // Wait a bit for login to complete
    await page.waitForTimeout(2000);
    
    // Check if logged in
    const welcomeText = page.locator('text=/Welcome/i');
    await expect(welcomeText).toBeVisible({ timeout: 10000 });
    
    // Check if recommendations section exists
    const recsSection = page.locator('text=/Recommendations/i');
    await expect(recsSection).toBeVisible();
    
    // Wait for any recommendations API calls
    await page.waitForTimeout(3000);
    
    // Check what's displayed
    const pageContent = await page.content();
    console.log('Page contains "No recommendations":', pageContent.includes('No recommendations'));
    
    // Take a screenshot
    await page.screenshot({ path: 'recommendations-debug.png', fullPage: true });
  });
});
