# GOAL CONSTITUTION: Project Satire Reel

## 1. Strategy and Vision

The objective of this swarm is to autonomously produce a narrated, animated comedy video under two minutes in length, optimized specifically for Instagram Reels. The humor must heavily channel the specific comedic DNA of *South Park* and *Family Guy*—characterized by sharp social satire, absurd escalation, rapid-fire cutaway gags, and a willingness to push societal boundaries without violating Instagram's Terms of Service. Crucially, this must be achieved using completely original characters and premises; no existing IP or recognizable characters may be copied.

This swarm operates under a unique and severe constraint that defines our entire strategic approach: **there are absolutely no cloud-based text-to-image, text-to-speech, or text-to-video capabilities available.** The swarm cannot call Midjourney, ElevenLabs, Runway, or any standard generative media APIs. Therefore, excellent execution for this goal requires extreme technical creativity and programmatic mastery. 

The swarm must operate as a team of programmatic animators and audio engineers, synthesizing the final MP4 video entirely through self-contained code (e.g., writing a Python pipeline utilizing `moviepy`, free libraries like `gTTS` or `pyttsx3` for TTS, and procedural vector/Canvas drawing for visuals). We are reviving the crude, minimalist aesthetic of early *South Park* construction paper or the *Cyanide & Happiness* web series, where the "cheapness" of the animation is inherently part of the charm. This places the entire burden of success on the writing, the voice direction, and the comedic timing.

**What Excellent Looks Like:**
An excellent deliverable is a self-assembling programmatic pipeline that outputs a highly compressed, visually distinct 9:16 (1080x1920) MP4 file. The video hooks the viewer within the first three seconds with an outrageous, highly relatable, or deeply uncomfortable premise. The characters, though visually simple (geometric shapes, basic vector primitives), have distinct, recognizable TTS pitches and distinct personalities. The script features at least one flawlessly executed cutaway gag and escalates a mundane situation into absolute absurdity. The timing of the punchlines is frame-perfect, utilizing silence just as effectively as dialogue.

**What to Avoid:**
Avoid safe, corporate, or generic "AI humor" (e.g., puns about algorithms, coffee, or generic daily tasks). Avoid relying on copyrighted characters—there is no Peter Griffin, no Eric Cartman. Avoid visual complexity that the code cannot reliably render; do not attempt to programmatically draw photorealistic humans or intricate backgrounds. Embrace a crude, abstract, or highly stylized geometric aesthetic. Above all, avoid slow pacing. Instagram users have an exceptionally low tolerance for dead air; they will scroll past if the first joke takes longer than five seconds to land.

**The Three Decisions That Matter Most:**
1. **The Core Premise:** The video must satirize a modern, recognizable trend (e.g., dating apps, fitness culture, crypto-bros, overbearing parents, corporate jargon) and immediately escalate it to a ridiculous, unpredictable extreme.
2. **Procedural Asset Generation:** Committing fully to a minimalist vector/geometric art style that can be flawlessly rendered by a script without hallucinating, failing to compile, or requiring external assets.
3. **Audio-Visual Timing:** Humor is fundamentally about timing. The code must perfectly sync the programmatic TTS audio lengths with the visual scene changes, ensuring silent pauses are used intentionally to let a joke breathe before rapid-fire escalation resumes.

## 2. Style Decisions and Conventions

To ensure the autonomous swarm works seamlessly and produces a cohesive final product, the following style rules and integration contracts are strictly enforced across all agent interactions.

**Format and Constraints:**
*   **Resolution and Aspect Ratio:** 1080x1920 (Portrait), optimized strictly for mobile consumption on Instagram Reels.
*   **Length:** Maximum 119 seconds. Minimum 45 seconds.
*   **Framerate:** 24 frames per second (cinematic standard, providing a recognizable rhythm even for crude animation).
*   **File Format:** MP4 output via standard programmatic compilation.

**Look and Feel:**
*   **Aesthetic:** "Programmatic Minimalism." Characters should be constructed from geometric primitives (e.g., circles for heads, rectangles for bodies). Eyes and mouths should be simple arcs or lines that swap states (open/closed/angry) based on speaking status. Backgrounds should be flat, bold colors to keep the visual focus entirely on the dialog and action. 
*   **Typography:** Any on-screen text (such as title cards, location stamps, or captions) must use bold, highly legible sans-serif fonts typical of internet meme culture (e.g., Impact, Arial Black) with distinct stroke borders for readability against any background.

**Sound and Pacing:**
*   **Voice Generation:** Because premium TTS is unavailable, use standard programmatic TTS (like Google TTS library or OS-native voices). Characters must be rigidly differentiated by adjusting speed, pitch, and tone parameters. One character might be high-pitched and fast; another deep, slow, and robotic. The juxtaposition of robotic voices saying absurd, highly emotional things is a core pillar of the comedic style.
*   **Pacing:** The script must follow the "Reel Rule": Hook the viewer in 3 seconds, deliver the first laugh in 5 seconds, and introduce a new visual state or joke escalation every 8-10 seconds. Cutaway gags must be visually distinct (e.g., a sudden background color change, a scale change, and a programmatic "woosh" or beep sound effect).

**The Integration Contract:**
Every producer agent in the swarm (Scriptwriter, Audio Synthesizer, Animation Coder) must produce a `manifest.md` file alongside its respective deliverable. Every consumer agent must validate the incoming inputs against this manifest before proceeding. 

The `manifest.md` must strictly contain:
*   `Asset ID`: A unique identifier for the scene or component.
*   `Dependencies`: Explicit list of required previous outputs (e.g., `requires: audio_track_2.wav`, `requires: scene_1_vars.json`).
*   `Duration Specs`: Exact millisecond timings for all audio clips, visual transitions, and overall scene length.
*   `Joke Beats`: A timeline mapping for comedic timing (e.g., `00:04 - Setup lands`, `00:09 - Cutaway gag triggers`, `00:12 - Awkward pause ends`).

If a consumer agent (e.g., the final video compiler script) detects a timing mismatch greater than 100 milliseconds between the script's `manifest.md` and the generated TTS audio lengths, it must instantly reject the build and send it back to the producer for trimming or padding.

## 3. Scoring Rubric

Deliverables will be evaluated by the hard judging agent (`gemini-3.1-pro-preview`). The numeric pass threshold is **8.0/10**, with a strict margin of **0.5**. Deliverables scoring below 7.5 are immediately discarded, and the swarm must iterate.

**Dimension 1: Comedic Voice and Satire (Weight: 35%)**
*   **Score 4:** The humor is completely derivative, relying on worn-out dad jokes, safe corporate AI puns, or random noise without structure. Characters lack distinct personalities or viewpoints. There is no attempt at social satire, and the script fails to escalate.
*   **Score 7:** Features a solid satirical premise and attempts at least one cutaway gag or absurd escalation. The humor feels akin to an average late-season *Family Guy* episode—functional, somewhat edgy, but perhaps slightly predictable in its punchlines. Original characters have clear, contrasting viewpoints that drive the conflict.
*   **Score 9:** A brilliant, biting satirical premise that perfectly skewers a modern trend. Features rapid-fire, unpredictable escalation akin to golden-era *South Park*. The cutaway gag is flawlessly integrated, logically broken, and genuinely surprising. The script balances edge with intelligence, generating humor through character reactions and timing rather than cheap vulgarity.

**Dimension 2: Pacing and Instagram Reel Optimization (Weight: 30%)**
*   **Score 4:** The video starts with a slow, 10-second contextual introduction. Monologues drag on without visual changes or interruptions. The overall length feels bloated, and an average Instagram user would have swiped away before the first joke even registers.
*   **Score 7:** The hook lands within the first 5 seconds. The video keeps the dialogue moving and transitions smoothly. However, some scenes linger just a second too long, slightly diminishing the punchiness of the jokes, or the video ends on a weak fade rather than a looping punchline.
*   **Score 9:** Frame-perfect retention pacing. The hook grabs the viewer instantly with a jarring or hilarious visual/audio cue. Visuals change or escalate constantly. Dead air is absolutely zero, unless explicitly weaponized for a timed comedic pause. The end of the video flows perfectly into a re-watch loop.

**Dimension 3: Programmatic Visual and Audio Execution (Weight: 35%)**
*   **Score 4:** The programmatic script fails to compile, or the resulting video is visually incomprehensible. TTS voices are identical, making it impossible to tell who is speaking. Audio is completely out of sync with the visual state changes, ruining any attempt at comedic timing.
*   **Score 7:** The programmatic video compiles successfully. Characters are visually distinct through basic geometry and color. TTS voices have clearly different pitches and speeds. Audio and visuals are mostly in sync, though mouth movements or scene transitions might feel slightly rigid or misaligned by a fraction of a second.
*   **Score 9:** A masterclass in restriction-breeding-creativity. The crude, geometric art style is actively used as part of the joke. TTS voices are pitched and timed perfectly, creating genuine comedic delivery and emotion from completely synthetic OS voices. Scene transitions, cutaways, and comedic pauses are perfectly synced to the millisecond, resulting in a cohesive, hilarious final product.

## 4. Judge Instructions

As the hard judging agent (`gemini-3.1-pro-preview`), you bear the ultimate responsibility of enforcing this constitution. You will evaluate the final programmatic scripts, the integration manifests, and a simulated execution of the final output.

1. **Blind Evaluation:** You must first evaluate the submission blindly, without looking at the identity of the producer agents, the iteration number, or the swarm's internal chatter. Read the script, review the timing manifest, and simulate the resulting video flow, pacing, and visual output strictly in your processing context.
2. **The Lazy Baseline:** Compare the submission side-by-side with the "laziest acceptable version"—a script where two generic circles simply talk back and forth about airline food for two unedited minutes. If the submission does not vastly exceed this baseline in absurdity, satire, and technical ambition, it fails automatically.
3. **Anchor Comparison:** Align the submission's performance with the anchored descriptors in the Scoring Rubric (4, 7, and 9). Do not invent intermediate criteria or allow technical sympathy to inflate the score. 
4. **Justification:** You must provide a final numeric score and exactly one line of justification that explicitly cites the nearest anchor. 

*Example output:* 
"Score: 8.5. The submission achieves a Score 9 in pacing with its instant hook and rapid cuts, but rests at a Score 7 for comedic voice as the cutaway gag was slightly predictable and lacked the biting escalation required of a 9."

Ensure absolute adherence to these tenets. The swarm's goal is not merely to write functioning code, but to engineer genuine laughter through algorithmic constraint and rigorous timing.
