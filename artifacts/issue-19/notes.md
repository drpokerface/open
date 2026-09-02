# Plan
1. [x] Write criteria.md (Turn 77)
2. [x] Write verify.py (RED) and define degenerate twins (Turn 77).
3. [x] Research/Distill exemplars for Family Guy / South Park style IG reels (Turn 77).
4. [x] Draft constitution.md (Turn 77).
5. [x] Score constitution.md with judge, improve if needed (Turn 89-91).
6. [x] Ship and pass gate (Turn 92).

# Node Tree
- C1 (constitution.md exists and is valid markdown): green [verified] (Turn 91)
- C2 (constitution.md has explicit 4/7/9 rubric descriptors): green [verified] (Turn 91)
- C3 (constitution.md specifies a numeric pass threshold of 7): green [verified] (Turn 91)
- C4 (constitution.md mandates delivery of manifest.md): green [verified] (Turn 91)
- C5 (LLM score of constitution.md >= 7): green [verified] (Turn 91)

# Degenerate Twins
- `_auto_blank`: Empty file. (verified FAIL by verify.py, Turn 91)
- `_auto_placeholder`: Placeholder text. (verified FAIL by verify.py, Turn 91)
- `_auto_truncated`: Truncated constitution. (verified FAIL by verify.py, Turn 91)
- `lazy_baseline`: Minimal baseline. (verified FAIL by verify.py, Turn 91)
- `missing_manifest`: Manifest file missing. (verified FAIL by verify.py, Turn 91)
- `missing_rubric`: Scores / rubric sections missing. (verified FAIL by verify.py, Turn 91)

# Facts
- F1 | `manifest.md` physical presence verified | evidence: Turn 91 [verified]
- F2 | `verify.py` passes on real files and fails on all degenerate twins | evidence: Turn 91 [verified]
- F3 | `verify.py` includes robust random-fault-proof mechanism with fresh random noise generation | evidence: Turn 91 [verified]
