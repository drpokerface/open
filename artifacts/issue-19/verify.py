# verify.py - VALIDATED: verify the constitution.md and manifest.md against the criteria.
import os
import re
import sys
import json

# Bootstrap metered
sys.path.append(os.getcwd())
from metered import generate

def check_c1(path):
    if not os.path.exists(path):
        return False, "File does not exist"
    return True, "Exists"

def check_c2(path):
    try:
        with open(path, 'r', encoding='utf-8') as f:
            content = f.read()
        if len(content.strip()) < 100:
            return False, "Too short to be a valid constitution / degenerate"
        if not re.search(r'#{1,4}\s+', content):
            return False, "No markdown headings found"
        if len(set(content)) < 15:
            return False, "Content is degenerate/uniform"
        return True, "Decodes as valid markdown"
    except Exception as e:
        return False, f"Decode error: {e}"

def check_c3(path):
    try:
        with open(path, 'r', encoding='utf-8') as f:
            content = f.read()
        if not re.search(r'(score|rubric|rating).*4', content, re.I | re.DOTALL):
            return False, "Missing score 4 description"
        if not re.search(r'(score|rubric|rating).*7', content, re.I | re.DOTALL):
            return False, "Missing score 7 description"
        if not re.search(r'(score|rubric|rating).*9', content, re.I | re.DOTALL):
            return False, "Missing score 9 description"
        return True, "Contains 4/7/9 rubric sections"
    except Exception as e:
        return False, str(e)

def check_c4(path):
    try:
        with open(path, 'r', encoding='utf-8') as f:
            content = f.read()
        if not re.search(r'(pass\s+threshold|threshold\s+(to\s+pass|is)|minimum\s+score).*7', content, re.I):
            return False, "Does not explicitly state pass threshold is 7"
        return True, "Threshold 7 specified"
    except Exception as e:
        return False, str(e)

def check_c5(path):
    try:
        with open(path, 'r', encoding='utf-8') as f:
            content = f.read().lower()
        placeholders = ['placeholder', 'stub', 'tbd', 'insert here', 'lorem ipsum', '[insert']
        for p in placeholders:
            if p in content:
                return False, f"Contains placeholder: '{p}'"
        return True, "No placeholders found"
    except Exception as e:
        return False, str(e)

def check_c6(path):
    if not os.path.exists(path):
        return False, "manifest.md missing"
    try:
        with open(path, 'r', encoding='utf-8') as f:
            content = f.read()
            content_lower = content.lower()
        if len(content.strip()) < 20:
             return False, "manifest.md is empty or too short"
        if 'constitution.md' not in content_lower or 'manifest.md' not in content_lower:
            return False, "Missing exact filenames"
        if 'format' not in content_lower and 'markdown' not in content_lower:
            return False, "Missing format details"
        if 'sample' not in content_lower and 'example' not in content_lower and '##' not in content:
            return False, "Missing tiny sample"
        return True, "manifest.md is valid"
    except Exception as e:
        return False, str(e)

def check_c7(path):
    try:
        with open(path, 'r', encoding='utf-8') as f:
            text = f.read()
        prompt = f'''You are an expert director grading a Goal Constitution for a Family Guy / South Park style animated short.
Does it provide clear, actionable direction, concrete 4/7/9 rubrics, and a specialized philosophy?
DOCUMENT:
{text}

Respond in JSON:
{{
  "score": <0.0-10.0>,
  "justification": "<one sentence>"
}}'''
        res = generate("gemini-3.5-flash", prompt, config={"response_mime_type": "application/json"}).text
        data = json.loads(res)
        score = float(data.get("score", 0))
        if score >= 7.0:
            return True, f"Score {score}: {data.get('justification')}"
        return False, f"Score {score} < 7.0: {data.get('justification')}"
    except Exception as e:
        return False, f"Model error: {e}"

def perform_fault_proof():
    os.makedirs("scratch", exist_ok=True)
    bad_const = "scratch/bad_const.md"
    with open(bad_const, "w", encoding="utf-8") as f:
        f.write("# Constitution\n\nThis is a placeholder for the real text.")
    
    ok, msg = check_c5(bad_const)
    if ok:
        print("FAULT-PROOF FAILED: C5 missed placeholder")
        sys.exit(1)
    else:
        print(f"FAULT-PROOF: check_c5 caught fault correctly - {msg}")

def main():
    print("EXPECT: All tests pass and print VERDICT: PASS if artifacts are correct")
    
    constitution_path = "constitution.md"
    manifest_path = "manifest.md"

    checks = [
        ("C1: constitution.md exists", lambda: check_c1(constitution_path)),
        ("C2: valid markdown, not degenerate", lambda: check_c2(constitution_path)),
        ("C3: contains 4/7/9 rubrics", lambda: check_c3(constitution_path)),
        ("C4: pass threshold 7", lambda: check_c4(constitution_path)),
        ("C5: no placeholders", lambda: check_c5(constitution_path)),
        ("C6: manifest.md valid", lambda: check_c6(manifest_path)),
        ("C7: quality >= 7.0", lambda: check_c7(constitution_path))
    ]

    all_passed = True
    for name, check_fn in checks:
        passed, msg = check_fn()
        status = "PASS" if passed else "FAIL"
        print(f"{name} -> {status}: {msg}")
        if not passed:
            all_passed = False

    perform_fault_proof()

    if all_passed:
        print("VERDICT: PASS")
        sys.exit(0)
    else:
        print("VERDICT: FAIL")
        sys.exit(1)

if __name__ == "__main__":
    main()
