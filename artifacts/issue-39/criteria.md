# criteria.md

## Interpretation
- C1: `script.json` exists and parses as valid JSON.
- C2: `script.json` contains dialogue entries, each requiring `character`, `pitch`, `rate`, and `subtitle`.
- C3: `script.json` contains at least 3 cutaways (identifiable via timestamps or explicit cutaway objects).
- C4: The computed duration is between 60 and 115 seconds, where duration = (total_words / 2.5) + (num_cutaways * 3).
- C5: Quality is >= 8.0 for "Comedic Writing and Original Satire", judged by gemini-3.1-pro-preview based on the constitution rubric.
- C6: `manifest.md` exists alongside `script.json` in the workspace root.

## Claims
C1: script.json exists and is valid JSON
C2: script.json contains required TTS keys
C3: script.json contains >= 3 cutaways
C4: script.json duration is 60-115 seconds
C5: Subjective quality >= 8.0
C6: manifest.md exists
