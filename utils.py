import os
import logging
import logging.config
from urllib import parse

from GPSPhoto import gpsphoto
from PIL import Image
from openlocationcode import openlocationcode as olc


CONFIG_FILE = 'config/logs.cfg'

def get_a_logger(name):
    cwd = os.getcwd()
    log_conf = os.path.join(cwd, CONFIG_FILE)

    if os.path.exists(log_conf):
        logging.config.fileConfig(log_conf)

    log = logging.getLogger(name)
    return log


def find_images_in_dir(dir_name):
    files = []

    for file_name in os.listdir(dir_name):
        if not file_name.endswith(".jpg"):
            continue

        full_path = os.path.join(os.path.abspath(dir_name), file_name)
        files.append(full_path)

    return files


def extract_gps_coordinates(files):
    result = {}

    for i, file_name in enumerate(files):
        # print('{} - {}'.format(i, file_name))
        data = gpsphoto.getGPSData(file_name)
        latit = data['Latitude']
        longi = data['Longitude']
        label = olc.encode(latit, longi)
        result[i] = {'name': file_name, 'lat': latit, 'lon': longi, 'label': label}

    return result


def create_plus_code_dirs(data, outputdir):

        # init the set of dirs we need to create
        directories = set()

        for file_data in data.values():
            name, lat, lon, label = file_data.values()
            directories.add(label)

        print('will create {} directories to group {} images'.format(len(directories), len(data)))

        for directory in directories:
            dir_name = os.path.join(outputdir, directory)
            map_url = 'https://www.google.com/maps/place/{}'.format(parse.quote(directory))

            print('image group: {} - {}'.format(directory, map_url))
            if not os.path.exists(dir_name):
                os.makedirs(dir_name)


def resize_and_tag(data, outputdir, new_width):

    i = 0

    for file_data in data.values():
        # print(file_data)

        name, lat, lon, label = file_data.values()
        file, ext = os.path.splitext(name)

        img = Image.open(name)
        percent = (new_width / float(img.size[0]))
        new_height = int((float(img.size[1]) * float(percent)))

        i = i + 1
        if i % 10 == 1:
            print('Processing image {} out of {}'.format(i, len(data)))

        prefix = str(i).zfill(4)
        resized_name = os.path.join(outputdir, label, 'thumb_{}_lat_{}_lon_{}{}'
                                    .format(prefix, lat, lon, ext))

        img_resized = img.resize((new_width, new_height), Image.ANTIALIAS)

        img_resized.save(resized_name)


