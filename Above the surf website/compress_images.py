from PIL import Image
import os

folder = "Pictures"
for filename in os.listdir(folder):
    if filename.lower().endswith((".jpg", ".jpeg", ".png")):
        filepath = os.path.join(folder, filename)
        try:
            img = Image.open(filepath)
            # Resize if width > 1000
            if img.width > 1200:
                ratio = 1200 / float(img.width)
                new_height = int((float(img.height) * float(ratio)))
                img = img.resize((1200, new_height), Image.Resampling.LANCZOS)
            
            # Save compressed
            if filename.lower().endswith(".png"):
                img.save(filepath, optimize=True)
            else:
                img.convert('RGB').save(filepath, "JPEG", quality=75, optimize=True)
            print(f"Compressed {filename}")
        except Exception as e:
            print(f"Failed {filename}: {e}")
