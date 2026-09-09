# perception and media - the model is also your senses (pack: perception)
- Images, rendered pages, audio, and video are INVISIBLE to you until a fresh model call
  has looked at them: kit.perceive([files], question) inside verify.py, or upload() +
  generate() inside your own code. Print what the judge saw next to what you intended -
  the gap between the two is your work list. A perceptual claim ("legible", "sounds
  natural", "motion is smooth", "depicts the Sun") turns green only by perception, never
  because the code that produced the artifact exited 0.
- Probe every generator with ONE tiny call before building a pipeline on it: which image,
  speech, and video models the catalog (providers.md) and capabilities.json actually make
  reachable on this key, what a unit costs (route through metered.generate_media), what
  they refuse. Record findings in notes.md - and in capabilities.md when the task asks.
- Primitive fallbacks (hand-drawn shapes, synthetic beeps, a static frame held for the
  whole clip) are forbidden unless the probe PROVED no better tier is reachable; then
  declare the fallback honestly in notes.md and manifest.md.
- verify.py samples the ACTUAL content: decode the media, extract frames or audio
  windows under scratch/ (ffmpeg when attested), and perceive them. Metadata-only checks
  that a blank, silent, uniform, or truncated file would still pass are a rejection.
- Assembly and measurement come from the file itself: duration, distinct frames, an
  audible voice track, sync at cuts. Bulky intermediates live under scratch/ and never
  ship; what ships must be lean enough to push and to judge.
