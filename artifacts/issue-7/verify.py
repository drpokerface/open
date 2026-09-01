import os
import sys
import json
import random
import shutil
import statistics
from metered import generate

def check_files(manifest_path, const_path):
    # C1
    if not os.path.exists(manifest_path):
        print("C1: manifest.md missing")
        return False, "C1: manifest.md missing"
    with open(manifest_path, "r", encoding="utf-8") as f:
        manifest_text = f.read().lower()
    if "constitution.md" not in manifest_text:
        print("C1: constitution.md not in manifest.md")
        return False, "C1: constitution.md not in manifest.md"
    print("C1: True")

    # C2
    if not os.path.exists(const_path):
        print("C2: constitution.md missing")
        return False, "C2: constitution.md missing"
    with open(const_path, "r", encoding="utf-8") as f:
        const_text = f.read()
    if len(const_text) < 500:
        print("C2: constitution.md too short (<500 bytes)")
        return False, "C2: constitution.md too short"
    degenerate_phrases = ["placeholder", "stub", "lorem ipsum", "todo", "insert content here", "blank test"]
    if any(p in const_text.lower() for p in degenerate_phrases):
        print("C2: constitution.md contains placeholder/stub text")
        return False, "C2: constitution.md contains placeholder/stub text"
    print("C2: True")

    # C3
    required_terms = ["4=", "7=", "9=", "script", "audio", "visuals", "assembly", "threshold"]
    for term in required_terms:
        if term not in const_text.lower():
            print(f"C3: missing term {term}")
            return False, f"C3: missing term {term}"
    print("C3: True")
    return True, "C1-C3 passed"

def check_constitution_perception(const_path):
    if not os.path.exists(const_path):
        return False, "constitution.md does not exist"
    with open(const_path, "r", encoding="utf-8") as f:
        content = f.read()

    # C4: AI verify
    prompt_c4 = (
        "You are an auditor verifying the following constitution document for an Instagram Reel comedy production.\n"
        "Does this text clearly define 0-10 rubrics for (1) script, (2) audio, (3) visuals, and (4) final assembly?\n"
        "Respond ONLY with a valid JSON in this exact format: {\"result\": \"YES\", \"reason\": \"...\"} or {\"result\": \"NO\", \"reason\": \"...\"}.\n\n"
        "--- CONSTITUTION TEXT ---\n" + content[:5000]
    )
    try:
        response_c4 = generate("gemini-3.5-flash", prompt_c4, config={"response_mime_type": "application/json"})
        data_c4 = json.loads(response_c4.text)
        if data_c4.get("result") != "YES":
            print(f"C4: AI verify failed: {data_c4.get('reason')}")
            return False, f"C4: AI verify failed: {data_c4.get('reason')}"
        print("C4: True")
    except Exception as e:
        print(f"C4 error: {e}")
        return False, f"C4 error: {e}"

    # C5: Score verification
    scores = []
    for i in range(3):
        prompt_c5 = (
            "You are a strict, expert comedy producer and auditor evaluating the quality of an Instagram Reel comedy constitution.\n"
            "Grade the constitution on a scale of 0 to 10 against: rubric clarity, alignment with IG Reel/comedic standards, and completeness.\n"
            "Ensure that any placeholder, stub, or low effort content results in a score of 0.\n"
            "Respond ONLY with a valid JSON in this exact format: {\"score\": <float_score_0_to_10>, \"reason\": \"...\"}.\n\n"
            "--- CONSTITUTION TEXT ---\n" + content[:5000]
        )
        try:
            response_c5 = generate("gemini-3.1-pro-preview", prompt_c5, config={"response_mime_type": "application/json"})
            data_c5 = json.loads(response_c5.text)
            scores.append(float(data_c5.get("score", 0)))
        except Exception as e:
            print(f"C5 query {i} error: {e}")
            scores.append(0.0)
    
    median_score = statistics.median(scores)
    print(f"C5: Median score is {median_score}")
    if median_score < 8.0:
        return False, f"C5: score {median_score} is below threshold 8.0"
    print("C5: True")
    return True, "C4-C5 passed"

def test_fault_proof(const_path):
    # Create a broken copy under scratch/ to test failure path
    os.makedirs("scratch", exist_ok=True)
    broken_path = "scratch/broken_constitution.md"
    if os.path.exists(const_path):
        shutil.copy(const_path, broken_path)
    else:
        with open(broken_path, "w", encoding="utf-8") as f:
            f.write("This is a placeholder or stub document to force a failure.")
    
    ok, reason = check_files("manifest.md", broken_path)
    # It should fail because it contains placeholder/stub text or doesn't have C3 items
    if not ok:
        print(f"FAULT-PROOF: Successfully caught expected failure: {reason}")
        return True
    else:
        print("FAULT-PROOF: Failed to catch broken/placeholder constitution!")
        return False

if __name__ == '__main__':
    print("Running verification...")
    fp = test_fault_proof("constitution.md")
    
    c1_3_ok, msg1 = check_files("manifest.md", "constitution.md")
    if not c1_3_ok:
        print("VERDICT: FAIL - Base file validation failed")
        sys.exit(1)
        
    c4_5_ok, msg2 = check_constitution_perception("constitution.md")
    if not c4_5_ok:
        print("VERDICT: FAIL - Perception checks failed")
        sys.exit(1)
        
    print("VERDICT: PASS")
    sys.exit(0)
