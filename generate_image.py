# -*- coding: utf-8 -*-
import math

from util import parse_bbox, latlon2tile, get_bounds, mm_to_pixel
from tile import (create_xyz_tile_links, download_tiles, get_files_from_disk,
                  sort_tiles)
from image_operations import combine_tiles


TILE_SIZE = 256


def determine_zoom(bbox, min_width, min_height):
    (left, bottom, right, top) = parse_bbox(bbox)
    w = -1
    h = -1
    for zoom in range(22, 0, -1):
        (maxx, maxy) = latlon2tile(bottom, right, zoom)
        (minx, miny) = latlon2tile(top, left, zoom)
        cols = maxx - minx + 1
        rows = maxy - miny + 1
        image_width = rows * TILE_SIZE
        image_height = cols * TILE_SIZE

        if image_width == min_width and image_height == min_height:
            return zoom
        if image_width < min_width or image_height < min_height:
            return zoom + 1

    raise Error('could not determine zoom')


def crop_image(image, w_offset, h_offset):
    left_offset = int(math.ceil(w_offset / 2.0))
    right_offset = int(math.floor(w_offset / 2.0))
    top_offset = int(math.ceil(h_offset / 2.0))
    bottom_offset = int(math.floor(h_offset / 2.0))
    print left_offset, right_offset
    return image.crop((
        left_offset,
        top_offset,
        int(image.size[0]) - right_offset,
        int(image.size[1]) - bottom_offset
    ))


def create_image(directory, filename, dpi, pixel_width, pixel_height):
    tiles = sort_tiles(get_files_from_disk(directory))
    image = combine_tiles(tiles)

    w_offset = image.size[0] - pixel_width
    h_offset = image.size[1] - pixel_height

    print w_offset, h_offset

    image = crop_image(image, w_offset, h_offset)

    image.save(filename, dpi=(dpi, dpi))


if __name__ == '__main__':
    directory = 'tiles'

    url = 'http://opencache.statkart.no/gatekeeper/gk/gk.open_gmaps?layers=topo2&zoom={z}&x={x}&y={y}'
    bbox = '9.5997073555,63.1427121204,11.0326168633,63.7064078339'
    width = 330  # mm
    height = 330  # mm
    dpi = 300
    filename = 'generated2.png'

    pixel_width = mm_to_pixel(width, dpi)
    pixel_height = mm_to_pixel(height, dpi)

    print 'Generating image of size %sx%s mm at %s dpi' % (width, height, dpi)
    print 'Resolves to %sx%s pixels' % (pixel_width, pixel_height)

    zoom = determine_zoom(bbox, pixel_width, pixel_height)
    (minx, maxx, miny, maxy) = get_bounds(bbox, zoom)
    cols = (maxx - minx) + 1
    rows = (maxy - miny) + 1

    print 'zoom = %s' % zoom

    img_width = TILE_SIZE * cols
    img_height = TILE_SIZE * rows

    print 'img_width = %s' % img_width
    print 'img_height = %s' % img_height

    tile_links = create_xyz_tile_links(url, minx, maxx, miny, maxy, zoom)

    print 'Downloading %s tiles..' % len(tile_links)
    download_tiles(tile_links, directory)
    create_image(directory, filename, dpi, pixel_width, pixel_height)
