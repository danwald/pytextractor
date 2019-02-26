#!/usr/bin/env python

import argparse
import sys

from pytextractor.pytextractor import PyTextractor

if __name__ == '__main__':
    # construct the argument parser and parse the arguments
    ap = argparse.ArgumentParser(description='Text/Number extractor from image')
    ap.add_argument('images', type=str, nargs='+', help='path(s) to input image(s)')
    ap.add_argument(
        '-east', '--east',
        type=str, default='./assets/models/frozen_east_text_detection.pb',
        help='path to input EAST text detector'
    )
    ap.add_argument('-c', '--confidence', type=float, default=0.5, help='minimum probability required to inspect a region')
    ap.add_argument('-w', '--width', type=int, default=320, help='resized image width (should be multiple of 32)')
    ap.add_argument('-e', '--height', type=int, default=320, help='resized image height (should be multiple of 32)')
    ap.add_argument('-d', '--display', action='store_true', help='Display bounding boxes')
    ap.add_argument('-n', '--numbers', action='store_true', help='Detect only numbers')
    ap.add_argument('-p', '--percentage', type=float, default=2.0, help='Expand/shrink detected bound box')
    kwargs = vars(ap.parse_args())

    extractor = PyTextractor(east=kwargs['east'])
    images = kwargs.pop('images')
    for image in images:
        kwargs.update({'image': image})
        for text in extractor.get_image_text(**kwargs):
            print(text)
    sys.exit(0)
else:
    sys.exit(1)
