from PIL import Image
import os

img = Image.open('Pictures/IMG_0657.jpeg')
img = img.rotate(-90, expand=True)
img.save('Pictures/IMG_0657.jpeg')
print('Rotated IMG_0657.jpeg')
