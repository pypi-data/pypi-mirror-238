import pygame as pg


class ScheduledEvent():

    def __init__(self, milisseconds, function, args, kwargs, repeat, events):
        self.start = pg.time.get_ticks()
        self.milisseconds = milisseconds
        self.function = lambda: function(*args, **kwargs)
        self.repeat = repeat
        self.events = events

    @property
    def finish(self):
        return self.start + self.milisseconds

    def call(self):
        current_time = pg.time.get_ticks()

        if current_time >= self.finish:
            self.function()

            if self.repeat:
                self.start = current_time
            else:
                self.events.remove(self)


