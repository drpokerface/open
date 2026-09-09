import os
import asyncio
from bs4 import BeautifulSoup
from verify_kit import Kit
from playwright.async_api import async_playwright

def run_headless_capture():
    errors = []
    spoken = []
    async def _capture():
        os.makedirs('scratch', exist_ok=True)
        async with async_playwright() as p:
            browser = await p.chromium.launch(headless=True, args=['--autoplay-policy=no-user-gesture-required'])
            page = await browser.new_page()
            
            def handle_console(msg):
                if msg.type == 'error':
                    errors.append(msg.text)
                elif msg.text.startswith('SPEECH_TEXT:'):
                    spoken.append(msg.text.replace('SPEECH_TEXT:', '').strip())
            
            page.on('console', handle_console)
            page.on('pageerror', lambda exc: errors.append(str(exc)))
            try:
                await page.add_init_script('''
                    const originalSpeak = window.speechSynthesis.speak.bind(window.speechSynthesis);
                    window.speechSynthesis.speak = function(utterance) {
                        console.log("SPEECH_TEXT: " + utterance.text);
                        return originalSpeak(utterance);
                    };
                ''')
                await page.goto(f"file://{os.path.abspath('slice.html')}")
                
                # Trigger playback realistically
                await page.click("body", force=True)
                
                await page.wait_for_timeout(2000)
                await page.screenshot(path='scratch/f1.png')
                await page.wait_for_timeout(4000)
                await page.screenshot(path='scratch/f2.png')
                await page.wait_for_timeout(4000)
                await page.screenshot(path='scratch/f3.png')
            finally:
                await browser.close()
    asyncio.run(_capture())
    
    with open('scratch/spoken_text.txt', 'w') as f:
        f.write('\n'.join(spoken))
        
    return len(errors) == 0 and len(spoken) > 0 and any(len(s.strip()) > 0 for s in spoken)

def main():
    kit = Kit()
    kit.check('C1', 'capabilities.md exists', lambda: kit.exists('capabilities.md'))
    kit.check('C2', 'manifest.md valid', lambda: kit.exists('manifest.md') and kit.has_all('manifest.md', ['format', 'sample']))
    kit.check('C3', 'slice.html exists', lambda: kit.exists('slice.html') and kit.no_placeholders('slice.html'))
    kit.check('C4', 'slice.html parses as valid HTML', lambda: bool(BeautifulSoup(kit.raw('slice.html'), 'html.parser').find('html')))
    kit.check('C5', 'slice.html contains window.speechSynthesis', lambda: kit.has_all('slice.html', ['window.speechSynthesis']))
    kit.check('C6', 'slice.html contains svg and style', lambda: kit.has_all('slice.html', ['<svg', '<style']))
    
    kit.check('C7', 'slice.html headless capture with no JS errors and triggers playback', run_headless_capture)
    
    def check_uniform():
        import hashlib
        try:
            h1 = hashlib.md5(open('scratch/f1.png', 'rb').read()).hexdigest()
            h2 = hashlib.md5(open('scratch/f2.png', 'rb').read()).hexdigest()
            h3 = hashlib.md5(open('scratch/f3.png', 'rb').read()).hexdigest()
            return len({h1, h2, h3}) > 1
        except Exception:
            return False
    kit.check('C7b', 'animation frames are not uniform', check_uniform)
    
    kit.perceive('C8', 'frames depict cutout animation with visible motion', ['scratch/f1.png', 'scratch/f2.png', 'scratch/f3.png'], 'Do these frames depict a cutout style animation, and is there clear visible motion or visual change between the three frames?')
    
    rubric = kit.text('artifacts/board-20260909-090123/constitution.md')
    captured_text = kit.text('scratch/spoken_text.txt') if os.path.exists('scratch/spoken_text.txt') else ''
    anchors = f'Note: This is a 10s tracer slice. Assess quality based on the HTML code and captured spoken text: {captured_text}'
    kit.judge('C9', 'score >= 7', 'slice.html', rubric, anchors, threshold=7)
    
    kit.fault_proof('slice.html')
    kit.verdict()

if __name__ == '__main__':
    main()
