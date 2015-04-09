# -*- coding: utf-8 -*-
from urllib import urlencode
import math
import os
import shutil
import requests
from PIL import Image
from io import BytesIO

wms_url = 'http://wms.geonorge.no/skwms1/wms.barents_watch?'
layer_name = 'barents_watch_WMS'
srs = 'EPSG:32633'

minx = -1500000.0
miny = 5800000.0
maxx = 2045984.0
maxy = 9045984.0

'''
minx = -27998
miny = 6.37792e+06
maxx = 1.14551e+06
maxy = 7.9768e+06
'''
height = 256 * 2
width = 256 * 2
min_row_col = 10


def create_bbox(minx=None, miny=None, maxx=None, maxy=None):
    return ','.join('{0}'.format(n) for n in [minx, miny, maxx, maxy])


def build_url(wms_url, layer_name, srs, bbox, width, height):
    params = {
        'LAYERS': layer_name,
        'TRANSPARENT': 'false',
        'FORMAT': 'image/png',
        'SERVICE': 'WMS',
        'VERSION': '1.1.1',
        'REQUEST': 'GetMap',
        'STYLES': '',
        'SRS': srs,
        'BBOX': bbox,
        'WIDTH': width,
        'HEIGHT': height,
    }

    return wms_url + urlencode(params)


def create_grid(minx, miny, maxx, maxy, min_size):
    width = maxx - minx
    height = maxy - miny

    if width < height:
        tile_size = width / min_size
    else:
        tile_size = height / min_size

    num_rows = int(math.ceil(width / tile_size))

    num_cols = int(math.ceil(height / tile_size))

    grid = []
    for x in range(0, num_rows):
        grid.append([])
        t_min_x = minx + (x * tile_size)
        t_max_x = minx + ((x + 1) * tile_size)
        for y in range(0, num_cols):
            t_min_y = miny + (y * tile_size)
            t_max_y = miny + ((y + 1) * tile_size)
            grid[x].append({
                'minx': t_min_x,
                'maxx': t_max_x,
                'miny': t_min_y,
                'maxy': t_max_y,
            })
    return grid


def create_tile_links(grid):
    tiles = []
    for x, row in enumerate(grid):
        for y, col in enumerate(reversed(row)):
            url = build_url(
                wms_url,
                layer_name,
                srs,
                create_bbox(**col),
                width,
                height
            )
            tiles.append({
                'x': x,
                'y': y,
                'url': url
            })
    return tiles


def create_xyz_tile_links(minx, maxx, miny, maxy, base, z):
    def get_xyz_url(base, x, y, z):
        return '%s/%s/%s/%s.png' % (base, z, x, y)
    tiles = []
    for x, tx in enumerate(range(minx, maxx)):
        print x
        for y, ty in enumerate(range(miny, maxy)):
            print y
            url = get_xyz_url(base, tx, ty, z)
            tiles.append({
                'x': x,
                'y': y,
                'url': url
            })
    return tiles


def save_image(filename, response, resize):
    with open(filename, 'wb') as out_file:

        if resize:
            image = Image.open(BytesIO(response.content))
            image = image.resize((width, height))
            image.save(filename)
            
        else:
            shutil.copyfileobj(response.raw, out_file)


def save_tiles(links, dir='tiles', resize=False):
    directory = os.getcwd() + '/' + dir
    if os.path.exists(directory):
        shutil.rmtree(directory)
    os.makedirs(directory)

    for link in links:
        response = requests.get(link['url'], stream=True)
        filename = directory + '/%03d_%03d.png' % (link['x'], link['y'])
        save_image(filename, response, resize)


if __name__ == '__main__':

    '''
    grid = create_grid(minx, miny, maxx, maxy, min_row_col)
    tile_links = create_tile_links(grid)
    save_tiles(tile_links)
    '''
    #tile_links = create_xyz_tile_links(32, 37, 13, 19, 'http://a.tile.stamen.com/toner', 6)

    tile_links = create_xyz_tile_links(34644, 34672, 17701, 17721, '', 16)

    #tile_links = create_xyz_tile_links(34644, 34646, 17710, 17712, '', 16)
    save_tiles(tile_links, dir='xyz', resize=False)
