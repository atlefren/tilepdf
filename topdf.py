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


def is_blank(infile):
    image = PilImage.open(infile)
    return len(image.getcolors()) < 2


def create_page(elements, infile):
    styles = getSampleStyleSheet()
    styleN = styles['Normal']
    styleN.alignment = TA_CENTER
    name = infile.split('/')[-1].split('.')[0]
    elements.append(Paragraph(name, styleN))
    elements.append(Spacer(1, .1 * inch))
    elements.append(Image(infile))
    elements.append(NextPageTemplate('OneCol'))
    elements.append(PageBreak())


def create_pdf(images, name):
    doc = BaseDocTemplate(name + '.pdf', showBoundary=0, pagesize=A4)
    frameT = Frame(doc.leftMargin, doc.bottomMargin, doc.width, doc.height)
    elements = []
    for image in images:
        create_page(elements, image)

    doc.addPageTemplates([PageTemplate(id='OneCol', frames=frameT)])
    doc.build(elements)

if __name__ == '__main__':
    directory = os.getcwd() + '/tiles'
    os.chdir(directory)
    files = [directory + '/' + png for png in glob.glob('*.png')]

    files = sorted(file for file in files if not is_blank(file))

    create_pdf(files, 'map')
