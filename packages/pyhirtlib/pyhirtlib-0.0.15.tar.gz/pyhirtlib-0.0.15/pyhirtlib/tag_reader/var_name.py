def getMmr3HashFromInt(integer: int) -> str:
    unsigned_integer = integer
    if integer < 0:
        unsigned_integer = integer + 2 ** 32

    bytes_val = unsigned_integer.to_bytes(4, 'little')
    return bytes_val.hex().upper()