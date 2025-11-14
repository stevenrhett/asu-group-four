import { defineConfig, devices } from '@playwright/test';

/**
 * Playwright Configuration for Job Portal E2E Tests
 * 
 * Based on Test Architect best practices:
 * - Network-first safeguards
 * - Deterministic waits
 * - Proper artifact management
 * - Parallel execution with sharding
 */
export default defineConfig({
  testDir: './tests',
  
  // Test execution settings
  fullyParallel: true,
  forbidOnly: !!process.env.CI, // Fail CI if test.only is used
  retries: process.env.CI ? 2 : 0, // Retry flaky tests in CI
  workers: process.env.CI ? 1 : undefined, // Parallel workers
  
  // Reporter configuration
  reporter: [
    ['html', { outputFolder: 'playwright-report' }],
    ['json', { outputFile: 'test-results.json' }],
    ['list'], // Console output
  ],
  
  // Global test settings
  use: {
    // Base URL for tests
    baseURL: process.env.BASE_URL || 'http://localhost:3000',
    
    // API base URL
    // @ts-ignore
    apiURL: process.env.API_URL || 'http://localhost:8000',
    
    // Browser context options
    trace: 'on-first-retry', // Capture trace on retry
    screenshot: 'only-on-failure', // Screenshot on failure
    video: 'retain-on-failure', // Video on failure
    
    // Network settings
    actionTimeout: 15000, // 15s for actions (click, fill, etc.)
    navigationTimeout: 30000, // 30s for page navigation
    
    // Viewport
    viewport: { width: 1280, height: 720 },
    
    // Ignore HTTPS errors (dev/test environments)
    ignoreHTTPSErrors: true,
  },
  
  // Test projects for different browsers
  projects: [
    {
      name: 'chromium',
      use: { ...devices['Desktop Chrome'] },
    },
    
    {
      name: 'firefox',
      use: { ...devices['Desktop Firefox'] },
    },
    
    {
      name: 'webkit',
      use: { ...devices['Desktop Safari'] },
    },
    
    // Mobile viewports
    {
      name: 'mobile-chrome',
      use: { ...devices['Pixel 5'] },
    },
    
    {
      name: 'mobile-safari',
      use: { ...devices['iPhone 13'] },
    },
  ],
  
  // Development server configuration
  webServer: {
    command: 'npm run dev',
    url: 'http://localhost:3000',
    reuseExistingServer: !process.env.CI,
    timeout: 120000, // 2 minutes for server startup
  },
  
  // Output directory
  outputDir: 'test-results/',
  
  // Global timeout
  timeout: 60000, // 60s per test (aligns with test quality standards)
  
  // Expect timeout
  expect: {
    timeout: 10000, // 10s for assertions
  },
});
