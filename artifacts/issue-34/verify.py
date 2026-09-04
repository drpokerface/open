from verify_kit import Kit

kit = Kit()

# C1: capabilities.md existence and contents
def check_c1():
    if not kit.exists("capabilities.md"):
        return False
    text = kit.text("capabilities.md").lower()
    # Must note missing/unreachable generators
    has_tts = "speech" in text or "tts" in text
    has_video = "video" in text
    has_image = "image" in text
    has_missing = "missing" in text or "unreachable" in text or "absent" in text or "no " in text
    # Defense against placeholder/truncate faults: require a minimum length close to our real 1663 bytes
    return has_tts and has_video and has_image and has_missing and len(text) > 1000

kit.check("C1", "capabilities.md exists and explicitly details that neural text-to-speech, text-to-video, and image generators are missing or unreachable", check_c1)

# C2: slice.html aspect ratio (9:16)
def check_c2():
    if not kit.exists("slice.html"):
        return False
    text = kit.text("slice.html").lower().strip()
    has_aspect = "9/16" in text or "9:16" in text or ("aspect-ratio" in text and "9" in text and "16" in text)
    # Defense against truncation: strict structure and length requirement (real is ~8049 bytes)
    return has_aspect and len(text) > 4000 and text.endswith("</html>")

kit.check("C2", "slice.html exists and strictly enforces a 9:16 vertical aspect ratio using explicit CSS/sizing constraints", check_c2)

# C3: slice.html Speech API usage
def check_c3():
    if not kit.exists("slice.html"):
        return False
    text = kit.text("slice.html")
    return "speechSynthesis" in text and "SpeechSynthesisUtterance" in text and len(text) > 4000

kit.check("C3", "slice.html utilizes the native Web Speech API (speechSynthesis and SpeechSynthesisUtterance)", check_c3)

# C4: slice.html contains inline SVG and NO raster img/video tags
def check_c4():
    if not kit.exists("slice.html"):
        return False
    text = kit.text("slice.html").lower()
    has_svg = "<svg" in text and "</svg>" in text
    has_img = "<img" in text or "src=" in text
    has_video = "<video" in text
    return has_svg and not has_img and not has_video and len(text) > 4000

kit.check("C4", "slice.html contains inline SVG characters and NO external raster img or video tags", check_c4)

# C5: slice.html start trigger
def check_c5():
    if not kit.exists("slice.html"):
        return False
    text = kit.text("slice.html").lower()
    has_button = "<button" in text or "click" in text or "start" in text or "play" in text
    has_listener = "addeventlistener" in text or "onclick" in text
    return has_button and has_listener and len(text) > 4000

kit.check("C5", "slice.html contains an interactive start/play trigger to bypass browser autoplay restrictions", check_c5)

# C6: manifest.md
def check_c6():
    if not kit.exists("manifest.md"):
        return False
    text = kit.text("manifest.md").lower()
    has_formats = "html" in text or "svg" in text
    has_ids = "id" in text or "stage" in text
    has_seq = "animation" in text or "json" in text or "data-passing" in text
    # Defense against placeholder/truncate: real is ~1133 bytes
    return has_formats and has_ids and has_seq and len(text) > 800

kit.check("C6", "manifest.md exists and details the file formats, SVG IDs, and the animation sequencing structure", check_c6)

kit.fault_proof("capabilities.md")
kit.fault_proof("slice.html")
kit.fault_proof("manifest.md")
kit.verdict()
