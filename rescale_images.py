from PIL import Image
import os

size = (300, 300)

def rescale(img_path):
    img = Image.open(img_path)
    return img.resize(size, Image.ANTIALIAS)

path = "/home/joakim/projects/VideoLabeler/videolabeler/videolabeler/output/pondo9/"
filenames = filenames = os.listdir(path)
gen = (filename for filename in filenames if ".jpg" in filename)

for img_name in gen:
    i = rescale(path + img_name)
    i.save("output/" + img_name)