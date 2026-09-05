# Notes

## Plan
1. Probe capabilities (Playwright installation using `sys.executable -m pip`), write `capabilities.md` [active].
2. Establish `criteria.md` following the coverage table and Node Contract.
3. Create `verify.py` using `verify_kit.py` as a basis.
4. Ensure degenerate twins are written under `twins/<name>/slice.html` and `twins/<name>/manifest.md`.
5. Implement `slice.html` with SVG character, CSS, synchronized animations, Web Speech API gating, 9:16 aspect ratio, and 1 scene cut.
6. Implement valid `manifest.md` corresponding to the HTML specs.
7. Test and iterate until the real passes and all twins fail.

## Node Tree
- ROOT [RED] Tracer Slice Verification
  - C1: capabilities.md content [RED]
  - C2: slice.html valid HTML [RED]
  - C3: slice.html zero external dependencies [RED]
  - C4: slice.html autoplay gating (no speechSynthesis on load) [RED]
  - C5: slice.html strict 9:16 visual ratio [RED]
  - C6: slice.html visual rendering (Tap to Play overlay, SVG character, 1 cut) [RED]
  - C7: slice.html animation sync (CSS class toggling matching speech timing) [RED]
  - C8: manifest.md schema and validity [RED]
  - C9: constitution.md alignment [RED]
  - C10: Technical execution quality rating >= 8.0/10 [RED]

## Facts
- [assumed] Playwright can be installed via `sys.executable -m pip`.
- [assumed] Web Speech API triggers can be tracked in Playwright via page console messages.
