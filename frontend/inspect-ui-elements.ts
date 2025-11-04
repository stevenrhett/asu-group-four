import { chromium } from '@playwright/test';

(async () => {
  const browser = await chromium.launch({ headless: false });
  const page = await browser.newPage();
  
  await page.goto('http://localhost:3000');
  await page.waitForTimeout(2000);
  
  // Take screenshot
  await page.screenshot({ path: 'ui-current.png', fullPage: true });
  
  // Get computed styles of main elements
  const styles = await page.evaluate(() => {
    const body = document.body;
    const main = document.querySelector('main');
    const nav = document.querySelector('nav');
    const card = document.querySelector('.glass-card');
    
    return {
      bodyBg: window.getComputedStyle(body).background,
      bodyColor: window.getComputedStyle(body).color,
      mainPadding: main ? window.getComputedStyle(main).padding : 'none',
      navBg: nav ? window.getComputedStyle(nav).background : 'none',
      navBackdrop: nav ? window.getComputedStyle(nav).backdropFilter : 'none',
      cardBg: card ? window.getComputedStyle(card).background : 'none',
      cardBackdrop: card ? window.getComputedStyle(card).backdropFilter : 'none',
      htmlContent: document.documentElement.outerHTML.substring(0, 2000)
    };
  });
  
  console.log('UI Inspection Results:');
  console.log('======================');
  console.log('Body Background:', styles.bodyBg);
  console.log('Body Color:', styles.bodyColor);
  console.log('Main Padding:', styles.mainPadding);
  console.log('Nav Background:', styles.navBg);
  console.log('Nav Backdrop Filter:', styles.navBackdrop);
  console.log('Card Background:', styles.cardBg);
  console.log('Card Backdrop Filter:', styles.cardBackdrop);
  console.log('\nHTML Preview:');
  console.log(styles.htmlContent);
  
  await page.waitForTimeout(5000); // Keep browser open for 5 seconds
  await browser.close();
})();
