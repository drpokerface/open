import os
import json
import sys
from verify_kit import Kit

kit = Kit()

def check_c1_manifest():
    if not kit.exists("manifest.md"): return False
    text = kit.text("manifest.md").lower()
    if "lorem ipsum" in text or "placeholder" in text or "todo" in text: return False
    ok, _ = kit.no_placeholders("manifest.md")
    if not ok: return False
    if not kit.min_length("manifest.md", 300): return False
    return True

is_manifest_valid = check_c1_manifest()
kit.check("C1", "manifest.md from task 1 is OPENED and VALIDATED FIRST", check_c1_manifest)

def check_c2_json():
    ok, msg = kit.no_placeholders("script.json")
    if not ok: return False
    if not kit.exists("script.json"): return False
    try:
        json.loads(kit.text("script.json"))
        return True
    except:
        return False

kit.check("C2", "script.json exists and is valid JSON", check_c2_json)

def get_script_data():
    if not kit.exists("script.json"): return None
    try:
        return json.loads(kit.text("script.json"))
    except:
        return None

def check_c3_keys():
    data = get_script_data()
    if not data: return False
    items = []
    if isinstance(data, list):
        items = data
    elif isinstance(data, dict):
        items = data.get("script", data.get("dialogue", []))
    if not items: return False
    has_dialogue = False
    for item in items:
        if "subtitle" in item or "text" in item:
            has_dialogue = True
        if item.get("type") == "dialogue" or "pitch" in item or "rate" in item:
            if "pitch" not in item or "rate" not in item:
                return False
    return has_dialogue

kit.check("C3", "script.json has TTS pitch/rate and exact subtitles", check_c3_keys)

def check_c4_gags():
    data = get_script_data()
    if not data: return False
    cutaways = 0
    if isinstance(data, list):
        cutaways = sum(1 for item in data if item.get("type") == "cutaway" or item.get("cutaway") or item.get("cutaway_gag"))
    elif isinstance(data, dict):
        items = data.get("script", data.get("dialogue", []))
        if "cutaway_timestamps" in data:
            cutaways = len(data["cutaway_timestamps"])
        else:
            cutaways = sum(1 for item in items if item.get("type") == "cutaway" or item.get("cutaway") or item.get("cutaway_gag"))
    return cutaways >= 3

kit.check("C4", "script.json contains >= 3 cutaway gag timestamps", check_c4_gags)

def check_c5_duration():
    data = get_script_data()
    if not data: return False
    items = []
    cutaways = 0
    if isinstance(data, list):
        items = data
        cutaways = sum(1 for item in data if item.get("type") == "cutaway" or item.get("cutaway") or item.get("cutaway_gag"))
    elif isinstance(data, dict):
        items = data.get("script", data.get("dialogue", []))
        if "cutaway_timestamps" in data:
            cutaways = len(data["cutaway_timestamps"])
        else:
            cutaways = sum(1 for item in items if item.get("type") == "cutaway" or item.get("cutaway") or item.get("cutaway_gag"))
    text_content = ""
    for item in items:
        if "subtitle" in item:
            text_content += " " + str(item["subtitle"])
        elif "text" in item:
            text_content += " " + str(item["text"])
    words = len(text_content.split())
    duration = (words / 2.5) + (cutaways * 3)
    return 60 <= duration <= 115

kit.check("C5", "script.json duration is 60-115 seconds", check_c5_duration)

if is_manifest_valid:
    rubric = '''Comedic Writing and Original Satire Rubric:
10: Perfection
8: Excellent satire, edgy, distinct characters, unpredictable. MUST explicitly feature >= 3 cutaways.
4: Generic AI text, bland, polite'''
    if os.path.exists("artifacts/board-20260904-202814/constitution.md"):
        with open("artifacts/board-20260904-202814/constitution.md", "r", encoding="utf-8") as f:
            const = f.read()
            if "Dimension 1:" in const:
                rubric += const.split("Dimension 1:")[1].split("Dimension 2:")[0]

    kit.judge("C6", "Satire score >= 8.0, minimum 3 gags", "script.json", rubric, "Anchors: South Park Margaritaville, Family Guy non-sequitur", threshold=8.0, model="gemini-3.1-pro-preview")
else:
    kit.check("C6", "Satire score >= 8.0 (SKIPPED due to invalid manifest)", lambda: False)

kit.fault_proof("manifest.md")
kit.fault_proof("script.json")
kit.verdict()
