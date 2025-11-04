# Test Execution Runbook

Quick reference for running the newly implemented tests.

---

## Backend Unit Tests

### ST-003: Indexing Retry & Failure Tests

```bash
cd backend

# Run all indexing failure tests
pytest tests/test_indexing_failures.py -v

# Run specific test class
pytest tests/test_indexing_failures.py::TestIndexingRetryLogic -v

# Run with coverage
pytest tests/test_indexing_failures.py --cov=app.services.indexer --cov-report=html
```

### ST-004: Scoring Configuration Tests

```bash
cd backend

# Run all scoring configuration tests
pytest tests/test_scoring_configuration.py -v

# Run specific test class
pytest tests/test_scoring_configuration.py::TestScoringWeightConfiguration -v

# Run with coverage
pytest tests/test_scoring_configuration.py --cov=app.services.scoring --cov-report=html
```

### Run All New Tests

```bash
cd backend

# Run both new test files
pytest tests/test_indexing_failures.py tests/test_scoring_configuration.py -v

# With coverage report
pytest tests/test_indexing_failures.py tests/test_scoring_configuration.py \
  --cov=app.services.indexer \
  --cov=app.services.scoring \
  --cov-report=term \
  --cov-report=html
```

---

## Frontend E2E Tests

### Prerequisites

```bash
cd frontend

# Install dependencies (including Playwright)
npm install

# Install Playwright browsers (first time only)
npx playwright install

# Verify installation
npx playwright --version
```

### Running E2E Tests

```bash
cd frontend

# Run all E2E tests (headless)
npm run test:e2e

# Run specific test file
npx playwright test e2e/tests/auth.spec.ts

# Run tests with specific tag
npx playwright test --grep @P0

# Run in headed mode (see browser)
npm run test:e2e:headed

# Run in debug mode (step through tests)
npm run test:e2e:debug

# Run single test by name
npx playwright test --grep "User can register"
```

### Test Reports

```bash
# Generate and open HTML report
npm run test:e2e:report

# View last test results
npx playwright show-report

# View trace for failed tests
npx playwright show-trace test-results/[test-name]/trace.zip
```

### Running Specific Browsers

```bash
# Run on Chromium only
npx playwright test --project=chromium

# Run on Firefox only
npx playwright test --project=firefox

# Run on mobile Chrome
npx playwright test --project=mobile-chrome
```

---

## CI/CD Integration

### GitHub Actions Example

```yaml
# .github/workflows/test.yml
name: Tests

on: [push, pull_request]

jobs:
  backend-tests:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      
      - name: Set up Python
        uses: actions/setup-python@v4
        with:
          python-version: '3.11'
      
      - name: Install dependencies
        run: |
          cd backend
          pip install -r requirements.txt
          pip install pytest pytest-cov pytest-asyncio
      
      - name: Run unit tests
        run: |
          cd backend
          pytest tests/ -v --cov=app --cov-report=xml
      
      - name: Upload coverage
        uses: codecov/codecov-action@v3
        with:
          file: ./backend/coverage.xml
  
  e2e-tests:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      
      - name: Set up Node
        uses: actions/setup-node@v3
        with:
          node-version: '18'
      
      - name: Install dependencies
        run: |
          cd frontend
          npm ci
      
      - name: Install Playwright
        run: |
          cd frontend
          npx playwright install --with-deps
      
      - name: Run E2E tests
        run: |
          cd frontend
          npm run test:e2e
      
      - name: Upload test results
        if: always()
        uses: actions/upload-artifact@v3
        with:
          name: playwright-report
          path: frontend/playwright-report/
```

---

## Troubleshooting

### Backend Tests

**Issue: Import errors**
```bash
# Ensure you're in the backend directory
cd backend

# Install dependencies
pip install -r requirements.txt
pip install pytest pytest-asyncio
```

**Issue: MongoDB connection errors**
```bash
# Check MongoDB is running
docker ps | grep mongo

# Or start MongoDB
docker run -d -p 27017:27017 mongo:latest

# Or use in-memory mock (update conftest.py)
```

**Issue: Async test errors**
```bash
# Ensure pytest-asyncio is installed
pip install pytest-asyncio

# Verify pytest.ini has asyncio_mode = auto
```

### E2E Tests

**Issue: Browser not installed**
```bash
cd frontend
npx playwright install
# Or for specific browser:
npx playwright install chromium
```

**Issue: Server not starting**
```bash
# Check if dev server is running
lsof -i :3000

# Start manually if needed
npm run dev
```

**Issue: API server not available**
```bash
# Set API URL in environment
export API_URL=http://localhost:8000

# Or update playwright.config.ts
```

**Issue: Timeout errors**
```bash
# Increase timeout for slow systems
npx playwright test --timeout=90000

# Or update playwright.config.ts timeout
```

---

## Test Output Examples

### Successful Backend Test Run

```
$ pytest tests/test_indexing_failures.py -v

tests/test_indexing_failures.py::TestIndexingRetryLogic::test_index_job_retries_on_embedding_failure PASSED
tests/test_indexing_failures.py::TestIndexingRetryLogic::test_index_job_logs_embedding_failures PASSED
tests/test_indexing_failures.py::TestIndexingRetryLogic::test_index_job_succeeds_without_embedding PASSED
...

==================== 15 passed in 2.34s ====================
```

### Successful E2E Test Run

```
$ npm run test:e2e

Running 16 tests using 4 workers

  ✓  auth.spec.ts:13:3 › ST-001-E2E-001: User can register as seeker (chromium) (3.2s)
  ✓  auth.spec.ts:47:3 › ST-001-E2E-002: User can log in with valid credentials (chromium) (2.8s)
  ✓  recommendations.spec.ts:13:3 › ST-003-E2E-001: Seeker receives job recommendations (chromium) (4.1s)
  ...

  16 passed (45.2s)

To open last HTML report run:

  npx playwright show-report
```

---

## Quick Commands Cheat Sheet

```bash
# Backend: Run all new tests
cd backend && pytest tests/test_indexing_failures.py tests/test_scoring_configuration.py -v

# Frontend: Run all E2E tests
cd frontend && npm run test:e2e

# Backend: Run with coverage
cd backend && pytest tests/ --cov=app --cov-report=html

# Frontend: Debug mode
cd frontend && npm run test:e2e:debug

# Frontend: Headed mode (watch)
cd frontend && npm run test:e2e:headed

# Run specific E2E test
cd frontend && npx playwright test --grep "User can register"

# View E2E test report
cd frontend && npm run test:e2e:report
```

---

## Next Steps After Running Tests

1. ✅ Verify all tests pass
2. ✅ Review coverage reports
3. ✅ Check test execution times (should be <60s per test)
4. ✅ Commit test files to repository
5. ✅ Update CI/CD pipeline to run new tests
6. ✅ Monitor test stability over time

---

**Last Updated:** November 5, 2025  
**Maintained By:** Test Architect Team
