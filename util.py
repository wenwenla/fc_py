
def u8(x):
    return x % 256

def s8(x):
    x = x % 256
    if 0 <= x <= 127:
        return x
    return x - 256


def u16(x):
    return x % 65536