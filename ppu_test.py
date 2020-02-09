from chip import CHRRom, VRam
from nes import Nes


def ppu_test():
    nes = Nes()
    nes.load('roms/mario.nes')

    chr_rom = CHRRom()
    chr_rom.load(nes.chr)
    v_ram = VRam()
    


if __name__ == "__main__":
    ppu_test()
