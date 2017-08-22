# -*- coding: utf-8 -*-
from PIL import Image as PilImage


def combine_tiles(tiles):
    rows = len(tiles[0])
    cols = len(tiles)

    width = cols * 256
    height = rows * 256

    merged = PilImage.new('RGB', (width, height))
    for row in range(0, rows):
        for col in range(0, cols):
            merged.paste(PilImage.open(tiles[row][col]), (row * 256, col * 256))
    return merged
