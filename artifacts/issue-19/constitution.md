# Constitution: Animated Comedy Instagram Reels

## 1. Goal-Specialized Philosophy
Our objective is to generate world-class, short-form animated comedy videos (under 2 minutes) optimized for Instagram Reels (1080x1920 vertical format). The stylistic lodestars are *Family Guy* and *South Park*: unapologetically satirical, culturally observant, slightly edgy, and fiercely reliant on immaculate comedic timing. 

To achieve this in a 9:16 scrolling environment, the following core principles apply:
*   **The 3-Second Hook:** The doomscroll is merciless. Videos must open *in media res* with high-stakes absurdity, a controversial statement, or a visual non-sequitur. No slow fade-ins.
*   **Vertical Dynamism (9:16):** Do not just crop a 16:9 video. The composition must be native to the vertical frame. Use extreme close-ups for dramatic/comedic effect, and stack characters vertically if they are conversing.
*   **Precision Timing & Cutaways:** Comedy is math. Utilize abrupt cuts, micro-pauses (the "blink"), and deadpan silence to contrast with chaotic action. The *Family Guy* cutaway structure is highly effective here if paced correctly.
*   **Sonic Punch:** Audio dictates the pacing. Dialogue must be crisp, rapid, and distinct. Layered, recognizable sound effects and abrupt audio cuts (cutting off a scream or music track instantly) are required for punchlines.
*   **Edgy, Satirical Core:** The humor must punch up or sideways, tackling modern cultural absurdities. It should push boundaries and evoke a strong reaction while remaining clever enough to avoid being merely offensive for shock value.

## 2. Outside Anchors
To ground our generated output, we draw upon the following real-world exemplars of animated comedy tailored to or thriving in short-form vertical video:

1.  **Family Guy - The "Cutaway Gag" Vertical Clips**
    *   *Exemplifies:* The art of the immediate pivot. A mundane setup abruptly hard-cuts to an absurd, visually distinct historical or pop-culture scenario. It teaches us economy of storytelling—establishing a joke's premise in exactly one sentence before delivering the visual punchline.
2.  **South Park - Cartman's Rapid-Fire Rants (TikTok/Reel Edits)**
    *   *Exemplifies:* Character-driven audio pacing and the "escalation of stakes." These clips show how a character starting at a 3/10 in anger and escalating to a 10/10 within 15 seconds hooks the viewer. Visually, it relies on minimal but highly expressive eye/mouth movements, proving that script and voice acting trump fluid animation.
3.  **MeatCanyon - YouTube Shorts / Instagram Reels**
    *   *Exemplifies:* Grotesque visual satire and extreme audio contrast. MeatCanyon shorts excel at taking recognizable pop-culture figures and pushing them into unsettling territory. It teaches the power of extreme close-ups, uncomfortable pauses, and ASMR-style whispers suddenly contrasted with loud bursts of audio for comedic shock value.

## 3. Scoring Rubric
Every generated video is evaluated against a 10-point scale based on strict technical adherence, visual framing, timing, and audio execution. 

*   **Score 4: (Poor):** Quantifiable failure of the short-form format. The time-to-first (TTF) comedic hook exceeds 72 frames (3.0 seconds at 24fps). Resolution padding is detected (e.g., 16:9 content nested with letterboxing comprising >5% of the 2,073,600 total pixels). Audio dynamic range is flat (RMS variance < 3dB), True Peak exceeds 0.0 dBTP (clipping), or audio LUFS falls outside the -20 to -10 range. Visuals lack Y-axis utilization, and duration exceeds 120.00 seconds. 
*   **Score 7: (Good):** The video meets absolute technical baseline standards. Resolution is strictly 1080x1920 with a Display Aspect Ratio (DAR) of 9:16 and Sample Aspect Ratio (SAR) of 1:1. Cutaways or transitions resolve within ±2 frames of the corresponding audio transient. Duration is strictly <120.00s. Audio strictly adheres to EBU R128 standards, measuring exactly -14.0 LUFS (±1.5) with a maximum True Peak of -1.0 dBTP. The script possesses a clear satirical target fitting the tone of the anchors, but may lack micro-timing precision (e.g., silence gaps before punchlines >250ms where <100ms is optimal).
*   **Score 9: (Exceptional):** Masterful execution with hyper-rigorous technical perfection. Frame-perfect audio-visual synchronization: audio transients for sudden actions/cuts align with video scene-change I-frames within <16ms. Visual comedy exploits the vertical frame flawlessly, mathematically proven by motion vector density distributed strategically across the top and bottom 33% of the 1920px Y-axis. The comedic "blink" or deadpan silence drops the noise floor below -60dBFS instantly, transitioning to punchline peaks within 1 frame (<=41.6ms at 24fps). Zero dropped frames, strictly encoded in H.264 High Profile Level 4.1 with `yuv420p` color space, utilizing precisely zero black padding pixels.

## 4. Pass Threshold
The numeric pass threshold is 7.

## 5. Integration Contract
You must ship a `manifest.md` file next to your deliverable. This file is subject to strict structural validation rules and must contain exact filenames, formats, and cryptographically sound technical proofs of the video properties.

The `manifest.md` MUST contain a compliant YAML code block (````yaml`) adhering to the following structural and validation requirements:

1.  **Exact Filenames and Container Specs:**
    *   `filename`: Must specify the exact string (e.g., `reel_final.mp4`).
    *   `container`: Must be `mp4` or `mov`.
2.  **Non-Trivial 1080x1920 & Format Checks:**
    *   `video_stream`: Must include exact extracted `ffprobe` values proving vertical native rendering: `width: 1080`, `height: 1920`, `codec_name: h264`, `profile: High`, `level: 4.1`, `pix_fmt: yuv420p`.
    *   `aspect_ratio_proof`: Must document SAR `1:1` and DAR `9:16`, with mathematical validation that `width/height == 0.5625`.
3.  **Audio Property Validation:**
    *   `audio_stream`: Must explicitly show `codec_name: aac`, `sample_rate: 48000`, `channels: 2`.
    *   `loudness_compliance`: Must contain an exact EBU R128 scan output snippet proving Integrated Loudness is `-14.0 LUFS` (±1.5) and True Peak is `<= -1.0 dBTP`.
4.  **Exact Byte & Frame Extraction Proofs (The "Tiny Sample"):**
    *   `magic_bytes`: A hex dump of the first 16 bytes of the video file to definitively prove container format signature (e.g., `00 00 00 18 66 74 79 70 6d 70 34 32...` proving `ftypmp42`).
    *   `frame_0_checksum`: The SHA-256 hash of exactly the first frame extracted via `ffmpeg -i filename -vf "select=eq(n\,0)" -vframes 1 frame0.png`, proving successful rendering and serving as a verifiable tiny sample of the vertical format.

**Example `manifest.md` Structural Expectation:**
```yaml
deliverable:
  filename: "satire_cutaway_01.mp4"
  duration_seconds: 45.24
technical_validation:
  video:
    width: 1080
    height: 1920
    codec: "h264"
    pix_fmt: "yuv420p"
    dar: "9:16"
    sar: "1:1"
    ratio_check: 0.5625
  audio:
    codec: "aac"
    sample_rate: 48000
    integrated_lufs: -14.2
    true_peak_dbtp: -1.1
cryptographic_proofs:
  magic_bytes_hex: "00 00 00 18 66 74 79 70 6d 70 34 32 00 00 00 00"
  frame_0_sha256: "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855"
```
*(Failure to strictly format the manifest or pass the extracted technical criteria results in an immediate invalidation of the deliverable).*

## Pass Threshold
Threshold: 7
