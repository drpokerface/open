import os
import json
from verify_kit import Kit

kit = Kit()

def check_c1():
    if not kit.exists("script.json"):
        return False
    try:
        json.loads(kit.text("script.json"))
        return True
    except:
        return False

kit.check("C1", "script.json exists and is valid JSON", check_c1)

def get_script_data():
    if not kit.exists("script.json"): return None
    try:
        return json.loads(kit.text("script.json"))
    except:
        return None

def check_c2():
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
            if not ("pitch" in item and "rate" in item and "character" in item):
                return False
    return has_dialogue

kit.check("C2", "script.json contains required TTS keys", check_c2)

def check_c3():
    data = get_script_data()
    if not data: return False
    cutaways = 0
    if isinstance(data, list):
        cutaways = sum(1 for item in data if item.get("type") == "cutaway" or item.get("cutaway"))
    elif isinstance(data, dict):
        if "cutaway_timestamps" in data:
            cutaways = len(data["cutaway_timestamps"])
        elif "cutaways" in data:
            cutaways = len(data["cutaways"])
        else:
            items = data.get("script", data.get("dialogue", []))
            cutaways = sum(1 for item in items if item.get("type") == "cutaway" or item.get("cutaway"))
    return cutaways >= 3

kit.check("C3", "script.json contains >= 3 cutaways", check_c3)

def check_c4():
    data = get_script_data()
    if not data: return False
    items = []
    cutaways = 0
    if isinstance(data, list):
        items = data
        cutaways = sum(1 for item in data if item.get("type") == "cutaway" or item.get("cutaway"))
    elif isinstance(data, dict):
        items = data.get("script", data.get("dialogue", []))
        if "cutaway_timestamps" in data:
            cutaways = len(data["cutaway_timestamps"])
        else:
            cutaways = sum(1 for item in items if item.get("type") == "cutaway" or item.get("cutaway"))
    text_content = ""
    for item in items:
        if "subtitle" in item:
            text_content += " " + str(item["subtitle"])
        elif "text" in item:
            text_content += " " + str(item["text"])
    words = len(text_content.split())
    duration = (words / 2.5) + (cutaways * 3)
    return 60 <= duration <= 115

kit.check("C4", "script.json duration is 60-115 seconds", check_c4)

rubric = "Comedic Writing and Original Satire Rubric:
10: Perfection
8: Excellent satire, edgy, distinct characters, unpredictable
4: Generic AI text, bland, polite"
if os.path.exists("artifacts/board-20260904-202814/constitution.md"):
    with open("artifacts/board-20260904-202814/constitution.md", "r", encoding="utf-8") as f:
        const = f.read()
        if "Dimension 1:" in const:
            rubric += const.split("Dimension 1:")[1].split("Dimension 2:")[0]

kit.judge("C5", "Satire score >= 8.0", "script.json", rubric, "Anchors: South Park Margaritaville, Family Guy non-sequitur", threshold=8.0, model="gemini-3.1-pro-preview")

kit.check("C6", "manifest.md exists", lambda: kit.exists("manifest.md"))

kit.fault_proof("script.json")
kit.verdict()
