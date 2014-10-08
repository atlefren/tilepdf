# -*- coding: utf-8 -*-
from urllib import urlencode
import math
import os
import shutil
import requests


wms_url = 'http://openwms.statkart.no/skwms1/wms.topo2?'
layer_name = 'topo2_WMS'
srs = 'EPSG:32633'
minx = -127998
miny = 6.37792e+06
maxx = 1.14551e+06
maxy = 7.9768e+06
height = 256 * 2
width = 256 * 2
min_row_col = 5


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


def save_tiles(links):
    directory = os.getcwd() + '/tiles'
    if os.path.exists(directory):
        shutil.rmtree(directory)
    os.makedirs(directory)

    for link in links:
        response = requests.get(link['url'], stream=True)
        filename = directory + '/%s_%s.png' % (link['x'], link['y'])
        with open(filename, 'wb') as out_file:
            shutil.copyfileobj(response.raw, out_file)


if __name__ == '__main__':
    grid = create_grid(minx, miny, maxx, maxy, min_row_col)
    tile_links = create_tile_links(grid)
    save_tiles(tile_links)
