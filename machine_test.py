from chip import *
from cpu import Cpu6502
from ppu import Ppu
from bus import Bus
from nes import Nes
from log import Log
from collections import OrderedDict


def main():
    _ppu_bus = Bus()
    _ppu_pattern = PatternTable()
    # _ppu_pattern.load(nes.chr)
    _ppu_name = NameTable()
    _ppu_palette = PaletteTable()
    _ppu_bus.connect(_ppu_pattern)
    _ppu_bus.connect(_ppu_name)
    _ppu_bus.connect(_ppu_palette)
    _ppu = Ppu(_ppu_bus)

    ram = Ram()
    pgr = PGRRom()
    ppu_reg = PPURegister(_ppu_bus)
    pau_exp = PAuExp()
    nes = Nes()
    nes.load('roms/nestest.nes')
    pgr.load(nes.pgr)

    bus = Bus()
    bus.connect(pgr)
    bus.connect(ram)
    bus.connect(pau_exp)
    bus.connect(ppu_reg)

    cpu = Cpu6502(bus)
    cpu.test_mode()

    real_log = Log()
    n = 0
    while True:
        n += 1
        log = cpu.log()
        if not real_log.check(log):
            # print('F: {}'.format(OrderedDict(log)))
            # print('T: {}'.format(OrderedDict(real_log.log())))
            # print('{} Addr: {}, Data: {}'.format(n, cpu._addr, cpu._data))
            break
        else:
            pass
            # print('T: {}'.format(OrderedDict(log)))
        cpu.run()
        end = real_log.next()
        if end:
            break
    print('{} ins passed'.format(n))


if __name__ == "__main__":
    main()
