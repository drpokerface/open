# Criteria

## Interpretation
- The script must be a valid JSON file containing an array of scenes, dialogue lines, Web Speech API settings (pitch, rate), and millisecond timing offsets.
- Total runtime must be mechanically calculated purely from the timing offsets in script.json and be between 60s and 119s.
- Character voices must show variation in pitch and rate.
- The script must use 0 copyrighted names/franchises (family guy, south park, etc.) and have original characters/IP.
- Subjective quality >= 8/10 as judged by gemini-3.1-pro-preview using the Goal Constitution rubric.
- manifest.md must exist and contain exact format details and a sample.

## Claims
- C1: script.json exists and is valid, parseable JSON.
- C2: script.json conforms to the schema (has scenes, dialogue, pitch, rate, and offset_ms).
- C3: Total calculated runtime is between 60,000 ms (60s) and 119,000 ms (119s).
- C4: Character voices are non-uniform (pitch and rate have variation).
- C5: Original IP check: zero copyrighted names from major animation franchises.
- C6: Subjective quality is >= 8/10 against the Goal Constitution.
- C7: manifest.md exists and contains exact format details and a sample.
