import os
import logging
import logging.config
import pprint
from urllib import parse


# from GPSPhoto import gpsphoto
from PIL import Image
from PIL.ExifTags import GPSTAGS
from PIL.ExifTags import TAGS
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

    names = os.listdir(dir_name)
    names.sort()

    for file_name in names:
        if not file_name.endswith(".jpg"):
            continue

        full_path = os.path.join(os.path.abspath(dir_name), file_name)
        files.append(full_path)

    return files


def get_exif(file_name):
    exif = Image.open(file_name)._getexif()

    # 34853: {1: 'N',
    #     2: ((29, 1), (38, 1), (558024, 10000)),
    #     3: 'W',
    #     4: ((82, 1), (20, 1), (587076, 10000)),
    #     5: b'\x00',
    #     6: (7192, 1000),
    #     7: ((16, 1), (26, 1), (9, 1)),
    #     27: b'ASCII\x00\x00\x00GPS\x00',
    #     29: '2019:11:19'},

    if exif is None:
        return {}

    exif_data = {}

    for (key, value) in exif.items():
        tag = TAGS.get(key)

        if tag == 'GPSInfo':
            # print('tag {} = {}'.format(TAGS.get(key), value))
            gps_data = {}
            for i in value:
                decoded = GPSTAGS.get(i, i)
                gps_data[decoded] = value[i]

            exif_data[tag] = gps_data
        else:
            exif_data[tag] = value

    return exif_data


def get_coordinates(info):
    result = {}

    for key in ['Latitude', 'Longitude']:
        if 'GPS'+key in info and 'GPS'+key+'Ref' in info:
            e = info['GPS'+key]
            ref = info['GPS'+key+'Ref']
            result[key] = (str(e[0][0]/e[0][1]) + '°' +
                           str(e[1][0]/e[1][1]) + '′' +
                           str(e[2][0]/e[2][1]) + '″ ' +
                           ref)
    return result


def get_decimal_coordinates(info):
    result = {}

    for key in ['Latitude', 'Longitude']:
        if 'GPS' + key in info and 'GPS' + key + 'Ref' in info:
            e = info['GPS' + key]
            ref = info['GPS' + key + 'Ref']

            val_deg = e[0][0] / e[0][1]
            val_min = e[1][0] / e[1][1] / 60
            val_sec = e[2][0] / e[2][1] / 3600

            # value = round(val_deg + val_min + val_sec, 7)
            value = val_deg + round(val_min, 7) + round(val_sec, 7)
            result[key] = value * (-1 if ref in ['S', 'W'] else 1)

    return result


def extract_gps_coordinates(files):
    result = {}

    for i, file_name in enumerate(files):
        print('{} - {}'.format(i, file_name))

        # data = gpsphoto.getGPSData(file_name)
        # latit = data['Latitude']
        # longi = data['Longitude']

        exif_data = get_exif(file_name)
        data_deg = get_coordinates(exif_data['GPSInfo'])
        data = get_decimal_coordinates(exif_data['GPSInfo'])

        # 29°38′55.8024 N 82°20′ 58.7076 W
        # Google: 29.6488386, -82.3518297
        #         29.648834, 'Longitude': -82.349641
        pprint.pprint(data_deg)
        pprint.pprint(data)
        latit = data['Latitude']
        longi = data['Longitude']

        # note the default accuracy is 10
        label = olc.encode(latit, longi, 13)
        result[i] = {'name': file_name, 'lat': latit, 'lon': longi, 'label': label}

    return result


def create_plus_code_dirs(data, outputdir):

        # init the set of dirs we need to create
        directories = set()

        for file_data in data.values():
            print(file_data)
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

        # convert to grayscale
        img = img.convert('L')

        percent = (new_width / float(img.size[0]))
        new_height = int((float(img.size[1]) * float(percent)))

        i = i + 1
        if i % 10 == 1:
            print('Processing image {} out of {}'.format(i, len(data)))

        prefix = str(i).zfill(4)
        resized_name = os.path.join(outputdir, label, 'thumb_{}_lat_{}_lon_{}{}'
                                    .format(prefix, lat, lon, ext))

        print('image {} path: {}'.format(i, resized_name))
        img_resized = img.resize((new_width, new_height), Image.ANTIALIAS)

        img_resized.save(resized_name)


