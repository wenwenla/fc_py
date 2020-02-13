import entity
import pygame


class FpsInfo(entity.Entity):

    LAST = 10

    def __init__(self):
        super().__init__()
        self.font = pygame.font.SysFont('consola', 18)
        self.render_cnt = 0
        self.start_time = pygame.time.get_ticks()
        self.fps = 0

    def on_update(self, delta):
        pass

    def on_render(self, screen):
        if self.render_cnt == FpsInfo.LAST:
            now = pygame.time.get_ticks()
            self.render_cnt = 0
            self.fps = 1000 * FpsInfo.LAST / (now - self.start_time)
            self.start_time = now
        self.render_cnt += 1
        hello = self.font.render('FPS: {:.2f}'.format(self.fps), True, (255, 0, 0))
        screen.blit(hello, (700, self.font.get_linesize()))

    def on_event(self, event):
        pass

