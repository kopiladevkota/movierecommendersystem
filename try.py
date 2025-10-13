from moviepy.editor import VideoFileClip, concatenate_videoclips
import random

# === Step 1: Load your video ===
input_path = ""C:\Users\devko\Downloads\lv_0_20240706004405.mp4""  # Replace with your actual video filename
clip = VideoFileClip(input_path)

# === Step 2: Split into 3-second chunks ===
chunk_duration = 3  # seconds
chunks = [
    clip.subclip(i, min(i + chunk_duration, clip.duration))
    for i in range(0, int(clip.duration), chunk_duration)
]

# === Step 3: Shuffle the chunks ===
random.shuffle(chunks)

# === Step 4: Concatenate and export ===
final_clip = concatenate_videoclips(chunks)
output_path = "randomized_birthday_video.mp4"
final_clip.write_videofile(output_path, codec="libx264", audio_codec="aac", preset="ultrafast", bitrate="800k")
