Tiles on a pdf
==============

What?
-----
I had an idea of making a big wall-map, but not having a plotter limits
the possiblities a bit, I thought.. But, tiles are great for this.

So: what this utility does is, given a bbox, a zoom-level and a tile
url, calculates the needed tiles, requests them and assembles them to a
pdf you can print.

I've found that the best solution is to merge 4 tiles on one A4-sheet of
paper, so the bbox is rounded up to get an even number of tiles in x and y.

One issue is that most printers will add a margin to your printed pages..


Usage
-----
1. setup a venv
2. pip install -r requirements.txt
3. edit generate_pdf.py (bbox, url and zoom)
4. python generate_pdf.py
5. look at xyz/generated_new.pdf
6. print without margins and assemble
