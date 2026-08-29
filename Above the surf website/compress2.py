import os
from moviepy import VideoFileClip

def compress_video(input_path, output_path):
    print(f"Compressing {input_path}...")
    try:
        # Load video
        clip = VideoFileClip(input_path)
        
        # Resize to 720p height if it's larger
        if clip.h > 720:
            print("Resizing to 720p...")
            clip = clip.resized(height=720)
            
        # Write compressed video
        clip.write_videofile(
            output_path,
            codec="libx264",
            audio=False, # Mute it to save space (since background videos are muted anyway)
            bitrate="2000k",
            preset="fast"
        )
        print(f"Finished {output_path}. Size: {os.path.getsize(output_path) / (1024*1024):.2f} MB")
        
    except Exception as e:
        print(f"Error compressing {input_path}: {e}")

if __name__ == "__main__":
    videos = {
        "Surf videos/7193316-hd_1920_1080_24fps.mp4": "Surf videos/7193316_compressed.mp4",
        "Surf videos/6981356-hd_1920_1080_25fps.mp4": "Surf videos/6981356_compressed.mp4"
    }
    
    for in_vid, out_vid in videos.items():
        if os.path.exists(in_vid):
            compress_video(in_vid, out_vid)
        else:
            print(f"Could not find {in_vid}")

