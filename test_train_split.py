import os
import random
import shutil

def make_folder(image_type):
    test_dir = '{}/{}/{}'.format(output_path, "test", image_type)
    if not os.path.exists(test_dir):
        os.makedirs(test_dir)
    train_dir = '{}/{}/{}'.format(output_path, "train", image_type)
    if not os.path.exists(train_dir):
        os.makedirs(train_dir)
    valid_dir = '{}/{}/{}'.format(output_path, "valid", image_type)
    if not os.path.exists(valid_dir):
        os.makedirs(valid_dir)

def copy_files(image_type, test_or_train, file_list):
    for filename in file_list:
        shutil.copyfile('{}/{}/{}'.format(input_path, image_type, filename),
                        '{}/{}/{}/{}'.format(output_path, test_or_train, image_type, filename))

def calc_index(image_list, percentage):
    return int((float(len(image_list)) / 100)*percentage)


train_percent = 70
test_percent = 20
valid_percent = 100-(train_percent+test_percent)


input_path = "output_ordered"
output_path = 'test_train'
output_types = filenames = os.listdir(input_path) #Needs fancy magic if data is not structured.

image_names_types = {}
for image_type in output_types:
    make_folder(image_type)
    image_names_types[image_type] = os.listdir('{}/{}'.format(input_path, image_type))
    random.shuffle(image_names_types[image_type])
print(image_names_types)

for image_type, image_list in image_names_types.items():
    print(image_list)
    train_num = calc_index(image_list, train_percent)
    test_num = calc_index(image_list, test_percent) + train_num
    train_files = image_list[:train_num]
    test_files = image_list[train_num:test_num]
    valid_files = image_list[test_num:]
    copy_files(image_type, 'train', train_files)
    copy_files(image_type, 'test', test_files)
    copy_files(image_type, 'valid', valid_files)
