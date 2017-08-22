# -*- coding: utf-8 -*-\
import os
import shutil

import requests


def get_xyz_url_templ(template, x, y, z):
    return template.format(x=x, y=y, z=z)


def create_xyz_tile_links(base_url, minx, maxx, miny, maxy, zoom):
    tiles = []
    for x, tx in enumerate(range(minx, maxx + 1)):
        for y, ty in enumerate(range(miny, maxy + 1)):
            url = get_xyz_url_templ(base_url, tx, ty, zoom)
            tiles.append({
                'x': x,
                'y': y,
                'url': url
            })
    return tiles


def save_image(filename, response):
    with open(filename, 'wb') as out_file:
        shutil.copyfileobj(response.raw, out_file)


def download_tiles(links, dir='tiles'):
    directory = os.path.join(os.getcwd(), dir)
    if os.path.exists(directory):
        shutil.rmtree(directory)
    try:
        os.makedirs(directory)
    except OSError:
        pass

    for link in links:
        print 'downloading %s' % link['url']
        response = requests.get(link['url'], stream=True)
        filename = os.path.join(directory, '%03d_%03d.png' % (link['x'], link['y']))
        save_image(filename, response)


def get_files_from_disk(dir='tiles'):
    directory = os.path.join(os.getcwd(), dir)

    return sorted([
        os.path.join(directory, file)
        for file in os.listdir(directory)
        if file.endswith('.png')
    ])


def sort_tiles(tiles):
    sorted_tiles = {}
    for tile in tiles:
        fn = tile.split('/')[-1].split('.')[0].split('_')
        x = int(fn[0])
        y = int(fn[1])
        xs = sorted_tiles.get(x, None)
        if not xs:
            xs = {}
            sorted_tiles[x] = xs
        xs[y] = tile
    return sorted_tiles
