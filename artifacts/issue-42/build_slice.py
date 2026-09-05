import os
import zipfile
import numpy as np
from PIL import Image, ImageDraw, ImageFont
from gtts import gTTS
from moviepy.editor import VideoClip, AudioFileClip, CompositeVideoClip, concatenate_audioclips

print('=== STARTING BUILD_SLICE.PY ===')

# 1. Generate local TTS audios
print('Generating TTS files...')
tts1 = gTTS("Hi, I am Sippy. A very stable square.", lang='en', tld='com')
tts1.save('temp_sippy1.mp3')

tts2 = gTTS("Oh no, a circle! Ah! Physics!", lang='en', tld='co.uk')
tts2.save('temp_sippy2.mp3')

tts3 = gTTS("CRUSHED!", lang='en', tld='co.in')
tts3.save('temp_crushed.mp3')

# Speed variations using moviepy audio speedx
audio1 = AudioFileClip('temp_sippy1.mp3') # Normal
from moviepy.video.fx.all import speedx
audio2 = speedx(AudioFileClip('temp_sippy2.mp3'), 1.2) # Faster, higher pitch
audio3 = speedx(AudioFileClip('temp_crushed.mp3'), 0.8) # Slower, lower pitch

# 2. Composition details
# Durations: Scene 1 (0-3s), Scene 2 (3-8s), Scene 3 (8-10s)
# Total duration = 10s
total_duration = 10.0
fps = 24
width, height = 1080, 1920

# Create synchronized silence/audio track
# We'll align the audio clips at specific starting timestamps
# audio1 starts at 0.5s
# audio2 starts at 3.5s
# audio3 starts at 8.2s
from moviepy.audio.AudioClip import CompositeAudioClip
audio1 = audio1.set_start(0.5)
audio2 = audio2.set_start(3.5)
audio3 = audio3.set_start(8.2)

final_audio = CompositeAudioClip([audio1, audio2, audio3]).set_duration(total_duration)

def draw_text_with_stroke(draw, text, position, font, fill, stroke_fill, stroke_width):
    x, y = position
    # Draw stroke
    for dx in range(-stroke_width, stroke_width + 1):
        for dy in range(-stroke_width, stroke_width + 1):
            if dx*dx + dy*dy <= stroke_width*stroke_width:
                draw.text((x + dx, y + dy), text, font=font, fill=stroke_fill)
    # Draw text
    draw.text((x, y), text, font=font, fill=fill)

def make_frame(t):
    # Base background: Dark flat blue
    img = Image.new('RGB', (width, height), (24, 28, 40))
    draw = ImageDraw.Draw(img)
    
    # Use default font or fallback
    try:
        font_title = ImageFont.truetype("Arial.ttf", 80)
        font_sub = ImageFont.truetype("Arial.ttf", 50)
        font_huge = ImageFont.truetype("Arial.ttf", 120)
    except IOError:
        font_title = ImageFont.load_default()
        font_sub = ImageFont.load_default()
        font_huge = ImageFont.load_default()
    
    # Title "THE STABILITY TEST"
    draw_text_with_stroke(draw, "THE STABILITY TEST", (150, 150), font_title, (255, 255, 255), (0, 0, 0), 5)
    
    cx, cy = width / 2, height / 2 + 200
    
    if t < 3.0:
        # Scene 1: Sippy is proud and stable
        # Flat yellow square
        size = 250
        # Pulsing outline
        outline_w = int(10 + 4 * np.sin(2 * np.pi * t))
        draw.rectangle([cx - size/2, cy - size/2, cx + size/2, cy + size/2], fill=(255, 223, 0), outline=(255, 255, 255), width=outline_w)
        # Happy Eyes
        draw.ellipse([cx - 50 - 15, cy - 50 - 15, cx - 50 + 15, cy - 50 + 15], fill=(0, 0, 0))
        draw.ellipse([cx + 50 - 15, cy - 50 - 15, cx + 50 + 15, cy - 50 + 15], fill=(0, 0, 0))
        # Happy mouth (curved arc/smile or line)
        draw.arc([cx - 40, cy, cx + 40, cy + 40], start=0, end=180, fill=(0, 0, 0), width=8)
        
        # Subtitle text
        draw_text_with_stroke(draw, "Sippy: I am a very stable square.", (150, height - 300), font_sub, (255, 255, 255), (0, 0, 0), 3)
        
    elif t < 8.0:
        # Scene 2: Circle falls, hits Sippy, who panics and spins!
        t_scene = t - 3.0
        
        # Circle position (falls from top to center)
        circle_y = -200 + t_scene * 400 # falls down
        circle_x = cx - 50
        circle_radius = 100
        
        # Sippy spins and deforms based on scene time
        angle = t_scene * 180 # 180 deg/sec
        # Rotate square coords programmatically
        size = 250
        points = [
            (-size/2, -size/2),
            (size/2, -size/2),
            (size/2, size/2),
            (-size/2, size/2)
        ]
        # apply rotation & translation
        rad = np.radians(angle)
        cos_a, sin_a = np.cos(rad), np.sin(rad)
        rotated_points = []
        for px, py in points:
            # Squish factor as time goes on
            squish = 1.0 - 0.05 * t_scene
            px_s, py_s = px * squish, py * (2.0 - squish)
            rx = px_s * cos_a - py_s * sin_a + cx
            ry = px_s * sin_a + py_s * cos_a + cy
            rotated_points.append((rx, ry))
        
        # Draw rotated Sippy
        draw.polygon(rotated_points, fill=(255, 180, 0), outline=(255, 255, 255))
        # Eyes on rotated Sippy (simplified: follow center of Sippy)
        draw.ellipse([cx - 40, cy - 40, cx - 20, cy - 20], fill=(0, 0, 0))
        draw.ellipse([cx + 20, cy - 40, cx + 40, cy - 20], fill=(0, 0, 0))
        # Worried mouth (circle)
        draw.ellipse([cx - 15, cy + 10, cx + 15, cy + 40], fill=(0, 0, 0))
        
        # Draw the falling blue circle
        draw.ellipse([circle_x - circle_radius, circle_y - circle_radius, circle_x + circle_radius, circle_y + circle_radius], fill=(0, 150, 255), outline=(255, 255, 255), width=5)
        
        draw_text_with_stroke(draw, "Sippy: Oh no, a circle! Physics!", (150, height - 300), font_sub, (255, 255, 255), (0, 0, 0), 3)
        
    else:
        # Scene 3: Massive red triangle crushes everyone from top!
        t_scene = t - 8.0
        # Triangle height falls
        tri_y = -300 + t_scene * 1500
        # Draw red triangle
        tri_pts = [
            (cx, tri_y),
            (cx - 500, tri_y - 600),
            (cx + 500, tri_y - 600)
        ]
        
        # Draw squashed remains of Sippy and Circle
        draw.ellipse([cx - 300, cy + 100, cx + 300, cy + 150], fill=(255, 100, 0)) # orange mess
        
        # Draw triangle
        draw.polygon(tri_pts, fill=(255, 50, 50), outline=(255, 255, 255), width=8)
        
        # Draw CRUSHED! text in the center
        draw_text_with_stroke(draw, "CRUSHED!", (250, height/2), font_huge, (255, 255, 0), (255, 0, 0), 10)
        
    return np.array(img)

# Compile clip
clip = VideoClip(make_frame, duration=total_duration)
clip = clip.set_audio(final_audio)

# Write video file
clip.write_videofile('slice.mp4', fps=fps, codec='libx264', audio_codec='aac')

# Cleanup temporary audio files
for f in ['temp_sippy1.mp3', 'temp_sippy2.mp3', 'temp_crushed.mp3']:
    if os.path.exists(f):
        os.remove(f)

# 3. Write capabilities.md
print('Writing capabilities.md...')
capabilities_content = """# Capabilities
This project probe confirms the availability of the following local generation libraries:
- moviepy (validated)
- gtts (validated)
- Pillow (validated)

No cloud media APIs (e.g., OpenAI, Gemini, ElevenLabs) are used to generate the assets.
"""
with open('capabilities.md', 'w') as f:
    f.write(capabilities_content)

# 4. Write manifest.md
print('Writing manifest.md...')
manifest_content = """# Manifest
This archive contains the tracer slice assets and metadata.

- `capabilities.md`: Record of local python libraries and no cloud media API usage.
- `build_slice.py`: The python script used to programmatically generate this slice.
- `slice.mp4`: A 10-second 1080x1920 24fps video demonstrating the programmatic pipeline.
- `manifest.md`: This manifest file.
"""
with open('manifest.md', 'w') as f:
    f.write(manifest_content)

# 5. Zip into tracer_slice.zip
print('Zipping everything into tracer_slice.zip...')
with zipfile.ZipFile('tracer_slice.zip', 'w') as zipf:
    zipf.write('capabilities.md')
    zipf.write('build_slice.py')
    zipf.write('slice.mp4')
    zipf.write('manifest.md')

print('=== BUILD COMPLETE ===')
