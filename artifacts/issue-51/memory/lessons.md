# lessons - lessons - Record of historical audit rejections, failures, and lessons learned.
- Turn 16 rejection: Audit (gemini-3.5-flash, gemini-3.1-pro-preview) rejected claim because verify.py performs static checks instead of executing slice.html in a native browser context or performing perceptual verification. (receipt: memory.md ## Turn 42)
- Audit rejection: verify.py timed out after 300 seconds. (receipt: memory.md ## Turn 46)
- Calling kit.text() on a file inside a check function makes the fault-proof harness assume a dependency, triggering expensive LLM re-evaluations for every mutation of that file and causing 300-second timeouts. (receipt: memory.md ## Turn 47)
- The audit gate rejected the claim because slice.html was excluded from the C9 LLM evaluation and because C5 lacked a headless browser execution to verify visual state. (receipt: memory.md ## Turn 48)
- C9 test failed because slice.html deviated significantly from manifest.md, specifically missing the character Jimmy and having timeline mismatches. (receipt: memory.md ## Turn 49)
- Using Python or other indirect probes to read a file that has already been read in a previous turn is blocked as a stall check failure with the error: 'a read by any means is a read, and a repeat read is a stall. Act on what you know.' (receipt: memory.md ## Turn 51)
