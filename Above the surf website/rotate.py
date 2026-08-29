from PIL import Image
import os

files_to_rotate = ['IMG_0657.jpeg', 'IMG_8732.jpeg', 'IMG_8709.jpeg', 'IMG_8726.jpeg']
for f in files_to_rotate:
    path = os.path.join('Pictures', f)
    if os.path.exists(path):
        img = Image.open(path)
        img = img.rotate(-90, expand=True) # Rotate 90 degrees right (or left, depends on original EXIF)
        img.save(path)
        print(f"Rotated {f}")
