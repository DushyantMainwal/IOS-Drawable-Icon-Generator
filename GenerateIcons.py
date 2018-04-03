from PIL import Image
import sys
import os
import imghdr
import shutil
import json


def resize_image(input_image_path, file_name):
    image = Image.open(input_image_path)
    count = 3
	
    for icon_ratio in icon_size_ratio:
        height = width = int(highest_resolution * (icon_ratio / icon_size_ratio[0]))
        resized_image = image.resize((height, width), Image.LANCZOS)
        filename = file_name.split('.', 1)[0]
        extension = file_name.split('.', 1)[1]
		
        resized_icon_directory = destination_directory + os.sep + filename + '.imageset'
        image_name = ""
		
        if count == 1:
            image_name = file_name;		
        else:
            image_name = filename + "_" + str(count) + "x." + extension
		
        path = resized_icon_directory + os.sep
        resized_icon_location = path + image_name
		
        if not os.path.isdir(resized_icon_directory):
            os.makedirs(resized_icon_directory)
        resized_image.save(resized_icon_location, quality=90)
        create_json(path, image_name, str(count))
        count -= 1

#Create JSON
jsonFileName = 'Contents.json'
data = {}
info = {
	'author': 'DigitalBitHub',
	'version': 1
}
data['images'] = []
data['info'] = {}

def create_json(path, image_name, scale):
    data['images'].append({
	    'filename': image_name,
		'idiom': 'universal',
		'scale': scale + 'x'
	})
    data['info'] = info
	
    jsonPath = path + jsonFileName
    with open(jsonPath, 'w') as outfile:  
	    json.dump(data, outfile)


def read_directory(input_location):
    for file_name in os.listdir(input_location + os.sep + os.sep.join(destination_subdirectories)):
        if destination_subdirectories.__len__() == 0:
            absolute_file_path = input_location + os.sep + file_name
        else:
            absolute_file_path = input_location + os.sep + os.sep.join(destination_subdirectories) \
                                 + os.sep + file_name
        if os.path.isdir(absolute_file_path):
            destination_subdirectories.append(file_name)
            read_directory(input_location)
            destination_subdirectories.pop()
        else:
            # check if file is image
            if imghdr.what(absolute_file_path):
                resize_image(absolute_file_path, file_name)


# get directory location
location = sys.argv[1]
icon_size_ratio = [3, 2, 1]
highest_resolution = 72
if location.endswith(os.sep):
    location = location[0:location.__len__() - 1]
destination_directory = location + os.sep + "ios_images"
destination_subdirectories = []

# check if resolution is specified first argument is default and value is file name
# second argument is location of directory of icons to be resized
if sys.argv.__len__() > 2:
    input_resolution_value = sys.argv[2] 
    if input_resolution_value.isdigit():
        highest_resolution = int(input_resolution_value)
    else:
        print("Enter correct resolution")
        print("using default hightest resolution")

# check if input location is directory
if not os.path.isdir(location):
    exit("Please provide correct directory location")
    exit()

# remove if destination directory exists
if os.path.isdir(destination_directory):
    shutil.rmtree(destination_directory)

# geneate resized icon  send absolution location and relative root
read_directory(location)

