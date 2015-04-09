# -*- coding: utf-8 -*-
import os
import glob
import StringIO

from PIL import Image as PilImage
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from reportlab.lib.utils import ImageReader


def pil_to_rl(image, name):
    output = StringIO.StringIO()
    image.save(output, format='png')
    contents = output.getvalue()
    output.close()
    return ImageReader(StringIO.StringIO(contents))


def physical_size(cols, rows):
    a4_width = 210.0  # mm
    size = a4_width * 0.95
    return ((cols * size) / 1000, (rows * size) / 1000)


def print_image(canvas, image, name):
    w, h = A4
    canvas.drawImage(
        pil_to_rl(image, name),
        0,
        0,
        height=w * 0.95,
        width=w * 0.95,
        preserveAspectRatio=True,
        anchor='sw'
    )
    canvas.drawCentredString(w / 2, 600, name)
    canvas.showPage()
    canvas.save()


def create_composite(ul, ll, ur, lr, name):
    new_im = PilImage.new('RGB', (512, 512))
    new_im.paste(PilImage.open(ul), (0, 0))
    new_im.paste(PilImage.open(ll), (256, 0))
    new_im.paste(PilImage.open(ur), (0, 256))
    new_im.paste(PilImage.open(lr), (256, 256))
    return new_im


def get_filename(x, y):
    return '/%03d_%03d.png' % (x, y)


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


def create_pdf(images, name):

    tiles = sort_tiles(images)

    height = 4 # len(tiles[0])
    width = 4 # len(tiles)

    cols = width / 2
    rows = height / 2
    physical_width, physical_height = physical_size(cols, rows)
    pages = rows * cols
    print 'generating PDF'
    print 'cols: %s' % cols
    print 'rows: %s' % rows
    print 'pages: %s' % pages
    print 'size: %.1f m x %.1f m (w x h)' % (physical_width, physical_height)

    c = canvas.Canvas(name + '_new.pdf', pagesize=A4)

    x_idx = 0
    for x_idx, x1 in enumerate(range(0, width - 1, 2)):
        x2 = x1 + 1
        for y_idx, y1 in enumerate(range(0, height - 1, 2)):
            y2 = y1 + 1
            filename = get_filename(x_idx, y_idx)
            image = create_composite(
                tiles[x1][y1],
                tiles[x2][y1],
                tiles[x1][y2],
                tiles[x2][y2],
                filename
            )
            print_image(c, image, filename)


if __name__ == '__main__':
    directory = os.getcwd() + '/xyz'
    os.chdir(directory)
    files = [directory + '/' + png for png in glob.glob('*.png')]

    files = sorted(file for file in files)

    create_pdf(files, 'map')
