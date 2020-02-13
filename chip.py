
class Chip:

    def __init__(self):
        pass

    def sensitive(self, addr):
        raise NotImplementedError

    def read(self, addr):
        raise NotImplementedError

    def write(self, addr, value):
        raise NotImplementedError


class Ram(Chip):

    def __init__(self):
        super().__init__()
        self._mem = [0] * 0x800

    def sensitive(self, addr):
        return 0x0000 <= addr < 0x2000

    def read(self, addr):
        return self._mem[addr % 0x800]

    def write(self, addr, value):
        assert isinstance(value, int)
        assert 0 <= value < 256
        self._mem[addr % 0x800] = value
        return True


class PPURegister(Chip):

    def __init__(self, ppu_bus):
        super().__init__()
        self._mem = [0] * 8

        self._buffered_data = 0

        self._ppu_addr = 0
        self._cpu_write_half_addr = False
        self._ppu_bus = ppu_bus

        self._debug_cnt = 0

    def sensitive(self, addr):
        return 0x2000 <= addr < 0x4000

    def read(self, addr):
        res = self._mem[(addr - 0x2000) % 8]
        addr = (addr - 0x2000) % 8
        if addr == 2:
            self._mem[2] &= 0b01100000
            res &= 0xE0
            self._cpu_write_half_addr = False
        elif addr == 7:
            # TODO: need fix
            # raise SyntaxError('WTF')
            # print('Cpu Read: {:04X} = {}'.format(self._ppu_addr, self._buffered_data))
            res = self._buffered_data
            self._buffered_data = self._ppu_bus.read(self._ppu_addr)
            if self._ppu_addr >= 0x3F00:
                res = self._buffered_data
            if (self.ctrl >> 2 & 1) == 0:
                self._ppu_addr += 1
            else:
                self._ppu_addr += 32
            # raise RuntimeError('brk')
        # print('Cpu Read: {:04X}'.format(addr))
        return res

    def write(self, addr, value):
        assert isinstance(value, int)
        assert 0 <= value < 256
        
        self._mem[(addr - 0x2000) % 8] = value
        # print('Cpu Write: {:04X} = {}'.format(addr, value))
        # input('waiting...')
        addr = (addr - 0x2000) % 8
        if addr == 0: # CTRL
            print('Cpu Write: CTRL = {}'.format(value))
        elif addr == 1: # MASK
            pass
        elif addr == 2: # STATUS
            pass
        elif addr == 3: # TODO
            pass
        elif addr == 4: # TODO
            pass
        elif addr == 5: # SCROLL
            pass
        elif addr == 6: # ADDR
            if self._cpu_write_half_addr:
                self._ppu_addr &= 0xFF00
                self._ppu_addr |= value
                self._cpu_write_half_addr = False
            else:
                self._ppu_addr = (((value & 0x3F) << 8) | (self._ppu_addr & 0x00FF))
                self._cpu_write_half_addr = True
        elif addr == 7: # DATA
            # print('Cpu Write: {:04X} = {}'.format(self._ppu_addr, value))
            self._ppu_bus.write(self._ppu_addr, value)
            if (self.ctrl >> 2 & 1) == 0:
                self._ppu_addr += 1
            else:
                self._ppu_addr += 32
        return True

    @property
    def ctrl(self):
        return self._mem[0]

    @ctrl.setter
    def ctrl(self, value):
        assert isinstance(value, int)
        assert 0 <= value < 256
        self._mem[0] = value

    @property
    def mask(self):
        return self._mem[1]

    @mask.setter
    def mask(self, value):
        assert isinstance(value, int)
        assert 0 <= value < 256
        self._mem[1] = value

    @property
    def status(self):
        return self._mem[2]

    @status.setter
    def status(self, value):
        assert isinstance(value, int)
        assert 0 <= value < 256
        self._mem[2] = value

    @property
    def oamaddr(self):
        return self._mem[3]

    @oamaddr.setter
    def oamaddr(self, value):
        assert isinstance(value, int)
        assert 0 <= value < 256
        self._mem[3] = value

    @property
    def oamdata(self):
        return self._mem[4]

    @oamdata.setter
    def oamdata(self, value):
        assert isinstance(value, int)
        assert 0 <= value < 256
        self._mem[4] = value

    @property
    def scroll(self):
        return self._mem[5]

    @scroll.setter
    def scroll(self, value):
        assert isinstance(value, int)
        assert 0 <= value < 256
        self._mem[5] = value

    @property
    def ppu_addr(self):
        return self._mem[6]

    @ppu_addr.setter
    def ppu_addr(self, value):
        assert isinstance(value, int)
        assert 0 <= value < 256
        self._mem[6] = value

    @property
    def ppu_data(self):
        return self._mem[7]

    @ppu_data.setter
    def ppu_data(self, value):
        assert isinstance(value, int)
        assert 0 <= value < 256
        self._mem[7] = value


class PAuExp(Chip):

    def __init__(self):
        super().__init__()
        self._mem = [0] * 0x2000

    def sensitive(self, addr):
        return 0x4000 <= addr < 0x6000

    def read(self, addr):
        return self._mem[addr - 0x4000]

    def write(self, addr, value):
        assert isinstance(value, int)
        assert 0 <= value < 256
        self._mem[addr - 0x4000] = value
        return True


class PGRRom(Chip):

    def __init__(self):
        super().__init__()
        self._mem = [0] * 0x4000 * 2

    def sensitive(self, addr):
        return 0x8000 <= addr < 0x8000 + 0x4000 * 2

    def load(self, content):
        for i, v in enumerate(content):
            self._mem[i] = v
        if len(content) == 0x4000:
            for i, v in enumerate(content):
                self._mem[i + 0x4000] = v

    def read(self, addr):
        return self._mem[addr - 0x8000]

    def write(self, addr, value):
        return False


class PatternTable(Chip):

    def __init__(self):
        super().__init__()
        self._mem = [0] * 0x2000

    def sensitive(self, addr):
        return 0 <= addr < 0x2000

    def read(self, addr):
        return self._mem[addr]

    def write(self, addr, value):
        assert False, "Cannot write PGR ROM"
        return False

    def load(self, content):
        assert len(content) == 0x2000
        for i, v in enumerate(content):
            self._mem[i] = v


class NameTable(Chip):

    def __init__(self):
        super().__init__()
        self._mem = [0] * (0x3F00 - 0x2000)

    def sensitive(self, addr):
        return 0x2000 <= addr < 0x3F00

    def read(self, addr):
        return self._mem[addr - 0x2000]

    def write(self, addr, value):
        assert isinstance(value, int)
        assert 0 <= value < 256
        if 0x2000 + 960 <= addr <= 0x2000 + 1024:
            print('NameTable Write: ${:04X} = {}'.format(addr, value))
        self._mem[addr - 0x2000] = value
        return True


class PaletteTable(Chip):

    def __init__(self):
        super().__init__()
        self._mem = [0] * 0x20

    def sensitive(self, addr):
        return 0x3F00 <= addr < 0x4000

    def read(self, addr):
        # print(self._mem[:16])
        addr = (addr - 0x3F00) % 0x20
        if addr == 0x10:
            addr = 0x00
        elif addr == 0x14:
            addr = 0x04
        elif addr == 0x18:
            addr = 0x08
        elif addr == 0x1C:
            addr = 0x0C
        if addr % 4 == 0:
            addr = 0
        return self._mem[addr]

    def write(self, addr, value):
        assert isinstance(value, int)
        assert 0 <= value < 256
        addr = (addr - 0x3F00) % 0x20
        if addr == 0x10:
            addr = 0x00
        elif addr == 0x14:
            addr = 0x04
        elif addr == 0x18:
            addr = 0x08
        elif addr == 0x1C:
            addr = 0x0C
        self._mem[addr] = value
        return True
