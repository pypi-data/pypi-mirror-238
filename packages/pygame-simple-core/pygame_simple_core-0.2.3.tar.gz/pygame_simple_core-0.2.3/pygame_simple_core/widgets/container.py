import pygame as pg


class Container():

    def __init__(
        self,
        elements,
        orientation='vertical',
        alignment='centerx',
        spacement=0
    ):
        self.elements = elements
        self.orientation = orientation
        self.alignment = alignment
        self.spacement = spacement
        self.rect_accessed_times = 1

        self.calculate_rect()

    def calculate_rect(self):
        widths = [element.rect.width for element in self.elements]
        heights = [element.rect.height for element in self.elements]
        spacement = self.spacement * (len(self.elements) - 1)

        if self.orientation in ('vertical', 'v'):
            height = sum(heights) + spacement
            width = max(widths)
        elif self.orientation in ('horizontal', 'h'):
            width = sum(widths) + spacement
            height = max(heights)

        self._rect = pg.Rect(0, 0, width, height)

    def update(self):
        if self.orientation in ('vertical', 'v'):
            top = self._rect.top
            last_height = 0

            for element in self.elements:
                top += last_height + self.spacement
                last_height = element.rect.height

                element.rect.top = top

                alignment_value = getattr(self._rect, self.alignment)
                setattr(element.rect, self.alignment, alignment_value)

                print(top)
        elif self.orientation in ('horizontal', 'h'):
            left = self._rect.left
            last_width = 0

            for element in self.elements:
                left += last_width + self.spacement
                last_width = element.rect.width

                element.rect.left = left

                alignment_value = getattr(self._rect, self.alignment)
                setattr(element.rect, self.alignment, alignment_value)

    @property
    def rect(self):
        self.rect_accessed_times += 1
        return self._rect

    def draw(self, screen=None):
        screen = pg.display.get_surface() if screen == None else screen

        if self.rect_accessed_times > 0:
            self.update()
            self.rect_accessed_times = 0

        for element in self.elements:
            element.draw(screen)
