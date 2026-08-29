from PIL import Image
import os

files = ['Pictures/IMG_8726.jpeg', 'Pictures/IMG_8709.jpeg']
for path in files:
    if os.path.exists(path):
        img = Image.open(path)
        img = img.rotate(180, expand=True)
        img.save(path)
        print(f"Rotated {path} 180 degrees.")
