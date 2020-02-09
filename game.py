import sys
import pygame
from pygame.locals import QUIT


class Game:

    def __init__(self, width, height, caption):
        pygame.display.init()
        pygame.font.init()
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

    def _fix_fps(self, fps):
        now_render = pygame.time.get_ticks()
        time_delta = now_render - self.prev_render
        self.prev_render = now_render
        needed_dleta = 1000 // fps
        if time_delta < needed_dleta:
            pygame.time.delay(needed_dleta - time_delta)

    def add_entity(self, entity):
        self.entities.append(entity)

    def run(self):
        while self.running:
            self.process_event()
            self.update(self._update_time_delta())
            self.render()
            self._fix_fps(30)
        pygame.quit()
        sys.exit()

    def process_event(self):
        for event in pygame.event.get():
            if event.type == QUIT:
                self.running = False

    def update(self, delta):
        for e in self.entities:
            e.on_update(delta)

    def render(self):
        for e in self.entities:
            e.on_render(self.display)
        pygame.display.update()
