# -*- coding: utf-8 -*-
import StringIO

from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from reportlab.lib.utils import ImageReader

from util import physical_size
from image_operations import combine_tiles


def get_filename(x, y):
    return '/%03d_%03d.png' % (x, y)


def pil_to_rl(image, name):
    output = StringIO.StringIO()
    image.save(output, format='png')
    contents = output.getvalue()
    output.close()
    return ImageReader(StringIO.StringIO(contents))


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


def create_pdf(tiles, filename):
    height = len(tiles[0])
    width = len(tiles)

    cols = width / 2
    rows = height / 2
    physical_width, physical_height = physical_size(cols, rows)
    pages = rows * cols
    print 'generating PDF'
    print 'cols: %s' % cols
    print 'rows: %s' % rows
    print 'pages: %s' % pages
    print 'size: %.1f m x %.1f m (w x h)' % (physical_width, physical_height)

    c = canvas.Canvas(filename, pagesize=A4)
    x_idx = 0
    for x_idx, x1 in enumerate(range(0, width - 1, 2)):
        x2 = x1 + 1
        for y_idx, y1 in enumerate(range(0, height - 1, 2)):
            y2 = y1 + 1

            image = combine_tiles({
                0: {0: tiles[x1][y1], 1: tiles[x1][y2]},
                1: {0: tiles[x2][y1], 1: tiles[x2][y2]},
            })
            print_image(c, image, get_filename(x_idx, y_idx))

