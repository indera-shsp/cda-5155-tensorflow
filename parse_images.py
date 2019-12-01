#!/usr/bin/env python

# See
#   https://stackoverflow.com/questions/19804768/interpreting-gps-info-of-exif-data-from-photo-in-python
#   https://pillow.readthedocs.io/en/3.1.x/reference/Image.html

import argparse
import time
# import os

import utils
from pprint import pprint
from datetime import timedelta

DEFAULT_INPUT_DIR = 'input'
DEFAULT_OUTPUT_DIR = 'output'

DEFAULT_RESIZE_WIDTH = 512

log = utils.get_a_logger(__name__)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        '-i', '--inputdir',
        # required=True,
        default=DEFAULT_INPUT_DIR,
        help='input directory name')
    parser.add_argument(
        '-o', '--outputdir',
        default=DEFAULT_OUTPUT_DIR,
        help='output directory name')
    parser.add_argument(
        '-w', '--width',
        default=DEFAULT_RESIZE_WIDTH,
        help='output image width (default 512 px)')


    args = parser.parse_args()

    start = time.monotonic()
    files = utils.find_images_in_dir(args.inputdir)
    log.info('Found {} files in directory [{}]'.format(len(files), args.inputdir))

    files_with_gps_data = utils.extract_gps_coordinates(files)
    pprint(files_with_gps_data)

    width = int(args.width)
    log.info('Resizing {} files to {} px width'.format(len(files), width))
    utils.resize_and_tag(files_with_gps_data, args.outputdir, width)

    end = time.monotonic()
    elapsed = (end - start)
    log.info("Done. Process duration: {}".format(str(timedelta(seconds=elapsed))))


if __name__ == '__main__':
    main()
