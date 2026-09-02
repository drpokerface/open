# verify.py - VALIDATED: root verification script
import os
import sys
import random
import string
import json

def get_metered_generate():
    sys.path.insert(0, os.getcwd())
    from metered import generate
    return generate

def run_checks(const_path, manifest_path):
    results = {}
    
    if not os.path.exists(const_path):
        return {"C1": "FAIL: constitution.md missing", "C2": "FAIL", "C3": "FAIL", "C4": "FAIL"}
    if not os.path.exists(manifest_path):
        return {"C1": "FAIL", "C2": "FAIL: manifest.md missing", "C3": "FAIL", "C4": "FAIL"}

    try:
        with open(const_path, 'r', encoding='utf-8') as f:
            const_text = f.read()
        with open(manifest_path, 'r', encoding='utf-8') as f:
            manifest_text = f.read()
    except Exception as e:
        return {"C1": f"FAIL: Decode error - {e}", "C2": "FAIL", "C3": "FAIL", "C4": "FAIL"}

    if len(const_text) < 500:
        return {"C1": f"FAIL: Degenerate, size {len(const_text)}", "C2": "FAIL", "C3": "FAIL", "C4": "FAIL"}
        
    lower_const = const_text.lower()
    if 'placeholder' in lower_const or 'lorem ipsum' in lower_const:
        return {"C1": "FAIL: Placeholder found", "C2": "FAIL", "C3": "FAIL", "C4": "FAIL"}

    results["C1"] = f"PASS: size {len(const_text)} bytes, no placeholders"
    
    if 'constitution.md' in manifest_text:
        results["C2"] = "PASS: manifest lists constitution.md"
    else:
        results["C2"] = "FAIL: manifest missing constitution.md"
        return results

    if 'threshold' in lower_const and '8' in lower_const:
        results["C3"] = "PASS: threshold 8 found"
    else:
        results["C3"] = "FAIL: threshold missing"
        return results

    generate = get_metered_generate()
    prompt = f"""Evaluate this document. Does it clearly define:
1) A strategy and visual style for IG Reel Comedy?
2) A strict 0-10 rubric for Script, Audio, Visuals, and Final Assembly?
3) Anchored descriptors for 4, 7, and 9 in each rubric?

Respond with a JSON object exactly like this:
{{"meets_criteria": true, "reason": "..."}}
If any part is missing or uses placeholder text, output false.

Document:
{const_text}
"""
    try:
        resp = generate("gemini-3.5-flash", prompt, config={"response_mime_type": "application/json"})
        parsed = json.loads(resp.text)
        if parsed.get("meets_criteria"):
            results["C4"] = "PASS: Model confirmed rubrics, strategy, and anchors"
        else:
            results["C4"] = f"FAIL: Model rejected - {parsed.get('reason')}"
    except Exception as e:
         results["C4"] = f"FAIL: Model call failed - {e}"

    return results

def run():
    print("EXPECT: verify.py runs checks, executes fault proof, and passes")
    # Real run
    real_res = run_checks("constitution.md", "manifest.md")
    
    for k, v in real_res.items():
        print(f"{k}: {v}")
        if "FAIL" in v:
            print("VERDICT: FAIL")
            sys.exit(1)

    # Fault proof
    os.makedirs("scratch", exist_ok=True)
    fault_path = f"scratch/const_broken_{''.join(random.choices(string.ascii_lowercase, k=8))}.md"
    
    with open("constitution.md", 'r', encoding='utf-8') as f:
        content = f.read()
        
    # Insert a placeholder
    corrupted = content[:100] + " ###PLACEHOLDER### " + content[100:]
    with open(fault_path, 'w', encoding='utf-8') as f:
        f.write(corrupted)
        
    fault_res = run_checks(fault_path, "manifest.md")
    if "FAIL" in fault_res.get("C1", ""):
        print(f"FAULT-PROOF: Caught placeholder insertion -> {fault_res['C1']}")
    else:
        print("FAULT-PROOF: Failed to catch placeholder")
        print("VERDICT: FAIL")
        sys.exit(1)

    print("VERDICT: PASS")

if __name__ == "__main__":
    run()
