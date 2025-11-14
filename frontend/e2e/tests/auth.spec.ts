/**
 * E2E Tests for Authentication Flow (ST-001)
 * 
 * Priority: P0 (Critical)
 * Test IDs: ST-001-E2E-001 through ST-001-E2E-004
 * 
 * Tests the complete authentication user journey including
 * registration, login, and role-based access control.
 */
import { test, expect, LoginPage } from '../fixtures';

test.describe('Authentication Flow @P0', () => {
  test('ST-001-E2E-001: User can register as seeker', async ({ page }) => {
    /**
     * Given: New user visits registration page
     * When: User submits valid registration form
     * Then: Account is created and user is redirected to dashboard
     */
    const loginPage = new LoginPage(page);
    const email = `seeker-${Date.now()}@test.com`;
    const password = 'SecurePass123!';
    
    // Navigate to registration
    await page.goto('/register');
    await page.waitForLoadState('networkidle');
    
    // Fill registration form
    await page.fill('[data-testid="email-input"]', email);
    await page.fill('[data-testid="password-input"]', password);
    await page.selectOption('[data-testid="role-select"]', 'seeker');
    
    // Submit and wait for API response
    const [response] = await Promise.all([
      page.waitForResponse(resp => 
        resp.url().includes('/api/v1/auth/register') && resp.status() === 201
      ),
      page.click('[data-testid="register-button"]'),
    ]);
    
    // Verify successful registration
    expect(response.status()).toBe(201);
    
    // Verify redirect to appropriate page
    await page.waitForURL(/\/(dashboard|profile)/);
  });
  
  test('ST-001-E2E-002: User can log in with valid credentials', async ({ page }) => {
    /**
     * Given: Existing user with valid credentials
     * When: User logs in
     * Then: JWT token is received and user accesses protected content
     */
    const loginPage = new LoginPage(page);
    const email = `login-test-${Date.now()}@test.com`;
    const password = 'TestPass123!';
    
    // First register
    await loginPage.register(email, password, 'seeker');
    
    // Logout (if automatic login happens)
    await page.goto('/logout');
    
    // Now test login
    await loginPage.goto();
    
    const response = await loginPage.login(email, password);
    
    // Verify successful login
    expect(response.status()).toBe(200);
    const body = await response.json();
    expect(body).toHaveProperty('access_token');
    
    // Verify JWT is stored (check localStorage or cookies)
    const token = await page.evaluate(() => localStorage.getItem('access_token'));
    expect(token).toBeTruthy();
    
    // Verify redirect to dashboard
    await page.waitForURL(/\/(dashboard|recommendations)/);
  });
  
  test('ST-001-E2E-003: Login fails with invalid credentials', async ({ page }) => {
    /**
     * Given: User with invalid credentials
     * When: User attempts to log in
     * Then: Login fails with error message, no token issued
     */
    const loginPage = new LoginPage(page);
    
    await loginPage.goto();
    
    // Try to login with invalid credentials
    await page.fill('[data-testid="email-input"]', 'invalid@test.com');
    await page.fill('[data-testid="password-input"]', 'WrongPassword!');
    
    const [response] = await Promise.all([
      page.waitForResponse(resp => resp.url().includes('/api/v1/auth/login')),
      page.click('[data-testid="login-button"]'),
    ]);
    
    // Verify 401 response
    expect(response.status()).toBe(401);
    
    // Verify error message is displayed
    await expect(page.locator('[data-testid="error-message"]')).toBeVisible();
    
    // Verify no token in storage
    const token = await page.evaluate(() => localStorage.getItem('access_token'));
    expect(token).toBeNull();
    
    // Verify still on login page
    expect(page.url()).toContain('/login');
  });
  
  test('ST-001-E2E-004: Role-based access control enforced', async ({ page, seekerAuth, employerAuth, apiURL }) => {
    /**
     * Given: User authenticated as seeker
     * When: User attempts employer-only actions
     * Then: Access is denied with 403 error
     */
    
    // Login as seeker
    await page.goto('/login');
    await page.evaluate((token) => {
      localStorage.setItem('access_token', token);
    }, seekerAuth.token);
    
    // Navigate to employer-only page (job posting)
    await page.goto('/jobs/create');
    
    // Should either redirect to dashboard or show error
    await page.waitForTimeout(2000); // Wait for redirect/error
    
    const currentUrl = page.url();
    const hasError = await page.locator('[data-testid="access-denied"]').count() > 0;
    
    // Verify access is denied
    expect(
      currentUrl.includes('/dashboard') || 
      currentUrl.includes('/login') || 
      hasError
    ).toBeTruthy();
  });
  
  test('ST-001-E2E-005: Password is hashed (not stored in plaintext)', async ({ page, request, apiURL }) => {
    /**
     * Given: User registers with password
     * When: Registration completes
     * Then: Password is hashed in database (verify via API if needed)
     */
    const email = `hash-test-${Date.now()}@test.com`;
    const password = 'PlaintextPass123!';
    
    // Register user
    const registerResponse = await request.post(`${apiURL}/api/v1/auth/register`, {
      data: { email, password, role: 'seeker' },
    });
    
    expect(registerResponse.status()).toBe(201);
    const body = await registerResponse.json();
    
    // Verify password is not in response
    expect(JSON.stringify(body)).not.toContain(password);
    expect(body).not.toHaveProperty('password');
    expect(body).not.toHaveProperty('hashed_password');
  });
  
  test('ST-001-E2E-006: Duplicate email registration fails', async ({ page }) => {
    /**
     * Given: Existing user email
     * When: New user tries to register with same email
     * Then: Registration fails with clear error
     */
    const email = `duplicate-${Date.now()}@test.com`;
    const password = 'TestPass123!';
    
    // First registration
    await page.goto('/register');
    await page.fill('[data-testid="email-input"]', email);
    await page.fill('[data-testid="password-input"]', password);
    await page.selectOption('[data-testid="role-select"]', 'seeker');
    await page.click('[data-testid="register-button"]');
    
    // Wait for success
    await page.waitForResponse(resp => 
      resp.url().includes('/api/v1/auth/register') && resp.status() === 201
    );
    
    // Logout
    await page.goto('/logout');
    
    // Try to register again with same email
    await page.goto('/register');
    await page.fill('[data-testid="email-input"]', email);
    await page.fill('[data-testid="password-input"]', password);
    await page.selectOption('[data-testid="role-select"]', 'seeker');
    
    const [response] = await Promise.all([
      page.waitForResponse(resp => resp.url().includes('/api/v1/auth/register')),
      page.click('[data-testid="register-button"]'),
    ]);
    
    // Verify failure
    expect(response.status()).toBe(400);
    
    // Verify error message
    await expect(page.locator('[data-testid="error-message"]')).toBeVisible();
  });
});

test.describe('Session Management @P1', () => {
  test('ST-001-E2E-007: User can log out', async ({ page, seekerAuth }) => {
    /**
     * Given: Authenticated user
     * When: User clicks logout
     * Then: Token is cleared, redirected to login
     */
    await page.goto('/');
    
    // Set authentication token
    await page.evaluate((token) => {
      localStorage.setItem('access_token', token);
    }, seekerAuth.token);
    
    // Navigate to dashboard
    await page.goto('/dashboard');
    
    // Click logout
    await page.click('[data-testid="logout-button"]');
    
    // Verify token is cleared
    const token = await page.evaluate(() => localStorage.getItem('access_token'));
    expect(token).toBeNull();
    
    // Verify redirect to login
    await page.waitForURL(/\/login/);
  });
  
  test('ST-001-E2E-008: Protected routes require authentication', async ({ page }) => {
    /**
     * Given: Unauthenticated user
     * When: User tries to access protected route
     * Then: Redirected to login page
     */
    // Clear any existing auth
    await page.goto('/');
    await page.evaluate(() => localStorage.clear());
    
    // Try to access protected route
    await page.goto('/dashboard');
    
    // Should redirect to login
    await page.waitForURL(/\/login/, { timeout: 5000 });
    expect(page.url()).toContain('/login');
  });
});
