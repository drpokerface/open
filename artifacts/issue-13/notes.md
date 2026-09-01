# Plan
1. Distill exemplars into a rubric and write criteria.md. [DONE]
2. Enumerate degenerate twins in notes.md. [DONE]
3. Write verify.py (RED). [DONE - Turn 8]
4. Generate constitution.md and manifest.md. [DONE]
5. Judge constitution.md using verify.py (GREEN) and refine if needed. [DONE]
6. Verify everything, perform premortem, and call done. [DONE]

# Node Tree
- C1 (Constitution exists/no placeholders): GREEN (turn 20)
- C2 (Manifest exists/no placeholders): GREEN (turn 20)
- C3 (Constitution semantic/rubric): GREEN (turn 20)

# Degenerate Twins
- Twin 1: Empty or near-empty files.
- Twin 2: Files containing placeholders like 'TODO', '[Insert Here]', 'Lorem Ipsum', 'draft', or 'TBD'.
- Twin 3: A constitution.md with a rubric that lacks concrete anchored descriptors for 4, 7, and 9, or has a threshold lower than 8/10.
- Twin 4: A manifest.md that does not define any actual inputs or outputs or uses dummy names.

# Premortem
1. Is verify.py fully robust against fresh environment execution? Yes, it uses stdlib (os, sys, json) and metered.py which handles its own LLM client. No complex third-party packages needed.
2. Do deliverables contain any leftover debugging comments or placeholder patterns? Checked, they are clean.
3. Does the rubric specify clear 4, 7, 9 descriptors for comedy, animation, and audio? Yes, and it establishes a strict pass threshold of 8/10.

# Facts
[verified] F1 | Internet unreachable directly, using model knowledge for exemplars. | evidence: turn 1
