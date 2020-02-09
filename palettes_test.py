import itertools
import pygame
from game import Game
from palettes import PALETTES
from entity import Entity


class Palettes(Entity):

    CELL_SIZE = 64

    def __init__(self):
        super().__init__()
        self._buf = [[0] * 16 * self.CELL_SIZE for _ in range(4 * self.CELL_SIZE)]
        for row in range(4):
            for col in range(16):
                for r, c in itertools.product(range(self.CELL_SIZE), range(self.CELL_SIZE)):
                    self._buf[row * self.CELL_SIZE + r][col * self.CELL_SIZE + c] = PALETTES[row * 16 + col]
        content = []
        for row in self._buf:
            for col in row:
                content.append(col[0])
                content.append(col[1])
                content.append(col[2])
        self._image = pygame.image.fromstring(bytes(content), (16 * self.CELL_SIZE, 4 * self.CELL_SIZE), 'RGB')
        print(self._image)

    def size(self):
        return (self.CELL_SIZE * 16, self.CELL_SIZE * 4)

    def on_render(self, screen):
        screen.fill((255, 255, 255))
        screen.blit(self._image, (0, 0))

    def on_update(self, delta):
        pass


def palettes_test():
    pal = Palettes()
    game = Game(*pal.size(), 'PALETTES')
    game.add_entity(pal)
    game.run()


if __name__ == "__main__":
    palettes_test()
