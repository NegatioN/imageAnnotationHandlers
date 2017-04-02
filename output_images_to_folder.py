from bs4 import BeautifulSoup
import os
import shutil
from PIL import Image

output_dir = "output_ordered"
path = "/home/joakim/projects/VideoLabeler/videolabeler/videolabeler/output/pondo9"
filenames = os.listdir(path)
imagenet_size = 224
do_crop = True
if not os.path.exists(output_dir):
    os.makedirs(output_dir)

def find_center_image(bound_box):
    xmin = int(bound_box.xmin.text)
    xmax = int(bound_box.xmax.text)
    ymin = int(bound_box.ymin.text)
    ymax = int(bound_box.ymax.text)
    return (xmax+xmin)/2, (ymax+ymin)/2


def crop_to_imagenet(filename, labeled_object):
    img = Image.open(filename)
    center_x, center_y = find_center_image(labeled_object.bndbox)
    half_size = imagenet_size/2
    return img.crop((center_x-half_size, center_y-half_size,
                     center_x+half_size, center_y+half_size))


def imagenet_to_theano_format(filename):
    with open(filename) as xml_file:
        soup = BeautifulSoup(xml_file, "lxml")
        annotation = soup.html.body.annotation
        image_path = annotation.path.text
        label = annotation.object.find('name').text
        if not os.path.exists('{}/{}'.format(output_dir,label)):
            os.makedirs('{}/{}'.format(output_dir,label))
        if not do_crop:
            output_filename = '{}/{}/{}.{}'.format(output_dir, label, annotation.filename.text, "jpg")
            shutil.copyfile(image_path, output_filename)
        else:
            for index, labeled_object in enumerate(annotation.find_all('object')):
                output_filename = '{}/{}/{}-{}.{}'.format(output_dir, label, annotation.filename.text, index, "jpg")
                cropped_img = crop_to_imagenet(image_path, labeled_object)
                cropped_img.save(output_filename)

for filename in filenames:
    if ".xml" in filename:
        print(filename)
        imagenet_to_theano_format('{}/{}'.format(path, filename))


#TODO do some sort of crop of the image?
#TODO add negative examples? all imgs which dont have an xml.
