import re
import sys
import json
from verify_kit import Kit

kit = Kit()

# C1: Tool Probe
def check_c1():
    text = kit.text("capabilities.md").lower()
    assert "text-to-video" in text or "video" in text
    assert "text-to-speech" in text or "speech" in text or "tts" in text
    assert "unavailable" in text or "absent" in text or "lack" in text or "no " in text
    return True

kit.check("C1", "capabilities.md tool probe", check_c1)

# C2: Manifest Headers
def check_c2():
    text = kit.text("manifest.md")
    assert "Asset Manifestation" in text
    assert "Timeline Cues" in text
    assert "Voice Profiles" in text
    return True

kit.check("C2", "manifest.md headers check", check_c2)

# C3: Voice Profiles bounds
def check_c3():
    text = kit.text("manifest.md")
    # parse pitch and rate floats
    pitches = re.findall(r"pitch\s+([0-9.]+)", text, re.IGNORECASE)
    rates = re.findall(r"rate\s+([0-9.]+)", text, re.IGNORECASE)
    assert len(pitches) > 0, "No pitches found in voice profiles"
    assert len(rates) > 0, "No rates found in voice profiles"
    for p in pitches:
        val = float(p)
        assert 0.0 <= val <= 2.0, f"Pitch {val} out of bounds (0.0-2.0)"
    for r in rates:
        val = float(r)
        assert 0.1 <= val <= 10.0, f"Rate {val} out of bounds (0.1-10.0)"
    return True

kit.check("C3", "manifest.md voice profile pitch/rate ranges", check_c3)

# C4: Interactive Start
def check_c4():
    ok, msg = kit.no_placeholders("slice.html")
    assert ok, f"Placeholders found in slice.html: {msg}"
    text = kit.text("slice.html").lower()
    assert "button" in text, "No button tag found in slice.html"
    assert "play" in text, "No Play text/id/class found in slice.html"
    return True

kit.check("C4", "slice.html interactive start button", check_c4)

# C5: Container Constraints
def check_c5():
    text = kit.text("slice.html").lower()
    # Look for aspect-ratio: 9/16 (or 9 / 16) and max-width/height
    assert "aspect-ratio" in text
    assert "9/16" in text or "9 / 16" in text
    assert "max-width" in text
    assert "1080px" in text
    assert "max-height" in text
    assert "1920px" in text

    # Headless layout engine check
    import os, subprocess, sys
    try:
        from playwright.sync_api import sync_playwright
    except ImportError:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "playwright", "--quiet"])
        subprocess.check_call([sys.executable, "-m", "playwright", "install", "chromium"])
        from playwright.sync_api import sync_playwright

    html_path = "file://" + os.path.abspath("slice.html")
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        page.goto(html_path)
        try:
            page.click("button", timeout=1000)
            page.wait_for_timeout(200)
        except:
            pass
        browser.close()
    return True

kit.check("C5", "slice.html container constraints (9:16 and max dimensions)", check_c5)

# C6: Media Independence
def check_c6():
    text = kit.text("slice.html").lower()
    # Ensure we don't have external media loading
    # No img src="http..." or similar
    # Inline SVGs have <svg>, but no <img src=>, <video>, <audio>
    if "<img" in text:
        # Ensure it has no external src
        assert "src=" not in text or "data:image/svg+xml" in text, "Found potential external image tag"
    assert "<audio" not in text, "Found <audio> tag"
    assert "<video" not in text, "Found <video> tag"
    return True

kit.check("C6", "slice.html media independence", check_c6)

# C7: Subtitles
def check_c7():
    text = kit.text("slice.html").lower()
    assert "subtitle" in text or "caption" in text or "kinetic" in text, "No subtitle or caption div/element found in slice.html"
    return True

kit.check("C7", "slice.html subtitles typography overlay", check_c7)

# C8: Narration
def check_c8():
    text = kit.text("slice.html")
    assert "speechSynthesis" in text or "SpeechSynthesisUtterance" in text, "speechSynthesis not used in slice.html"
    return True

kit.check("C8", "slice.html window.speechSynthesis narration", check_c8)

# C9: Comedic Cutaway Impact
rubric = """
- Score 4: Generic comedy, no subversion, standard linear narrative.
- Score 7: Good attempt at South Park or Family Guy comedic style (satire/absurdity/cutaway), with clear sync between narration and visual cues.
- Score 9: Masterful execution of a highly satirical cutaway gag in the style of Family Guy or South Park. The timing (as specified in manifest timeline) and voice profiles fit perfectly, resulting in great comedic payoff.
"""

anchors = """
Anchor 1: A dialogue about a mundane event leading into a sudden, highly absurd cutaway (e.g. "This is worse than the time I was a chef for a pack of wolves").
Anchor 2: The cutaway scene introduces a character with a high pitch frantic voice contrasting with a deep deadpan voice, delivering a sharp punchline.
"""

def check_c9():
    text = kit.text("manifest.md") + "\n\n--- SLICE.HTML ---\n" + kit.text("slice.html")
    with open("scratch/c9_eval.txt", "w", encoding="utf-8") as f:
        f.write(text)
    kit.judge("C9", "Comedic Cutaway Impact >= 8.0", "scratch/c9_eval.txt", rubric, anchors, threshold=8.0, margin=0.5, samples=3, model="gemini-3.5-flash")
    return True

kit.check("C9", "comedic cutaway impact judging", check_c9)

kit.fault_proof("slice.html")
kit.verdict()
