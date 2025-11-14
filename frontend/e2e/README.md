# E2E Testing Setup with Playwright

This directory contains end-to-end browser tests using Playwright.

## Setup

```bash
# Install Playwright
npm install -D @playwright/test
npx playwright install

# Run tests
npm run test:e2e

# Run tests in headed mode (see browser)
npm run test:e2e:headed

# Run tests in debug mode
npm run test:e2e:debug

# Generate test report
npm run test:e2e:report
```

## Test Structure

```
e2e/
├── fixtures/           # Reusable test fixtures and helpers
├── tests/             # Test specifications
│   ├── auth.spec.ts   # Authentication flows
│   ├── resume.spec.ts # Resume upload and parsing
│   ├── recommendations.spec.ts # Job recommendations
│   └── applications.spec.ts    # Job applications
├── playwright.config.ts # Playwright configuration
└── README.md          # This file
```

## Best Practices

1. **Network-First Safeguards**: Intercept API calls before navigation
2. **Deterministic Waits**: Use `waitForResponse`, `waitForSelector` instead of `waitForTimeout`
3. **Isolation**: Each test is independent, cleans up its data
4. **Page Object Pattern**: Reusable page objects in fixtures/
5. **Visual Debugging**: Screenshots and videos on failure

## Test Priorities

- **P0 (Critical)**: Auth, core user journeys
- **P1 (High)**: Resume upload, recommendations, applications
- **P2 (Medium)**: Error handling, edge cases
- **P3 (Low)**: UI polish, accessibility

## Running Specific Tests

```bash
# Run single test file
npx playwright test tests/auth.spec.ts

# Run tests matching pattern
npx playwright test --grep "login"

# Run tests by tag
npx playwright test --grep @P0
```
