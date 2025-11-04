/**
 * UI Inspection Script
 * Takes screenshots of the current UI and checks for styling issues
 */
import { chromium } from '@playwright/test';

async function inspectUI() {
  console.log('🔍 Inspecting Job Portal UI...\n');
  
  const browser = await chromium.launch({ headless: false });
  const context = await browser.newContext({
    viewport: { width: 1280, height: 720 },
  });
  const page = await context.newPage();
  
  try {
    // Navigate to homepage
    console.log('📸 Capturing homepage...');
    await page.goto('http://localhost:3001', { waitUntil: 'networkidle' });
    await page.screenshot({ path: 'ui-screenshots/01-homepage.png', fullPage: true });
    
    // Get page title and main content
    const title = await page.title();
    console.log(`   Title: ${title}`);
    
    // Check for styling
    const bodyStyles = await page.evaluate(() => {
      const body = document.body;
      const computed = window.getComputedStyle(body);
      return {
        backgroundColor: computed.backgroundColor,
        fontFamily: computed.fontFamily,
        margin: computed.margin,
        padding: computed.padding,
      };
    });
    console.log('   Body styles:', bodyStyles);
    
    // Check for main elements
    const hasNav = await page.locator('nav').count() > 0;
    const hasHeader = await page.locator('header').count() > 0;
    const hasMain = await page.locator('main').count() > 0;
    
    console.log(`   Has navigation: ${hasNav}`);
    console.log(`   Has header: ${hasHeader}`);
    console.log(`   Has main content: ${hasMain}`);
    
    // Get text content to see what's visible
    const bodyText = await page.locator('body').textContent();
    console.log(`   Visible text preview: ${bodyText?.substring(0, 200)}...\n`);
    
    // Check if there are any CSS files loaded
    const stylesheets = await page.evaluate(() => {
      return Array.from(document.styleSheets).map(sheet => {
        try {
          return sheet.href || 'inline styles';
        } catch (e) {
          return 'unable to access';
        }
      });
    });
    console.log('   Loaded stylesheets:', stylesheets);
    
    // Look for Tailwind or other CSS frameworks
    const hasTailwind = await page.evaluate(() => {
      const html = document.documentElement;
      return html.className.includes('tailwind') || 
             document.querySelector('[class*="tw-"]') !== null ||
             Array.from(document.styleSheets).some(sheet => {
               try {
                 return sheet.href?.includes('tailwind');
               } catch (e) {
                 return false;
               }
             });
    });
    console.log(`   Using Tailwind CSS: ${hasTailwind}\n`);
    
    // Check console errors
    page.on('console', msg => {
      if (msg.type() === 'error') {
        console.log('   ❌ Console error:', msg.text());
      }
    });
    
    console.log('✅ Screenshot saved to: ui-screenshots/01-homepage.png');
    console.log('\n📊 UI Analysis:');
    
    if (!hasNav && !hasHeader) {
      console.log('   ⚠️  No navigation or header found - UI might be unstyled');
    }
    
    if (bodyStyles.backgroundColor === 'rgba(0, 0, 0, 0)' || bodyStyles.backgroundColor === 'transparent') {
      console.log('   ⚠️  No background color set');
    }
    
    if (!hasTailwind) {
      console.log('   ⚠️  Tailwind CSS not detected - styling may be missing');
    }
    
    // Wait a bit so you can see the browser
    console.log('\n🔍 Browser will stay open for 10 seconds for inspection...');
    await page.waitForTimeout(10000);
    
  } catch (error) {
    console.error('❌ Error inspecting UI:', error);
  } finally {
    await browser.close();
  }
}

inspectUI().catch(console.error);
