# -*- coding: utf-8 -*-
import os
import shutil
import requests

from tileutils import GlobalMercator
from topdf import create_pdf

mercator = GlobalMercator()


def physical_size(cols, rows):
    a4_width = 210.0  # mm
    size = a4_width * 0.95
    return ((cols * size) / 1000, (rows * size) / 1000)


def latlon2tile(lat, lon, zoom):
    mx, my = mercator.LatLonToMeters(lat, lon)
    tx, ty = mercator.MetersToTile(mx, my, zoom)
    return mercator.GoogleTile(tx, ty, zoom)


def parse_bbox(bbox):
    return tuple([float(c) for c in bbox.split(',')])


def get_even(min_val, max_val):
    size = max_val - min_val
    if size % 2 == 0:
        return min_val, max_val
    return min_val, max_val + 1


def get_xyz_url(base, x, y, z):
        return '%s/%s/%s/%s.png' % (base, z, x, y)


def create_xyz_tile_links(base_url, minx, maxx, miny, maxy, zoom):
    tiles = []
    for x, tx in enumerate(range(minx, maxx)):
        for y, ty in enumerate(range(miny, maxy)):
            url = get_xyz_url(base_url, tx, ty, zoom)
            tiles.append({
                'x': x,
                'y': y,
                'url': url
            })
    return tiles


def save_image(filename, response):
    with open(filename, 'wb') as out_file:
        shutil.copyfileobj(response.raw, out_file)


def save_tiles(links, dir='tiles'):
    directory = os.getcwd() + '/' + dir
    if os.path.exists(directory):
        shutil.rmtree(directory)
    os.makedirs(directory)

    for link in links:
        response = requests.get(link['url'], stream=True)
        filename = directory + '/%03d_%03d.png' % (link['x'], link['y'])
        save_image(filename, response)


def get_bounds(bbox, zoom):
    (left, bottom, right, top) = parse_bbox(bbox)
    (maxx, maxy) = latlon2tile(bottom, right, zoom)
    (minx, miny) = latlon2tile(top, left, zoom)

    (minx, maxx) = get_even(minx, maxx)
    (miny, maxy) = get_even(miny, maxy)
    return (minx, maxx, miny, maxy)

if __name__ == '__main__':
    zoom = 13
    url = 'http://a.tile.stamen.com/toner'
    bbox = '10.307612896,63.4103527915,10.4711933136,63.4574290025'
    directory = 'xyz'
    filename = 'generated'

    (minx, maxx, miny, maxy) = get_bounds(bbox, zoom)

    num_tiles = (maxx - minx) * (maxy - miny)
    cols = (maxx - minx) / 2
    rows = (maxy - miny) / 2
    physical_width, physical_height = physical_size(cols, rows)
    pages = rows * cols
    tile_links = create_xyz_tile_links(url, minx, maxx, miny, maxy, zoom)

    print 'Stats:'
    print 'cols: %s' % cols
    print 'rows: %s' % rows
    print 'tiles: %s' % num_tiles
    print 'pages: %s' % pages
    print 'size: %.1f m x %.1f m (w x h)' % (physical_width, physical_height)

    print 'Saving %s tiles from %s' % (num_tiles, url)
    save_tiles(tile_links, dir=directory)

    print 'Generating pdf'
    create_pdf(directory, filename)
