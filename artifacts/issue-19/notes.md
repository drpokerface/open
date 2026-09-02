# Plan
1. Create criteria.md (done)
2. Enumerate degenerate twins in notes.md (done)
3. Write verify.py and run it RED (done)
4. Probe model for exemplars of Family Guy/South Park style animated reels (done)
5. Draft constitution.md and manifest.md (done)
6. Subjective judging loop (done)

## Node Tree
- C1 (constitution.md exists): [verified] (turn 20)
- C2 (valid markdown): [verified] (turn 20)
- C3 (4/7/9 sections): [verified] (turn 20)
- C4 (pass threshold): [verified] (turn 20)
- C5 (no placeholders): [verified] (turn 20)
- C6 (manifest.md exists): [verified] (turn 20)
- C7 (quality >= 7): [verified] (turn 20)

## Degenerate Twins
- `twins/blank`: Empty `constitution.md` (correctly fails verifier)
- `twins/no_rubric`: Missing 4/7/9 rubric sections (correctly fails verifier)
- `twins/bad_quality`: Low effort, fails C7 (correctly fails verifier)
- `twins/no_manifest`: Missing `manifest.md` (correctly fails verifier)
- `twins/placeholder`: Contains 'stub' or 'placeholder' (correctly fails verifier)

## Facts
- F1 | constitution.md exists and is valid markdown | [verified] (turn 20)
- F2 | constitution.md contains 4/7/9 sections | [verified] (turn 20)
- F3 | manifest.md lists constitution.md and manifest.md with valid format details and sample commands | [verified] (turn 20)
- F4 | subjective quality of constitution.md is rated 10.0 (above threshold 7.0) by strong model judge | [verified] (turn 20)
