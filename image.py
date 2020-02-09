import pygame


class FCImage:

    def __init__(self):
        self._buf = [[0] * 256 for _ in range(240)]


def main():
    img = pygame.image.load('test.jpg')
    bt = pygame.image.tostring(img, 'RGBA')
    print(type(bt))


if __name__ == "__main__":
    main()
