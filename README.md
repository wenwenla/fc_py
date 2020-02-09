# 参考资料
1. [指令表格](http://www.oxyron.de/html/opcodes02.html)
2. [指令详解](https://wusiyu.me/6502-cpu%E6%B1%87%E7%BC%96%E8%AF%AD%E8%A8%80%E6%8C%87%E4%BB%A4%E9%9B%86/)
3. [TEST ROM](https://wiki.nesdev.com/w/index.php/Emulator_tests)
4. [非常详细的指令](http://www.6502.org/tutorials/6502opcodes.html)

## 花了一些额外的debug时间

|Instruction|	Bits 5 and 4|	Side effects after pushing|
|:----:|:----:|:----:|
|PHP|11|None|
|BRK|11|I is set to 1|
|/IRQ|10|I is set to 1|
|/NMI|10|I is set to 1|

CYC1992:
- 注意stack的起始地址是**0x100**，但是sp $\in$ [0x00, 0xff].

CYC2029:
- 注意push下一条指令地址 -1