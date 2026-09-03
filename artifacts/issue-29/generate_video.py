import cv2
import numpy as np
from moviepy.editor import VideoClip, AudioFileClip
import wave

FPS = 24
DURATION = 10
W, H = 1080, 1920

# Generate Gibberish Audio
sample_rate = 44100
t_audio = np.linspace(0, DURATION, int(sample_rate * DURATION), False)
beep_mask = (t_audio % 0.25) < 0.1
freq = 440 + np.sin(t_audio * 10) * 150
tone = np.sin(2 * np.pi * freq * t_audio) * 0.5
audio_data = tone * beep_mask

with wave.open("temp_audio.wav", "w") as wav_file:
    wav_file.setnchannels(1)
    wav_file.setsampwidth(2)
    wav_file.setframerate(sample_rate)
    pcm_data = (audio_data * 32767).astype(np.int16)
    wav_file.writeframes(pcm_data.tobytes())

def make_frame(t):
    frame = np.zeros((H, W, 3), dtype=np.uint8)
    
    if t < 3.0:
        frame[:] = (40, 40, 100)
        y_bounce = int(np.abs(np.sin(t * 8)) * 100)
        cv2.rectangle(frame, (W//2 - 400, H//2 - 200), (W//2 - 100, H//2 + 200), (0, 0, 255), -1)
        cv2.circle(frame, (W//2 + 250, H//2 + 100 - y_bounce), 200, (0, 255, 0), -1)
        lines = ["ARE WE JUST A", "PYTHON SCRIPT?"]
    elif t < 6.5:
        frame[:] = (0, 255, 255)
        x_slide = int((t - 3.0) * 600) - 400
        pts = np.array([[W//2 + x_slide, H//2 - 400], [W//2 - 400 + x_slide, H//2 + 400], [W//2 + 400 + x_slide, H//2 + 400]], np.int32)
        cv2.fillPoly(frame, [pts], (255, 0, 0))
        lines = ["CUTAWAY TO A", "GIANT BLUE TRIANGLE!"]
    else:
        frame[:] = (40, 40, 100)
        cv2.rectangle(frame, (W//2 - 400, H//2 - 200), (W//2 - 100, H//2 + 200), (0, 0, 255), -1)
        cv2.circle(frame, (W//2 + 250, H//2), 200, (0, 255, 0), -1)
        lines = ["THAT WAS", "PROFOUNDLY STUPID."]
        
    font = cv2.FONT_HERSHEY_SIMPLEX
    font_scale = 3.5
    thickness = 15
    
    y_offset = H // 4
    for line in lines:
        text_size = cv2.getTextSize(line, font, font_scale, thickness)[0]
        text_x = (W - text_size[0]) // 2
        cv2.putText(frame, line, (text_x, y_offset), font, font_scale, (0, 0, 0), thickness + 15, cv2.LINE_AA)
        cv2.putText(frame, line, (text_x, y_offset), font, font_scale, (255, 255, 255), thickness, cv2.LINE_AA)
        y_offset += text_size[1] + 150
        
    return frame[:, :, ::-1]

clip = VideoClip(make_frame, duration=DURATION)
audio = AudioFileClip("temp_audio.wav")
clip = clip.set_audio(audio)
clip.write_videofile("tracer_slice.mp4", fps=FPS, codec="libx264", audio_codec="aac", logger=None, ffmpeg_params=['-g', '1'])
