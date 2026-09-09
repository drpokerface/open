# 1. Strategy and Vision

The objective is to produce a narrated, animated comedy short, strictly under two minutes in length, engineered specifically for distribution as an Instagram Reel. The comedic voice must heavily channel the irreverent, absurd, and socially satirical tone of *South Park* or the rapid-fire, non-sequitur, cutaway-heavy style of *Family Guy*. However, under no circumstances will the swarm utilize existing copyrighted characters, locations, or specific lore from these properties. We are extracting the *essence* of their comedic mechanics—subversive themes, sharp juxtaposition, deeply flawed but distinct characters, and unapologetic absurdity—and applying it to an entirely original intellectual property tailored for short-form social media.

Crucially, this swarm operates under severe media-generation constraints. We have absolutely no access to external text-to-speech services, image generators, or video rendering pipelines like text-to-video APIs or even a guaranteed local FFmpeg installation. Therefore, the swarm must execute a brilliant technical pivot: the "video" will not be an .mp4 file. Instead, the final deliverable will be a self-contained, highly choreographed HTML/CSS/JavaScript web application that *acts* as a video when launched in a modern web browser.

This constraint is actually a stylistic superpower. The crude, rigid, construction-paper cutout animation style of early *South Park* translates flawlessly to CSS-manipulated SVG elements and basic DOM shapes. The narration and character dialogue will be synthesized natively in real-time using the browser's built-in `window.speechSynthesis` API (Web Speech API), manipulating pitch and rate to create distinct comedic voices. When a user or publisher opens the HTML file and clicks "Play", the browser will render a perfect 9:16 aspect ratio animation sequence accompanied by generated voices, which can then be trivially screen-recorded for Instagram upload.

**What excellent looks like:**
An excellent deliverable is a hilarious, fast-paced HTML5 sequence that hooks the viewer within the first three seconds. The dialogue is snappy, cynical, and rhythmically precise. The humor relies on escalating absurdity, perhaps featuring a mundane situation (e.g., waiting in line at a futuristic DMV, or two geometric shapes arguing about the literal boundaries of their 2D existence) that rapidly spirals into chaotic, disproportionate stakes. The visual aesthetic fully embraces its programmatic nature: rigid, bouncing SVGs, sudden scaling for emphasis, and flat, bold colors. It feels like an intentional, highly stylized artistic choice, not a technological limitation. The writing carries the entire experience, making the viewer forget they are watching code execute.

**What to avoid:**
Avoid safe, corporate, or generic AI humor at all costs. Puns, dad jokes, and gentle situational comedy are catastrophic failures for this specific goal. Avoid overly complex visual ambitions; attempting Disney-level fluidity or 3D rendering with vanilla CSS will look broken and distract from the comedy. Avoid slow pacing; any pause longer than one second kills the comedic momentum and destroys Instagram Reel retention metrics. Avoid writing dialogue that sounds like a language model attempting to be helpful; characters must be flawed, opinionated, and aggressively funny.

**The decisive factors:**
1. *The Script's Edge:* The writing must be sharp, willing to be mildly offensive (within Instagram's acceptable use policies), and structurally reliant on comedic escalation or cutaway gags. It must provoke a genuine laugh.
2. *Timing and Orchestration:* The JavaScript must perfectly synchronize the `speechSynthesis` events with the CSS animations. A joke's punchline depends entirely on timing; rendering a visual gag half a second before the audio punchline ruins the joke.
3. *The Hook:* The first three seconds must introduce a bizarre conflict, an outrageous statement, or an immediate subversion of expectations to stop the user from swiping to the next Reel.

# 2. Style Decisions and Conventions

To ensure flawless integration and execution across the swarm, all agents will adhere to the following strict technical and stylistic conventions. Any deviation will result in immediate failure of the integration step.

**Format and File Specifications:**
The core deliverable will be a single file named `index.html`. This file must contain all HTML structure, inline CSS styling, and inline JavaScript logic necessary to execute the entire animation and audio sequence from start to finish. External dependencies (like fetching images, fonts, or scripts from CDNs) are strictly prohibited to ensure offline reliability and execution safety. All visual assets must be generated natively via DOM elements (e.g., `<div>` tags styled as circles, rectangles, and polygons) or fully inline SVG code blocks.

**The Integration Contract:**
Every producer agent generating a component, script, or final deliverable must ship a `manifest.md` file alongside their code. This serves as the unbending integration contract. Every consumer agent must validate the payload against this manifest before proceeding with judging or orchestration.
The `manifest.md` must strictly contain the following structure:
- Component Name: [Name of the scene or full video]
- Expected Duration: [Runtime in seconds, must be between 60s and 119s]
- Aspect Ratio: [Must strictly state "9:16"]
- Characters: [List of characters with their assigned SpeechSynthesis pitch/rate values, e.g., "Bob (Pitch: 0.8, Rate: 1.2)"]
- Dependencies: [Must strictly state "None - Pure HTML/JS/CSS"]

**Look and Canvas Dimensions:**
The visual container must be absolutely locked to a 9:16 aspect ratio to simulate a mobile screen for Instagram Reels. The CSS must define a central, unscrollable wrapper: `width: 1080px; height: 1920px;` (or perfectly scaled responsive equivalents using `vh` and `vw` units while maintaining the exact ratio, clipped with `overflow: hidden`). The background should be a flat, bold color or a simple geometric landscape. Characters should be constructed from clear, distinct geometric primitives. Movement should be blocky and discrete—mimicking stop-motion or cutout animation. When a character speaks, their "mouth" (a simple black line or oval) should simply flip vertically or scale up and down in time with the text.

**Sound and Narration:**
Audio relies completely on the Web Speech API (`window.speechSynthesis`). The script must instantiate `SpeechSynthesisUtterance` objects for every line of dialogue. To differentiate characters, agents must assign mathematically distinct `pitch` (ranging from 0.1 to 2.0) and `rate` (ranging from 0.5 to 2.0) values.
*Convention:* A "narrator" or straight-man character should have a standard pitch (1.0) and rate (1.0). A "manic" or panicked character should have a high pitch (1.8) and fast rate (1.5). A "depressed/cynical" character should have a low pitch (0.4) and slow rate (0.8). The JavaScript must chain the dialogue sequentially, strictly utilizing the `onend` event listener of one utterance to trigger the animation and speech of the next, completely preventing overlapping audio chaos.

**Pacing and Length:**
The total runtime must fall precisely between 60 and 119 seconds. The script must contain an average of one scene change, cutaway gag, or major visual shift every 10 to 15 seconds to maintain visual interest for the TikTok/Reels generation. The dialogue must be continuous, with no dead air unless specifically used for a timed comedic beat (e.g., a two-second awkward silence following an outrageous claim, immediately broken by a chaotic event or loud noise simulated by a character yelling).

# 3. Scoring Rubric

Judges will evaluate deliverables based on three primary dimensions. The numeric pass threshold is 8.0 out of 10, with a margin of 0.5. A score below 7.5 results in immediate rejection and a mandate for total script or orchestration rewrite. Evaluators must be incredibly strict; mediocre comedy is worse than no comedy.

**Dimension 1: Comedic Impact & Writing (Weight: 40%)**
This measures the success of the humor. Does it capture the satirical, irreverent, and absurd essence of *South Park* or *Family Guy* without copying them? Is the dialogue sharp, punchy, and surprising?
*   **Score 9 (Exceptional):** The script is genuinely hilarious and subversive. It features a brilliant, ridiculous premise that escalates perfectly. The characters have highly distinct comedic voices and worldview conflicts. It includes perfectly placed cutaway gags or non-sequiturs that land flawlessly. Example: A deeply satirical take on gig-economy culture where two basic SVG rectangles argue about their union rights as background props, culminating in a visual gag of a giant realistic (ASCII art) cursor deleting them. The humor relies on wit and shock value seamlessly blended.
*   **Score 7 (Acceptable):** The humor is solid and clearly attempts a satirical or absurd tone. It successfully avoids generic tropes, but the escalation might plateau, or the punchlines are slightly predictable. It feels like an average, mid-season episode of a competent Adult Swim show. It provokes a smile, but perhaps not a loud laugh.
*   **Score 4 (Failure):** The comedy is safe, bland, or relies entirely on generic puns and wordplay. The tone feels like a corporate training video attempting to be "edgy" or relatable. Alternatively, it is entirely random without being structurally funny, confusing mere chaos with authored comedy. It is boring.

**Dimension 2: Technical Execution of Constraints (Weight: 30%)**
This measures the swarm's ability to orchestrate the HTML/CSS/JS architecture as a substitute for traditional video rendering.
*   **Score 9 (Exceptional):** The `index.html` runs flawlessly in a browser. The Web Speech API is utilized brilliantly, with distinct voices and zero overlapping audio bugs. The CSS cutout animation is charming, deliberate, and highly expressive despite its simplicity. The 9:16 framing is perfectly locked and responsive. The JavaScript code is clean, modular, and the asynchronous chaining of audio-visual events is mathematically precise.
*   **Score 7 (Acceptable):** The file runs without crashing and the story is fully comprehensible. Voices are distinguishable from one another. However, the animation might be a bit too static, relying only on color changes, or there might be occasional split-second delays between an utterance ending and the next beginning, which slightly hurts the comedic timing.
*   **Score 4 (Failure):** The application throws JavaScript errors preventing playback. Voices overlap, making dialogue an incomprehensible wall of noise. The aspect ratio is broken, requiring the user to scroll horizontally or vertically to see the action. The animation consists of nothing more than raw text appearing on a white screen.

**Dimension 3: Pacing & Instagram Suitability (Weight: 30%)**
This measures the short's viability for a high-churn algorithmic feed (Instagram Reels), where attention spans are measured in milliseconds.
*   **Score 9 (Exceptional):** The video grabs attention instantly—the core conflict or primary joke is introduced within the first 3 seconds. The pacing is relentless, with rapid-fire dialogue and sharp visual shifts keeping the viewer locked in. The runtime is perfectly under 120 seconds, ending abruptly on a strong, memorable punchline that encourages loop re-watching.
*   **Score 7 (Acceptable):** Fits the time constraints and has a decent initial hook. It might linger a few seconds too long on a single static shot or recurring gag, risking a swipe-away from a low-attention-span viewer, but recovers well enough to finish strong before the 120-second mark.
*   **Score 4 (Failure):** The first 10 seconds are bogged down in exposition or slow setup. The pacing drags terribly. Pauses between dialogue are far too long, destroying momentum. The video abruptly cuts off before the central joke resolves, or it blatantly exceeds the 120-second hard limit.

# 4. Judge Instructions

As an autonomous agentic judge, you are the final quality gate before this artifact is presented for human recording and publishing. You must enforce the 8.0/10 threshold ruthlessly. Accept nothing less than exceptional structural comedy and flawless programmatic timing.

1.  **Blind Scoring:** You must evaluate the deliverable purely on its output. Open the `index.html` in a sandboxed headless browser environment (or execute a highly rigorous mental trace of the DOM/JS lifecycle if headless execution is temporarily unavailable). Do not let the complexity or length of the underlying code sway you; only the final audio-visual comedic output matters to the end user.
2.  **Side-by-Side Anchor Alignment:** You must place the work side-by-side with the rubric anchors. Do not invent your own standards. If the comedy is safe, polite, and uninspired, it is definitively a 4, even if the JavaScript orchestration is flawless.
3.  **The "Laziest Acceptable" Baseline:** Compare the submission against the laziest acceptable version: a 60-second video of two static colored squares talking to each other with generic, unmodified Web Speech voices about something mildly absurd, with zero visual movement. If the submission does not significantly exceed this baseline in comedic writing, visual charm, and precise timing, it categorically fails.
4.  **Justification Requirements:** You must output your final numeric score, explicitly check it against the pass margin, followed by a single-line justification directly citing the nearest rubric anchor for each dimension.
    *   *Format Example:* "Score: 6.5/10 - Fails threshold. Dimension 1 aligns with anchor 4 (relies on safe puns), Dimension 2 aligns with anchor 7 (runs well but static), Dimension 3 aligns with anchor 7 (decent pacing). Rewrite required."
