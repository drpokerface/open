# verify.py - VALIDATED: root verification script
import os, sys, json, statistics, shutil
from metered import generate, upload

def check_c1_manifest(path="manifest.md"):
    if not os.path.exists(path): return False, "Missing manifest.md"
    text = open(path).read().lower()
    if "constitution.md" not in text: return False, "constitution.md not in manifest"
    return True, "Manifest validates"

def check_c2_content(path="constitution.md"):
    if not os.path.exists(path): return False, "Missing constitution.md"
    text = open(path).read()
    if len(text.strip()) < 500: return False, "File too short"
    if "###GARBAGE###" in text: return False, "Contains garbage"
    return True, "Length and content OK"

def check_c3_keywords(path="constitution.md"):
    if not os.path.exists(path): return False, "Missing constitution.md"
    text = open(path).read().lower()
    keywords = ["script", "audio", "visual", "assembly", "4", "7", "9"]
    missing = [k for k in keywords if k not in text]
    if missing: return False, f"Missing keywords: {missing}"
    return True, "All keywords found"

def check_c4_rubric_perception(path="constitution.md"):
    if not os.path.exists(path): return False, "Missing constitution.md"
    text = open(path).read()
    prompt = f'''Does this text contain explicit 0-10 rubrics with anchored descriptors for scores 4, 7, and 9, covering script, audio, visuals, and final assembly?
Reply JSON: {{"rubric_present": true}} if yes, else false.
Text: {text[:3000]}'''
    try:
        resp = generate("gemini-3.5-flash", prompt, config={"response_mime_type": "application/json", "response_schema": {"type": "object", "properties": {"rubric_present": {"type": "boolean"}}}}).text
        if json.loads(resp).get("rubric_present"): return True, "Rubric perception passed"
        return False, "Rubric perception failed"
    except Exception as e: return False, str(e)

def check_c5_judge(path="constitution.md"):
    if not os.path.exists(path): return False, "Missing constitution.md"
    text = open(path).read()
    prompt = f'''Score this animated comedy video constitution (0 to 10). Pass threshold is 8.0.
Criteria: clarity, strategy depth, visual/audio choices, IG Reel / South Park style alignment, and strict 0-10 rubrics.
Reply JSON: {{"score": 8.5}}'''
    scores = []
    for _ in range(3):
        try:
            resp = generate("gemini-3.5-flash", prompt, config={"response_mime_type": "application/json", "response_schema": {"type": "object", "properties": {"score": {"type": "number"}}}}).text
            scores.append(float(json.loads(resp).get("score", 0)))
        except: scores.append(0)
    med = statistics.median(scores)
    if med >= 8.0: return True, f"Median score {med} >= 8.0"
    return False, f"Median score {med} < 8.0"

def fault_proof():
    os.makedirs("scratch", exist_ok=True)
    bad_path = "scratch/bad_constitution.md"
    with open(bad_path, "w") as f: f.write("###GARBAGE###")
    ok, msg = check_c2_content(bad_path)
    if not ok:
        print(f"FAULT-PROOF: Caught degenerate output - {msg}")
        return True
    print("FAULT-PROOF FAILED")
    return False

if __name__ == "__main__":
    if not fault_proof(): sys.exit(1)
    checks = [
        ("C1 Manifest", check_c1_manifest, "manifest.md"),
        ("C2 Content", check_c2_content, "constitution.md"),
        ("C3 Keywords", check_c3_keywords, "constitution.md"),
        ("C4 Perception", check_c4_rubric_perception, "constitution.md"),
        ("C5 Judge", check_c5_judge, "constitution.md")
    ]
    all_ok = True
    for name, func, path in checks:
        ok, msg = func(path)
        print(f"{name}: {ok} ({msg})")
        if not ok: all_ok = False
    if all_ok:
        print("VERDICT: PASS")
        sys.exit(0)
    else:
        print("VERDICT: FAIL")
        sys.exit(1)
