from re import search
import pygame as pg
from . import font_finder


def load_font(font):
    font_size = font[0]
    font_args = font[1:]

    font_path = font_finder.find_font(*font_args)

    if font_path == None:
        name = font_args[0]
        bold = search(r'bold|black', font_args[1].lower()) if len(
            font_args) >= 2 else False
        italic = font_args[2] if len(font_args) >= 3 else False

        font = pg.font.SysFont(None, font_size, bold=bold, italic=italic)
    else:
        font = pg.font.Font(font_path, font_size)

    return font
