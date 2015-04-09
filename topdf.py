# -*- coding: utf-8 -*-
import os
import glob

from PIL import Image as PilImage
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.pagesizes import A4
from reportlab.platypus import Image, Paragraph, Spacer, BaseDocTemplate, \
    NextPageTemplate, PageBreak, Frame, PageTemplate
from reportlab.lib.enums import TA_CENTER
from reportlab.lib.units import inch


def pil_to_rl(image, name):
    filename = '/tmp/' + name + '.png'
    image.save(filename)
    return Image(filename)


def is_blank(infile):
    #image = PilImage.open(infile)
    #return len(image.getcolors()) < 2
    return False


def create_page(elements, infile, name):
    styles = getSampleStyleSheet()
    styleN = styles['Normal']
    styleN.alignment = TA_CENTER
    #name = infile.split('/')[-1].split('.')[0]
    elements.append(Paragraph(name, styleN))
    elements.append(Spacer(1, .1 * inch))
    elements.append(pil_to_rl(infile, name))
    elements.append(NextPageTemplate('OneCol'))
    elements.append(PageBreak())


def create_composite(ul, ll, ur, lr, name):
    new_im = PilImage.new('RGB', (512,512))
    new_im.paste(PilImage.open(ul), (0,0))
    new_im.paste(PilImage.open(ll), (256,0))
    new_im.paste(PilImage.open(ur), (0,256))
    new_im.paste(PilImage.open(lr), (256, 256))
    return new_im


def get_filename(x, y):
    return '/%03d_%03d.png' % (x, y)


def create_pdf(images, name):
    doc = BaseDocTemplate(name + '.pdf', showBoundary=0, pagesize=A4, rightMargin=0, leftMargin=0, topMargin=0, bottomMargin=0)
    frameT = Frame(doc.leftMargin, doc.bottomMargin, doc.width, doc.height)
    elements = []

    imgs = {}
    for image in images:
        fn = image.split('/')[-1].split('.')[0].split('_')
        x = int(fn[0])
        y = int(fn[1])
        xs = imgs.get(x, None)
        if not xs:
            xs = {}
            imgs[x] = xs
        xs[y] = image

    height= len(imgs[0])
    width = len(imgs)

    print height
    print width

    x_idx = 0
    for x1 in range(0, width-1, 2):
        print x1
        x2 = x1 + 1
        y_idx = 0
        for y1 in range(0, height-1, 2):
            y2 = y1 + 1
            fn = get_filename(x_idx, y_idx)
            ul = imgs[x1][y1]
            ll = imgs[x2][y1]

            ur = imgs[x1][y2]
            lr = imgs[x2][y2]
            image = create_composite(ul, ll, ur, lr, fn)
            create_page(elements, image, fn)
            y_idx += 1
        x_idx += 1

            

    doc.addPageTemplates([PageTemplate(id='OneCol', frames=frameT)])
    doc.build(elements)

if __name__ == '__main__':
    directory = os.getcwd() + '/xyz'
    os.chdir(directory)
    files = [directory + '/' + png for png in glob.glob('*.png')]

    files = sorted(file for file in files if not is_blank(file))

    create_pdf(files, 'map')
