import random
from bus import Bus
from chip import PPURegister
from palettes import PALETTES
import pygame.image as Image


class Ppu:

    def __init__(self, bus: Bus):
        self._reg = PPURegister(bus)
        self._row = 0
        self._col = 0
        self._req_nmi = lambda: print('Should set requeset nmi function')

        self._bus = bus
        self._pattern = None
        self._pattern_bytes = bytearray(256 * 128 * 3)
        self._fill_pattern()
        self._prepare_pattern()
        self._pattern_image = Image.frombuffer(self._pattern_bytes, (256, 128), 'RGB')

    def set_request_nmi(self, func):
        self._req_nmi = func

    def run(self):
        # print('PPU: {}, {}'.format(self._row, self._col))
        self._col += 1
        if self._col == 340:
            self._row += 1
            self._col = 0
        if self._row == 261:
            self._row = 0
            self._col = 0
            self._reg.status &= 0xEF
            print('UNSET VBANK')
            # print(self._reg.status)
            # input('WAITING...')
        if self._row == 240 and self._col == 0:
            self._reg.status |= (1 << 7)
            print('Set VBANK...')
            # print(self._reg.status)
            # input('WAITING...')
            if (self._reg.ctrl >> 7 & 1) == 1:
                self._req_nmi()
        # print('PPU: {}, {}'.format(self._row, self._col))

    def _prepare_pattern(self):
        pos = 0
        for row in range(128):
            for col in range(256):
                self._pattern_bytes[pos] = PALETTES[self._pattern[col // 128][row][col % 128]][0]
                pos += 1
                self._pattern_bytes[pos] = PALETTES[self._pattern[col // 128][row][col % 128]][1]
                pos += 1
                self._pattern_bytes[pos] = PALETTES[self._pattern[col // 128][row][col % 128]][2]
                pos += 1

    def get_register(self):
        return self._reg

    def get_pattern_image(self):
        return self._pattern_image

    def _fill_pattern(self):
        left = [[0] * 128 for _ in range(128)]
        right = [[0] * 128 for _ in range(128)]

        self._pattern = [
            left,
            right
        ]
        for t in [0x0000, 0x1000]:
            now_row = 0
            now_col = 0
            for addr in range(t, t + 0x1000, 16):
                for row in range(8):
                    lo = self._bus.read(addr + row)
                    hi = self._bus.read(addr + row + 8)
                    for col in range(8):
                        this_index = ((lo >> (7 - col) & 1) | ((hi >> (7 - col) & 1) << 1))
                        self._pattern[t // 0x1000][now_row * 8 + row][now_col * 8 + col] = this_index
                        # self._pattern[t // 0x1000][now_row * 8 + row][now_col * 8 + col] = 1
                now_col += 1
                if now_col == 16:
                    now_col = 0
                    now_row += 1

    def get_palettes_image(self):
        addr_start = 0x3F00
        buffer = []
        for i in range(32):
            color = PALETTES[self._bus.read(addr_start + i)]
            buffer.extend(color)
        return Image.fromstring(bytes(buffer), (8, 4), 'RGB')

    def _get_sprite(self, block, index):
        addr = [0x0000, 0x1000][block] + index * 16
        pattern = [[0] * 8 for _ in range(8)]
        for row in range(8):
            lo = self._bus.read(addr + row)
            hi = self._bus.read(addr + row + 8)
            for col in range(8):
                this_index = ((lo >> (7 - col) & 1) | ((hi >> (7 - col) & 1) << 1))
                pattern[row][col] = this_index
        return pattern

    def get_background(self, name_tbl_index):
        start_addr = [0x2000, 0x2400, 0x2800, 0x2C00][name_tbl_index]
        buf_pixel_index = [[0] * 256 for _ in range(240)]
        sprite_index = (self._reg.ctrl >> 4 & 1)
        for row in range(30):
            for col in range(32):
                block_sprite_index = self._bus.read(start_addr)
                start_addr += 1
                pattern = self._get_sprite(sprite_index, block_sprite_index)
                for r in range(8):
                    for c in range(8):
                        attr = self.get_attr(name_tbl_index, row * 8 + r, col * 8 + c)
                        if pattern[r][c] == 0:
                            addr = 0x3F00
                        else:
                            addr = 0x3F00 + ((attr << 2) | pattern[r][c])
                        buf_pixel_index[row * 8 + r][col * 8 + c] = self._bus.read(addr) 
        buffer = []
        for row in range(240):
            for col in range(256):
                buffer.extend(PALETTES[buf_pixel_index[row][col]])
        return Image.fromstring(bytes(buffer), (256, 240), 'RGB')

    def get_attr(self, name_tbl_index, pixel_row, pixel_col):
        # TODO
        start_addr = [0x2000, 0x2400, 0x2800, 0x2C00][name_tbl_index]
        start_addr += 960
        
        block_row = pixel_row // 8 # [0, 30)
        block_col = pixel_col // 8 # [0, 32)

        block_row_8_8 = block_row // 4
        block_col_8_8 = block_col // 4

        addr = start_addr + block_col_8_8 + block_row_8_8 * 8
        byte = self._bus.read(addr)

        byte_index_row = block_row % 4
        byte_index_col = block_col % 4

        if 0 <= byte_index_row < 2:
            if 0 <= byte_index_col < 2:
                res = (byte & 3)
            else:
                res = ((byte >> 2) & 3)
        else:
            if 0 <= byte_index_col < 2:
                res = ((byte >> 4) & 3)
            else:
                res = ((byte >> 6) & 3)
        return res
