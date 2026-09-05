import os
import sys
import subprocess
import json
import re
import hashlib
from html.parser import HTMLParser
from verify_kit import Kit

def ensure_playwright():
    try:
        import playwright
    except ImportError:
        subprocess.run([sys.executable, "-m", "pip", "install", "playwright", "--quiet"], check=True)
    if not os.path.exists("scratch/pw_installed"):
        subprocess.run([sys.executable, "-m", "playwright", "install", "chromium"], check=False)
        os.makedirs("scratch", exist_ok=True)
        with open("scratch/pw_installed", "w") as f: f.write("yes")

ensure_playwright()
kit = Kit()

browser_res_cache = {}
def get_browser():
    text = kit.raw("slice.html") if kit.exists("slice.html") else b""
    h = hashlib.md5(text).hexdigest()
    if h not in browser_res_cache:
        for f in ["scratch/1_before_click.png", "scratch/2_after_click.png", "scratch/3_after_cut.png", "scratch/browser_logs.txt"]:
            if os.path.exists(f): 
                try: os.remove(f)
                except: pass
        if not text:
            browser_res_cache[h] = {'speech_before': False, 'speech_after': False, 'images': [], 'logs': [], 'aspect_ratio_ok': False}
            with open("scratch/browser_logs.txt", "w") as f: f.write("")
        else:
            from playwright.sync_api import sync_playwright
            import threading
            import http.server
            import socketserver
            import socket
            
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                s.bind(("", 0))
                port = s.getsockname()[1]
                
            class Handler(http.server.SimpleHTTPRequestHandler):
                def log_message(self, format, *args): pass
            httpd = socketserver.TCPServer(("", port), Handler)
            thread = threading.Thread(target=httpd.serve_forever)
            thread.daemon = True
            thread.start()
            
            res = {'speech_before': False, 'speech_after': False, 'images': [], 'logs': [], 'aspect_ratio_ok': False}
            try:
                with sync_playwright() as p:
                    browser = p.chromium.launch(headless=True)
                    context = browser.new_context(viewport={'width': 360, 'height': 640})
                    page = context.new_page()
                    
                    init_script = """
                    window.speechSynthesis.speak = (function(orig) {
                        return function(utterance) {
                            console.log('speechSynthesis triggered');
                            utterance.addEventListener('start', () => console.log('speech start'));
                            utterance.addEventListener('end', () => console.log('speech end'));
                            return orig.apply(this, arguments);
                        };
                    })(window.speechSynthesis.speak);
                    
                    window.addEventListener('DOMContentLoaded', () => {
                        const observer = new MutationObserver(mutations => {
                            for (let m of mutations) {
                                if (m.type === 'attributes' && m.attributeName === 'class') {
                                    console.log('DOM class changed: ' + (m.target.getAttribute('class') || ''));
                                }
                            }
                        });
                        observer.observe(document.documentElement, {attributes: true, subtree: true});
                    });
                    """
                    page.add_init_script(init_script)
                    
                    logs = []
                    page.on("console", lambda msg: logs.append(msg.text))
                    
                    page.goto(f"http://localhost:{port}/slice.html")
                    page.wait_for_timeout(1000)
                    
                    res['speech_before'] = any("speechSynthesis triggered" in l for l in logs)
                    
                    os.makedirs("scratch", exist_ok=True)
                    page.screenshot(path="scratch/1_before_click.png")
                    
                    ar_script = "window.getComputedStyle(document.body).aspectRatio"
                    ar = page.evaluate(ar_script)
                    res['aspect_ratio_ok'] = ('9 / 16' in str(ar) or '0.5625' in str(ar) or '360' in str(ar))
                    
                    try:
                        page.mouse.click(180, 320)
                        page.wait_for_timeout(2000)
                    except:
                        pass
                    
                    res['speech_after'] = any("speechSynthesis triggered" in l for l in logs)
                    
                    page.screenshot(path="scratch/2_after_click.png")
                    
                    page.wait_for_timeout(5000)
                    page.screenshot(path="scratch/3_after_cut.png")
                    
                    res['images'] = ["scratch/1_before_click.png", "scratch/2_after_click.png", "scratch/3_after_cut.png"]
                    res['logs'] = logs
                    with open("scratch/browser_logs.txt", "w") as f:
                        f.write("\n".join(logs))
                    browser.close()
            except Exception as e:
                print(f"Browser test failed: {e}")
                with open("scratch/browser_logs.txt", "w") as f: f.write(f"Browser test failed: {e}")
            finally:
                httpd.shutdown()
                httpd.server_close()
            browser_res_cache[h] = res
    return browser_res_cache[h]

# C1
kit.check("C1", "capabilities.md content exists", lambda: kit.exists("capabilities.md") and len(kit.text("capabilities.md")) > 0)

# C2
def c2():
    if not kit.min_length("slice.html", 3000): return False
    if not kit.exists("slice.html"): return False
    if not hasattr(kit, "no_placeholders") or not kit.no_placeholders("slice.html")[0]: return False
    class MP(HTMLParser):
        def handle_error(self, m): raise ValueError(m)
    try:
        p = MP()
        p.feed(kit.text("slice.html"))
        return True
    except: return False
kit.check("C2", "slice.html is valid HTML", c2)

# C3
def c3():
    if not kit.exists("slice.html"): return False
    if not hasattr(kit, "no_placeholders") or not kit.no_placeholders("slice.html")[0]: return False
    text = kit.text("slice.html")
    has_script = bool(re.search(r'<script[^>]+src\s*=', text, re.I))
    has_link = bool(re.search(r'<link[^>]+href\s*=', text, re.I))
    has_img = bool(re.search(r'<img[^>]+src\s*=\s*["\']http', text, re.I))
    return not (has_script or has_link or has_img)
kit.check("C3", "zero external resources", c3)

# C4
kit.check("C4", "autoplay gating requiring user interaction", lambda: get_browser().get('speech_after') and not get_browser().get('speech_before'))

# C5
def c5():
    if not kit.exists("slice.html"): return False
    if not hasattr(kit, "no_placeholders") or not kit.no_placeholders("slice.html")[0]: return False
    text = kit.text("slice.html")
    has_css = "aspect-ratio: 9/16" in text or "aspect-ratio: 9 / 16" in text or "aspect-ratio:9/16" in text or "aspect-ratio: 0.5625" in text
    return has_css or get_browser().get('aspect_ratio_ok')
kit.check("C5", "strict 9:16 aspect ratio", c5)

# C6
kit.perceive("C6", "visual rendering confirms 'Tap to Play' overlay, crude SVG character, and 1 cut", ["scratch/1_before_click.png", "scratch/2_after_click.png", "scratch/3_after_cut.png"], "Look at the sequence of 3 screenshots. 1. Does the first show a massive 'Tap to Play' overlay blocking content? 2. Does the second show a crude SVG character? 3. Does the third show a distinct visual scene cut compared to the second? (Answer yes if all 3 are met)")

# C7
def c7():
    if not kit.exists("slice.html"): return False
    if not hasattr(kit, "no_placeholders") or not kit.no_placeholders("slice.html")[0]: return False
    logs = get_browser().get('logs', [])
    speech_idx = -1
    for i, l in enumerate(logs):
        if "speechSynthesis triggered" in l or "speech start" in l:
            speech_idx = i
            break
    if speech_idx == -1: return False
    return any("DOM class changed" in l for l in logs[speech_idx:])
kit.check("C7", "mouth animation synced with speech", c7)

# C8
def c8():
    if not kit.exists("manifest.md"): return False
    try:
        text = kit.text("manifest.md")
        json_str = re.search(r'```json\s*(\{.*?\})\s*```', text, re.DOTALL)
        if not json_str: return False
        data = json.loads(json_str.group(1))
        return "runtime" in data and "start_overlay" in data and "speech_settings" in data and "timeline" in data
    except:
        return False
kit.check("C8", "manifest.md contains valid JSON contract", c8)

# C9
const_text = kit.text("artifacts/board-20260905-114048/constitution.md") if kit.exists("artifacts/board-20260905-114048/constitution.md") else ""
rubric_c9 = f"""
Evaluate if slice.html perfectly aligns with this GOAL CONSTITUTION:
{const_text}
Specifically, unapologetic absurdist humor and crude animation styling like early South Park or Family Guy.
Score 0-10.
"""
kit.judge("C9", "strictly aligns with constitution.md guidelines", "slice.html", rubric_c9, "Anchor: 9 is perfect alignment.", threshold=8)

# C10
rubric_c10 = """
Technical Execution Rubric (0-10):
4: Basic HTML, missing CSS animations or Web Speech API triggers.
7: Functional Web Speech API and simple visuals, but timing is off or autoplay fails.
9: Perfect zero-dependency execution: 'Tap to Play' works, speech plays, mouth flaps precisely with audio, 9:16 aspect ratio enforced, distinct cut happens.
"""
kit.judge("C10", "technical execution score >= 8.0/10", ["scratch/1_before_click.png", "scratch/2_after_click.png", "scratch/3_after_cut.png", "scratch/browser_logs.txt"], rubric_c10, "Anchor: 9 is perfect execution as defined.", threshold=8)

kit.fault_proof("slice.html")
kit.verdict()
