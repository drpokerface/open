# notes.md

## Plan
1. Write `criteria.md` with explicit claims. (turn 1)
2. Write `verify.py` and run it RED. (turn 1)
3. Draft `constitution.md` and `manifest.md`.
4. Run `verify.py` to evaluate the draft.
5. Improve `constitution.md` based on judge feedback until median score >= 8.
6. Declare "done".

## Degenerate Twins
- Twin 1: Empty or very short file. (Caught by entropy/length check).
- Twin 2: Text without strict rubric anchors 4, 7, 9. (Caught by keyword and perception check).
- Twin 3: Generic rubric not aligned with IG Reels or South Park style. (Caught by judge C5).

## Node Tree
- [assumed] C1: `manifest.md` exists and lists files.
- [assumed] C2: `constitution.md` exists and is readable text > 500 bytes.
- [assumed] C3: `constitution.md` has mechanical keywords (script, audio, visual, assembly, 4, 7, 9).
- [assumed] C4: Perception confirms strict rubric and threshold.
- [assumed] C5: Blind judge scores median >= 8.0 on clarity and style alignment.
