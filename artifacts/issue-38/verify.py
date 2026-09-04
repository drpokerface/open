import os
from verify_kit import Kit
from metered import generate

kit = Kit()

def check_manifest():
    if not kit.exists("slice.html") or not kit.exists("manifest.md"): return False
    content = kit.text("manifest.md")
    import json
    import re
    match = re.search(r'```(?:json)?\s*(\{.*?\})\s*```', content, re.DOTALL)
    if not match: return False
    try:
        data = json.loads(match.group(1))
        keys = ["version", "characters", "gag_count", "estimated_duration", "cutaway_timestamps"]
        if not all(k in data for k in keys): return False
        if int(data.get("gag_count", 0)) < 3: return False
        return True
    except Exception:
        return False

kit.check("C1", "Files exist and manifest valid", check_manifest)

def check_structure():
    if not kit.exists("slice.html"): return False
    html = kit.text("slice.html")
    struct_ok = "<svg" in html and "@keyframes" in html and "speechSynthesis" in html
    if not struct_ok: return False
    return kit.no_placeholders("slice.html")

kit.check("C2", "HTML contains SVG, keyframes, and speechSynthesis", check_structure)

def check_aspect():
    if not kit.exists("slice.html"): return False
    html = kit.text("slice.html")
    prompt = "Analyze this HTML source code. Does the active CSS strictly constrain the layout or main container to a 9:16 aspect ratio (e.g., using `aspect-ratio: 9/16`, `aspect-ratio: 9 / 16`, or equivalent styling on a utilized element), ignoring any HTML comments, plain text, or unused classes? Answer strictly YES or NO."
    ans = generate("gemini-3.5-flash", [prompt, html]).text
    return isinstance(ans, str) and "YES" in ans.upper()

kit.check("C3", "Enforces 9:16 viewport", check_aspect)

def check_logic():
    if not kit.exists("slice.html"): return False
    prompt = """Analyze this HTML source code for an animated short.
Does it meet ALL these requirements?
1. Has logic to synchronize subtitles with TTS output (e.g., onboundary, setTimeout, or syncing DOM text with utterance).
2. Contains a CSS animation cutaway (a transition or visual switch).
3. The content is NOT a placeholder or stub (has actual dialogue and distinct visual definitions).
Answer strictly YES or NO."""
    ans = generate("gemini-3.5-flash", [prompt, kit.text("slice.html")]).text
    return isinstance(ans, str) and "YES" in ans.upper()

kit.check("C4", "JS syncs subtitles and handles cutaway", check_logic)

rubric = """
We are evaluating an edgy, satirical, relentless 9:16 HTML5 animated scene.
Score 0-10.
10: Genuinely funny, relentless pacing, original edgy character, crude flat-vector style, clear cutaway gag, perfect South Park/Family Guy style satirical bite, strictly no placeholders.
8: Meets the edgy/satirical tone well, has a functional cutaway, crude SVG character, synchronized subtitles logic.
4: Safe, bland, corporate humor, or slow pacing, or missing a cutaway/TTS.
0: Degenerate, broken, placeholder, or completely fails the task.
"""
anchors = """
10: South Park / Family Guy core principles - absurd premise, tight timing, ruthless satire.
8: Original web animations with decent timing and functional gags.
"""

kit.judge("C5", "Quality >= 8", "slice.html", rubric, anchors, threshold=8.0)


def check_capabilities():
    if not kit.exists("capabilities.md"): return False
    text = kit.text("capabilities.md")
    if len(text) < 50: return False
    from metered import generate
    prompt = "Analyze this text. Does it document findings from a capability probe for generation tools (like TTS, models, or browser APIs)? Answer strictly YES or NO."
    ans = generate("gemini-3.5-flash", [prompt, text]).text
    return isinstance(ans, str) and "YES" in ans.upper()

kit.check("C6", "Capabilities probe documented", check_capabilities)

kit.fault_proof("slice.html")
kit.verdict()
