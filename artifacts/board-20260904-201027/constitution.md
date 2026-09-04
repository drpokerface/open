# GOAL CONSTITUTION: Project Subversive Shorts (Insta Reel)

## 1. Strategy and Vision

**The Prime Directive**
The ultimate objective of this swarm is to conceive, engineer, and deliver a fully narrated, animated comedy video under two minutes in length, explicitly optimized for Instagram Reels. Because our operational environment lacks raster image generation, native video generation APIs, and external text-to-speech APIs, we must embrace a radically clever technical strategy. The final deliverable will be a self-contained, programmatic HTML5/JS/CSS file that functions as an automatic video player. It will render vector-based SVG cutout animation directly to a strict 9:16 aspect ratio canvas, utilizing the browser's native Web Speech API (`window.speechSynthesis`) for character narration, and the Web Audio API for synthetic sound effects. The end-user will simply load the file in a modern browser and screen-record the output to post on Instagram.

**The Comedic Philosophy**
Excellent execution for this goal demands a complete mastery of the comedic styles popularized by *South Park* and *Family Guy*, without ever plagiarizing their intellectual property. The humor must be sharp, satirical, highly irreverent, and heavily reliant on escalation and non-sequiturs. Excellent work in this medium recognizes that since our visual fidelity is intentionally crude (programmatic SVG cutouts), the script and comedic timing must be flawless.

What to avoid: Do not write generic, safe, or easily predictable humor. Avoid continuous, fluid animation attempts that will break the HTML5 canvas performance or bloat the code. Avoid using any pre-existing characters. Do not rely on subtle visual gags; Insta Reel audiences watch on small screens, often with divided attention.

**The Three Decisions That Matter Most:**
1. **The 3-Second Hook and Kinetic Captions**: Instagram Reels demand immediate engagement. The video must start *in media res* with an absurd statement, a loud noise, or a shocking visual. Furthermore, to survive the Reels algorithm and compensate for any Web Speech API mumbling, big, bold, kinetic text captions must be rendered onto the HTML canvas, perfectly synced with the dialogue.
2. **Satirical Escalation**: The narrative must follow a hyper-compressed arc. Establish a seemingly mundane premise in the first 15 seconds, and relentlessly escalate it to absolute, unhinged absurdity by the one-minute mark. Use hard-cut cutaway gags (the *Family Guy* method) to break tension and introduce secondary punchlines.
3. **Technical Elegance over Complexity**: The early *South Park* cutout style is our savior. Characters should be basic geometric SVGs. Animation should be limited to bouncing torsos, flapping jaws (the iconic floating head technique is highly encouraged), and rotating arms. The humor comes from the stiffness and the dialogue, not fluid motion.

## 2. Style Decisions and Conventions

**Format and Length**
The output must strictly enforce a viewport of 1080x1920 pixels (9:16 portrait orientation). The CSS must include a master container that scales seamlessly using `transform: scale()` to fit the user's browser window while maintaining the 9:16 ratio. The runtime of the animation and narrative script must fall precisely between 60 and 110 seconds.

**Visual Look and Technical Implementation**
All visuals must be generated via inline SVGs manipulated by JavaScript and CSS. Use thick black strokes, bold, highly saturated flat colors, and minimal shading. Backgrounds should be simplistic, stylized vector horizons or rooms. Animation will rely on CSS transitions or `requestAnimationFrame` JavaScript loops. When characters speak, their mouths should alternate rapidly between open and closed vector states, or their entire heads should bounce.

**Sound and Narration**
Because we lack external TTS capabilities, dialogue is exclusively handled by `window.speechSynthesis`. Each original character must be assigned a distinct voice profile in the JavaScript configuration. You must manipulate the `pitch` (e.g., 0.5 for a booming voice, 1.8 for a squeaky voice) and `rate` (e.g., 1.2 for fast-talking anxiety) to create recognizable personas. Sound effects (explosions, punches, alarms) must be generated using `AudioContext` oscillators or visualized as massive, on-screen comic-book text.

**Naming and File Formats**
There is exactly one acceptable file format for the final video payload: a singular `index.html` file. It must contain all HTML, CSS, JavaScript, and SVG data within its tags. No external API calls to remote servers. No hosted images. Code variables should be strictly camelCase and highly descriptive (e.g., `charOnePitch`, `sceneTwoTimerMs`, `animateCutaway`).

**The Integration Contract**
To ensure seamless collaboration across the swarm, every producer agent (Scriptwriter, Storyboarder, Audio Coder, Vector Artist) MUST ship a `manifest.md` alongside their deliverable.
The `manifest.md` must contain:
- A timestamped chronological event timeline (e.g., `00:00 - 00:05: Character A speaks, pitch 1.2`).
- A strict inventory of all SVG IDs required or provided.
- A structural validation checklist confirming zero external asset dependencies.
Every consumer agent MUST aggressively validate the upstream deliverable against this `manifest.md` before proceeding. If a script requests an action that violates the single-file SVG constraint or the 9:16 layout, the consumer agent must reject it, halt, and rewrite the integration to enforce the overarching constraints.

## 3. Scoring Rubric

This rubric is the absolute standard by which all deliverables in this medium will be judged. The numeric pass threshold is **8.0/10**, with a margin of **0.5**.

**Dimension 1: Comedic Writing and Pacing (The Humor Engine)**
This measures the sharpness of the satire, the quality of the cutaway gags, and the sheer density of jokes.
- **Score 4**: The humor is derivative, safe, or relies on tired tropes. The pacing is sluggish, leaving dead air between lines of dialogue. The narrative lacks escalation. It feels like a boring corporate presentation rather than an edgy comedy short.
- **Score 7**: The script is genuinely funny and competent. It includes at least one solid cutaway gag and maintains a brisk pace suitable for an Insta Reel. Characters have distinct comedic voices, and the premise escalates properly, though the climax might feel slightly predictable.
- **Score 9**: Exceptional, laugh-out-loud writing. The humor is daring, absurd, and brilliantly subversive, rivaling the best golden-era episodes of *South Park* or *Family Guy*. The pacing is relentless. Cutaway gags are jarring and perfectly timed. The 3-second hook is mesmerizing, and the script utilizes the limitations of the medium as part of the joke.

**Dimension 2: Visual Aesthetic and Reel Formatting (The Cutout Canvas)**
This measures the execution of the 9:16 HTML/SVG programmatic canvas and the effectiveness of the cutout animation style.
- **Score 4**: The aspect ratio is broken or not optimized for vertical viewing. SVGs are overly complex, breaking the HTML file, or they are too abstract to be recognizable. Animation is non-existent, leaving characters completely static while they speak.
- **Score 7**: The 1080x1920 layout is strictly enforced. The cutout characters are visually distinct with bold colors and thick outlines. Characters bob or their mouths move when the TTS speaks. The visual aesthetic clearly successfully mimics a crude, charming 2D animation style.
- **Score 9**: A technical marvel. The SVGs are expressive despite their simplicity. CSS transforms are used creatively to simulate dramatic camera zooms, pans, or screen shakes. The cutout aesthetic is weaponized for comedic effect (e.g., character limbs detaching humorously). Kinetic captions dominate the screen with perfect sync, typography, and styling, making it a native-feeling Instagram Reel.

**Dimension 3: Audio Synthesis and Sound Design**
This measures the creative manipulation of the Web Speech API and Web Audio API to replace traditional voice acting and Foley.
- **Score 4**: All characters sound exactly the same using the default browser TTS voice. Rates and pitches are unadjusted. There are no sound effects, making the cutaway gags feel empty and lifeless.
- **Score 7**: Pitch and rate are manipulated to give each character a unique, identifiable voice. The TTS triggers reliably in sync with the visual changes. Basic Web Audio oscillators (or text-based sound effects) are used to punctuate jokes and scene transitions.
- **Score 9**: The manipulation of the Web Speech API is so clever that it feels like intentional, stylized voice acting. Pauses, stutters, and varying speeds are programmed directly into the dialogue strings to enhance comedic timing. Web Audio API is used to generate rudimentary but effective musical stings, drum beats for cutaways, or satisfying sound effects that elevate the physical comedy.

**Dimension 4: Adherence to the Integration Contract**
This measures the swarm's discipline in utilizing `manifest.md` and maintaining a single-file, dependency-free architecture.
- **Score 4**: The deliverable requires external libraries, images, or internet access to function. Producers failed to include `manifest.md`, or consumers blindly accepted broken code that violates the technical constraints.
- **Score 7**: The integration contract is respected. `manifest.md` is present and accurate. The final output is a single, functioning `index.html` file that operates completely offline and contains all necessary vector and audio logic.
- **Score 9**: The swarm demonstrates flawless modularity. The `manifest.md` is beautifully detailed, and the final code is incredibly well-commented, organized, and optimized for performance. Consumer agents actively caught and corrected upstream inefficiencies, resulting in a lightweight, robust, and mathematically perfect programmatic video file.

## 4. Judge Instructions

As an evaluative agent, your role is to enforce this constitution with cold, objective precision. When judging a deliverable, you must adhere to the following workflow:

1. **Blind Evaluation**: Review the `index.html` file and the final script blindly, without analyzing the agent logs or the iterations that led to the final product. Focus solely on the resulting user experience.
2. **The Baseline Test**: First, compare the deliverable against the laziest acceptable version (a static stick figure with default, unedited TTS reading a basic script). If it does not significantly surpass this baseline in all four dimensions, it automatically fails and receives a score capped at 5.
3. **Side-by-Side Anchoring**: Evaluate the deliverable side-by-side with the specific 4, 7, and 9 anchors detailed in the Scoring Rubric. Do not invent new criteria. For each dimension, determine which anchor the work most closely resembles.
4. **Scoring and Justification**: Assign a numerical score (1-10) for each dimension. You must explicitly cite the nearest anchor and provide exactly one line of justification for your score.

*Example format for judging a dimension:*
"Dimension 1 (Humor): 8.5/10. Nearest Anchor: 9. Justification: The script achieves the hyper-fast pacing and absurd escalation of the 9 anchor, though it lacked a definitive 3-second hook to truly max out the score."

If the final aggregated score is below the 8.0 pass threshold (accounting for the 0.5 margin), you must mandate a targeted rewrite based precisely on the failing dimension.
