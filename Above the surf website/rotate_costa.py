from PIL import Image
import os

path = 'Pictures/IMG_8709.jpeg'
if os.path.exists(path):
    img = Image.open(path)
    # Let's rotate it another 90 degrees right
    img = img.rotate(-90, expand=True)
    img.save(path)
    print(f"Rotated {path} 90 degrees clockwise.")
