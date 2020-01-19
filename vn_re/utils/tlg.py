import sys
import array

from PIL import Image

from vn_re.formats.tlg0 import Tlg0
from vn_re.formats.tlg5 import Tlg5
from vn_re.formats.tlg6 import Tlg6

TLG0_MAGIC = b"TLG0.0\x00sds\x1a"
TLG5_MAGIC = b"TLG5.0\x00raw\x1A"
TLG6_MAGIC = b"TLG6.0\x00raw\x1A"

TVP_TLG6_GOLOMB_N_COUNT = 4
W_BLOCK_SIZE = 8
H_BLOCK_SIZE = 8

LEADING_ZERO_TABLE_BITS = 12
LEADING_ZERO_TABLE_SIZE = 1 << LEADING_ZERO_TABLE_BITS

LEADING_ZERO_TABLE = list(bytes(LEADING_ZERO_TABLE_SIZE))
GOLOMB_BIT_LENGTH_TABLE = list(
    [
        list(bytes(TVP_TLG6_GOLOMB_N_COUNT))
        for _ in range(TVP_TLG6_GOLOMB_N_COUNT * 2 * 128)
    ]
)

TRANSFORMERS = [
    lambda r, g, b: ((r) & 0xFF, (g) & 0xFF, (b) & 0xFF),
    lambda r, g, b: ((r + g) & 0xFF, (g) & 0xFF, (b + g) & 0xFF),
    lambda r, g, b: ((r + g + b) & 0xFF, (g + b) & 0xFF, (b) & 0xFF),
    lambda r, g, b: ((r) & 0xFF, (g + r) & 0xFF, (b + r + g) & 0xFF),
    lambda r, g, b: ((r + r + g + b) & 0xFF, (g + b + r) & 0xFF, (b + r) & 0xFF),
    lambda r, g, b: ((r) & 0xFF, (g + b + r) & 0xFF, (b + r) & 0xFF),
    lambda r, g, b: ((r) & 0xFF, (g) & 0xFF, (b + g) & 0xFF),
    lambda r, g, b: ((r) & 0xFF, (g + b) & 0xFF, (b) & 0xFF),
    lambda r, g, b: ((r + g) & 0xFF, (g) & 0xFF, (b) & 0xFF),
    lambda r, g, b: ((r + b) & 0xFF, (g + r + b) & 0xFF, (b + r + b + g) & 0xFF),
    lambda r, g, b: ((r) & 0xFF, (g + r) & 0xFF, (b + r) & 0xFF),
    lambda r, g, b: ((r + b) & 0xFF, (g + b) & 0xFF, (b) & 0xFF),
    lambda r, g, b: ((r + b) & 0xFF, (g + r + b) & 0xFF, (b) & 0xFF),
    lambda r, g, b: ((r + b + g) & 0xFF, (g + r + b + g) & 0xFF, (b + g) & 0xFF),
    lambda r, g, b: ((r + b + g + r) & 0xFF, (g + r) & 0xFF, (b + g + r) & 0xFF),
    lambda r, g, b: ((r + (b << 1)) & 0xFF, (g + (b << 1)) & 0xFF, (b) & 0xFF),
]


def _init_table():
    golomb_compression_table = [
        [3, 7, 15, 27, 63, 108, 223, 448, 130],
        [3, 5, 13, 24, 51, 95, 192, 384, 257],
        [2, 5, 12, 21, 39, 86, 155, 320, 384],
        [2, 3, 9, 18, 33, 61, 129, 258, 511],
    ]
    for i in range(LEADING_ZERO_TABLE_SIZE):
        count = 0
        j = 1
        while j != LEADING_ZERO_TABLE_SIZE and not (i & j):
            j <<= 1
            count += 1
        count += 1
        if j == LEADING_ZERO_TABLE_SIZE:
            count = 0

        LEADING_ZERO_TABLE[i] = count

    for n in range(TVP_TLG6_GOLOMB_N_COUNT):
        a = 0
        for i in range(9):
            for j in range(golomb_compression_table[n][i]):
                GOLOMB_BIT_LENGTH_TABLE[a][n] = i
                a += 1


def _lzss_decompress(
    state: bytearray, input_buf: bytearray, input_size: int, output_buf: bytearray,
) -> bytearray:
    output_buff_index = 0
    state_offset = 0
    flags = 0
    i = 0

    while i < input_size:
        flags >>= 1
        if (flags & 0x100) != 0x100:
            flags = input_buf[i] | 0xFF00
            i += 1
        if (flags & 1) == 1:
            x0 = input_buf[i]
            i += 1
            x1 = input_buf[i]
            i += 1
            position = x0 | ((x1 & 0xF) << 8)
            length = 3 + ((x1 & 0xF0) >> 4)
            if length == 18:
                length += input_buf[i]
                i += 1
            for j in range(length):
                c = state[position]
                output_buf[output_buff_index] = c
                output_buff_index += 1
                state[state_offset] = c
                state_offset += 1
                state_offset &= 0xFFF
                position += 1
                position &= 0xFFF
        else:
            c = input_buf[i]
            i += 1
            output_buf[output_buff_index] = c
            output_buff_index += 1
            state[state_offset] = c
            state_offset += 1
            state_offset &= 0xFFF

    return output_buf


def _decompress_filter_types(
    filter_types: bytearray, header: Tlg6.Tlg6Header
) -> bytearray:
    output = bytearray(header.x_block_count * header.y_block_count)
    state = bytearray(4096)
    state_index = 0
    for i in range(32):
        for j in range(16):
            for _ in range(4):
                state[state_index] = i
                state_index += 1
            for _ in range(4):
                state[state_index] = j
                state_index += 1

    _lzss_decompress(state, filter_types, len(filter_types), output)
    return output


def _decode_golomb(
    pixel_buf: bytearray, start_index, pixel_count: int, bit_pool: bytearray
) -> None:
    bit_pool_index = 0
    pixel_buf_index = start_index
    n = TVP_TLG6_GOLOMB_N_COUNT - 1
    a = 0

    bit_pos = 1
    zero = bit_pool[0] & 1 == 0
    while pixel_buf_index < pixel_count * 4:
        count = 0
        t = (
            int.from_bytes(bit_pool[bit_pool_index : bit_pool_index + 4], "little")
            >> bit_pos
        )
        b = LEADING_ZERO_TABLE[t & (LEADING_ZERO_TABLE_SIZE - 1)]
        bit_count = b
        while not b:
            bit_count += LEADING_ZERO_TABLE_BITS
            bit_pos += LEADING_ZERO_TABLE_BITS
            bit_pool_index += bit_pos >> 3
            bit_pos &= 7
            t = (
                int.from_bytes(bit_pool[bit_pool_index : bit_pool_index + 4], "little")
                >> bit_pos
            )
            b = LEADING_ZERO_TABLE[t & (LEADING_ZERO_TABLE_SIZE - 1)]
            bit_count += b

        bit_pos += b
        bit_pool_index += bit_pos >> 3
        bit_pos &= 7

        bit_count -= 1
        count = 1 << bit_count
        t = int.from_bytes(bit_pool[bit_pool_index : bit_pool_index + 4], "little")
        count += (t >> bit_pos) & (count - 1)

        bit_pos += bit_count
        bit_pool_index += bit_pos >> 3
        bit_pos &= 7

        if zero:
            while True:
                pixel_buf[pixel_buf_index] = 0
                pixel_buf_index += 4

                count -= 1
                if count <= 0:
                    break
        else:
            while True:

                bit_count = 0
                b = 0
                t = (
                    int.from_bytes(
                        bit_pool[bit_pool_index : bit_pool_index + 4], "little"
                    )
                    >> bit_pos
                )
                if t:
                    b = LEADING_ZERO_TABLE[t & (LEADING_ZERO_TABLE_SIZE - 1)]
                    bit_count = b
                    while not b:
                        bit_count += LEADING_ZERO_TABLE_BITS
                        bit_pos += LEADING_ZERO_TABLE_BITS
                        bit_pool_index += bit_pos >> 3
                        bit_pos &= 7
                        t = (
                            int.from_bytes(
                                bit_pool[bit_pool_index : bit_pool_index + 4], "little"
                            )
                            >> bit_pos
                        )
                        b = LEADING_ZERO_TABLE[t & (LEADING_ZERO_TABLE_SIZE - 1)]
                        bit_count += b
                    bit_count -= 1
                else:
                    bit_pool_index += 5
                    bit_count = bit_pool[bit_pool_index - 1]
                    bit_pos = 0
                    t = int.from_bytes(
                        bit_pool[bit_pool_index : bit_pool_index + 4], "little"
                    )
                    b = 0

                k = GOLOMB_BIT_LENGTH_TABLE[a][n]
                v = (bit_count << k) + ((t >> b) & ((1 << k) - 1))
                sign = (v & 1) - 1
                v >>= 1
                a += v
                pixel_buf[pixel_buf_index] = ((v ^ sign) + sign + 1) & 0xFF
                pixel_buf_index += 4

                bit_pos += b
                bit_pos += k
                bit_pool_index += bit_pos >> 3
                bit_pos &= 7

                n -= 1
                if n < 0:
                    a >>= 1
                    n = TVP_TLG6_GOLOMB_N_COUNT - 1

                count -= 1
                if count <= 0:
                    break

        zero = not zero


def _gt_mask(a: int, b: int) -> int:
    x = ~b
    y = ((a & x) + (((a ^ x) >> 1) & 0x7F7F7F7F)) & 0x80808080
    return ((y >> 7) + 0x7F7F7F7F) ^ 0x7F7F7F7F


def _packed_bytes_add(a: int, b: int) -> int:
    return a + b - ((((a & b) << 1) + ((a ^ b) & 0xFEFEFEFE)) & 0x01010100)


def _med(a: int, b: int, c: int, v: int) -> int:
    mask = _gt_mask(a, b)
    ab = (a ^ b) & mask
    aa = ab ^ a
    bb = ab ^ b
    a_mask = _gt_mask(aa, c)
    b_mask = _gt_mask(c, bb)
    m = ~(a_mask | b_mask)
    return (
        _packed_bytes_add(
            (b_mask & aa) | (a_mask & bb) | ((bb & m) - (c & m) + (aa & m)), v
        )
        & 0xFFFFFFFF
    )


def _avg(a: int, b: int, c: int, v: int) -> int:
    return (
        _packed_bytes_add(
            (a & b) + (((a ^ b) & 0xFEFEFEFE) >> 1) + ((a ^ b) & 0x01010101), v
        )
        & 0xFFFFFFFF
    )


def _decode_line(
    prev_line: array.array,
    cur_line: array.array,
    width: int,
    start_block: int,
    block_limit: int,
    filter_types: bytearray,
    skip_block_bytes: int,
    input_buf: bytearray,
    initialp: int,
    odd_skip: int,
    dir: int,
    channel_count: int,
):
    p = 0
    up = 0
    step = 0
    i = 0

    prev_line_index = 0
    cur_line_index = 0
    input_buf_index = 0

    if start_block:
        prev_line_index += start_block * W_BLOCK_SIZE
        cur_line_index += start_block * W_BLOCK_SIZE
        up = prev_line[prev_line_index - 1]
        p = cur_line[cur_line_index - 1]
    else:
        p = up = initialp

    input_buf_index += (skip_block_bytes * start_block) * 4
    step = 1 if (dir & 1) else -1

    for i in range(start_block, block_limit):
        w = width - i * W_BLOCK_SIZE
        if w > W_BLOCK_SIZE:
            w = W_BLOCK_SIZE

        ww = w
        if step == -1:
            input_buf_index += (ww - 1) * 4
        if i & 1:
            input_buf_index += (odd_skip * ww) * 4

        filter_fn = _avg if (filter_types[i] & 1) else _med
        transformer_fn = TRANSFORMERS[filter_types[i] >> 1]

        while True:
            a = input_buf[input_buf_index + 3]
            r = input_buf[input_buf_index + 2]
            g = input_buf[input_buf_index + 1]
            b = input_buf[input_buf_index]

            r, g, b = transformer_fn(r, g, b)
            u = prev_line[prev_line_index]
            p = filter_fn(
                p,
                u,
                up,
                (0xFF0000 & (b << 16)) + (0xFF00 & (g << 8)) + (0xFF & r) + (a << 24),
            )
            if channel_count == 3:
                p |= 0xFF000000

            up = u
            cur_line[cur_line_index] = p

            cur_line_index += 1
            prev_line_index += 1
            input_buf_index += step * 4

            w -= 1
            if w <= 0:
                break

        input_buf_index += (skip_block_bytes + (-ww if step == 1 else 1)) * 4
        if i & 1:
            input_buf_index -= (odd_skip * ww) * 4


def from_tlg6_bytes(data: bytearray) -> Image:
    return _from_tlg6(Tlg6.from_bytes(data))


def from_tlg6_file(file_name: str) -> Image:
    return _from_tlg6(Tlg6.from_file(file_name))


def _from_tlg6(tlg: Tlg6) -> Image:
    _init_table()
    pixels = array.array("I")

    filter_types = _decompress_filter_types(tlg.filter_types.buffer, tlg.header)
    pixel_buf = bytearray(4 * 4 * tlg.header.width * tlg.tlg6_h_block_size)
    zero_line = array.array("I")
    zero_line.frombytes(bytes(4 * tlg.header.width))
    prev_line = zero_line

    y = 0
    y_lim = y + tlg.tlg6_h_block_size

    for i, line in enumerate(tlg.lines):
        y = i * tlg.tlg6_h_block_size
        y_lim = y + tlg.tlg6_h_block_size
        if y_lim > tlg.header.height:
            y_lim = tlg.header.height

        pixel_count = (y_lim - y) * tlg.header.width

        for c, bits in enumerate(line.bits):
            if bits.method == 0:
                _decode_golomb(pixel_buf, c, pixel_count, bits.bit_pool)
            else:
                raise ValueError(
                    "Invalid compression method: {}. Only Golomb is supported".format(
                        bits.method
                    )
                )

        ft = filter_types[(y // H_BLOCK_SIZE) * tlg.header.x_block_count :]
        skip_bytes = (y_lim - y) * W_BLOCK_SIZE

        for yy in range(y, y_lim):
            cur_line = array.array("I")
            cur_line.frombytes(bytearray(4 * tlg.header.width))
            dir = (yy & 1) ^ 1
            odd_skip = (y_lim - yy - 1) - (yy - y)

            if tlg.main_count:
                start = (
                    tlg.header.width
                    if tlg.header.width < W_BLOCK_SIZE
                    else W_BLOCK_SIZE
                ) * (yy - y)

                _decode_line(
                    prev_line,
                    cur_line,
                    tlg.header.width,
                    0,
                    tlg.main_count,
                    ft,
                    skip_bytes,
                    pixel_buf[start * 4 :],
                    0xFF000000 if tlg.header.colors == 3 else 0,
                    odd_skip,
                    dir,
                    tlg.header.colors,
                )

            if tlg.main_count != tlg.header.x_block_count:
                ww = tlg.fraction
                if ww > W_BLOCK_SIZE:
                    ww = W_BLOCK_SIZE

                start = ww * (yy - y)
                _decode_line(
                    prev_line,
                    cur_line,
                    tlg.header.width,
                    tlg.main_count,
                    tlg.header.x_block_count,
                    ft,
                    skip_bytes,
                    pixel_buf[start * 4 :],
                    0xFF000000 if tlg.header.colors == 3 else 0,
                    odd_skip,
                    dir,
                    tlg.header.colors,
                )

            pixels.extend(cur_line)
            prev_line = cur_line

    return Image.frombytes(
        "RGBA", (tlg.header.width, tlg.header.height), pixels.tobytes()
    )


def from_tlg5_bytes(data: bytearray) -> Image:
    return _from_tlg5(Tlg5.from_bytes(data))


def from_tlg5_file(file_name: str) -> Image:
    return _from_tlg5(Tlg5.from_file(file_name))


def _from_tlg5(file_name: str) -> Image:
    raise ValueError("TLG5 processing is unimplemented!")


def from_tlg0_bytes(data: bytearray) -> Image:
    return _from_tlg0(Tlg0.from_bytes(data))


def from_tlg0_file(file_name: str) -> Image:
    return _from_tlg0(Tlg0.from_file(file_name))


def _from_tlg0(tlg: Tlg0) -> Image:
    if tlg.raw_data_magic == TLG6_MAGIC:
        return from_tlg6_bytes(tlg.tlg_raw_data)
    else:
        raise ValueError("Unsupported tlg version: {}".format(tlg.raw_data_magic))


def __main():
    file_name = sys.argv[1]
    image = Image.new("RGBA", (0, 0))
    with open(file_name, "rb") as tlg_file:
        magic = tlg_file.read(11)
        if magic == TLG0_MAGIC:
            image = from_tlg0_file(file_name)
        elif magic == TLG5_MAGIC:
            image = from_tlg5_file(file_name)
        elif magic == TLG6_MAGIC:
            image = from_tlg6_file(file_name)
        else:
            raise ValueError("Unsupported TLG version: {}".format(magic))

    image.save(sys.argv[1].replace(".tlg", ".png"), "PNG")


if __name__ == "__main__":
    __main()
