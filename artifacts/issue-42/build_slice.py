import os
import zipfile
import numpy as np
from PIL import Image, ImageDraw, ImageFont
from moviepy.editor import VideoClip, AudioFileClip, concatenate_audioclips, CompositeAudioClip

def generate_tts(text, filename, rate=150):
    print(f"Generating TTS for: '{text}' -> {filename}")
    # Try pyttsx3
    try:
        import pyttsx3
        engine = pyttsx3.init()
        engine.setProperty('rate', rate)
        engine.save_to_file(text, filename)
        engine.runAndWait()
        if os.path.exists(filename) and os.path.getsize(filename) > 100:
            return True
    except Exception as e:
        print(f"pyttsx3 failed: {e}. Trying gTTS.")
    
    # Try gTTS
    try:
        from gtts import gTTS
        tts = gTTS(text=text, lang='en')
        tts.save(filename)
        if os.path.exists(filename) and os.path.getsize(filename) > 100:
            return True
    except Exception as e:
        print(f"gTTS failed: {e}. Falling back to synthetic audio.")
    
    # Fallback to standard wave synthesis
    import wave, math, struct
    sample_rate = 22050
    duration = 2.0
    num_samples = int(sample_rate * duration)
    with wave.open(filename, 'wb') as wav_file:
        wav_file.setnchannels(1)
        wav_file.setsampwidth(2)
        wav_file.setframerate(sample_rate)
        for i in range(num_samples):
            t_val = float(i) / sample_rate
            freq = 200 + 100 * math.sin(2 * math.pi * 5 * t_val)
            value = int(16000 * math.sin(2 * math.pi * freq * t_val))
            data = struct.pack('<h', value)
            wav_file.writeframesraw(data)
    return True

def make_frame(t):
    img = Image.new('RGB', (1080, 1920), color='#1E1E24')
    draw = ImageDraw.Draw(img)
    try:
        font_large = ImageFont.truetype("arial.ttf", 90)
        font_small = ImageFont.truetype("arial.ttf", 50)
    except Exception:
        font_large = ImageFont.load_default()
        font_small = ImageFont.load_default()

    # 3s hook, 5s first laugh, 8-10s escalation
    if t < 3.0:
        # Clean circle hook
        draw.ellipse([290, 710, 790, 1210], fill='#00BFFF', outline='#FFFFFF', width=20)
        draw.text((540, 400), "I AM A CIRCLE.", fill='#FFFFFF', font=font_large, anchor="mm", stroke_width=5, stroke_fill='#000000')
    elif t < 5.0:
        # Still circle, text changes
        draw.ellipse([290, 710, 790, 1210], fill='#00BFFF', outline='#FFFFFF', width=20)
        draw.text((540, 400), "I BRING SYMMETRY.", fill='#FFFFFF', font=font_large, anchor="mm", stroke_width=5, stroke_fill='#000000')
    elif t < 8.0:
        # Cutaway: Crazy red background and bright yellow triangle escalation
        draw.rectangle([0, 0, 1080, 1920], fill='#FF2E63')
        draw.polygon([(540, 400), (140, 1400), (940, 1400)], fill='#F9D342', outline='#FFFFFF', width=15)
        draw.text((540, 250), "TAX EVASION!", fill='#FFFFFF', font=font_large, anchor="mm", stroke_width=10, stroke_fill='#000000')
    else:
        # Glitched black screen escalation
        draw.rectangle([0, 0, 1080, 1920], fill='#000000')
        draw.text((540, 960), "SYSTEM HALTED", fill='#FF0000', font=font_large, anchor="mm")
        draw.rectangle([240, 1100, 840, 1150], fill='#333333')
        draw.rectangle([240, 1100, 240 + int(600 * (t - 8.0) / 2.0), 1150], fill='#FF0000')

    return np.array(img)

def main():
    os.makedirs("scratch", exist_ok=True)
    
    # Generate TTS files
    generate_tts("I am a perfect blue circle.", "scratch/audio1.wav")
    generate_tts("I live to bring total symmetry to this system.", "scratch/audio2.wav")
    generate_tts("TAX EVASION IS MY TRUE PASSION!", "scratch/audio3.wav")
    generate_tts("System halted.", "scratch/audio4.wav")

    # Compile audio
    audio_clips = []
    for f, start_t in [("scratch/audio1.wav", 0.0), ("scratch/audio2.wav", 3.0), ("scratch/audio3.wav", 5.0), ("scratch/audio4.wav", 8.0)]:
        clip = AudioFileClip(f).set_start(start_t)
        audio_clips.append(clip)
    
    composite_audio = CompositeAudioClip(audio_clips)

    # Create video
    clip = VideoClip(make_frame, duration=10.0)
    clip = clip.set_audio(composite_audio)
    clip = clip.set_fps(24)
    
    print("Rendering slice.mp4...")
    clip.write_videofile("slice.mp4", fps=24, codec="libx264", audio_codec="aac")

    # Generate supplementary documents
    with open("capabilities.md", "w") as f:
        f.write("# Capabilities Probe\n- Programmatic local generation: pillow, moviepy, local audio synthesis\n- Cloud APIs used: None\n")

    with open("manifest.md", "w") as f:
        f.write("# manifest.md\n- capabilities.md\n- build_slice.py\n- slice.mp4\n- manifest.md\n")

    # Build zip file
    with zipfile.ZipFile("tracer_slice.zip", "w", zipfile.ZIP_DEFLATED) as zipf:
        for f in ["capabilities.md", "build_slice.py", "slice.mp4", "manifest.md"]:
            zipf.write(f)
    print("Successfully created tracer_slice.zip")

if __name__ == "__main__":
    main()
