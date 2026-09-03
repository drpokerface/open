import numpy as np
from moviepy.editor import VideoClip, AudioArrayClip
from PIL import Image, ImageDraw, ImageFont

def get_font():
    for f in ["DejaVuSans-Bold.ttf", "FreeSansBold.ttf", "LiberationSans-Bold.ttf", "arial.ttf"]:
        try:
            return ImageFont.truetype(f, 60)
        except:
            pass
    return ImageFont.load_default()

FONT = get_font()

def draw_text_large(img, text, y_center):
    small = Image.new('RGBA', (1200, 200), (0,0,0,0))
    d = ImageDraw.Draw(small)
    d.text((5, 5), text, fill="white", font=FONT)
    bbox = small.getbbox()
    if not bbox:
        return
    small = small.crop(bbox)
    w, h = small.size
    target_w = img.width - 100
    ratio = target_w / w
    if ratio < 1: ratio = 1
    if ratio > 10: ratio = 10
    new_w, new_h = int(w * ratio), int(h * ratio)
    large = small.resize((new_w, new_h), Image.NEAREST)
    img.paste(large, ((img.width - new_w)//2, y_center - new_h//2), large)

def make_frame(t):
    W, H = 720, 1280
    if 4.0 <= t < 6.0:
        img = Image.new('RGB', (W, H), color=(200, 0, 0))
        draw = ImageDraw.Draw(img)
        draw.polygon([(100, 100), (300, 400), (200, 900), (50, 700)], fill=(0, 255, 0))
        draw.polygon([(400, 200), (600, 100), (700, 600), (500, 800)], fill=(0, 0, 255))
        draw_text_large(img, "CUTAWAY TO A", H - 400)
        draw_text_large(img, "FATAL MEMORY LEAK", H - 250)
    else:
        img = Image.new('RGB', (W, H), color=(10, 20, 40))
        draw = ImageDraw.Draw(img)
        cy = 400
        r = 200
        draw.ellipse([W//2 - r, cy - r, W//2 + r, cy + r], fill=(255, 140, 0))
        
        if t < 2.0:
            draw_text_large(img, "I AM A CIRCLE TRAPPED", H - 400)
            draw_text_large(img, "IN A PYTHON SCRIPT.", H - 250)
        elif 2.0 <= t < 4.0:
            draw_text_large(img, "MY ONLY HOPE IS", H - 400)
            draw_text_large(img, "A KERNEL PANIC.", H - 250)
        elif t >= 6.0:
            draw_text_large(img, "WOW. THAT EXPLAINS", H - 400)
            draw_text_large(img, "THE FRAME DROPS.", H - 250)
            
    return np.array(img)

def generate():
    W, H = 720, 1280
    duration = 10.0
    sr = 44100
    t_audio = np.linspace(0, duration, int(sr * duration), False)
    audio = np.zeros_like(t_audio)
    
    def add_beep(start, end, freq=440, volume=0.5):
        s = int(start * sr)
        e = int(end * sr)
        if s >= len(audio): return
        if e > len(audio): e = len(audio)
        t_slice = t_audio[s:e]
        audio[s:e] += volume * np.sin(2 * np.pi * freq * t_slice)
        
    for i in range(5): add_beep(0.2 + i*0.3, 0.35 + i*0.3, 800)
    for i in range(5): add_beep(2.2 + i*0.3, 2.35 + i*0.3, 750)
    add_beep(4.0, 4.2, 150, 0.8)
    add_beep(4.4, 4.6, 120, 0.8)
    add_beep(4.8, 5.0, 180, 0.8)
    add_beep(5.2, 5.8, 140, 0.8)
    for i in range(6): add_beep(6.2 + i*0.4, 6.35 + i*0.4, 800)
        
    stereo = np.column_stack((audio, audio))
    audioclip = AudioArrayClip(stereo, fps=sr)
    
    clip = VideoClip(make_frame, duration=duration)
    clip = clip.set_audio(audioclip)
    clip.write_videofile("tracer_slice.mp4", fps=24, codec="libx264", audio_codec="aac")

if __name__ == "__main__":
    generate()
