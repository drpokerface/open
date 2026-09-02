import os
import random
import shutil
import json
import sys

try:
    from metered import generate
except ImportError:
    print("metered module not found")
    sys.exit(1)

def run_checks(const_path, manifest_path):
    issues = []
    claims = {}
    
    if not os.path.exists(manifest_path):
        issues.append(f"manifest missing: {manifest_path}")
    else:
        with open(manifest_path, 'r', encoding='utf-8') as f:
            text = f.read()
            if len(text.strip()) < 10 or 'manifest.md' not in text:
                issues.append("manifest.md is degenerate")
            if "lorem" in text.lower() or "[insert" in text.lower():
                issues.append("manifest.md has placeholders")
        claims['manifest_valid'] = True

    if not os.path.exists(const_path):
        issues.append(f"constitution missing: {const_path}")
    else:
        with open(const_path, 'r', encoding='utf-8') as f:
            text = f.read()
            if len(text.strip()) < 100:
                issues.append("constitution.md is too short")
            if "lorem" in text.lower() or "[insert" in text.lower():
                issues.append("constitution.md has placeholders")
            
            if not ("Score 4" in text):
                issues.append("Missing Score 4 anchor")
            if not ("Score 7" in text):
                issues.append("Missing Score 7 anchor")
            if not ("Score 9" in text):
                issues.append("Missing Score 9 anchor")
            if "8/10" not in text:
                issues.append("Missing 8/10 threshold")
            if "Comedy" not in text or "Animation" not in text or "Audio" not in text:
                issues.append("Missing required categories")
        claims['constitution_valid'] = True

        if not issues:
            prompt = f"You are an auditor. Check this Goal Constitution:
{text}
Does it have a scoring rubric specific to South Park/Family Guy style edgy 9:16 vertical animation?
Does it have concrete anchors describing exactly what a score of 4, 7, and 9 look like for Comedy, Animation, and Audio?
Does it state a pass threshold of 8/10?
Reply JSON strictly: {{"valid": true_or_false}}"
            try:
                resp = generate("gemini-3.5-flash", prompt, config={"response_mime_type": "application/json"}).text
                result = json.loads(resp)
                if not result.get("valid"):
                    issues.append("LLM Perceptual check failed: missing required rubric elements")
            except Exception as e:
                issues.append(f"LLM check failed: {str(e)}")

    return issues, claims

def main():
    print("Starting verification...")
    issues, claims = run_checks('constitution.md', 'manifest.md')
    print(f"C1: manifest.md valid - {claims.get('manifest_valid', False)}")
    print(f"C2: constitution.md valid - {claims.get('constitution_valid', False)}")
    
    if issues:
        print("REAL ARTIFACT FAILED:")
        for issue in issues:
            print(f"- {issue}")
        sys.exit(1)

    os.makedirs('scratch', exist_ok=True)
    fault_path = f"scratch/fault_constitution_{random.randint(1000,9999)}.md"
    shutil.copy('constitution.md', fault_path)
    
    with open(fault_path, 'r', encoding='utf-8') as f:
        lines = f.readlines()
    
    for i, line in enumerate(lines):
        if "Score 9" in line:
            lines[i] = "- **Score 9**: [insert description here]
"
            break
            
    with open(fault_path, 'w', encoding='utf-8') as f:
        f.writelines(lines)
        
    fault_issues, _ = run_checks(fault_path, 'manifest.md')
    if not fault_issues:
        print("FAULT-PROOF FAILED: Did not catch corruption")
        sys.exit(1)
        
    print(f"FAULT-PROOF: caught induced fault in {fault_path} (Errors: {fault_issues})")
    print("VERDICT: PASS")
    sys.exit(0)

if __name__ == '__main__':
    main()
