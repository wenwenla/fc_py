import sys
import pygame
from pygame.locals import QUIT


class Game:

    def __init__(self, width, height, caption):
        pygame.init()
        # pygame.display.init()
        # pygame.font.init()
        # pygame.time.init()
        self.width = width
        self.height = height
        self.display = pygame.display.set_mode((width, height))
        pygame.display.set_caption(caption)
        self.running = True
        self.prev_update = pygame.time.get_ticks()
        self.prev_render = pygame.time.get_ticks()
        self.entities = []

    def _update_time_delta(self):
        now_update = pygame.time.get_ticks()
        time_delta = now_update - self.prev_update
        self.prev_update = now_update
        return time_delta

    def add_entity(self, entity):
        self.entities.append(entity)

    def run(self):
        while self.running:
            self.process_event()
            self.update(self._update_time_delta())
            self.render()
        pygame.quit()
        sys.exit()

    def process_event(self):
        for event in pygame.event.get():
            if event.type == QUIT:
                self.running = False
            for e in self.entities:
                e.on_event(event)

    def update(self, delta):
        for e in self.entities:
            e.on_update(delta)

    def render(self):
        self.display.fill((255, 255, 255))
        for e in self.entities:
            e.on_render(self.display)
        pygame.display.update()
