import os
import logging
import logging.config

from GPSPhoto import gpsphoto
from PIL import Image


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
        print('{} - {}'.format(i, file_name))
        data = gpsphoto.getGPSData(file_name)
        latit = data['Latitude']
        longi = data['Longitude']
        result[i] = {'name': file_name, 'lat': latit, 'lon': longi}

    return result


def resize_and_tag(data, outputdir, new_width):

    for file_data in data.values():
        # print(file_data)

        name, lat, lon = file_data.values()
        file, ext = os.path.splitext(name)

        img = Image.open(name)
        percent = (new_width / float(img.size[0]))
        new_height = int((float(img.size[1]) * float(percent)))

        img_resized = img.resize((new_width, new_height), Image.ANTIALIAS)

        resized_name = os.path.join(outputdir, '{}_thumb_lat_{}_lon_{}{}'.format(file, lat, lon, ext))
        img_resized.save(resized_name)

