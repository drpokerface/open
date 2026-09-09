import os
import asyncio
from bs4 import BeautifulSoup
from verify_kit import Kit
from playwright.async_api import async_playwright

def run_headless_capture():
    errors = []
    async def _capture():
        os.makedirs('scratch', exist_ok=True)
        async with async_playwright() as p:
            browser = await p.chromium.launch(headless=True, args=['--autoplay-policy=no-user-gesture-required'])
            page = await browser.new_page()
            page.on('console', lambda msg: errors.append(msg.text) if msg.type == 'error' else None)
            page.on('pageerror', lambda exc: errors.append(str(exc)))
            try:
                await page.goto(f"file://{os.path.abspath('slice.html')}")
                await page.wait_for_timeout(2000)
                await page.screenshot(path='scratch/f1.png')
                await page.wait_for_timeout(3000)
                await page.screenshot(path='scratch/f2.png')
                await page.wait_for_timeout(3000)
                await page.screenshot(path='scratch/f3.png')
            finally:
                await browser.close()
    asyncio.run(_capture())
    return len(errors) == 0

def main():
    kit = Kit()
    kit.check('C1', 'capabilities.md exists', lambda: kit.exists('capabilities.md'))
    kit.check('C2', 'manifest.md valid', lambda: kit.exists('manifest.md') and kit.has_all('manifest.md', ['format', 'sample']))
    kit.check('C3', 'slice.html exists', lambda: kit.exists('slice.html') and kit.no_placeholders('slice.html'))
    kit.check('C4', 'slice.html parses as valid HTML', lambda: bool(BeautifulSoup(kit.raw('slice.html'), 'html.parser').find('html')))
    kit.check('C5', 'slice.html contains window.speechSynthesis', lambda: kit.has_all('slice.html', ['window.speechSynthesis']))
    kit.check('C6', 'slice.html contains svg and style', lambda: kit.has_all('slice.html', ['<svg', '<style']))
    
    kit.check('C7', 'slice.html headless capture with no JS errors', run_headless_capture)
    
    kit.perceive('C8', 'frames depict cutout animation', ['scratch/f1.png', 'scratch/f2.png', 'scratch/f3.png'], 'Do these frames depict a cutout style animation?')
    
    rubric = kit.text('artifacts/board-20260909-090123/constitution.md')
    kit.judge('C9', 'score >= 7', 'slice.html', rubric, 'No external anchors available, use constitution as absolute baseline', threshold=7)
    
    kit.fault_proof('slice.html')
    kit.verdict()

if __name__ == '__main__':
    main()
