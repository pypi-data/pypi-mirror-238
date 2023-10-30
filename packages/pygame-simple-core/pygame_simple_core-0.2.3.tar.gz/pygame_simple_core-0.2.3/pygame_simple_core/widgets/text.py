import pygame as pg
from ..tools import load_font


class Text():

    def __init__(
        self,
        text,
        font=(20, None),
        antialias=True,
        foreground='#000000',
        background=None,
        shadow=None, # ('#000000', (-2, 2))
        spacement=0.1,
        width=None,
        alignment='left' # left, center, right
    ):
        self.text = str(text)
        self.font = load_font(font)
        self.antialias = antialias
        self.foreground = foreground
        self.background = background
        self.shadow = shadow
        self.spacement = spacement
        self.width = width if width != None else \
            pg.display.get_surface().get_rect().width
        self.alignment = alignment
        self._lines = []
        self.update()

    def update(self):
        self._split_lines()
        self._render_surf()

    def _split_lines(self):
        for line in self.text.split('\n'):
            words = line.split(' ')
            last_sentence = ''
            last_surf = None
            last_rect = None

            for i, word in enumerate(words):
                is_last_word = i + 1 == len(words)
                sentence = f'{last_sentence} {word}'.strip()
                surf, rect = self._render_line(sentence)

                if rect.width > self.width and is_last_word:
                    if last_sentence == '':
                        self._lines.append((surf, rect))
                    else:
                        self._lines.append((last_surf, last_rect))
                        self._lines.append(self._render_line(word))
                elif rect.width > self.width and not(is_last_word):
                    self._lines.append((last_surf, last_rect))
                    last_sentence = f'{word} '
                    last_surf, last_rect = self._render_line(word)
                elif rect.width <= self.width and is_last_word:
                    self._lines.append((surf, rect))
                elif rect.width <= self.width and not(is_last_word):
                    last_sentence = sentence
                    last_surf = surf
                    last_rect = rect

    def _render_line(self, text):
        text_surf = self.font.render(
            text, self.antialias, self.foreground)
        text_rect = text_surf.get_rect()

        if self.shadow != None:
            shadow_color = self.shadow[0]
            shadow_pos_x = self.shadow[1][0]
            shadow_pos_y = self.shadow[1][1]

            shadow_surf = self.font.render(
                text, self.antialias, shadow_color)
            shadow_rect = shadow_surf.get_rect()

            if shadow_pos_x >= 0:
                shadow_rect.move_ip(shadow_pos_x, 0)
            else:
                text_rect.move_ip(-shadow_pos_x, 0)

            if shadow_pos_y >= 0:
                shadow_rect.move_ip(0, shadow_pos_y)
            else:
                text_rect.move_ip(0, -shadow_pos_y)

            left = min(shadow_rect.left, text_rect.left)
            right = max(shadow_rect.right, text_rect.right)
            top = min(shadow_rect.top, text_rect.top)
            bottom = max(shadow_rect.bottom, text_rect.bottom)
            width = right - left
            height = bottom - top

            surf = pg.Surface((width, height), pg.SRCALPHA)
            surf.blit(shadow_surf, shadow_rect)
            surf.blit(text_surf, text_rect)
            rect = surf.get_rect()
        else:
            surf = text_surf
            rect = text_rect

        return (surf, rect)

    def _render_surf(self):
        if len(self._lines) > 1:
            surfs = []
            rects = []

            for surf, rect in self._lines:
                surfs.append(surf)
                rects.append(rect)

            right = max(rect.width for rect in rects)
            height = max(rect.height for rect in rects)
            spacement = height + (height * self.spacement)

            for i, rect in enumerate(rects):
                rect.move_ip(0, spacement * i)

                if self.alignment == 'left':
                    rect.left = 0
                elif self.alignment == 'center':
                    rect.centerx = right // 2
                elif self.alignment == 'right':
                    rect.right = right

            top = min(rect.top for rect in rects)
            bottom = max(rect.bottom for rect in rects)
            height = bottom - top
            width = right

            surf = pg.Surface((width, height), pg.SRCALPHA)
            rect = pg.Rect(0, right, width, height)

            if self.background != None:
                surf.fill(self.background)
                convert_surf = surf.convert
            else:
                convert_surf = surf.convert_alpha

            for line_surf, line_rect in zip(surfs, rects):
                surf.blit(line_surf, line_rect)

            self.surf = convert_surf()

            self.surf = surf
            self.rect = rect
        else:
            surf, rect = self._lines[0]

            if self.background != None:
                self.surf = pg.Surface((rect.width, rect.height), pg.SRCALPHA)
                self.surf.fill(self.background)
                self.surf.blit(surf, rect)
                self.rect = self.surf.get_rect()
            else:
                self.surf = surf
                self.rect = rect

    def draw(self, screen=None):
        screen = pg.display.get_surface() if screen == None else screen

        screen.blit(self.surf, self.rect)
