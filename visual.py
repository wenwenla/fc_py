from entity import Entity
from bus import Bus
from cpu import Cpu6502
from nes import Nes
from chip import Ram, PGRRom, PAuExp, PPURegister
from game import Game
import pygame


class Machine(Entity):

    def __init__(self):
        super().__init__()
        nes = Nes()
        nes.load('roms/nestest.nes')
        self._cpu_ram = Ram()
        self._pgr = PGRRom()
        self._pgr.load(nes.pgr)
        self._papu_ram = PAuExp()

        self._ppu_register = PPURegister()

        self._cpu_bus = Bus()
        self._cpu_bus.connect(self._pgr)
        self._cpu_bus.connect(self._cpu_ram)
        self._cpu_bus.connect(self._papu_ram)
        self._cpu_bus.connect(self._ppu_register)
        self._cpu = Cpu6502(self._cpu_bus)
        self._cpu.test_mode()
        self._addr_map, self._code = self._cpu.decode(0xC000, 0xFF00)
        self._font = pygame.font.SysFont('inconsolatan', 24)

        self._cpu_running = False

    def draw_code(self, screen):
        log = self._cpu.log()
        pc = log['PC']
        assert pc in self._addr_map
        now_pos = self._addr_map[pc]
        code_x_start = 550
        code_y_start = 100
        code_line = 0
        code_height = 20
        for pos in range(now_pos - 10, now_pos + 11):
            if pos < 0 or pos >= len(self._code):
                continue
            if pos == now_pos:
                now_code = self._font.render(self._code[pos], True, (255, 0, 0))
            else:
                now_code = self._font.render(self._code[pos], True, (0, 0, 0))    
            screen.blit(now_code, (code_x_start, code_line * code_height + code_y_start))
            code_line += 1

    def draw_flag(self, screen):
        flag_x_start = 620
        flag_y_start = 50
        width = 20
        flag_tips = self._font.render('Flags:', True, (0, 0, 0))
        screen.blit(flag_tips, (550, flag_y_start))
        # n v - b d i z c
        char = 'nv-bdizc'
        log = self._cpu.log()
        flag = log['F']
        for i in range(8):
            if ((flag >> (7 - i))) & 1 == 1:
                f = self._font.render(char[i], True, (0, 0, 0))
            else:
                f = self._font.render(char[i], True, (128, 128, 128))
            screen.blit(f, (flag_x_start + i * width, flag_y_start))


    def draw_reg(self, screen):
        reg_x_start = 550
        reg_y_start = 0
        one_width = 100
        one_height = 20
        log = self._cpu.log()
        reg_a = self._font.render('A: ${:02X}'.format(log['A']), True, (0, 0, 0))
        reg_sp = self._font.render('S: ${:02X}'.format(log['SP']), True, (0, 0, 0))
        reg_x = self._font.render('X: ${:02X}'.format(log['X']), True, (0, 0, 0))
        reg_y = self._font.render('Y: ${:02X}'.format(log['Y']), True, (0, 0, 0))
        screen.blit(reg_a, (reg_x_start, reg_y_start))
        screen.blit((reg_sp), (reg_x_start + one_width, reg_y_start))
        screen.blit(reg_x, (reg_x_start, reg_y_start + one_height))
        screen.blit(reg_y, (reg_x_start + one_width, reg_y_start + one_height))

    def on_update(self, delta):
        if self._cpu_running:
            self._cpu.run()

    def on_render(self, screen):
        screen.fill((255, 255, 255))
        self.draw_code(screen)
        self.draw_reg(screen)
        self.draw_flag(screen)

    def on_event(self, event):
        if event.type == pygame.locals.KEYDOWN:
            if event.key == pygame.locals.K_r:
                self._cpu_running = not self._cpu_running
            if event.key == pygame.locals.K_SPACE:
                if not self._cpu_running:
                    self._cpu.run()


def main():
    game = Game(800, 600, "FCEMU")
    machine = Machine()
    game.add_entity(machine)
    game.run()


if __name__ == "__main__":
    main()
