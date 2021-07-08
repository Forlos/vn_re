import sys
import os

from PIL import Image

from vn_re.formats.compressedbg import Compressedbg
from vn_re.utils.util import (
    wrapping_add,
    wrapping_add8,
    wrapping_add16,
    wrapping_mul,
    wrapping_sub,
    wrapping_sub8,
)
from vn_re.utils.image import bgra_to_rgba
from hexdump import hexdump


def prng(state):
    prev_state = state
    val = wrapping_mul(0x4E35, (state & 0xFFFF))
    state = wrapping_add(
        wrapping_add(
            wrapping_add(
                wrapping_add(
                    (val & 0xFFFF_0000), wrapping_mul(0x015A_0000, prev_state)
                ),
                wrapping_mul(0x4E35_0000, (prev_state >> 16)),
            ),
            (val & 0xFFFF),
        ),
        1,
    )
    val = (
        wrapping_sub(
            wrapping_add(wrapping_mul(0x15A, prev_state), (val >> 16)),
            wrapping_mul(0x31CB, (prev_state >> 16)),
        )
    ) & 0x7FFF
    return val, state


def fill_some_buf(src):
    src_index = 0
    dest = bytearray()
    for _ in range(256):
        b = 0xFF
        c = 0
        d = 0
        while b >= 0x80:
            b = src[src_index]
            src_index += 1

            a = b
            a &= 0x7F
            a <<= c
            c += 7
            d |= a

        dest += d.to_bytes(4, "little")

    return dest


def fill_some_big_buf(src):
    v25 = 0
    v6 = 0
    dest = bytearray(12264)
    dest_index = 8
    for i in range(256):
        b = int.from_bytes(src[i * 4 : i * 4 + 4], "little")
        dest_index += 24
        dest[dest_index - 32 : dest_index - 28] = (b > 0).to_bytes(4, "little")
        dest[dest_index - 28 : dest_index - 24] = b.to_bytes(4, "little")
        dest[dest_index - 24 : dest_index - 20] = (0).to_bytes(4, "little")
        dest[dest_index - 20 : dest_index - 16] = (0xFFFFFFFF).to_bytes(4, "little")
        dest[dest_index - 16 : dest_index - 12] = i.to_bytes(4, "little")
        dest[dest_index - 12 : dest_index - 8] = i.to_bytes(4, "little")
        v6 = wrapping_add(b, v25)
        v25 = wrapping_add(v25, b)

    xd = (
        b"\x00\x00\x00\x00\x00\x00\x00\x00\x01\x00\x00\x00\xFF\xFF\xFF\xFF"
        + b"\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF"
    )
    for i in range(255):
        dest[0x100 * 24 + i * 24 : 0x100 * 24 + i * 24 + 24] = xd

    dest_index = 0x1800
    result = 0x100
    d = 0
    some_arr = [0, 0]
    while True:
        for i in range(2):
            some_arr[i] = 0xFFFFFFFF
            d = 0xFFFFFFFF
            s = 0xFFFFFFFF
            v13 = 0
            if result == 0:
                break

            index = 0
            while v13 < result:
                if int.from_bytes(dest[index : index + 4], "little") != 0:
                    b = int.from_bytes(dest[index + 4 : index + 8], "little")
                    if b < s:
                        d = v13
                        some_arr[i] = v13
                        s = b
                v13 += 1
                index += 24

            if d != 0xFFFFFFFF:
                dest[d * 24 : d * 24 + 4] = (0).to_bytes(4, "little")
                dest[d * 24 + 12 : d * 24 + 16] = (result).to_bytes(4, "little")

        s = 0
        if some_arr[1] != 0xFFFFFFFF:
            s = int.from_bytes(
                dest[some_arr[1] * 24 + 4 : some_arr[1] * 24 + 8], "little"
            )

        val = wrapping_add(
            int.from_bytes(dest[some_arr[0] * 24 + 4 : some_arr[0] * 24 + 8], "little"),
            s,
        )

        xmm_1 = (
            b"\x01\x00\x00\x00"
            + val.to_bytes(4, "little")
            + b"\x01\x00\x00\x00\xFF\xFF\xFF\xFF"
        )
        xmm_2 = some_arr[0].to_bytes(4, "little") + some_arr[1].to_bytes(4, "little")

        dest[dest_index : dest_index + 0x10] = xmm_1
        dest[dest_index + 0x10 : dest_index + 0x18] = xmm_2
        if val == v25:
            return dest, result

        result += 1

        dest_index += 24


def fill_unk3_data(data_size, src, big_buf, result):
    src_index = 0
    dest = bytearray(data_size)
    some_val = int.from_bytes(big_buf[result * 24 + 8 : result * 24 + 12], "little")
    a = 0x80
    b = result
    d = some_val
    for i in range(data_size):
        if d == 1:
            while True:
                d = 0
                if (src[src_index] & a) != 0:
                    d = 1
                d = d * 4 + 16
                b = int.from_bytes(big_buf[d + b * 24 : d + b * 24 + 4], "little")

                a >>= 1
                d = a
                if a == 0:
                    a = 0x80
                if d == 0:
                    src_index += 1
                if int.from_bytes(big_buf[b * 24 + 8 : b * 24 + 12], "little") != 1:
                    break

            d = some_val

        dest[i] = b & 0xFF
        b = result

    return dest


def fill_pixel_buf(size, src):
    dest = bytearray(size)
    src_index = 0
    dest_index = 0
    result = 0
    flag = True
    while src_index < len(src):
        b = 0xFF
        c = 0
        d = 0
        while b >= 0x80:
            b = src[src_index]
            src_index += 1

            a = b
            a &= 0x7F
            a <<= c
            c += 7
            d |= a

        result = wrapping_add(result, d)
        if flag:
            dest[dest_index : dest_index + d] = src[src_index : src_index + d]
            flag = False
            src_index += d
        else:
            flag = True
        dest_index += d

    return dest


def packuswb(xmm0):
    result = bytearray()
    for i in range(0, 8, 2):
        b = int.from_bytes(xmm0[i : i + 2], "little", signed=True)
        if b > 0xFF:
            b = 0xFF
        if b < 0:
            b = 0
        else:
            b &= 0xFF
        result.append(b)
    return result


def paddw_psrlw1(x, x2):
    dest = bytearray(8)
    for i in range(0, 8, 2):
        dest[i : i + 2] = (
            wrapping_add16(
                int.from_bytes(x[i : i + 2], "little"),
                int.from_bytes(x2[i : i + 2], "little"),
            )
            >> 1
        ).to_bytes(2, "little")
    return dest


def punpcklbw(xmm0, xmm1):
    dest = bytearray()
    for i in range(4):
        dest.append(xmm0[i])
        dest.append(xmm1[i])
    return dest


def parse_pixel_data(src, width, height, bytes_per_pixel):
    src_index = 0
    dest_index = 0
    dest = bytearray(width * height * 4)
    pixel = bytearray(b"\x00\x00\x00\x00")
    for _ in range(width):
        p = src[src_index : src_index + bytes_per_pixel]
        for i in range(bytes_per_pixel):
            pixel[i] = wrapping_add8(pixel[i], p[i])
        src_index += bytes_per_pixel
        dest[dest_index : dest_index + 4] = pixel
        dest_index += 4

    for i in range(height - 1):
        prev_line_index = 0
        prev_line = dest[dest_index - width * 4 : dest_index - width * 4 + width * 4]
        p = src[src_index : src_index + bytes_per_pixel]
        x = prev_line[prev_line_index : prev_line_index + 4]
        src_index += bytes_per_pixel
        prev_line_index += 4
        for i in range(bytes_per_pixel):
            x[i] = wrapping_add8(p[i], x[i])
        dest[dest_index : dest_index + 4] = x
        dest_index += 4
        x = punpcklbw(x, b"\x00\x00\x00\x00")
        for _ in range(width - 1):
            p2 = src[src_index : src_index + bytes_per_pixel]
            x2 = prev_line[prev_line_index : prev_line_index + 4]
            prev_line_index += 4
            src_index += bytes_per_pixel
            x2 = punpcklbw(x2, b"\x00\x00\x00\x00")
            x = paddw_psrlw1(x, x2)
            p2 = punpcklbw(p2 + b"\x00", b"\x00\x00\x00\x00")
            for i in range(8):
                x[i] = wrapping_add8(p2[i], x[i])
            p2 = x
            result = packuswb(p2)
            dest[dest_index : dest_index + 4] = result
            dest_index += 4

    return dest


def extract_file(filename):
    bg = Compressedbg.from_file(filename)
    print(
        filename,
        bg.header.width,
        bg.header.height,
        bg.header.bpp >> 3,
        bg.header.width * bg.header.height * bg.header.bpp >> 3,
    )
    bg.some_alloc = bytearray(bg.some_alloc)
    state = bg.header.prng_seed
    for i in range(bg.header.some_size):
        val, state = prng(state)
        x = bg.some_alloc[i]
        bg.some_alloc[i] = wrapping_sub8(x, val & 0xFF)
    some_buf = fill_some_buf(bg.some_alloc)
    some_big_buf, result = fill_some_big_buf(some_buf)
    data = fill_unk3_data(bg.header.unk3, bg.pixel_data, some_big_buf, result)
    pixel_data = fill_pixel_buf(
        bg.header.width * bg.header.height * bg.header.bpp >> 3, data
    )

    pixel_data = bgra_to_rgba(
        parse_pixel_data(
            pixel_data, bg.header.width, bg.header.height, bg.header.bpp >> 3
        )
    )

    path = os.path.splitext(os.path.basename(filename))[0]
    os.makedirs("ext", exist_ok=True)

    i = Image.frombytes("RGBA", (bg.header.width, bg.header.height), bytes(pixel_data))
    i.save(f"ext/{path}.png")
    return


if __name__ == "__main__":
    for filename in sys.argv[1:]:
        try:
            extract_file(filename)
        except Exception as e:
            print(filename, e)
