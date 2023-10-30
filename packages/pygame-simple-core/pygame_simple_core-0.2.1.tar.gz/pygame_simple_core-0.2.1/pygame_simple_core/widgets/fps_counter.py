import pygame as pg
from ..tools import load_font


class FpsCounter():

    def __init__(
        self,
        clock,
        font=(20, None),
        text_pattern='[fps] FPS',
        precision=1,
        antialias=True,
        foreground='#ffffff',
        background='#000000',
        position='topright',
        visible=True,
    ):
        self.clock = clock
        self.font = load_font(font)
        self.text_pattern = text_pattern
        self.precision = precision
        self.antialias = antialias
        self.foreground = foreground
        self.background = background
        self.position = position
        self.visible = visible

    def draw(self, screen=None):
        if self.visible:
            screen = pg.display.get_surface() if screen == None else screen

            fps_value = self.clock.get_fps()
            fps_text = self.text_pattern.replace(
                '[fps]', f'{fps_value:.{self.precision}f}')
            fps_surf = self.font.render(
                fps_text, self.antialias, self.foreground, self.background)
            fps_rect = fps_surf.get_rect()
            position_value = getattr(screen.get_rect(), self.position)
            setattr(fps_rect, self.position, position_value)

            screen.blit(fps_surf, fps_rect)
