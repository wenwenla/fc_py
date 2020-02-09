from game import Game
from info_disp import FpsInfo

def main():
    g = Game(800, 600, "FcEMU")
    g.add_entity(FpsInfo())
    g.run()


if __name__ == "__main__":
    main()
