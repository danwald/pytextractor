#!/usr/bin/env python

from pkg_resources import resource_string
import argparse
import sys

from pytextractor import PyTextractor


def text_detector():
    # construct the argument parser and parse the arguments
    ap = argparse.ArgumentParser(description='Text/Number extractor from image')
    ap.add_argument('images', type=str, nargs='+',
            help='path(s) to input image(s)')
    ap.add_argument( '--east', type=str, required=False,
        help='path to input EAST text detector')
    ap.add_argument('-c', '--confidence', type=float, default=0.5,
        help='minimum probability required to inspect a region')
    ap.add_argument('-w', '--width', type=int, default=320,
        help='resized image width (should be multiple of 32)')
    ap.add_argument('-e', '--height', type=int, default=320,
        help='resized image height (should be multiple of 32)')
    ap.add_argument('-d', '--display', action='store_true',
        help='Display bounding boxes')
    ap.add_argument('-n', '--numbers', action='store_true',
        help='Detect only numbers')
    ap.add_argument('-p', '--percentage', type=float, default=2.0,
        help='Expand/shrink detected bound box')
    ap.add_argument('-b', '--min-boxes', type=int, default=1,
        help='minimum number of detected boxes to return')
    ap.add_argument('-i', '--max-iterations', type=int, default=20,
        help='max number of iterations finding min_boxes')

    kwargs = vars(ap.parse_args())
    images = kwargs.pop('images')
    extractor = PyTextractor(kwargs.pop('east'))
    for image in images:
        for text in extractor.get_image_text(image, **kwargs):
            print(text)
    return 0


if __name__ == '__main__':
    sys.exit(text_detector())
