from PIL import Image
import os

files = ['Pictures/IMG_8726.jpeg', 'Pictures/IMG_8709.jpeg']
for path in files:
    if os.path.exists(path):
        img = Image.open(path)
        # In PIL, positive angle is counter-clockwise. To rotate clockwise (ground on left -> ground on bottom), use -90
        img = img.rotate(-90, expand=True)
        img.save(path)
        print(f"Rotated {path} clockwise by 90 degrees.")
