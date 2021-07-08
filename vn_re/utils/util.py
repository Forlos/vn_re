def chunks(lst, n):
    """Yield successive n-sized chunks from lst."""
    for i in range(0, len(lst), n):
        yield lst[i : i + n]


def wrapping_sub(a, b):
    v = (a - b) & 0xFFFF_FFFF
    if v < 0:
        v = 0xFFFF_FFFF + v + 1
    return v


def wrapping_add(a, b):
    return (a + b) & 0xFFFF_FFFF


def wrapping_mul(a, b):
    return (a * b) & 0xFFFF_FFFF


def wrapping_shl(a, bits):
    return (a << bits) & 0xFFFF_FFFF


def wrapping_add8(a, b):
    return (a + b) & 0xFF


def wrapping_add16(a, b):
    return (a + b) & 0xFFFF


def wrapping_sub8(a, b):
    v = (a - b) & 0xFF
    if v < 0:
        v = 0xFF + v + 1
    return v


ror = lambda val, r_bits, max_bits: (
    (val & (2 ** max_bits - 1)) >> r_bits % max_bits
) | (val << (max_bits - (r_bits % max_bits)) & (2 ** max_bits - 1))

rol = lambda val, r_bits, max_bits: (val << r_bits % max_bits) & (2 ** max_bits - 1) | (
    (val & (2 ** max_bits - 1)) >> (max_bits - (r_bits % max_bits))
)
