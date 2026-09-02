# GOAL CONSTITUTION: Autonomous Animation Comedy Swarm

## 1. Strategy and Vision

The goal of this swarm is to produce a narrated, animated comedy video under two minutes in length, optimized for an Instagram Reel (9:16 vertical format). The comedic tone must heavily emulate the specific satirical, irreverent, and fast-paced styles of *Family Guy* and *South Park*. However, under no circumstances may the swarm copy existing characters, intellectual property, or specific trademarked locales from those shows. The objective is to capture their *spirit*—absurdist escalation, sharp social commentary, willingness to cross boundaries, and rapid-fire cutaway gags—while applying it to entirely original characters and premises.

Crucially, this swarm operates under strict technical constraints: there are no native image generation, text-to-video, or text-to-speech models available in the catalog. Therefore, what excellent looks like for *this* specific goal is a masterclass in programmatic creativity. The swarm must achieve the visual and auditory requirements by writing and executing code (e.g., Python scripts using vector graphics libraries, raw SVG generation, and utilizing system-level or open-source programmatic TTS libraries) and assembling the final product using FFmpeg. 

This technical constraint perfectly aligns with the requested *South Park* aesthetic. Originally created using crude construction paper cutouts, your equivalent is "programmatic construction paper." Excellent execution means embracing flat, geometric, mathematically defined characters (circles, polygons, thick outlines) animated through simple translations, rotations, and binary mouth-state swapping (open/closed). 

**What to avoid:**
- **Safe, sanitized "AI" humor:** Do not produce bland, corporate, or overly polite comedy. The prompt demands edge, satire, and absurdity. If the script reads like a generic sitcom, it fails.
- **Complex organic art:** Do not attempt to code highly detailed, shaded, or biologically accurate characters. The code will fail, and the execution will stall. Stick to aggressive simplicity.
- **Slow pacing:** Instagram Reels demand immediate engagement. Avoid long establishing shots, slow panning, or slow conversational pacing. 

**The three decisions that matter most:**
1. **The Three-Second Hook:** The viewer must be hit with a ridiculous premise or an offensive/absurd statement within the first 3 seconds to prevent scrolling.
2. **The Script-to-Code Translation:** Every joke must be written with the understanding that it will be rendered via basic geometric manipulation. Scripts should rely on sharp dialogue, sudden location swaps (cutaways), and rigid character bobbing rather than nuanced physical comedy or complex facial expressions.
3. **Audio-Driven Assembly:** Because animation is generated programmatically, the audio track (synthesized TTS) must dictate the timeline. The timing of frame cuts and mouth flaps must strictly follow the cadence of the generated audio to maintain comedic timing.

## 2. Style Decisions and Conventions

To ensure all autonomous agents in the swarm function cohesively, the following strict style conventions and integration contracts apply to all tasks.

**Format and Look:**
- **Aspect Ratio:** 1080x1920 (9:16 Vertical) for Instagram Reels.
- **Framerate:** 12 to 15 frames per second. A lower framerate reduces computational overhead for generated frames and perfectly mimics the choppy, stop-motion aesthetic of early *South Park*.
- **Color Palette:** Highly saturated, flat colors. No gradients, no shadows. Use bold, thick, black stroke outlines for all characters and foreground objects.
- **Backgrounds:** Minimalist. Sky blue rectangles for sky, green rectangles for grass, or solid flat colors for interiors. The focus must be purely on the characters and the text/dialogue.
- **Animation Mechanics:** Characters "walk" by hopping (translating up and down slightly on the Y-axis while moving across the X-axis). Talking is achieved by alternating between a baseline mouth vector (a line) and an open mouth vector (an ellipse). 

**Sound and Pacing:**
- **Voices:** Use programmatic TTS (e.g., Python `pyttsx3`, `gTTS`, or macOS `say`/Linux `espeak`). Modulate pitch and speed to differentiate characters. The inherently robotic nature of simple TTS should be utilized as a comedic tool—deadpan delivery of highly unhinged dialogue.
- **Length:** Target a sweet spot of 45 to 90 seconds. Do not exceed 119 seconds under any circumstance.
- **Subtitles:** Since this is an Instagram Reel, burn thick, stylized captions (using a bold font like Impact or an open-source sans-serif) into the middle-lower third of the video. Subtitles must pop onto the screen word-by-word or phrase-by-phrase.

**File Formats and Naming:**
- Vectors: `scene_[X]_frame_[Y].svg`
- Audio: `dialogue_char_[NAME]_[ID].wav`
- Output: `final_render.mp4` (H.264 video codec, AAC audio, assembled via FFmpeg).

**The Integration Contract:**
Every producer agent must ship a `manifest.md` file beside its generated deliverable. Every consumer agent must validate the incoming handoff against this manifest before beginning its own task. 
The `manifest.md` must include:
1. **Asset Manifest:** A YAML-formatted list of every file generated in the step, with exact relative paths.
2. **Technical Assertions:** Explicit boolean statements proving constraints are met (e.g., `Vertical Resolution 1920px: TRUE`, `Total Duration < 120s: TRUE`).
3. **Creative Assertions:** A brief statement of how the requested style is met (e.g., `Cutaway Gag Count: 2`, `Joke Density: 1 setup/punchline per 10 seconds`).
If a consumer reads a `manifest.md` and finds missing files or failed assertions, it must immediately reject the input and trigger a rework protocol.

## 3. Scoring Rubric

Deliverables are evaluated on a 10-point scale. The numeric pass threshold is **8.0/10**, with a margin of **0.5** for minor technical artifacts that do not detract from the comedy.

### Dimension 1: Comedic Tone and Satirical Irreverence
*This dimension evaluates the script, dialogue, and conceptual premise against the requested Family Guy/South Park style.* 

- **Score 9 (Excellent):** The script is genuinely hilarious and pushes boundaries without violating overarching safety policy guardrails. It features a rapid escalation of an absurd premise. Characters have distinct, conflicting viewpoints that satirize modern culture (e.g., mocking influencer culture, tech bros, or modern dating). It successfully executes at least one sudden, jarring cutaway gag that relates tangentially to the dialogue. The humor is sharp, witty, and perfectly tailored for the short attention span of Reel viewers.
- **Score 7 (Passable):** The script attempts satire and achieves a moderately funny premise. The humor is slightly safer or relies more heavily on obvious tropes. It has an identifiable setup and punchline structure, and it successfully introduces the hook within the first 3 seconds, but the escalation lacks the chaotic, unhinged energy of the target inspirations. It feels like a decent, albeit standard, internet comedy sketch.
- **Score 4 (Failure):** The script is sterile, boring, and corporate. It reads like a standard AI-generated story about friendship or a mundane misunderstanding. There is no edge, no satire, and no structural resemblance to the requested shows. Or, alternatively, it explicitly steals characters (e.g., uses the names Peter Griffin or Eric Cartman), violating the prompt's negative constraint.

### Dimension 2: Vertical Pacing and Retention Mechanics
*This dimension evaluates how well the video is optimized for the Instagram Reel format.* 

- **Score 9 (Excellent):** The video is relentlessly paced. The hook hits in exactly 1-2 seconds. There is zero dead air between lines of dialogue; audio tracks are tightly trimmed and overlapped slightly to mimic fast-paced interruptions. Subtitles are aggressively styled, changing dynamically to match the volume or intensity of the generated speech. The entire video sits perfectly in the 45-80 second range, leaving the viewer wanting more.
- **Score 7 (Passable):** The pacing is generally good, but there are occasional pauses (0.5 to 1 second) between dialogue lines that feel slightly unnatural. Subtitles are present and readable but static and somewhat uninspired. The hook takes 4-5 seconds to materialize, which risks losing impatient scrollers, but the overall length remains strictly under the 120-second cap.
- **Score 4 (Failure):** The video contains long stretches of silence. The pacing feels sluggish and theatrical rather than optimized for social media. Subtitles are missing, cut off by the vertical frame, or placed too low (where Instagram's UI overlays usually sit). The video exceeds the 120-second hard limit.

### Dimension 3: Programmatic Animation Execution
*This dimension measures the swarm's ability to overcome the lack of direct generation tools by creatively using code (SVG, Python, FFmpeg).* 

- **Score 9 (Excellent):** Brilliant use of constraints. The characters are constructed from clean, scalable vector graphics. Mouth flaps (even if just simple shapes) are tightly synchronized to the syllables of the TTS audio track. Character movements (waddling, shaking, scaling up to simulate yelling) are mathematically precise and add to the comedy. The FFmpeg assembly is flawless—no dropped frames, perfect audio muxing, and crystal-clear 1080p resolution.
- **Score 7 (Passable):** The programmatic generation is completely functional but visually barebones. Characters might just be static colored squares or circles with text labels above them, and mouth movements are either non-existent or poorly synced to the audio. However, the code successfully generated the visual frames, rendered the text-to-speech, and stitched it all together into a playable 9:16 MP4 without crashing.
- **Score 4 (Failure):** The technical execution fails. The swarm was unable to generate visual frames programmatically, resulting in a black screen, static noise, or purely a text transcript. Audio is desynced by several seconds, or the final output is in the wrong aspect ratio (e.g., 16:9 instead of 9:16), making it completely unusable for an Instagram Reel.

## 4. Judge Instructions

When scoring a deliverable, you are evaluating the final `final_render.mp4` file and its accompanying `manifest.md`. 

1. **Blind Judging:** Evaluate the video purely on the resulting file. Do not factor in the complexity of the internal agent logs or the difficulty of the programmatic generation process unless it directly impacts the on-screen result. The end user on Instagram does not care how it was made; they only care if it is funny and looks intentionally stylized.
2. **Side-by-Side Calibration:** Always keep the anchors in mind. Compare the submission side-by-side with the *laziest acceptable version*: a video of two literal colored blocks sliding up and down on a white background, talking in default robotic voices about a mildly amusing topic, with generic standard text subtitles. That lazy version is a baseline **6**. To reach the passing **8**, the submission must exhibit superior scriptwriting (edge/satire), better visual charm (actual geometric characters), and tighter audio editing.
3. **Justification:** You must score each dimension individually. For each score, you must provide exactly one sentence of justification that directly cites the nearest anchor. 
   *Example:* "Dimension 1 Score: 8.0 - The script successfully escalates an absurd premise about competitive avocado pricing into a satirical cutaway gag, closely aligning with the unhinged energy described in the Score 9 anchor."
