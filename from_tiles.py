# -*- coding: utf-8 -*-
import os
import shutil
import requests


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


if __name__ == '__main__':
    tile_links = create_xyz_tile_links(34644, 34672, 17701, 17721, 'http://www.webatlas.no/maptiles/tiles/webatlas-standard-vektor/wa_grid', 16)
    save_tiles(tile_links, dir='xyz')
