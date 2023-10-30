import pygame as pg


class Image():

    def __init__(
        self, path, alpha=False, flip_x=False, flip_y=False, scale=None,
        rotation=None
    ):
        surf = pg.image.load(path)
        self.surf = surf.convert_alpha() if alpha else surf.convert()
        self.rect = self.surf.get_rect()

        if flip_x or flip_y:
            self.flip(flip_x, flip_y)

        if scale != None and rotation != None and isinstance(scale, (int, float)):
            self.rotozoom(rotation, scale)
        else:
            if rotation != None:
                self.rotate(rotation)

            if scale != None:
                self.scale(scale)

    def flip(self, flip_x, flip_y):
        self.surf = pg.transform.flip(self.surf, flip_x, flip_y)

    def rotate(self, angle):
        self.surf = pg.transform.rotate(self.surf, angle)
        self.rect = self.surf.get_rect()

    def scale(self, scale, smooth=True):
        if scale == 2:
            self.surf = pg.transform.scale2x(self.surf)
        else:
            scale = (scale, scale) if isinstance(scale, (int, float)) else scale

            width = scale[0] * self.rect.width
            height = scale[1] * self.rect.height

            self.surf = pg.transform.smoothscale(self.surf, (width, height)) if \
                smooth else pg.transform.scale(self.surf, (width, height))

        self.rect = self.surf.get_rect()

    def rotozoom(self, angle, scale):
        self.surf = pg.transform.rotozoom(self.surf, angle, scale)
        self.rect = self.surf.get_rect()

    def draw(self, screen=None):
        screen = pg.display.get_surface() if screen == None else screen

        screen.blit(self.surf, self.rect)
