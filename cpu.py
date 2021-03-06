from enum import Enum
from bus import Bus
from util import u8, u16, s8


AddrMode = Enum('AddrMode', [
    'Implied',                  # AddrMode.Implied
    'Accumulator',              # AddrMode.Accumulator
    'Immediate',                # AddrMode.Immediate
    'Absolute',                 # AddrMode.Absolute
    'ZeroPage',                 # AddrMode.ZeroPage
    'AbslouteIndexedX',         # AddrMode.AbslouteIndexedX
    'AbslouteIndexedY',         # AddrMode.AbslouteIndexedY
    'ZeroIndexedX',             # AddrMode.ZeroIndexedX
    'ZeroIndexedY',             # AddrMode.ZeroIndexedY
    'Relative',                 # AddrMode.Relative
    'ZeroIndexedIndirectX',     # AddrMode.ZeroIndexedIndirectX
    'AbslouteIndexedIndirectX', # AddrMode.AbslouteIndexedIndirectX
    'IndexedIndirectY',         # AddrMode.IndexedIndirectY
    'ZeroIndirect',             # AddrMode.ZeroIndirect
    'AbslouteIndirect'          # AddrMode.AbslouteIndirect
])


class Instruction:

    def __init__(self, name: str, mode: AddrMode, cycle: int, func):
        self._name = name
        self._mode = mode
        self._cycle = cycle
        self._func = func # execute the insturction

    def length(self):
        if self._mode == AddrMode.Implied:
            res = 1
        elif self._mode == AddrMode.Accumulator:
            res = 1
        elif self._mode == AddrMode.Immediate:
            res = 2
        elif self._mode == AddrMode.Absolute:
            res = 3
        elif self._mode == AddrMode.ZeroPage:
            res = 2
        elif self._mode == AddrMode.AbslouteIndexedX:
            res = 3
        elif self._mode == AddrMode.AbslouteIndexedY:
            res = 3
        elif self._mode == AddrMode.ZeroIndexedX:
            res = 2
        elif self._mode == AddrMode.ZeroIndexedY:
            res = 2
        elif self._mode == AddrMode.Relative:
            res = 2
        elif self._mode == AddrMode.ZeroIndexedIndirectX:
            res = 2
        elif self._mode == AddrMode.AbslouteIndexedIndirectX:
            res = 3
        elif self._mode == AddrMode.IndexedIndirectY:
            res = 2
        elif self._mode == AddrMode.ZeroIndirect:
            res = 2
        elif self._mode == AddrMode.AbslouteIndirect:
            res = 3
        assert res != -1
        return res

    def pc_increment(self):
        if self._name in {'JMP', 'JSR', 'RTI'}:
            return 0
        return self.length()
        
    def addr_mode(self):
        return self._mode

    def cycle(self):
        return self._cycle

    def name(self):
        return self._name

    def execute(self):
        '''
        if branch is taken, we will need one more cycle
        '''
        return self._func()

    def format(self, *args):
        res = self._name
        if self._mode == AddrMode.Implied:
            pass
        elif self._mode == AddrMode.Accumulator:
            next_byte = args[0]
            res += ' ${:02X}'.format(next_byte)
        elif self._mode == AddrMode.Immediate:
            next_byte = args[0]
            res += ' #${:02X}'.format(next_byte)
        elif self._mode == AddrMode.Absolute:
            lo = args[0]
            hi = args[1]
            res += ' ${:04X}'.format((hi << 8) + lo)
        elif self._mode == AddrMode.ZeroPage:
            next_byte = args[0]
            res += ' ${:02X}'.format(next_byte)
        elif self._mode == AddrMode.AbslouteIndexedX:
            lo = args[0]
            hi = args[1]
            res += ' ${:04X}, X'.format((hi << 8) + lo)
        elif self._mode == AddrMode.AbslouteIndexedY:
            lo = args[0]
            hi = args[1]
            res += ' ${:04X}, Y'.format((hi << 8) + lo)
        elif self._mode == AddrMode.ZeroIndexedX:
            next_byte = args[0]
            res += ' ${:02X}, X'.format(next_byte)
        elif self._mode == AddrMode.ZeroIndexedY:
            next_byte = args[0]
            res += ' ${:02X}, Y'.format(next_byte)
        elif self._mode == AddrMode.Relative:
            next_byte = args[0]
            res += ' ${:02X}'.format(next_byte)
        elif self._mode == AddrMode.ZeroIndexedIndirectX:
            next_byte = args[0]
            res += ' (${:02X}, X)'.format(next_byte)
        elif self._mode == AddrMode.AbslouteIndexedIndirectX:
            lo = args[0]
            hi = args[1]
            res += ' (${:04X}, X)'.format((hi << 8) + lo)
        elif self._mode == AddrMode.IndexedIndirectY:
            next_byte = args[0]
            res += ' (${:02X}), Y'.format(next_byte)
        elif self._mode == AddrMode.ZeroIndirect:
            next_byte = args[0]
            res += ' (${:02X})'.format(next_byte)
        elif self._mode == AddrMode.AbslouteIndirect:
            lo = args[0]
            hi = args[1]
            res += ' (${:04X})'.format((hi << 8) + lo)
        return res


class Flag:

    def __init__(self):
        self._n = False # 7
        self._v = False # 6
        # bit 5 is not used, always True
        self._b = False # 4
        self._d = False # 3
        self._i = False # 2
        self._z = False # 1
        self._c = False # 0

    def set(self, value: int):
        self.n = (value >> 7 & 1) == 1
        self.v = (value >> 6 & 1) == 1
        self.b = (value >> 4 & 1) == 1
        self.d = (value >> 3 & 1) == 1
        self.i = (value >> 2 & 1) == 1
        self.z = (value >> 1 & 1) == 1
        self.c = (value >> 0 & 1) == 1

    def get(self):
        res = 1 << 5
        if self.n:
            res |= (1 << 7)
        if self.v:
            res |= (1 << 6)
        if self.b:
            res |= (1 << 4)
        if self.d:
            res |= (1 << 3)
        if self.i:
            res |= (1 << 2)
        if self.z:
            res |= (1 << 1)
        if self.c:
            res |= (1 << 0)
        return res

    @property
    def n(self):
        return self._n

    @n.setter
    def n(self, v):
        assert isinstance(v, bool)
        self._n = v
    
    @property
    def v(self):
        return self._v

    @v.setter
    def v(self, v):
        assert isinstance(v, bool)
        self._v = v

    @property
    def b(self):
        return self._b

    @b.setter
    def b(self, v):
        assert isinstance(v, bool)
        self._b = v

    
    @property
    def d(self):
        return self._d

    @d.setter
    def d(self, v):
        assert isinstance(v, bool)
        self._d = v

    @property
    def i(self):
        return self._i

    @i.setter
    def i(self, v):
        assert isinstance(v, bool)
        self._i = v

    @property
    def z(self):
        return self._z

    @z.setter
    def z(self, v):
        assert isinstance(v, bool)
        self._z = v

    @property
    def c(self):
        return self._c

    @c.setter
    def c(self, v):
        assert isinstance(v, bool)
        self._c = v


class Register8:

    def __init__(self):
        self._value = 0

    @property
    def value(self):
        return self._value

    @value.setter
    def value(self, v):
        assert isinstance(v, int)
        assert 0 <= v < (1 << 8)
        self._value = v


class Register16:

    def __init__(self):
        self._value = 0

    @property
    def value(self):
        return self._value
    
    @value.setter
    def value(self, v):
        assert isinstance(v, int)
        assert 0 <= v < (1 << 16)
        self._value = v


class Cpu6502:

    def __init__(self, bus: Bus):
        self._ins = [
            # 0
            Instruction('BRK', AddrMode.Implied, 7, self.brk),
            Instruction('ORA', AddrMode.ZeroIndexedIndirectX, 6, self.ora),
            Instruction('KIL', AddrMode.Implied, 6, self.kil),
            Instruction('SLO', AddrMode.ZeroIndexedIndirectX, 8, self.slo),
            Instruction('NOP', AddrMode.ZeroPage, 3, self.nop),
            Instruction('ORA', AddrMode.ZeroPage, 3, self.ora),
            Instruction('ASL', AddrMode.ZeroPage, 5, self.asl),
            Instruction('SLO', AddrMode.ZeroPage, 5, self.slo),
            Instruction('PHP', AddrMode.Implied, 3, self.php),
            Instruction('ORA', AddrMode.Immediate, 2, self.ora),
            Instruction('ASL', AddrMode.Accumulator, 2, self.asl),
            Instruction('ANC', AddrMode.Immediate, 2, self.anc),
            Instruction('NOP', AddrMode.Absolute, 4, self.nop),
            Instruction('ORA', AddrMode.Absolute, 4, self.ora),
            Instruction('ASL', AddrMode.Absolute, 6, self.asl),
            Instruction('SLO', AddrMode.Absolute, 6, self.slo),
            # 1
            Instruction('BPL', AddrMode.Relative, 2, self.bpl),
            Instruction('ORA', AddrMode.IndexedIndirectY, 5, self.ora),
            Instruction('KIL', AddrMode.Implied, 6, self.kil),
            Instruction('SLO', AddrMode.IndexedIndirectY, 8, self.slo),
            Instruction('NOP', AddrMode.ZeroIndexedX, 4, self.nop),
            Instruction('ORA', AddrMode.ZeroIndexedX, 4, self.ora),
            Instruction('ASL', AddrMode.ZeroIndexedX, 6, self.asl),
            Instruction('SLO', AddrMode.ZeroIndexedX, 6, self.slo),
            Instruction('CLC', AddrMode.Implied, 2, self.clc),
            Instruction('ORA', AddrMode.AbslouteIndexedY, 4, self.ora),
            Instruction('NOP', AddrMode.Implied, 2, self.nop),
            Instruction('SLO', AddrMode.AbslouteIndexedY, 7, self.slo),
            Instruction('NOP', AddrMode.AbslouteIndexedX, 4, self.nop),
            Instruction('ORA', AddrMode.AbslouteIndexedX, 4, self.ora),
            Instruction('ASL', AddrMode.AbslouteIndexedX, 7, self.asl),
            Instruction('SLO', AddrMode.AbslouteIndexedX, 7, self.slo),
            # 2
            Instruction('JSR', AddrMode.Absolute, 6, self.jsr),
            Instruction('AND', AddrMode.ZeroIndexedIndirectX, 6, self.and_),
            Instruction('KIL', AddrMode.Implied, 6, self.kil),
            Instruction('RLA', AddrMode.ZeroIndexedIndirectX, 8, self.rla),
            Instruction('BIT', AddrMode.ZeroPage, 3, self.bit),
            Instruction('AND', AddrMode.ZeroPage, 3, self.and_),
            Instruction('ROL', AddrMode.ZeroPage, 5, self.rol),
            Instruction('RLA', AddrMode.ZeroPage, 5, self.rla),
            Instruction('PLP', AddrMode.Implied, 4, self.plp),
            Instruction('AND', AddrMode.Immediate, 2, self.and_),
            Instruction('ROL', AddrMode.Accumulator, 2, self.rol),
            Instruction('ANC', AddrMode.Immediate, 2, self.anc),
            Instruction('BIT', AddrMode.Absolute, 4, self.bit),
            Instruction('AND', AddrMode.Absolute, 4, self.and_),
            Instruction('ROL', AddrMode.Absolute, 6, self.rol),
            Instruction('RLA', AddrMode.Absolute, 6, self.rla),
            # 3
            Instruction('BMI', AddrMode.Relative, 2, self.bmi),
            Instruction('AND', AddrMode.IndexedIndirectY, 5, self.and_),
            Instruction('KIL', AddrMode.Implied, 6, self.kil),
            Instruction('RLA', AddrMode.IndexedIndirectY, 8, self.rla),
            Instruction('NOP', AddrMode.ZeroIndexedX, 4, self.nop),
            Instruction('AND', AddrMode.ZeroIndexedX, 4, self.and_),
            Instruction('ROL', AddrMode.ZeroIndexedX, 6, self.rol),
            Instruction('RLA', AddrMode.ZeroIndexedX, 6, self.rla),
            Instruction('SEC', AddrMode.Implied, 2, self.sec),
            Instruction('AND', AddrMode.AbslouteIndexedY, 4, self.and_),
            Instruction('NOP', AddrMode.Implied, 2, self.nop),
            Instruction('RLA', AddrMode.AbslouteIndexedY, 7, self.rla),
            Instruction('NOP', AddrMode.AbslouteIndexedX, 4, self.nop),
            Instruction('AND', AddrMode.AbslouteIndexedX, 4, self.and_),
            Instruction('ROL', AddrMode.AbslouteIndexedX, 7, self.rol),
            Instruction('RLA', AddrMode.AbslouteIndexedX, 7, self.rla),
            # 4
            Instruction('RTI', AddrMode.Implied, 6, self.rti),
            Instruction('EOR', AddrMode.ZeroIndexedIndirectX, 6, self.eor),
            Instruction('KIL', AddrMode.Implied, 6, self.kil),
            Instruction('SRE', AddrMode.ZeroIndexedIndirectX, 8, self.sre),
            Instruction('NOP', AddrMode.ZeroPage, 3, self.nop),
            Instruction('EOR', AddrMode.ZeroPage, 3, self.eor),
            Instruction('LSR', AddrMode.ZeroPage, 5, self.lsr),
            Instruction('SRE', AddrMode.ZeroPage, 5, self.sre),
            Instruction('PHA', AddrMode.Implied, 3, self.pha),
            Instruction('EOR', AddrMode.Immediate, 2, self.eor),
            Instruction('LSR', AddrMode.Accumulator, 2, self.lsr),
            Instruction('ALR', AddrMode.Immediate, 2, self.alr),
            Instruction('JMP', AddrMode.Absolute, 3, self.jmp),
            Instruction('EOR', AddrMode.Absolute, 4, self.eor),
            Instruction('LSR', AddrMode.Absolute, 6, self.lsr),
            Instruction('SRE', AddrMode.Absolute, 6, self.sre),
            # 5
            Instruction('BVC', AddrMode.Relative, 2, self.bvc),
            Instruction('EOR', AddrMode.IndexedIndirectY, 5, self.eor),
            Instruction('KIL', AddrMode.Implied, 6, self.kil),
            Instruction('SRE', AddrMode.IndexedIndirectY, 8, self.sre),
            Instruction('NOP', AddrMode.ZeroIndexedX, 4, self.nop),
            Instruction('EOR', AddrMode.ZeroIndexedX, 4, self.eor),
            Instruction('LSR', AddrMode.ZeroIndexedX, 6, self.lsr),
            Instruction('SRE', AddrMode.ZeroIndexedX, 6, self.sre),
            Instruction('CLI', AddrMode.Implied, 2, self.cli),
            Instruction('EOR', AddrMode.AbslouteIndexedY, 4, self.eor),
            Instruction('NOP', AddrMode.Implied, 2, self.nop),
            Instruction('SRE', AddrMode.AbslouteIndexedY, 7, self.sre),
            Instruction('NOP', AddrMode.AbslouteIndexedX, 4, self.nop),
            Instruction('EOR', AddrMode.AbslouteIndexedX, 4, self.eor),
            Instruction('LSR', AddrMode.AbslouteIndexedX, 7, self.lsr),
            Instruction('SRE', AddrMode.AbslouteIndexedX, 7, self.sre),
            # 6
            Instruction('RTS', AddrMode.Implied, 6, self.rts),
            Instruction('ADC', AddrMode.ZeroIndexedIndirectX, 6, self.adc),
            Instruction('KIL', AddrMode.Implied, 6, self.kil),
            Instruction('RRA', AddrMode.ZeroIndexedIndirectX, 8, self.rra),
            Instruction('NOP', AddrMode.ZeroPage, 3, self.nop),
            Instruction('ADC', AddrMode.ZeroPage, 3, self.adc),
            Instruction('ROR', AddrMode.ZeroPage, 5, self.ror),
            Instruction('RRA', AddrMode.ZeroPage, 5, self.rra),
            Instruction('PLA', AddrMode.Implied, 4, self.pla),
            Instruction('ADC', AddrMode.Immediate, 2, self.adc),
            Instruction('ROR', AddrMode.Accumulator, 2, self.ror),
            Instruction('ARR', AddrMode.Immediate, 2, self.arr),
            Instruction('JMP', AddrMode.AbslouteIndirect, 5, self.jmp),
            Instruction('ADC', AddrMode.Absolute, 4, self.adc),
            Instruction('ROR', AddrMode.Absolute, 6, self.ror),
            Instruction('RRA', AddrMode.Absolute, 6, self.rra),
            # 7
            Instruction('BVS', AddrMode.Relative, 2, self.bvs),
            Instruction('ADC', AddrMode.IndexedIndirectY, 5, self.adc),
            Instruction('KIL', AddrMode.Implied, 6, self.kil),
            Instruction('RRA', AddrMode.IndexedIndirectY, 8, self.rra),
            Instruction('NOP', AddrMode.ZeroIndexedX, 4, self.nop),
            Instruction('ADC', AddrMode.ZeroIndexedX, 4, self.adc),
            Instruction('ROR', AddrMode.ZeroIndexedX, 6, self.ror),
            Instruction('RRA', AddrMode.ZeroIndexedX, 6, self.rra),
            Instruction('SEI', AddrMode.Implied, 2, self.sei),
            Instruction('ADC', AddrMode.AbslouteIndexedY, 4, self.adc),
            Instruction('NOP', AddrMode.Implied, 2, self.nop),
            Instruction('RRA', AddrMode.AbslouteIndexedY, 7, self.rra),
            Instruction('NOP', AddrMode.AbslouteIndexedX, 4, self.nop),
            Instruction('ADC', AddrMode.AbslouteIndexedX, 4, self.adc),
            Instruction('ROR', AddrMode.AbslouteIndexedX, 7, self.ror),
            Instruction('RRA', AddrMode.AbslouteIndexedX, 7, self.rra),
            # 8
            Instruction('NOP', AddrMode.Immediate, 2, self.nop),
            Instruction('STA', AddrMode.ZeroIndexedIndirectX, 6, self.sta),
            Instruction('NOP', AddrMode.Immediate, 2, self.nop),
            Instruction('SAX', AddrMode.ZeroIndexedIndirectX, 6, self.sax),
            Instruction('STY', AddrMode.ZeroPage, 3, self.sty),
            Instruction('STA', AddrMode.ZeroPage, 3, self.sta),
            Instruction('STX', AddrMode.ZeroPage, 3, self.stx),
            Instruction('SAX', AddrMode.ZeroPage, 3, self.sax),
            Instruction('DEY', AddrMode.Implied, 2, self.dey),
            Instruction('NOP', AddrMode.Immediate, 2, self.nop),
            Instruction('TXA', AddrMode.Implied, 2, self.txa),
            Instruction('XAA', AddrMode.Immediate, 2, self.xaa),
            Instruction('STY', AddrMode.Absolute, 4, self.sty),
            Instruction('STA', AddrMode.Absolute, 4, self.sta),
            Instruction('STX', AddrMode.Absolute, 4, self.stx),
            Instruction('SAX', AddrMode.Absolute, 4, self.sax),
            # 9
            Instruction('BCC', AddrMode.Relative, 2, self.bcc),
            Instruction('STA', AddrMode.IndexedIndirectY, 6, self.sta),
            Instruction('KIL', AddrMode.Implied, 6, self.kil),
            Instruction('AHX', AddrMode.IndexedIndirectY, 6, self.ahx),
            Instruction('STY', AddrMode.ZeroIndexedX, 4, self.sty),
            Instruction('STA', AddrMode.ZeroIndexedX, 4, self.sta),
            Instruction('STX', AddrMode.ZeroIndexedY, 4, self.stx),
            Instruction('SAX', AddrMode.ZeroIndexedY, 4, self.sax),
            Instruction('TYA', AddrMode.Implied, 2, self.tya),
            Instruction('STA', AddrMode.AbslouteIndexedY, 5, self.sta),
            Instruction('TXS', AddrMode.Implied, 2, self.txs),
            Instruction('TAS', AddrMode.AbslouteIndexedY, 5, self.tas),
            Instruction('SHY', AddrMode.AbslouteIndexedX, 5, self.shy),
            Instruction('STA', AddrMode.AbslouteIndexedX, 5, self.sta),
            Instruction('SHX', AddrMode.AbslouteIndexedY, 5, self.shx),
            Instruction('AHX', AddrMode.AbslouteIndexedY, 5, self.ahx),
            # A
            Instruction('LDY', AddrMode.Immediate, 2, self.ldy),
            Instruction('LDA', AddrMode.ZeroIndexedIndirectX, 6, self.lda),
            Instruction('LDX', AddrMode.Immediate, 2, self.ldx),
            Instruction('LAX', AddrMode.ZeroIndexedIndirectX, 6, self.lax),
            Instruction('LDY', AddrMode.ZeroPage, 3, self.ldy),
            Instruction('LDA', AddrMode.ZeroPage, 3, self.lda),
            Instruction('LDX', AddrMode.ZeroPage, 3, self.ldx),
            Instruction('LAX', AddrMode.ZeroPage, 3, self.lax),
            Instruction('TAY', AddrMode.Implied, 2, self.tay),
            Instruction('LDA', AddrMode.Immediate, 2, self.lda),
            Instruction('TAX', AddrMode.Implied, 2, self.tax),
            Instruction('LAX', AddrMode.Immediate, 2, self.lax),
            Instruction('LDY', AddrMode.Absolute, 4, self.ldy),
            Instruction('LDA', AddrMode.Absolute, 4, self.lda),
            Instruction('LDX', AddrMode.Absolute, 4, self.ldx),
            Instruction('LAX', AddrMode.Absolute, 4, self.lax),
            # B
            Instruction('BCS', AddrMode.Relative, 2, self.bcs),
            Instruction('LDA', AddrMode.IndexedIndirectY, 5, self.lda),
            Instruction('KIL', AddrMode.Implied, 6, self.kil),
            Instruction('LAX', AddrMode.IndexedIndirectY, 5, self.lax),
            Instruction('LDY', AddrMode.ZeroIndexedX, 4, self.ldy),
            Instruction('LDA', AddrMode.ZeroIndexedX, 4, self.lda),
            Instruction('LDX', AddrMode.ZeroIndexedY, 4, self.ldx),
            Instruction('LAX', AddrMode.ZeroIndexedY, 4, self.lax),
            Instruction('CLV', AddrMode.Implied, 2, self.clv),
            Instruction('LDA', AddrMode.AbslouteIndexedY, 4, self.lda),
            Instruction('TSX', AddrMode.Implied, 2, self.tsx),
            Instruction('LAS', AddrMode.AbslouteIndexedY, 4, self.las),
            Instruction('LDY', AddrMode.AbslouteIndexedX, 4, self.ldy),
            Instruction('LDA', AddrMode.AbslouteIndexedX, 4, self.lda),
            Instruction('LDX', AddrMode.AbslouteIndexedY, 4, self.ldx),
            Instruction('LAX', AddrMode.AbslouteIndexedY, 4, self.lax),
            # C
            Instruction('CPY', AddrMode.Immediate, 2, self.cpy),
            Instruction('CMP', AddrMode.ZeroIndexedIndirectX, 6, self.cmp),
            Instruction('NOP', AddrMode.Immediate, 2, self.nop),
            Instruction('DCP', AddrMode.ZeroIndexedIndirectX, 8, self.dcp),
            Instruction('CPY', AddrMode.ZeroPage, 3, self.cpy),
            Instruction('CMP', AddrMode.ZeroPage, 3, self.cmp),
            Instruction('DEC', AddrMode.ZeroPage, 5, self.dec),
            Instruction('DCP', AddrMode.ZeroPage, 5, self.dcp),
            Instruction('INY', AddrMode.Implied, 2, self.iny),
            Instruction('CMP', AddrMode.Immediate, 2, self.cmp),
            Instruction('DEX', AddrMode.Implied, 2, self.dex),
            Instruction('AXS', AddrMode.Immediate, 2, self.axs),
            Instruction('CPY', AddrMode.Absolute, 4, self.cpy),
            Instruction('CMP', AddrMode.Absolute, 4, self.cmp),
            Instruction('DEC', AddrMode.Absolute, 6, self.dec),
            Instruction('DCP', AddrMode.Absolute, 6, self.dcp),
            # D
            Instruction('BNE', AddrMode.Relative, 2, self.bne),
            Instruction('CMP', AddrMode.IndexedIndirectY, 5, self.cmp),
            Instruction('KIL', AddrMode.Implied, 6, self.kil),
            Instruction('DCP', AddrMode.IndexedIndirectY, 8, self.dcp),
            Instruction('NOP', AddrMode.ZeroIndexedX, 4, self.nop),
            Instruction('CMP', AddrMode.ZeroIndexedX, 4, self.cmp),
            Instruction('DEC', AddrMode.ZeroIndexedX, 6, self.dec),
            Instruction('DCP', AddrMode.ZeroIndexedX, 6, self.dcp),
            Instruction('CLD', AddrMode.Implied, 2, self.cld),
            Instruction('CMP', AddrMode.AbslouteIndexedY, 4, self.cmp),
            Instruction('NOP', AddrMode.Implied, 2, self.nop),
            Instruction('DCP', AddrMode.AbslouteIndexedY, 7, self.dcp),
            Instruction('NOP', AddrMode.AbslouteIndexedX, 4, self.nop),
            Instruction('CMP', AddrMode.AbslouteIndexedX, 4, self.cmp),
            Instruction('DEC', AddrMode.AbslouteIndexedX, 7, self.dec),
            Instruction('DCP', AddrMode.AbslouteIndexedX, 7, self.dcp),
            # E
            Instruction('CPX', AddrMode.Immediate, 2, self.cpx),
            Instruction('SBC', AddrMode.ZeroIndexedIndirectX, 6, self.sbc),
            Instruction('NOP', AddrMode.Immediate, 2, self.nop),
            Instruction('ISC', AddrMode.ZeroIndexedIndirectX, 8, self.isc),
            Instruction('CPX', AddrMode.ZeroPage, 3, self.cpx),
            Instruction('SBC', AddrMode.ZeroPage, 3, self.sbc),
            Instruction('INC', AddrMode.ZeroPage, 5, self.inc),
            Instruction('ISC', AddrMode.ZeroPage, 5, self.isc),
            Instruction('INX', AddrMode.Implied, 2, self.inx),
            Instruction('SBC', AddrMode.Immediate, 2, self.sbc),
            Instruction('NOP', AddrMode.Implied, 2, self.nop),
            Instruction('SBC', AddrMode.Immediate, 2, self.sbc),
            Instruction('CPX', AddrMode.Absolute, 4, self.cpx),
            Instruction('SBC', AddrMode.Absolute, 4, self.sbc),
            Instruction('INC', AddrMode.Absolute, 6, self.inc),
            Instruction('ISC', AddrMode.Absolute, 6, self.isc),
            # F
            Instruction('BEQ', AddrMode.Relative, 2, self.beq),
            Instruction('SBC', AddrMode.IndexedIndirectY, 5, self.sbc),
            Instruction('KIL', AddrMode.Implied, 6, self.kil),
            Instruction('ISC', AddrMode.IndexedIndirectY, 8, self.isc),
            Instruction('NOP', AddrMode.ZeroIndexedX, 4, self.nop),
            Instruction('SBC', AddrMode.ZeroIndexedX, 4, self.sbc),
            Instruction('INC', AddrMode.ZeroIndexedX, 6, self.inc),
            Instruction('ISC', AddrMode.ZeroIndexedX, 6, self.isc),
            Instruction('SED', AddrMode.Implied, 2, self.sed),
            Instruction('SBC', AddrMode.AbslouteIndexedY, 4, self.sbc),
            Instruction('NOP', AddrMode.Implied, 2, self.nop),
            Instruction('ISC', AddrMode.AbslouteIndexedY, 7, self.isc),
            Instruction('NOP', AddrMode.AbslouteIndexedX, 4, self.nop),
            Instruction('SBC', AddrMode.AbslouteIndexedX, 4, self.sbc),
            Instruction('INC', AddrMode.AbslouteIndexedX, 7, self.inc),
            Instruction('ISC', AddrMode.AbslouteIndexedX, 7, self.isc),
        ]
        self._bus = bus
        self._pc = Register16()
        self._sp = Register8()
        self._flag = Flag()
        self._a = Register8()
        self._x = Register8()
        self._y = Register8()

        self._now_cycle = 0
        self._addr = 0
        self._data = 0
        self._next_addr = 0

        self._nmi_set = False

    def reset(self):
        lo = self._bus.read(0xfffc)
        hi = self._bus.read(0xfffd)
        self._pc.value = (hi << 8) + lo
        self._now_cycle = 7 # TODO: need to check how many cycles are needed
        self._sp.value = 0xff
        self._push(hi)
        self._push(lo)
        self._flag.i = True
        self._nmi_set = False
        
    def test_mode(self):
        self._pc.value = 0xc000
        self._sp.value = 0xfd
        self._now_cycle = 7
        self._flag.i = True
        self._nmi_set = False

    def pre_fill(self, read_data=True):
        opcode = self._bus.read(self._pc.value)
        ins = self._ins[opcode]
        mode = ins.addr_mode()
        cross_boundry = False
        if mode == AddrMode.Implied:
            self._addr = -1
            self._data = -1
        elif mode == AddrMode.Absolute:
            lo = self.fetch(1)
            hi = self.fetch(2)
            self._addr = u16((hi << 8) + lo)
            if read_data:
                self._data = self._bus.read(self._addr)
        elif mode == AddrMode.Accumulator:
            self._addr = -1
            self._data = self._a.value
        elif mode == AddrMode.Immediate:
            self._addr = -1
            self._data = self.fetch(1)
        elif mode == AddrMode.ZeroPage:
            self._addr = self.fetch(1)
            if read_data:
                self._data = self._bus.read(self._addr)
        elif mode == AddrMode.Relative:
            self._addr = -1
            self._data = self.fetch(1)
            prev_ = self._next_addr
            next_ = self._next_addr + s8(self._data)
            if (prev_ & 0xff00) != (next_ & 0xff00):
                cross_boundry = True
        elif mode == AddrMode.IndexedIndirectY:
            addr = self.fetch(1)
            lo = self._bus.read(addr)
            hi = self._bus.read((addr + 1) % 256)
            self._addr = u16((hi << 8) + lo + self._y.value)
            if read_data:
                self._data = self._bus.read(self._addr)
            cross_boundry = (lo + self._y.value) > 0xff
        elif mode == AddrMode.ZeroIndexedIndirectX:
            index = u8(self.fetch(1) + self._x.value)
            self._addr = u16(self._bus.read(index) + ((self._bus.read((index + 1) & 0xff)) << 8))
            if read_data:
                self._data = self._bus.read(self._addr)
        elif mode == AddrMode.AbslouteIndirect:
            addr = self.fetch(1) + (self.fetch(2) << 8)
            if (addr & 0xff) == 0xff:
                self._addr = self._bus.read(addr) + (self._bus.read(addr & 0xff00) << 8)
            else: 
                self._addr = self._bus.read(addr) + (self._bus.read(addr + 1) << 8)
            self._data = -1
        elif mode == AddrMode.AbslouteIndexedY:
            self._addr = u16(self._y.value + self.fetch(1) + (self.fetch(2) << 8))
            if read_data:
                self._data = self._bus.read(self._addr)
            cross_boundry = (self._y.value + self.fetch(1) > 0xff)
        elif mode == AddrMode.ZeroIndexedX:
            self._addr = u8(self._x.value + self.fetch(1))
            if read_data:
                self._data = self._bus.read(self._addr)
        elif mode == AddrMode.ZeroIndexedY:
            self._addr = u8(self._y.value + self.fetch(1))
            if read_data:
                self._data = self._bus.read(self._addr)
        elif mode == AddrMode.AbslouteIndexedX:
            self._addr = u16(self._x.value + self.fetch(1) + (self.fetch(2) << 8))
            if read_data:
                self._data = self._bus.read(self._addr)
            cross_boundry = (self._x.value + self.fetch(1) > 0xff)
        else:
            assert False, 'Need to impl, {}'.format(mode)
        return cross_boundry

    def _push(self, val):
        self._bus.write(self._sp.value + 0x100, val)
        self._sp.value -= 1
    
    def _pop(self):
        self._sp.value += 1
        return self._bus.read(self._sp.value + 0x100)

    def request_nmi(self):
        self._nmi_set = True

    def log(self):
        status = {
            'PC': self._pc.value,
            'A': self._a.value,
            'X': self._x.value,
            'Y': self._y.value,
            'F': self._flag.get(),
            'SP': self._sp.value,
            'CYC': self._now_cycle
        }
        return status

    def nmi(self):
        print('NMI CALLED, addr={:04X}'.format(self._pc.value))
        self._nmi_set = False
        self._push((self._pc.value >> 8) & 0xFF)
        self._push(self._pc.value & 0xFF)
        self._push(self._flag.get() & 0b11101111)
        self._flag.i = True
        self._pc.value = ((self._bus.read(0xFFFB) << 8) | self._bus.read(0xFFFA))
        return False

    def irq(self):
        pass

    def run(self):
        pre_cycle = self._now_cycle

        if self._nmi_set:
            self.nmi()
            self._now_cycle += 7
            return self._now_cycle - pre_cycle

        #TODO: check irq && brk
        opcode = self._bus.read(self._pc.value)
        ins = self._ins[opcode]
        self._next_addr = self._pc.value + ins.length()
        cross_boundary = self.pre_fill(ins.name() not in {'STA', 'STX', 'STY'})
        branch_taken = ins.execute()
        if branch_taken is None:
            assert False
        self._pc.value += ins.pc_increment()
        self._now_cycle += ins.cycle()
        if ins.name() in {'BPL', 'BMI', 'BVC', 'BVS', 'BCC', 'BCS', 'BNE', 'BEQ'}:
            if branch_taken:
                self._now_cycle += 1
                if cross_boundary:
                    self._now_cycle += 1
        else:
            if cross_boundary and ins.name() not in {'RRA', 'STA', 'STX', 'STY', 'DCP', 'ISC', 'SLO', 'RLA', 'SRE'}:
                self._now_cycle += 1
        return self._now_cycle - pre_cycle
    
    def fetch(self, index):
        return self._bus.read(self._pc.value + index)

    def decode(self, l, r):
        res = []
        addr_item = {}
        now_addr = l
        while True:
            opcode = self._bus.read(now_addr)
            ins = self._ins[opcode]
            if now_addr + ins.length() > r:
                break
            parm = []
            for i in range(now_addr + 1, now_addr + 3):
                if i > r:
                    break
                parm.append(self._bus.read(i))
            res.append('${:04X}: {}'.format(now_addr, ins.format(*parm)))
            addr_item[now_addr] = len(res) - 1
            now_addr += ins.length()
        return (addr_item, res)

    def brk(self):
        pass

    def nop(self):
        return False

    def php(self):
        flag = self._flag.get()
        flag |= (1 << 4)
        self._push(flag)
        return False

    def bpl(self):
        if not self._flag.n:
            self._pc.value = self._pc.value + s8(self._data)
            return True
        return False

    def clc(self):
        self._flag.c = False
        return False

    def ora(self):
        self._a.value |= self._data
        self._flag.z = (self._a.value == 0)
        self._flag.n = (self._a.value >> 7 & 1) == 1
        return False

    def kil(self):
        pass

    def asl(self):
        val = u8(self._data << 1)
        if self._addr == -1:
            self._a.value = u8(self._data << 1)
        else:
            self._bus.write(self._addr, val)
        self._flag.c = (self._data >> 7 & 1) == 1
        self._flag.n = (val >> 7 & 1) == 1
        self._flag.z = (val == 0)
        return False

    def slo(self):
        v = u8(self._data * 2)
        self._bus.write(self._addr, v)
        self._a.value |= v
        self._flag.c = (self._data >> 7 & 1) == 1
        self._flag.z = (self._a.value == 0)
        self._flag.n = (self._a.value >> 7 & 1) == 1
        return False

    def anc(self):
        pass

    def jsr(self):
        push = self._next_addr - 1
        hi = (push >> 8 & 0xff)
        lo = (push & 0xff)
        self._push(hi)
        self._push(lo)
        self._pc.value = self._addr
        return False

    def bit(self):
        self._flag.n = (self._data >> 7 & 1) == 1
        self._flag.v = (self._data >> 6 & 1) == 1
        self._flag.z = (self._data & self._a.value) == 0
        return False

    def plp(self):
        self._flag.set(self._pop() & 0xef)
        return False

    def bmi(self):
        if self._flag.n:
            self._pc.value = self._pc.value + s8(self._data)
            return True
        return False

    def sec(self):
        self._flag.c = True
        return False

    def and_(self):
        self._a.value &= self._data
        self._flag.z = self._a.value == 0
        self._flag.n = (self._a.value >> 7 & 1) == 1
        return False

    def rol(self):
        new_carry = (self._data >> 7 & 1) == 1
        val = u8(self._data << 1)
        if self._flag.c:
            val |= 1
        if self._addr == -1:
            self._a.value = val
        else:
            self._bus.write(self._addr, val)
        self._flag.c = new_carry
        self._flag.z = (val == 0)
        self._flag.n = (val >> 7 & 1) == 1
        return False

    def rla(self):
        # ROL
        new_carry = (self._data >> 7 & 1) == 1
        val = u8(self._data << 1)
        if self._flag.c:
            val |= 1
        self._bus.write(self._addr, val)
        self._flag.c = new_carry
        # AND
        self._a.value &= val
        self._flag.z = (self._a.value == 0)
        self._flag.n = (self._a.value >> 7 & 1) == 1
        return False

    def rti(self):
        flag = self._pop()
        lo = self._pop()
        hi = self._pop()
        self._pc.value = (hi << 8) + lo
        self._flag.set(flag)
        print('RTI CALLED, ADDR={:04X}'.format(self._pc.value))
        return False

    def pha(self):
        self._push(self._a.value)
        return False

    def jmp(self):
        self._pc.value = self._addr
        return False

    def bvc(self):
        if not self._flag.v:
            self._pc.value = self._pc.value + s8(self._data)
            return True
        return False

    def cli(self):
        pass

    def eor(self):
        self._a.value ^= self._data
        self._flag.z = (self._a.value == 0)
        self._flag.n = (self._a.value >> 7 & 1) == 1
        return False

    def lsr(self):
        val = (self._data >> 1)
        if self._addr == -1:
            self._a.value = val
        else:
            self._bus.write(self._addr, val)
        self._flag.c = (self._data & 1) == 1
        self._flag.n = False
        self._flag.z = val == 0
        return False

    def sre(self):
        # LSR
        val = (self._data >> 1)
        self._bus.write(self._addr, val)
        self._flag.c = (self._data & 1) == 1
        # EOR
        self._a.value ^= val
        self._flag.z = (self._a.value == 0)
        self._flag.n = (self._a.value >> 7 & 1) == 1
        return False

    def alr(self):
        pass

    def rts(self):
        lo = self._pop()
        hi = self._pop()
        self._pc.value = (hi << 8) + lo
        return False

    def pla(self):
        self._a.value = self._pop()
        self._flag.z = self._a.value == 0
        self._flag.n = (self._a.value >> 7 & 1) == 1
        return False

    def bvs(self):
        if self._flag.v:
            self._pc.value = self._pc.value + s8(self._data)
            return True
        return False

    def sei(self):
        self._flag.i = True
        return False

    def adc(self):
        c = self._flag.c
        res = self._a.value + self._data + (1 if c else 0)
        self._flag.n = (u8(res) >> 7 & 1) == 1
        self._flag.z = (u8(res) == 0)
        self._flag.c = (res & 0xff00) != 0
        ah = (self._a.value >> 7) & 1
        dh = (self._data >> 7) & 1
        rh = (u8(res) >> 7 & 1)
        self._flag.v = (ah == 0 and dh == 0 and rh == 1) or (ah == 1 and dh == 1 and rh == 0)
        self._a.value = u8(res)
        return False

    def ror(self):
        new_carry = (self._data & 1) == 1
        val = self._data >> 1
        if self._flag.c:
            val |= (1 << 7)
        if self._addr == -1:
            self._a.value = val
        else:
            self._bus.write(self._addr, val)
        self._flag.c = new_carry
        self._flag.z = (val == 0)
        self._flag.n = (val >> 7 & 1) == 1
        return False

    def rra(self):
        # ROR
        new_carry = (self._data & 1) == 1
        val = self._data >> 1
        if self._flag.c:
            val |= (1 << 7)
        self._bus.write(self._addr, val)
        # ADC
        c = new_carry
        res = self._a.value + val + (1 if c else 0)
        self._flag.n = (u8(res) >> 7 & 1) == 1
        self._flag.z = (u8(res) == 0)
        self._flag.c = (res & 0xff00) != 0
        ah = (self._a.value >> 7) & 1
        dh = (val >> 7) & 1
        rh = (u8(res) >> 7 & 1)
        self._flag.v = (ah == 0 and dh == 0 and rh == 1) or (ah == 1 and dh == 1 and rh == 0)
        self._a.value = u8(res)
        return True

    def arr(self):
        pass

    def sty(self):
        self._bus.write(self._addr, self._y.value)
        return False

    def dey(self):
        self._y.value = u8(self._y.value - 1)
        self._flag.z = (self._y.value == 0)
        self._flag.n = (self._y.value >> 7 & 1) == 1
        return False

    def bcc(self):
        if not self._flag.c:
            self._pc.value = self._pc.value + s8(self._data)
            return True
        return False

    def tya(self):
        self._a.value = self._y.value
        self._flag.n = (self._a.value >> 7 & 1) == 1
        self._flag.z = (self._a.value == 0)
        return False

    def shy(self):
        pass

    def sta(self):
        self._bus.write(self._addr, self._a.value)
        return False

    def stx(self):
        self._bus.write(self._addr, self._x.value)
        return False

    def txa(self):
        self._a.value = self._x.value
        self._flag.n = (self._a.value >> 7 & 1) == 1
        self._flag.z = (self._a.value == 0)
        return False

    def txs(self):
        self._sp.value = self._x.value
        return False

    def shx(self):
        pass

    def sax(self):
        self._bus.write(self._addr, self._a.value & self._x.value)
        return False

    def xaa(self):
        pass

    def ahx(self):
        pass

    def tas(self):
        pass

    def ldy(self):
        self._y.value = self._data
        self._flag.n = (self._data >> 7 & 1) == 1
        self._flag.z = self._data == 0
        return False

    def tay(self):
        self._y.value = self._a.value
        self._flag.n = (self._y.value >> 7 & 1) == 1
        self._flag.z = (self._y.value == 0)
        return False

    def bcs(self):
        if self._flag.c:
            self._pc.value = self._pc.value + s8(self._data)
            return True
        return False

    def clv(self):
        self._flag.v = False
        return False

    def lda(self):
        self._a.value = self._data
        self._flag.n = (self._data >> 7 & 1) == 1
        self._flag.z = self._data == 0
        return False

    def ldx(self):
        self._x.value = self._data
        self._flag.n = (self._data >> 7 & 1) == 1
        self._flag.z = self._data == 0
        return False

    def tax(self):
        self._x.value = self._a.value
        self._flag.n = (self._x.value >> 7 & 1) == 1
        self._flag.z = (self._x.value == 0)
        return False

    def tsx(self):
        self._x.value = self._sp.value
        self._flag.n = (self._x.value >> 7 & 1) == 1
        self._flag.z = (self._x.value == 0)
        return False

    def lax(self):
        self._a.value = self._data
        self._x.value = self._data
        self._flag.z = (self._a.value == 0)
        self._flag.n = (self._a.value >> 7 & 1) == 1
        return False

    def las(self):
        pass

    def cpy(self):
        value = self._y.value - self._data
        self._flag.z = (u8(value) == 0)
        self._flag.n = (u8(value) >> 7 & 1) == 1
        self._flag.c = (self._y.value >= self._data)
        return False

    def iny(self):
        self._y.value = u8(self._y.value + 1)
        self._flag.z = (self._y.value == 0)
        self._flag.n = (self._y.value >> 7 & 1) == 1
        return False

    def bne(self):
        if not self._flag.z:
            self._pc.value = self._pc.value + s8(self._data)
            return True
        return False

    def cld(self):
        self._flag.d = False
        return False

    def cmp(self):
        value = self._a.value - self._data
        self._flag.z = (u8(value) == 0)
        self._flag.n = (u8(value) >> 7 & 1) == 1
        self._flag.c = (self._a.value >= self._data)
        return False

    def dec(self):
        val = u8(self._data - 1)
        self._bus.write(self._addr, val)
        self._flag.n = (val >> 7 & 1) == 1
        self._flag.z = (val == 0)
        return False

    def dex(self):
        self._x.value = u8(self._x.value - 1)
        self._flag.z = (self._x.value == 0)
        self._flag.n = (self._x.value >> 7 & 1) == 1
        return False

    def dcp(self):
        v = u8(self._data - 1)
        self._bus.write(self._addr, v)
        tmp = u8(self._a.value - v)
        self._flag.z = (tmp == 0)
        self._flag.n = (tmp >> 7 & 1) == 1
        self._flag.c = ((self._a.value - v) & 0xff00) == 0
        return False

    def axs(self):
        pass

    def cpx(self):
        value = self._x.value - self._data
        self._flag.z = (u8(value) == 0)
        self._flag.n = (u8(value) >> 7 & 1) == 1
        self._flag.c = (self._x.value >= self._data)
        return False

    def inx(self):
        self._x.value = u8(self._x.value + 1)
        self._flag.z = (self._x.value == 0)
        self._flag.n = (self._x.value >> 7 & 1) == 1
        return False

    def beq(self):
        if self._flag.z:
            self._pc.value = self._pc.value + s8(self._data)
            return True
        return False

    def sed(self):
        self._flag.d = True
        return False

    def sbc(self):
        c = self._flag.c
        res = self._a.value - self._data - (0 if c else 1)
        self._flag.n = (u8(res) >> 7 & 1) == 1
        self._flag.z = u8(res) == 0
        self._flag.c = (res & 0xff00) == 0
        ah = self._a.value >> 7 & 1
        mh = self._data >> 7 & 1
        rh = u8(res) >> 7 & 1
        self._flag.v = (ah == 1 and mh == 0 and rh == 0) or (ah == 0 and mh == 1 and rh == 1)
        self._a.value = u8(res)
        return False

    def inc(self):
        val = u8(1 + self._data)
        self._bus.write(self._addr, val)
        self._flag.z = (val == 0)
        self._flag.n = (val >> 7 & 1) == 1
        return False

    def isc(self):
        v = u8(self._data + 1)
        tmp = self._a.value - v - (0 if self._flag.c else 1)
        self._bus.write(self._addr, v)
        self._flag.z = (self._a.value == 0)
        self._flag.n = (self._a.value >> 7 & 1) == 1
        self._flag.c = (tmp & 0xff00) == 0
        ah = (self._a.value >> 7 & 1)
        mh = (v >> 7 & 1)
        rh = (u8(tmp) >> 7 & 1)
        self._flag.v = (ah == 0 and mh == 1 and rh == 1) or (ah == 1 and mh == 0 and rh == 0) 
        self._a.value = u8(tmp)
        return False
