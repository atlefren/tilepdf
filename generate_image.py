# -*- coding: utf-8 -*-
from util import parse_bbox, latlon2tile, get_bounds
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


def create_image(directory, filename):
    tiles = sort_tiles(get_files_from_disk(directory))
    image = combine_tiles(tiles)
    image.save(filename)


if __name__ == '__main__':
    directory = 'tiles'

    url = 'http://opencache.statkart.no/gatekeeper/gk/gk.open_gmaps?layers=topo2&zoom={z}&x={x}&y={y}'
    bbox = '9.5997073555,63.1427121204,11.0326168633,63.7064078339'
    width = 2000
    height = 2000
    filename = 'generated.png'

    zoom = determine_zoom(bbox, width, height)
    (minx, maxx, miny, maxy) = get_bounds(bbox, zoom)
    cols = (maxx - minx) + 1
    rows = (maxy - miny) + 1

    print 'zoom = %s' % zoom

    img_width = TILE_SIZE * cols
    img_height = TILE_SIZE * rows

    print 'img_width = %s' % img_width
    print 'img_height = %s' % img_height

    tile_links = create_xyz_tile_links(url, minx, maxx, miny, maxy, zoom)

    print 'downloading..'
    download_tiles(tile_links, directory)
    create_image(directory, filename)
