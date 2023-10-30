import pygame as pg
from . import Text


class Button():

    def __init__(
        self,
        text,
        background='#808080',
        size=None,
        padding=[0.1],
        border=None,
        border_radius=[0],
        shadow=None,
        click_offset=(2, 2),
        hover=None
    ):
        self.text = text
        self.background = background
        self.size = size
        self.padding = [padding[i % len(padding)] for i in range(4)]
        self.border = border
        self.border_radius = [
            border_radius[i % len(border_radius)] for i in range(4)
        ]
        self.shadow = shadow
        self.click_offset = click_offset
        self.hover = hover if hover != None else {}

        for value in (
            'text', 'background', 'size', 'padding', 'border',
            'border_radius', 'shadow'
        ):
            if not value in self.hover:
                self.hover[value] = getattr(self, value)

        if isinstance(self.text, dict):
            for key, value in self.text.items():
                self.hover['text'][key] = value
        elif not 'text' in self.hover['text'] and isinstance(self.hover['text'], dict):
            self.hover['text']['text'] = self.text

        self.update()

    def update(self):
        self.render_surf()
        surf = self.surf
        old_args = {}

        for key, value in self.hover.items():
            old_args[key] = value
            setattr(self, key, value)

        self.render_surf()
        self.surf_hover = self.surf
        self.surf = surf

        for key, value in old_args.items():
            setattr(self, key, value)

    def render_surf(self):
        self.render_front()

        if self.shadow != None:
            self.render_shadow()

        self.surf = self.surf.convert_alpha()

    def render_front(self):
        text = Text(**self.text) if isinstance(
            self.text, dict) else Text(self.text)
        inner_width, inner_height, border_width, border_height = \
            self.get_size(text)

        surf = pg.Surface((border_width, border_height), pg.SRCALPHA)
        border_rect = surf.get_rect()
        inner_rect = pg.Rect(0, 0, inner_width, inner_height)
        inner_rect.center = border_rect.center

        if self.border != None:
            pg.draw.rect(surf, self.border[0], border_rect, 0, *self.border_radius)

        pg.draw.rect(surf, self.background, inner_rect, 0, *self.border_radius)
        text.draw(surf)

        self.surf = surf
        self.rect = border_rect

    def render_shadow(self):
        shadow_color = self.shadow[0]
        shadow_x = self.shadow[1][0]
        shadow_y = self.shadow[1][1]
        shadow_rect = self.surf.get_rect()

        rect = self.rect.inflate(abs(shadow_x), abs(shadow_y))
        surf = pg.Surface((rect.width, rect.height), pg.SRCALPHA)

        if shadow_x > 0:
            shadow_rect.move_ip(shadow_x, 0)
        else:
            self.rect.move_ip(-shadow_x, 0)

        if shadow_y > 0:
            shadow_rect.move_ip(0, shadow_y)
        else:
            self.rect.move_ip(0, -shadow_y)

        pg.draw.rect(surf, shadow_color, shadow_rect, 0, *self.border_radius)
        surf.blit(self.surf, self.rect)

        self.surf = surf
        self.rect = rect


    def get_size(self, text):
        inner_width, inner_height = self.get_inner_size(text)

        if self.border != None:
            borders = [self.border[1][i % len(self.border[1])] for i in range(4)]
            border_left = borders[0]
            border_top = borders[1]
            border_right = borders[2]
            border_bottom = borders[3]

            width = border_left + inner_width + border_right
            height = border_top + inner_height + border_bottom

            text.rect.move_ip(border_left, border_top)
        else:
            width = inner_width
            height = inner_height

        return inner_width, inner_height, width, height

    def get_inner_size(self, text):
        if self.size != None:
           width, height = self.size
           text.rect.center = (width // 2, height // 2)
        else:
            padding_left = self.padding[0] * text.rect.width
            padding_top = self.padding[1] * text.rect.height
            padding_right = self.padding[2] * text.rect.width
            padding_bottom = self.padding[3] * text.rect.height

            width = padding_left + text.rect.width + padding_right
            height = padding_top + text.rect.height + padding_bottom

            text.rect.move_ip(padding_left, padding_top)

        return width, height

    def check_hover(self):
        return self.surf_hover if self.is_hovered else self.surf

    def check_activate(self):
        return self.rect.move(self.click_offset) if self.is_active else self.rect

    @property
    def is_hovered(self):
        return self.rect.collidepoint(pg.mouse.get_pos())

    @property
    def is_active(self):
        return self.is_hovered and pg.mouse.get_pressed()[0]

    def draw(self, screen=None):
        screen = pg.display.get_surface() if screen == None else screen

        surf = self.check_hover()
        rect = self.check_activate()

        screen.blit(surf, rect)
