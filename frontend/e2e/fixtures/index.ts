import { test as base, expect } from '@playwright/test';

/**
 * Custom fixtures for Job Portal E2E tests
 * 
 * Provides reusable test helpers and page objects following
 * fixture architecture best practices.
 */

// Type definitions for API responses
interface User {
  id: string;
  email: string;
  role: 'seeker' | 'employer';
}

interface LoginResponse {
  access_token: string;
  token_type: string;
}

interface Job {
  id: string;
  title: string;
  description: string;
  location: string;
  skills: string[];
}

// Extended test fixtures
type TestFixtures = {
  apiURL: string;
  authenticatedContext: any;
  seekerAuth: { email: string; token: string };
  employerAuth: { email: string; token: string };
};

/**
 * Extended test with custom fixtures
 */
export const test = base.extend<TestFixtures>({
  // API URL fixture
  apiURL: async ({}, use) => {
    const url = process.env.API_URL || 'http://localhost:8000';
    await use(url);
  },
  
  // Authenticated seeker context
  seekerAuth: async ({ request, apiURL }, use) => {
    const email = `seeker-${Date.now()}@test.com`;
    const password = 'TestPass123!';
    
    // Register seeker
    await request.post(`${apiURL}/api/v1/auth/register`, {
      data: {
        email,
        password,
        role: 'seeker',
      },
    });
    
    // Login
    const loginResponse = await request.post(`${apiURL}/api/v1/auth/login`, {
      form: {
        username: email,
        password,
      },
    });
    
    const { access_token } = await loginResponse.json();
    
    await use({ email, token: access_token });
  },
  
  // Authenticated employer context
  employerAuth: async ({ request, apiURL }, use) => {
    const email = `employer-${Date.now()}@test.com`;
    const password = 'TestPass123!';
    
    // Register employer
    await request.post(`${apiURL}/api/v1/auth/register`, {
      data: {
        email,
        password,
        role: 'employer',
      },
    });
    
    // Login
    const loginResponse = await request.post(`${apiURL}/api/v1/auth/login`, {
      form: {
        username: email,
        password,
      },
    });
    
    const { access_token } = await loginResponse.json();
    
    await use({ email, token: access_token });
  },
});

/**
 * API Helper Class
 * 
 * Provides typed API calls for test data setup
 */
export class APIHelper {
  constructor(private request: any, private apiURL: string) {}
  
  /**
   * Create a job posting (employer only)
   */
  async createJob(token: string, job: Partial<Job>): Promise<Job> {
    const response = await this.request.post(`${this.apiURL}/api/v1/jobs/`, {
      headers: {
        Authorization: `Bearer ${token}`,
      },
      data: {
        title: job.title || 'Test Job',
        description: job.description || 'Test description',
        location: job.location || 'Remote',
        skills: job.skills || ['test'],
      },
    });
    
    return response.json();
  }
  
  /**
   * Reindex jobs for recommendations
   */
  async reindexJobs(token: string): Promise<void> {
    await this.request.post(`${this.apiURL}/api/v1/recommendations/index`, {
      headers: {
        Authorization: `Bearer ${token}`,
      },
    });
  }
  
  /**
   * Upload resume (seeker only)
   */
  async uploadResume(token: string, filename: string, content: Buffer): Promise<any> {
    const response = await this.request.post(`${this.apiURL}/api/v1/uploads/resume`, {
      headers: {
        Authorization: `Bearer ${token}`,
      },
      multipart: {
        file: {
          name: filename,
          mimeType: 'application/vnd.openxmlformats-officedocument.wordprocessingml.document',
          buffer: content,
        },
      },
    });
    
    return response.json();
  }
}

/**
 * Page Object: Login Page
 */
export class LoginPage {
  constructor(private page: any) {}
  
  async goto() {
    await this.page.goto('/login');
    await this.page.waitForLoadState('networkidle');
  }
  
  async login(email: string, password: string) {
    await this.page.fill('[data-testid="email-input"]', email);
    await this.page.fill('[data-testid="password-input"]', password);
    
    // Wait for navigation
    const [response] = await Promise.all([
      this.page.waitForResponse((resp: any) => 
        resp.url().includes('/api/v1/auth/login') && resp.status() === 200
      ),
      this.page.click('[data-testid="login-button"]'),
    ]);
    
    return response;
  }
  
  async register(email: string, password: string, role: 'seeker' | 'employer') {
    await this.page.goto('/register');
    await this.page.fill('[data-testid="email-input"]', email);
    await this.page.fill('[data-testid="password-input"]', password);
    await this.page.selectOption('[data-testid="role-select"]', role);
    
    const [response] = await Promise.all([
      this.page.waitForResponse((resp: any) => 
        resp.url().includes('/api/v1/auth/register')
      ),
      this.page.click('[data-testid="register-button"]'),
    ]);
    
    return response;
  }
}

/**
 * Page Object: Recommendations Page
 */
export class RecommendationsPage {
  constructor(private page: any) {}
  
  async goto() {
    await this.page.goto('/recommendations');
    await this.page.waitForLoadState('networkidle');
  }
  
  async waitForRecommendations() {
    await this.page.waitForSelector('[data-testid="recommendation-card"]', {
      timeout: 15000,
    });
  }
  
  async getRecommendationCount(): Promise<number> {
    const cards = await this.page.locator('[data-testid="recommendation-card"]').count();
    return cards;
  }
  
  async clickRecommendation(index: number = 0) {
    await this.page.click(`[data-testid="recommendation-card"]:nth-of-type(${index + 1})`);
  }
  
  async getExplanationChips(): Promise<string[]> {
    const chips = await this.page.locator('[data-testid="explanation-chip"]').allTextContents();
    return chips;
  }
}

/**
 * Page Object: Resume Upload Page
 */
export class ResumeUploadPage {
  constructor(private page: any) {}
  
  async goto() {
    await this.page.goto('/profile/resume');
    await this.page.waitForLoadState('networkidle');
  }
  
  async uploadFile(filePath: string) {
    await this.page.setInputFiles('[data-testid="resume-input"]', filePath);
    
    // Wait for upload to complete
    await this.page.waitForResponse((resp: any) => 
      resp.url().includes('/api/v1/uploads/resume') && resp.status() === 200
    );
  }
  
  async waitForSkillExtraction() {
    await this.page.waitForSelector('[data-testid="extracted-skill"]', {
      timeout: 10000,
    });
  }
  
  async getExtractedSkills(): Promise<string[]> {
    const skills = await this.page.locator('[data-testid="extracted-skill"]').allTextContents();
    return skills;
  }
}

export { expect };
