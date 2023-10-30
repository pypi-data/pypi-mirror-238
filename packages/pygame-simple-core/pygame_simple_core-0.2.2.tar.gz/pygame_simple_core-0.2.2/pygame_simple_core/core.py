import os
import pygame as pg
from .tools import ScheduledEvent
from .widgets import FpsCounter


class Core():

    # in execution order:

    def __init__(
        self,
        icon=None,
        title='Pygame Simple Core',
        size=(0, 0),
        flags=pg.FULLSCREEN | pg.SRCALPHA,
        fps_limit=0,
        fps_counter={}
    ):
        pg.init()

        if icon != None:
            icon = pg.image.load(icon) if isinstance(icon, str) else icon
            pg.display.set_icon(icon)

        pg.display.set_caption(title)
        self.screen = pg.display.set_mode(size, flags)
        self.screen_rect = self.screen.get_rect()
        self.screen_color = '#ffffff'
        self.clock = pg.time.Clock()
        self.fps_counter = FpsCounter(self.clock, **fps_counter)
        self.frametime = 0
        self.fps_limit = fps_limit
        self.scheduled_events = []
        self.quit_keys = [pg.K_ESCAPE]
        self.running = True

    def run(self):
        while self.running:
            self._check_scheduled_events()
            self._check_quit_events()
            self.update()
            self._draw()
            self.frametime = self.clock.tick(self.fps_limit) / 1000

    def _check_scheduled_events(self):
        for event in self.scheduled_events:
            event.call()

    def _check_quit_events(self):
        for event in pg.event.get():
            if event.type == pg.QUIT or event.type == pg.KEYDOWN and \
                    event.key in self.quit_keys:
                self.running = False
                self.quit()
            else:
                self.check_event(event)

    def _draw(self):
        self.screen.fill(self.screen_color)
        self.draw()
        self.fps_counter.draw()
        pg.display.flip()

    # other utilities:

    def set_timeout(self, milisseconds, function, *args, **kwargs):
        event = ScheduledEvent(
            milisseconds, function, args, kwargs,
            False, self.scheduled_events
        )

        self.scheduled_events.append(event)
        return event

    def set_interval(self, milisseconds, function, *args, **kwargs):
        event = ScheduledEvent(
            milisseconds, function, args, kwargs,
            True, self.scheduled_events
        )

        self.scheduled_events.append(event)
        return event

    # to be overrided:

    def check_event(self, event):
        pass

    def update(self):
        pass

    def draw(self):
        pass

    def quit(self):
        pass
