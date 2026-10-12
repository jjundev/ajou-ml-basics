from pathlib import Path
from playwright.sync_api import sync_playwright
path=Path('과제/과제1/과제1_문제설명_Homework1.html').resolve()
with sync_playwright() as pw:
    browser=pw.chromium.launch(headless=True)
    page=browser.new_page(viewport={'width':375,'height':812})
    page.goto(path.as_uri(),wait_until='networkidle')
    page.locator('#pager-next').click()
    short=page.locator('#p1 [data-explanation="start"] .katex').first
    assert short.evaluate('(e)=>getComputedStyle(e).overflowX')=='visible', 'Short inline math must not be a scroll container'
    section=page.locator('#p1 [data-explanation="understand"]')
    assert section.evaluate('(e)=>parseFloat(getComputedStyle(e).marginTop)')>=24, 'Source-to-explanation gap missing'
    browser.close()
print('PASS short-math and section-gap regression')
