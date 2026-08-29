from moviepy import VideoFileClip
import os
import glob

for f in glob.glob('Surf videos/*.mp4'):
    try:
        clip = VideoFileClip(f)
        print(f"{os.path.basename(f)}: {clip.w}x{clip.h}, rotation={clip.rotation}")
        clip.close()
    except Exception as e:
        print(f"{os.path.basename(f)} Error: {e}")
