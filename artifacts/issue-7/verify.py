# verify.py - VALIDATED: gate rollup
import os, sys, json, random, shutil
from metered import generate

def run_checks(m_path, c_path):
    if not os.path.exists(m_path):
        return False, "C1: 0 (missing manifest)"
    if not os.path.exists(c_path):
        return False, "C2: 0 (missing constitution)"
    
    with open(m_path, 'r', encoding='utf-8') as f:
        m_txt = f.read().strip()
    with open(c_path, 'r', encoding='utf-8') as f:
        c_txt = f.read().strip()
        
    if len(m_txt) < 10 or 'manifest.md' not in m_txt.lower() or 'constitution.md' not in m_txt.lower():
        return False, f"C1: FAIL (degenerate manifest, len={len(m_txt)})"
        
    if len(c_txt) < 500:
        return False, f"C2: FAIL (degenerate constitution, len={len(c_txt)})"
        
    stubs = ['placeholder', 'todo', 'stub', 'insert here']
    if any(stub in c_txt.lower() for stub in stubs):
        return False, "C2: FAIL (stub content detected)"
        
    # C3: Check for rubrics
    p1 = 'Analyze this document. Does it explicitly contain 0-10 rubrics with anchored descriptors (4=bad, 7=pass, 9=excellent) for ALL of: script, audio, visuals, and final assembly? Respond with JSON: {"has_rubrics": true, "explanation": "..."} or false. TEXT:\n' + c_txt
    try:
        res1 = generate("gemini-3.5-flash", p1, config={"response_mime_type": "application/json"}).text
        d1 = json.loads(res1)
        if not d1.get("has_rubrics"):
            return False, f"C3: FAIL (missing rubrics: {d1.get('explanation')})"
    except Exception as e:
        return False, f"C3: FAIL (LLM error: {e})"
        
    # C4: Subjective quality
    p2 = 'Evaluate this Instagram Reel comedy style constitution. We expect a high-quality, professional-level document specifying pacing, editing, comedy structure, original characters, audio requirements, visual rules (9:16 aspect ratio), and 0-10 score sheets. Score the document from 0 to 10 (pass threshold is 8.0). Be critical and strict. Respond with JSON: {"score": 8.5, "explanation": "..."} TEXT:\n' + c_txt
    scores = []
    for _ in range(3):
        try:
            res2 = generate("gemini-3.5-pro", p2, config={"response_mime_type": "application/json"}).text
            d2 = json.loads(res2)
            scores.append(float(d2.get("score", 0)))
        except Exception as e:
            scores.append(0)
    
    scores.sort()
    median_score = scores[1] if len(scores) == 3 else 0
    if median_score < 8.0:
        return False, f"C4: FAIL {median_score} (below threshold 8.0)"
        
    return True, f"C1: PASS\nC2: PASS\nC3: PASS\nC4: PASS ({median_score})"

def main():
    # 1. Fault Proof
    os.makedirs('scratch', exist_ok=True)
    bad_c = 'scratch/bad_c_' + str(random.randint(1000,9999)) + '.md'
    with open(bad_c, 'w', encoding='utf-8') as f:
        f.write('This is a placeholder constitution. It lacks rubrics and details.')
    bad_m = 'scratch/bad_m_' + str(random.randint(1000,9999)) + '.md'
    with open(bad_m, 'w', encoding='utf-8') as f:
        f.write('manifest')
    
    fp_pass, fp_msg = run_checks(bad_m, bad_c)
    if fp_pass:
        print("FAULT-PROOF FAILED: checks passed on bad input!")
        sys.exit(1)
    else:
        print(f"FAULT-PROOF: checks correctly caught degenerate input. Reason: {fp_msg}")
        
    # 2. Actual Checks
    if not os.path.exists('manifest.md') or not os.path.exists('constitution.md'):
        print("Files missing")
        sys.exit(1)
        
    act_pass, act_msg = run_checks('manifest.md', 'constitution.md')
    print(act_msg)
    if not act_pass:
        sys.exit(1)
        
    print("VERDICT: PASS")

if __name__ == '__main__':
    main()
