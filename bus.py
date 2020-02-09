from chip import Chip


class Bus:

    def __init__(self):
        self.chips = []

    def connect(self, chip: Chip):
        self.chips.append(chip)

    def read(self, addr):
        read_chip = None
        for chip in self.chips:
            if chip.sensitive(addr):
                read_chip = chip
                break
        assert read_chip is not None, 'ADDR: {}'.format(addr)
        return read_chip.read(addr)

    def write(self, addr, value):
        write_chip = None
        for chip in self.chips:
            if chip.sensitive(addr):
                write_chip = chip
                break
        assert write_chip is not None
        return write_chip.write(addr, value)