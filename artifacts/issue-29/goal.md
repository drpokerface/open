Tracer Slice & Capability Probe

PROBE for reachable generation tools (consult providers.md and API keys). Note that per the constitution, text-to-speech, text-to-video, and image generation are UNAVAILABLE. You must record your findings in capabilities.md. HARDEST FIRST: The plan's riskiest assumption is that programmatic Python code (using moviepy and Pillow) can generate synchronized kinetic typography, geometric character animation, and synthetic 'beep' narration fast enough and convincingly enough to be funny without neural generators. We test this cheapest and earliest here. Build a TINY but COMPLETE end-to-end version of the final deliverable (tracer_slice.mp4): ~10 seconds long, one scene, one voiced line of beep-narration, and one cutaway. Assemble it exactly the way the final task will. Output `tracer_slice.mp4` as the main deliverable, alongside `capabilities.md` and an integration contract `manifest.md` (containing component_id, duration_ms, scene_count, humor_mechanics, file_dependencies, and a tiny sample). JUDGING: Mechanical: verify.py checks tracer_slice.mp4 exists, decodes, and duration is ~10s. capabilities.md and manifest.md must exist. Subjective: 8.0/10 score against the constitution's rubric. verify.py must consume the deliverable the way its audience will - decode and sample its ACTUAL content, failing degenerate output (blank, silent, empty, uniform, truncated) regardless of metadata - and for perceptual deliverables must include one cheap model-perception call confirming the sampled content actually depicts what the task requires (geometric shapes and synced text). Placeholder or stub content anywhere in the deliverable is an automatic FAIL at any threshold. SHARED SPEC:

# GOAL CONSTITUTION: Autonomous Comedy Video Swarm

## 1. Strategy and Vision

The ultimate objective of this autonomous swarm is to conceptualize, write, programmatically generate, and assemble a narrated, animated comedy video under two minutes in length, optimized specifically for Instagram Reels. The comedic DNA must draw heavily from the rapid-fire, non-sequitur cutaway gags of *Family Guy* and the biting, topical, absurdist satire of *South Park*. However, under no circumstances will any characters, specific settings, or copyrighted intellectual property from these shows be replicated. The humor must stand on its own, relying on sharp writing, subversive themes, and impeccable comedic timing.

### The Grand Constraint: Embracing Programmatic Lo-Fi
Given the strict operational constraints of this swarm—specifically the total absence of neural text-to-speech (TTS), text-to-video, and image generation APIs—we must pivot our strategy to a brilliant, deliberate aesthetic choice: **Programmatic Lo-Fi Minimalism**. 

Because we cannot generate high-fidelity illustrations or human voiceovers, the swarm will generate the video entirely via code (e.g., Python using `moviepy`, `Pillow` for frame generation, and programmatic audio beeps for narration). Characters will be constructed from crude, highly stylized geometric shapes (reminiscent of the early construction-paper cutout days of *South Park*), and "narration" will be achieved through rhythmically generated synthesizer tones (similar to the gibberish voices in *Animal Crossing* or *Banjo-Kazooie*) paired with aggressive, perfectly timed kinetic typography (subtitles) that dominate the screen.

### What Excellent Looks Like
An excellent output is a video that leans into its technological limitations, using the crude, coded aesthetic as part of the joke. It hooks the Instagram scroller within the first 1.5 seconds with an outrageous premise or a loud visual interruption. The writing is sharp, cynical, and observant, featuring at least one unexpected cutaway gag or surreal juxtaposition. The pacing is relentless. The viewer is laughing not just at the dialogue, but at the sheer audacity and cleverness of how the video was constructed.

### What to Avoid
- **Boring, generic humor:** Dad jokes, safe corporate humor, or slow setups will fail. We are aiming for edgy, late-night animation vibes.
- **IP Infringement:** Do not name-drop Peter Griffin, Cartman, or use recognizable silhouettes.
- **Technical Overreach:** Do not attempt to code complex walk cycles or 3D rotations in Pillow/Python. Embrace static, bouncing, or sliding geometry.
- **Platform Banning:** While aiming for edgy/satirical, avoid outright hate speech, extreme gore (even geometrically), or anything that triggers Instagram's automated NSFW filters.

### The Three Critical Decisions
1. **The Hook & Pacing:** The script must front-load the joke. Instagram users swipe away in 2 seconds. The opening frame must be visually striking, and the text must immediately introduce conflict or absurdity.
2. **The Audio-Visual Sync:** Since the "narration" is just timed beeps and subtitles, the code must sync the appearance of the text precisely with the audio bumps. This rhythm dictates the comedic timing.
3. **The "Cutaway" Implementation:** To mimic the requested style, the script must feature a sudden, jarring context switch (a visual cutaway to a completely different geometric scene) that breaks the narrative flow for a punchline before snapping back.

## 2. Style Decisions and Conventions

### Format and Deliverables
The final output must be a rendered MP4 video file. Because the swarm must build this via script, the primary codebase deliverable is a self-contained Python project leveraging `moviepy` (and potentially `ffmpeg` CLI calls for final muxing) that, when executed, renders the final video.

### Visual and Audio Specifications
- **Aspect Ratio:** 1080x1920 (Vertical 9:16), mandatory for Instagram Reels.
- **Length:** 45 to 85 seconds. Do not approach the 120-second absolute maximum unless the narrative strictly requires it.
- **Color Palette:** High contrast, neon-on-dark or aggressively bright pastels. Backgrounds should be flat colors or simple gradients to ensure the kinetic typography remains readable.
- **Typography:** Heavy, bold, sans-serif fonts (e.g., Impact, Arial Black). Text must appear dynamically—word by word or phrase by phrase—syncing with the pseudo-narration.
- **Characters:** Composed of basic geometric primitives (circles, squares, triangles) drawn via `Pillow` or raw SVG paths if rendering via a browser engine. 
- **Sound Design:** 
  - Pseudo-narration: Programmatically generated sine/square wave beeps of varying pitches to represent different "characters" speaking.
  - Foley/SFX: Simple synthesized noise (crashes, thuds) to accompany physical comedy.

### The Integration Contract (`manifest.md`)
Every single agent acting as a producer within the swarm (whether generating the script, the frame-drawing functions, or the audio-sync arrays) MUST output a `manifest.md` file adjacent to its primary deliverable. 

Consumers (downstream agents) will validate against this manifest before proceeding. The manifest must contain:
1. `component_id`: A unique string identifier for the deliverable.
2. `duration_ms`: The exact planned duration of the component in milliseconds.
3. `scene_count`: Number of distinct visual setups.
4. `humor_mechanics`: A brief JSON array of the comedic tropes used (e.g., `["cutaway", "non-sequitur", "satire"]`).
5. `file_dependencies`: Any localized assets or scripts required to compile this node.
If a downstream agent detects a missing manifest or a `duration_ms` that pushes the total over 120,000ms, it must instantly reject the deliverable and trigger a regeneration.

## 3. Scoring Rubric

Deliverables are judged on a 10-point scale across four dimensions. The absolute pass threshold is **8.0/10**, with a margin of 0.5. Any total score belo

Save the main deliverable as tracer_slice.mp4.

Already provided in your working directory: artifacts/board-20260903-204411/constitution.md

SWARM CHANNEL: you are working issue #29 of the GitHub repo drpokerface/open (token in GITHUB_TOKEN env). If you discover work this plan is missing, you may post ONE comment on your own issue via the API starting exactly 'PROPOSE-TASK: ' (state: title, why, which existing deliverable it unblocks, what it produces). Facing an irreversible, genuinely ambiguous choice, you may post ONE comment starting exactly 'QUESTION: ', then continue on the reversible path without waiting. If a PROVIDED input artifact fails your validation (placeholder, degenerate, or broken contract), post ONE comment starting exactly 'INPUT-REJECT: #<producing issue number> ' plus one line of evidence - the swarm will reopen that task; then declare impossible honestly instead of building on garbage. If providers.md lacks an adequate tool for a capability this task needs, you may post ONE comment starting exactly 'PROPOSE-PROVIDER: ' (capability, best candidate service, pricing, what it unlocks) - the owner decides about subscribing; continue meanwhile on the best reachable tier. Never create issues yourself; an owner-side arbiter reviews and answers as an 'ARBITER re' comment on this issue.
