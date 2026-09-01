# verify.py - VALIDATED: verify the Goal Constitution and Manifest
import os, sys, json, shutil
from metered import generate

def check_file_content(path):
    if not os.path.exists(path):
        return False, "File not found"
    with open(path, "r", encoding="utf-8") as f:
        content = f.read()
    if len(content.strip()) < 100:
        return False, "File is degenerate/too short"
    bad_words = ["todo", "placeholder", "lorem", "[", "]", "tbd", "dummy"]
    for w in bad_words:
        if w in content.lower():
            return False, f"Contains placeholder word: {w}"
    return True, "Pass"

def judge_constitution(path):
    with open(path, "r", encoding="utf-8") as f:
        content = f.read()
    
    prompt = f"""
Analyze the following Goal Constitution for a satirical 9:16 Instagram Reel.
Does it have explicit anchored descriptors of what a 4, a 7, and a 9 concretely look like for COMEDY?
Does it have explicit anchored descriptors of what a 4, a 7, and a 9 concretely look like for ANIMATION?
Does it have explicit anchored descriptors of what a 4, a 7, and a 9 concretely look like for AUDIO?
Does it set a numeric pass threshold of 8/10?
Score the overall quality of the constitution and its humor rubric from 0 to 10 (as a float).
Constitution text:
{content}
"""
    schema = {
        "type": "object",
        "properties": {
            "has_comedy_anchors": {"type": "boolean"},
            "has_animation_anchors": {"type": "boolean"},
            "has_audio_anchors": {"type": "boolean"},
            "has_threshold_8": {"type": "boolean"},
            "score": {"type": "number"}
        },
        "required": ["has_comedy_anchors", "has_animation_anchors", "has_audio_anchors", "has_threshold_8", "score"]
    }
    
    scores = []
    for _ in range(3):
        try:
            resp = generate("gemini-3.5-flash", prompt, config={"response_mime_type": "application/json", "response_schema": schema}).text
            data = json.loads(resp)
            if not data.get("has_comedy_anchors") or not data.get("has_animation_anchors") or not data.get("has_audio_anchors") or not data.get("has_threshold_8"):
                return False, "Missing anchors or threshold according to judge"
            scores.append(float(data.get("score", 0)))
        except Exception as e:
            return False, f"LLM error: {e}"
    scores.sort()
    median = scores[1]
    if median < 8.0:
        return False, f"Median score {median} < 8.0"
    return True, f"Median Score: {median}"

def judge_manifest(path):
    with open(path, "r", encoding="utf-8") as f:
        content = f.read()
    prompt = f"""
Analyze the following manifest.md for a satirical 9:16 Instagram Reel.
Does it contain concrete, real inputs and outputs rather than dummy names or generic placeholders?
Manifest text:
{content}
"""
    schema = {
        "type": "object",
        "properties": {
            "is_concrete": {"type": "boolean"}
        },
        "required": ["is_concrete"]
    }
    try:
        resp = generate("gemini-3.5-flash", prompt, config={"response_mime_type": "application/json", "response_schema": schema}).text
        data = json.loads(resp)
        if not data.get("is_concrete"):
            return False, "Manifest contains dummy names or lacks concrete inputs/outputs"
        return True, "Manifest is concrete"
    except Exception as e:
        return False, f"LLM error: {e}"

def run_checks(const_path, manifest_path):
    c1, msg1 = check_file_content(const_path)
    if not c1:
        print(f"C1 (constitution length/placeholders): FAILED - {msg1}")
        return False
    print(f"C1 (constitution length/placeholders): PASS")
    
    c2, msg2 = check_file_content(manifest_path)
    if not c2:
        print(f"C2 (manifest length/placeholders): FAILED - {msg2}")
        return False
    print(f"C2 (manifest length/placeholders): PASS")
    
    c3, msg3 = judge_constitution(const_path)
    if not c3:
        print(f"C3 (constitution rubric validation): FAILED - {msg3}")
        return False
    print(f"C3 (constitution rubric validation): PASS - {msg3}")
    
    c4, msg4 = judge_manifest(manifest_path)
    if not c4:
        print(f"C4 (manifest real inputs/outputs): FAILED - {msg4}")
        return False
    print(f"C4 (manifest real inputs/outputs): PASS - {msg4}")
    
    return True

if __name__ == "__main__":
    ok = run_checks("constitution.md", "manifest.md")
    
    os.makedirs("scratch", exist_ok=True)
    
    # Fault Proof 1: Placeholder
    shutil.copy("constitution.md", "scratch/faulty_const_1.md")
    with open("scratch/faulty_const_1.md", "a") as f:
        f.write("\n\n(insert title here)\n[\n")
    c1_f, _ = check_file_content("scratch/faulty_const_1.md")
    
    # Fault Proof 2: Subjective Rubric Validation
    with open("scratch/faulty_const_2.md", "w") as f:
        f.write("This is a constitution. It has some text so it passes length but lacks anchors.")
        f.write(" " * 100) # padding length
    c3_f, _ = judge_constitution("scratch/faulty_const_2.md")

    if c1_f is False and c3_f is False:
        print("FAULT-PROOF: Successfully caught placeholder and subjective rubric faults.")
    else:
        print(f"FAULT-PROOF FAILED: Placeholder caught: {c1_f is False}, Rubric caught: {c3_f is False}")
        sys.exit(1)
        
    if ok:
        print("VERDICT: PASS")
        sys.exit(0)
    else:
        print("VERDICT: FAIL")
        sys.exit(1)
