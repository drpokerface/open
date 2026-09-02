# verify.py - VALIDATED: strictly verify constitution.md and manifest.md exist and meet all criteria.
import os, sys, re, random, shutil, json, statistics

try:
    from metered import generate
except ImportError:
    from google import genai
    def generate(model, prompt, **kwargs):
        client = genai.Client(api_key=os.environ.get("GEMINI_API_KEY"))
        class Res:
            def __init__(self, t): self.text = t
        if "response_schema" in kwargs.get("config", {}):
            return Res(client.models.generate_content(
                model=model, 
                contents=prompt,
                config=kwargs["config"]
            ).text)
        return Res(client.models.generate_content(model=model, contents=prompt).text)

LAZY_BASELINE = """# Constitution: Animated Comedy Instagram Reels
Philosophy for a narrated animated comedy video (Humor style: Family Guy or South Park).
Format: 9:16 Instagram Reel.
Score 4: Not very funny or poorly paced.
Score 7: Good timing, satirical, meets format requirements.
Score 9: Excellent animation, hilarious edgy humor, perfect pacing.
Pass threshold is 7.
Integration Contract: You must ship manifest.md next to your deliverable."""

RUBRIC = f"""You are a STRICT, unforgiving grader. Score the provided constitution.md from 0 to 10.
Requirements for the document:
1. It must be a philosophy for a narrated animated comedy video (Family Guy/South Park style, edgy, satirical, 9:16).
2. It must distill a scoring rubric from real exemplars.
3. It must have highly concrete descriptors for scores 4, 7, and 9.
4. It must set a pass threshold of 7.
5. It must define integration contracts requiring a manifest.md.

Crucially, you must compare it against this LAZY BASELINE:
---
{LAZY_BASELINE}
---
The provided document must clearly BEAT this lazy baseline by a significant margin in terms of detail, concreteness, and actionable guidance.
If ANY of the requirements are missing, vague, or replaced with garbage, OR if the document does not clearly beat the lazy baseline, score BELOW 7.
Provide your response purely in JSON format."""

def get_judge_score(content):
    prompt = f"{RUBRIC}\n\nDocument text:\n{content[:8000]}\n\n" + 'Respond purely in JSON format: {"score": number, "justification": "string"}'
    scores = []
    justifications = []
    for _ in range(3):
        try:
            resp = generate(
                "gemini-3.5-flash", 
                prompt, 
                config={"response_mime_type": "application/json"}
            ).text
            if resp.startswith("```json"):
                resp = resp[7:-3]
            elif resp.startswith("```"):
                resp = resp[3:-3]
            data = json.loads(resp.strip())
            scores.append(float(data.get("score", 0.0)))
            justifications.append(data.get("justification", "No justification"))
        except Exception as e:
            scores.append(0.0)
            justifications.append(f"Error parsing JSON: {str(e)}")
    
    median_score = statistics.median(scores)
    
    idx = 0
    for i, s in enumerate(scores):
        if s == median_score:
            idx = i
            break
            
    return median_score, justifications[idx], scores

def evaluate_doc(content):
    mech_ok = True
    msg = ""
    if not content or len(content.strip()) < 100:
        mech_ok = False; msg = "Too short or empty"
    elif len(set(content)) < 20:
        mech_ok = False; msg = "Degenerate uniform content"
    else:
        c2 = bool(re.search(r'(?i)score\s*4[\s:]', content) and 
                  re.search(r'(?i)score\s*7[\s:]', content) and 
                  re.search(r'(?i)score\s*9[\s:]', content))
        c3 = bool(re.search(r'(?i)threshold[^\n]*7', content))
        if not c2:
            mech_ok = False; msg = "Missing exact 'Score X' descriptors"
        elif not c3:
            mech_ok = False; msg = "Missing threshold 7"

    if not mech_ok:
        return False, f"Mechanical fail: {msg}"

    score, justification, all_scores = get_judge_score(content)
    if score >= 7.0:
        return True, f"LLM median score: {score} (scores: {all_scores}). Justification: {justification}"
    else:
        return False, f"LLM median score: {score} (scores: {all_scores}). Justification: {justification}"

def run_fault_proof():
    os.makedirs('scratch', exist_ok=True)
    if not os.path.exists('constitution.md'):
        return True 
    with open('constitution.md', 'r', encoding='utf-8') as f:
        content = f.read()
    
    faulty_content = re.sub(r'(?i)score\s*4', 'Score X', content)
    faulty_content = re.sub(r'(?i)score\s*7', 'Score Y', faulty_content)
    faulty_content = re.sub(r'(?i)score\s*9', 'Score Z', faulty_content)
    faulty_content = re.sub(r'(?i)threshold', 'banana', faulty_content)
    faulty_content = faulty_content.replace('9:16', 'Z:16').replace('1920', '1Z20')
    
    rnd = random.randint(1000, 9999)
    with open(f'scratch/faulty_{rnd}.md', 'w', encoding='utf-8') as f:
        f.write(faulty_content)
        
    ok, msg = evaluate_doc(faulty_content)
    if ok:
        print("FAULT-PROOF FAILED: verify.py passed a corrupted document!")
        sys.exit(1)
    else:
        print(f"FAULT-PROOF: Successfully caught induced fault! {msg}")
        return True

def main():
    run_fault_proof()
    
    if not os.path.exists('constitution.md'):
        print("C1_exists: False - constitution.md missing")
        sys.exit(1)
    with open('constitution.md', 'r', encoding='utf-8') as f:
        content = f.read()
    if not content.strip():
        print("C1_exists: False - constitution.md is empty")
        sys.exit(1)
    print("C1_exists: True")
    
    c2 = bool(re.search(r'(?i)score\s*4[\s:]', content) and 
              re.search(r'(?i)score\s*7[\s:]', content) and 
              re.search(r'(?i)score\s*9[\s:]', content))
    print(f"C2_rubric: {c2}")
    if not c2:
        sys.exit(1)
        
    c3 = bool(re.search(r'(?i)threshold[^\n]*7', content))
    print(f"C3_threshold: {c3}")
    if not c3:
        sys.exit(1)
        
    c4 = bool(re.search(r'(?i)manifest\.md', content))
    if not os.path.exists('manifest.md'):
        print("C4_manifest: False - manifest.md missing from disk")
        sys.exit(1)
    with open('manifest.md', 'r', encoding='utf-8') as f:
        manifest_content = f.read()
    has_filename = bool(re.search(r'(?i)filename', manifest_content)) and 'constitution.md' in manifest_content
    has_format = bool(re.search(r'(?i)format', manifest_content))
    has_sample = bool(re.search(r'(?i)sample', manifest_content))
    if not (has_filename and has_format and has_sample):
        print("C4_manifest: False - manifest.md lacks filenames, formats, or a tiny sample")
        sys.exit(1)
    print(f"C4_manifest: {c4 and True}")
    if not c4:
        sys.exit(1)
        
    ok, msg = evaluate_doc(content)
    print(f"C5_score: {ok} ({msg})")
    
    if not ok:
        sys.exit(1)
        
    print("VERDICT: PASS")
    sys.exit(0)

if __name__ == "__main__":
    main()
