

class Nes:

    def __init__(self):
        self._mapper = 0
        self._flag_f = False
        self._flag_t = False
        self._flag_b = False
        self._flag_m = False
        self._flag_p = False
        self._flag_v = False
        self.trainer = None
        self.pgr = None
        self.chr = None

    def load(self, path):
        with open(path, 'rb') as file_in:
            buffer = file_in.read()
        if buffer[0] != ord('N') or buffer[1] != ord('E') or buffer[2] != ord('S'):
            raise RuntimeError('Not a valid nes file')
        flag6 = buffer[6]
        flag7 = buffer[7]
        self._mapper = (flag7 & 0xff00 << 4) | (flag6 & 0xff00)
        self._flag_f = (flag6 >> 3 & 1) == 1
        self._flag_t = (flag6 >> 2 & 1) == 1
        self._flag_b = (flag6 >> 1 & 1) == 1
        self._flag_m = (flag6 >> 0 & 1) == 1
        self._flag_p = (flag7 >> 1 & 1) == 1
        self._flag_v = (flag7 >> 0 & 1) == 1
        print('Nes info:')
        print('PRG-size: {} bytes'.format(buffer[4] * 16384))
        print('CHR-size: {} bytes'.format(buffer[5] * 8192))
        print('Mapper: {}'.format(self._mapper))
        print('Flags on: ', end='')
        if self._flag_f:
            print('F', end=' ')
        if self._flag_t:
            print('T', end=' ')
        if self._flag_b:
            print('B', end=' ')
        if self._flag_m:
            print('M', end=' ')
        if self._flag_p:
            print('P', end=' ')
        if self._flag_v:
            print('V', end='')
        print('\nNes info end\n================')
        now_start = 16
        if self._flag_t:
            self.trainer = buffer[now_start:now_start + 512]
            now_start += 512
        self.pgr = buffer[now_start:now_start + buffer[4] * 16384]
        now_start += buffer[4] * 16384
        self.chr = buffer[now_start:now_start + buffer[5] * 8192]
        now_start += buffer[5] * 8192


if __name__ == '__main__':
    nes = Nes()
    nes.load('roms/mario.nes')