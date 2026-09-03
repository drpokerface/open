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

Deliverables are judged on a 10-point scale across four dimensions. The absolute pass threshold is **8.0/10**, with a margin of 0.5. Any total score below 7.5 results in automatic rejection. 

### Dimension 1: Comedic Efficacy & Tone
Evaluates the script and visual gags against the requested *South Park*/*Family Guy* aesthetic (subversive, satirical, fast-paced, cutaway-heavy) without relying on stolen IP.
- **4 (Poor):** The humor is safe, bland, or relies on tired internet memes. Dialogue feels robotic. No attempt at a cutaway or structural joke. 
- **7 (Good):** Captures the edgy, absurd tone. Includes a cutaway gag. The satire makes sense, but the joke drags slightly or the punchline is predictable.
- **9 (Exceptional):** Razor-sharp, cynical, and hilarious. Distinct "voices" for the characters despite being text/beeps. The cutaway gag is a brilliant non-sequitur. The script leans fully into the absurdity of being a lo-fi coded video. Matches the energy of classic adult animation flawlessly.

### Dimension 2: Pacing and Instagram Fit
Evaluates the video's optimization for the Reels algorithm and vertical viewing experience.
- **4 (Poor):** The hook takes longer than 3 seconds. The aspect ratio is wrong (e.g., 16:9). Text is too small to read on a mobile screen. The video feels sluggish.
- **7 (Good):** 9:16 aspect ratio. Text is large and readable. The first joke hits within 2 seconds. The video is under 2 minutes, but perhaps a middle section lingers for a few seconds too long without visual changes.
- **9 (Exceptional):** Aggressively paced. The visual state or text changes every 1-2 seconds. The hook is immediate and visually arresting. Total length is perfectly constrained to a highly re-watchable 45-60 seconds.

### Dimension 3: Technical Execution (Programmatic Lo-Fi)
Evaluates the swarm's ability to bypass the lack of media tools by writing flawless code to generate the video, sync the text, and generate synthetic "voices."
- **4 (Poor):** The code fails to compile or render, or the resulting video has severely unsynced text and audio. The visual output is a jumbled, unreadable mess.
- **7 (Good):** The Python/moviepy script compiles and renders a complete MP4. Text appears roughly in time with the audio beeps. The geometric characters are simple but distinguishable. 
- **9 (Exceptional):** The rendering code is highly optimized. Text and synthesized audio beeps are locked in perfect frame-sync. The crude geometric shapes are animated with clever programmatic bounces or rotations that enhance the physical comedy. The "limitations" look like a brilliant, intentional artistic choice.

### Dimension 4: Integration Contract Adherence
Evaluates strict adherence to the swarm's communication protocols.
- **4 (Poor):** Missing `manifest.md` entirely, or missing required fields like `duration_ms`.
- **7 (Good):** `manifest.md` is present and well-formatted, but metadata slightly mismatches the actual deliverable (e.g., duration is off by a few seconds).
- **9 (Exceptional):** `manifest.md` is perfectly formatted. All metadata aligns perfectly with the output. Downstream validation passes instantly.

## 4. Judge Instructions

You are a blind, impartial judge. You will not see the prompts that generated the deliverables; you will only see the final outputs (the code, the rendered video, and the manifests). 

**Evaluation Process:**
1. **Blind Review:** Watch the rendered video output exactly once without pausing, simulating an Instagram user's scrolling experience. Note your immediate gut reaction to the pacing and humor.
2. **Side-by-Side Anchor Comparison:** Place the deliverable next to the Scoring Rubric. You must evaluate the output against the "laziest acceptable version" (a 7.5 score). If the deliverable is merely "okay" but doesn't punch hard, it fails.
3. **Holistic Verification:** Open the codebase. Verify that no banned tools (external TTS APIs, external image APIs) were sneaked in via unauthorized curl commands. Ensure the MP4 was generated purely via code and local assets.
4. **Scoring and Justification:** For each of the four dimensions, assign a numeric score (up to one decimal place). You must provide exactly ONE line of justification for each score, which MUST cite the nearest anchor descriptor.

*Example Justification:* "Score: 8.5 - Pacing and Instagram Fit: The pacing is relentless and the 9:16 text is highly readable, perfectly matching the exceptional anchor's requirement for a sub-2-second hook and aggressive visual changes."
