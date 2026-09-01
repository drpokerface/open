import warnings, logging, os
warnings.filterwarnings("ignore")
logging.getLogger().setLevel(logging.ERROR)
logging.getLogger("google").setLevel(logging.ERROR)
logging.getLogger("google.genai").setLevel(logging.ERROR)
logging.getLogger("httpx").setLevel(logging.ERROR)
logging.captureWarnings(True)
os.environ["GRPC_VERBOSITY"] = "ERROR"
os.environ["GLOG_minloglevel"] = "3"
# verify.py - VALIDATED: gate rollup
import os
import sys
import random
import shutil
import json

import os, sys
def silence():
    try:
        s_out = os.dup(1)
        s_err = os.dup(2)
        dn = os.open(os.devnull, os.O_WRONLY)
        os.dup2(dn, 1)
        os.dup2(dn, 2)
        return s_out, s_err, dn
    except Exception:
        return None, None, None

def restore(s_out, s_err, dn):
    try:
        if s_out is not None:
            os.dup2(s_out, 1)
            os.close(s_out)
        if s_err is not None:
            os.dup2(s_err, 2)
            os.close(s_err)
        if dn is not None:
            os.close(dn)
    except Exception:
        pass


try:
    s_out, s_err, dn = silence()
    try:
        from metered import generate
    finally:
        restore(s_out, s_err, dn)
except ImportError:
    print("metered not found")
    sys.exit(1)

def verify_artifact(const_path, manifest_path):
    issues = []
    measured = {}
    
    # C1
    if not os.path.exists(const_path):
        issues.append("constitution.md missing")
        measured['C1'] = "missing"
    else:
        with open(const_path, 'r', encoding='utf-8') as f:
            content = f.read()
        words = len(content.split())
        if words <= 150:
            issues.append(f"constitution.md too short ({words} words)")
        measured['C1'] = f"{words} words"
            
    # C2
    if not os.path.exists(manifest_path):
        issues.append("manifest.md missing")
        measured['C2'] = "missing"
    else:
        with open(manifest_path, 'r', encoding='utf-8') as f:
            m_content = f.read()
        if "constitution.md" not in m_content:
            issues.append("manifest.md does not reference constitution")
        measured['C2'] = "present, references constitution" if "constitution.md" in m_content else "present, no reference"

    if issues:
        return False, issues, measured

    content_lower = content.lower()
    
    # C3
    c3_ok = "strategy" in content_lower and "style decisions" in content_lower and "conventions" in content_lower
    measured['C3'] = str(c3_ok)
    if not c3_ok:
        issues.append("missing strategy, style decisions, or conventions sections")

    # C4
    c4_ok = all(x in content_lower for x in ["4", "7", "9", "comedy", "animation", "audio"])
    measured['C4'] = str(c4_ok)
    if not c4_ok:
        issues.append("missing rubric anchors (4,7,9) or dimensions (comedy, animation, audio)")

    # C5
    c5_ok = "8/10" in content_lower or "8 out of 10" in content_lower
    measured['C5'] = str(c5_ok)
    if not c5_ok:
        issues.append("missing 8/10 threshold")

    # C6
    c6_ok = content_lower.count("http") >= 3 or content_lower.count("exemplar") >= 1
    measured['C6'] = str(c6_ok)
    if not c6_ok:
        issues.append("missing exemplars (need links or clear references)")

    if issues:
        return False, issues, measured

    # C7 Perceptual check
    prompt = f"""You are a strict judge evaluating a constitution for an edgy, animated comedy project (like South Park/Family Guy for IG Reels).
Output a JSON object with: {{"score": <0-10>, "reason": "<reason>"}}
Score it 10 if it has crystal clear, actionable guidelines, captures the edgy tone well, and has an excellent anchored rubric.
Score it <8 if it's generic, safe, or vague.
Constitution text:
{content}
"""
    try:
        s_out, s_err, dn = silence()
        try:
            res = generate("gemini-3.5-flash", prompt, config={"response_mime_type": "application/json"})
        finally:
            restore(s_out, s_err, dn)
        data = json.loads(res.text)
        score = data.get("score", 0)
        measured['C7'] = f"Score: {score}"
        if score < 8:
            issues.append(f"Subjective score too low: {score} - {data.get('reason')}")
    except Exception as e:
        issues.append(f"Model call failed: {e}")
        measured['C7'] = "Model call failed"

    if issues:
        return False, issues, measured
    return True, [], measured

def main():
    print("EXPECT: Verify checks all criteria, fails on missing files, and induces fault")
    
    real_const = "constitution.md"
    real_man = "manifest.md"
    
    ok, issues, measured = verify_artifact(real_const, real_man)
    
    for k, v in measured.items():
        print(f"{k}: {v}")
        
    if ok:
        # Fault proof
        os.makedirs("scratch", exist_ok=True)
        bad_const = f"scratch/bad_const_{random.randint(1000,9999)}.md"
        shutil.copy(real_const, bad_const)
        
        # Corrupt it by removing lines that contain '4', '7', or '9'
        with open(bad_const, 'r', encoding='utf-8') as f:
            lines = f.readlines()
        corrupted = [line for line in lines if not any(x in line for x in ['4', '7', '9'])]
        with open(bad_const, 'w', encoding='utf-8') as f:
            f.writelines(corrupted)
            
        ok_f, issues_f, _ = verify_artifact(bad_const, real_man)
        if not ok_f:
            print("FAULT-PROOF: Caught corrupted constitution missing rubric anchors. Issues:", issues_f)
            print("VERDICT: PASS")
            sys.exit(0)
        else:
            print("FAULT-PROOF: FAILED to catch corrupted file.")
            sys.exit(1)
    else:
        print("VERDICT: FAIL")
        print("Issues:", issues)
        sys.exit(1)

if __name__ == '__main__':
    main()
