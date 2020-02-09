
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


class PPURegister(Chip):

    def __init__(self):
        super().__init__()
        self._mem = [0] * 8

    def sensitive(self, addr):
        return 0x2000 <= addr < 0x4000

    def read(self, addr):
        return self._mem[(addr - 0x2000) % 8]

    def write(self, addr, value):
        assert isinstance(value, int)
        assert 0 <= value < 256
        self._mem[(addr - 0x2000) % 8] = value


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