# -*- coding: utf-8 -*-
import os
import shutil
import math

import requests

from tileutils import GlobalMercator


mercator = GlobalMercator()


def parse_bbox(bbox):
    return tuple([float(c) for c in bbox.split(',')])


def mm_to_pixel(mm, dpi):
    inches = float(mm) / 25.4
    return int(math.ceil(inches * float(dpi)))


def get_even(min_val, max_val):
    size = max_val - min_val
    if size % 2 == 0:
        return min_val, max_val
    return min_val, max_val + 1


def get_bounds(bbox, zoom):
    (left, bottom, right, top) = parse_bbox(bbox)
    (maxx, maxy) = latlon2tile(bottom, right, zoom)
    (minx, miny) = latlon2tile(top, left, zoom)

    (minx, maxx) = get_even(minx, maxx)
    (miny, maxy) = get_even(miny, maxy)
    return (minx, maxx, miny, maxy)


def latlon2tile(lat, lon, zoom):
    mx, my = mercator.LatLonToMeters(lat, lon)
    tx, ty = mercator.MetersToTile(mx, my, zoom)
    return mercator.GoogleTile(tx, ty, zoom)


def physical_size(cols, rows):
    a4_width = 210.0  # mm
    size = a4_width * 0.95
    return ((cols * size) / 1000, (rows * size) / 1000)
