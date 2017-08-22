# -*- coding: utf-8 -*-

from util import get_bounds, physical_size
from tile import (create_xyz_tile_links, download_tiles, get_files_from_disk,
                  sort_tiles)
from pdf_operations import create_pdf

if __name__ == '__main__':

    bbox = '9.5997073555,63.1427121204,11.0326168633,63.7064078339'
    zoom = 10
    # url = 'http://a.tile.stamen.com/toner/{z}/{x}/{y}.png'
    url = 'http://opencache.statkart.no/gatekeeper/gk/gk.open_gmaps?layers=topo2&zoom={z}&x={x}&y={y}'

    directory = 'tiles'
    filename = 'generated.pdf'

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
    download_tiles(tile_links, dir=directory)

    print 'Generating pdf'

    tiles = sort_tiles(get_files_from_disk(directory))
    print tiles
    create_pdf(tiles, filename)
