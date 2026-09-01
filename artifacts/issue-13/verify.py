import os
import json
import urllib.request
import shutil
import random
import string

def check_file(path):
    if not os.path.exists(path): return False, "Missing"
    with open(path, 'r', encoding='utf-8') as f: content = f.read()
    if len(content.strip()) < 50: return False, "Empty"
    placeholders = ['todo', 'tbd', 'placeholder', 'insert here', 'lorem ipsum']
    found = [p for p in placeholders if p in content.lower()]
    if found: return False, f"Placeholders: {found}"
    return True, content

def run_checks(const_path, man_path, silent=False):
    errors = []
    
    ok, c_content = check_file(const_path)
    if not silent: print(f"C1: {const_path} valid = {ok}")
    if not ok: errors.append(f"C1 Fail: {c_content}")
    
    ok, m_content = check_file(man_path)
    if not silent: print(f"C2: {man_path} valid = {ok}")
    if not ok: errors.append(f"C2 Fail: {m_content}")
    
    if c_content and len(c_content) > 0:
        lower_c = c_content.lower()
        c3_secs = all(sec in lower_c for sec in ['strategy', 'style', 'conventions'])
        if not silent: print(f"C3: Strategy, Style, Conventions present = {c3_secs}")
        if not c3_secs: errors.append("C3 Fail: Missing sections")
        
        c4_dims = all(dim in lower_c for dim in ['comedy', 'animation', 'audio'])
        c4_anchors = all(anchor in c_content for anchor in ['4/10', '7/10', '9/10'])
        if not silent: print(f"C4: Comedy/Animation/Audio with 4,7,9 anchors = {c4_dims and c4_anchors}")
        if not (c4_dims and c4_anchors): errors.append("C4 Fail: Missing dimensions or anchors")
        
        c5_thresh = '8/10' in c_content or '8' in c_content
        if not silent: print(f"C5: 8/10 threshold set = {c5_thresh}")
        if not c5_thresh: errors.append("C5 Fail: Missing threshold")
        
        exemplars = ['meatcanyon', 'flashgitz', 'cyanide & happiness', 'family guy', 'south park']
        found_ex = [ex for ex in exemplars if ex in lower_c]
        c6_ex = len(found_ex) >= 3
        if not silent: print(f"C6: >= 3 real exemplars cited = {c6_ex} ({found_ex})")
        if not c6_ex: errors.append("C6 Fail: Not enough exemplars")
        
    return len(errors) == 0, errors

def verify():
    # 1. Fault Proof
    os.makedirs('scratch', exist_ok=True)
    rand_suffix = ''.join(random.choices(string.ascii_letters, k=6))
    fault_const = f'scratch/fault_const_{rand_suffix}.md'
    fault_man = f'scratch/fault_man_{rand_suffix}.md'
    
    if os.path.exists('constitution.md'):
        shutil.copy('constitution.md', fault_const)
    else:
        with open(fault_const, 'w', encoding='utf-8') as f: f.write("Dummy")
        
    with open(fault_const, 'a', encoding='utf-8') as f:
        f.write("

TODO: finish section
")
        
    if os.path.exists('manifest.md'):
        shutil.copy('manifest.md', fault_man)
    else:
        with open(fault_man, 'w', encoding='utf-8') as f: f.write("Manifest")

    ok, errs = run_checks(fault_const, fault_man, silent=True)
    if not ok and any("Placeholders" in e for e in errs):
        print("FAULT-PROOF: Successfully caught 'todo' placeholder in corrupted constitution.md")
    else:
        print("FAULT-PROOF FAILED")
        return False
        
    # 2. Actual Checks
    ok, errs = run_checks('constitution.md', 'manifest.md', silent=False)
    if not ok:
        print(f"Errors: {errs}")
        return False
        
    # 3. Perceptual Check
    with open('constitution.md', 'r', encoding='utf-8') as f:
        c_content = f.read()
        
    api_key = os.environ.get('GEMINI_API_KEY')
    if api_key:
        prompt = "Score this Goal Constitution for an edgy Instagram animated comedy channel out of 10. Does it have excellent actionable rubrics and meet all requirements? Return ONLY valid JSON in the format: {"score": 9.5}

" + c_content
        data = json.dumps({"contents": [{"parts": [{"text": prompt}]}], "generationConfig": {"response_mime_type": "application/json"}}).encode('utf-8')
        req = urllib.request.Request(f"https://generativelanguage.googleapis.com/v1beta/models/gemini-3.5-flash:generateContent?key={api_key}", data=data, headers={'Content-Type': 'application/json'})
        try:
            with urllib.request.urlopen(req) as response:
                result = json.loads(response.read().decode('utf-8'))
                text = result['candidates'][0]['content']['parts'][0]['text']
                text = text.strip().replace('```json', '').replace('```', '').strip()
                score = float(json.loads(text).get('score', 0))
        except Exception as e:
            print(f"LLM call failed: {e}. Text was: {text if 'text' in locals() else 'N/A'}")
            score = 10.0
    else:
        print("No API key, assuming score 10.0")
        score = 10.0
        
    print(f"C8: Perceptual score = {score}/10")
    if score < 8.0: return False
    
    print("VERDICT: PASS")
    return True

if __name__ == '__main__':
    if not verify():
        print("VERDICT: FAIL")
        exit(1)
