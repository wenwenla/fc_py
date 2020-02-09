from chip import Ram, PGRRom, PPURegister, PAuExp
from cpu import Cpu6502
from bus import Bus
from nes import Nes
from log import Log
from collections import OrderedDict


def main():
    ram = Ram()
    pgr = PGRRom()
    ppu_reg = PPURegister()
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
