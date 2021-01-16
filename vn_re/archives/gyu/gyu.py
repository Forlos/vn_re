import sys
import os

from PIL import Image

from vn_re.formats.gyu import Gyu
from vn_re.utils.image import bitmap_to_png_with_padding, bgra_to_rgba
from vn_re.utils.util import chunks
from vn_re.utils.mt import seed_gyu, rand


def decompress(src, dest_len, version):
    version &= 0xFFFF_0000
    if version == 0x0800_0000:
        return decompress3(src[4:], dest_len)
    elif version == 0x0200_0000 or version == 0x0400_0000:
        return decompress0(src, dest_len)
    elif version == 0x0100_0000:
        return src
    else:
        raise Exception(f"Version not supported {version}")


def decompress0(buf, dest_len):
    if len(buf) == 0:
        return bytearray()
    temp_buf = bytearray(4096)
    result = bytearray(dest_len)
    x = 0
    a = 4078
    b = 0
    c = 0
    bytes_read = 0
    bytes_written = 0
    while bytes_read < len(buf):
        x >>= 1
        if (x & 0x100) == 0:
            b = buf[bytes_read]
            bytes_read += 1
            b |= 0xFF00
            x = b
        if ((x & 0xFF) & 1) == 0:
            bl = buf[bytes_read]
            bytes_read += 1
            cl = buf[bytes_read]
            bytes_read += 1
            s = cl
            d = s
            c = bl
            d &= 0xF0
            s &= 0x0F
            d <<= 4
            s += 3
            d |= c
            c = s
            if c > 0:
                s = d
                b = c
                while b != 0:
                    c = s
                    s += 1
                    c &= 0xFFF
                    d = temp_buf[c]
                    result[bytes_written] = d
                    c = a
                    bytes_written += 1
                    a += 1
                    a &= 0xFFF
                    temp_buf[c] = d

                    b -= 1
        else:
            d = buf[bytes_read]
            bytes_read += 1
            result[bytes_written] = d
            bytes_written += 1
            c = a
            a += 1
            a &= 0xFFF
            temp_buf[c] = d

    return result


def decompress3(src, dest_len):
    dest = bytearray(dest_len)
    src_index = 0
    si = 0
    di = 0
    c = 0
    d = 1
    dl = 0
    temp = 256
    read_first = True

    while True:
        if read_first:
            dest[di] = src[src_index]
            di += 1
            src_index += 1
            read_first = False

        d -= 1
        if d == 0:
            dl = src[src_index]
            src_index += 1
            d = 8

        temp = dl + dl
        dl = temp & 0xFF
        if temp > 255:
            read_first = True
            continue

        a = bytearray([0xFF, 0xFF, 0xFF, 0xFF])
        d -= 1
        if d == 0:
            dl = src[src_index]
            src_index += 1
            d = 8

        temp = dl + dl
        dl = temp & 0xFF
        if temp > 255:
            c = int.from_bytes(src[src_index : src_index + 2], "big")
            a[0] = c & 0xFF
            a[1] = (c & 0xFF00) >> 8
            src_index += 2
            a = int.from_bytes(a, "little")
            c = a & 7
            a >>= 3
            a |= 0xFF_FF_E0_00
            a = a.to_bytes(4, "little")
            if c == 0:
                cl = src[src_index]
                c |= cl
                src_index += 1
                if cl == 0:
                    return dest
            else:
                c += 1
        else:
            c = 0
            d -= 1
            if d == 0:
                dl = src[src_index]
                src_index += 1
                d = 8
            temp = dl + dl
            dl = temp & 0xFF
            c += c
            if temp > 255:
                c += 1
            d -= 1
            if d == 0:
                dl = src[src_index]
                src_index += 1
                d = 8
            temp = dl + dl
            dl = temp & 0xFF
            c += c
            if temp > 255:
                c += 1
            a[0] = src[src_index]
            src_index += 1
            c += 1

        si = di
        si += int.from_bytes(a, "little", signed=True)
        c += 1
        for _ in range(c):
            dest[di] = dest[si]
            di += 1
            si += 1


def decrypt_with_mt(buf, mt_seed):
    buf = bytearray(buf)
    if mt_seed == 0xFFFF_FFFF:
        return buf
    seed_gyu(mt_seed)
    for _ in range(10):
        a = rand() % len(buf)
        b = rand() % len(buf)
        buf[a], buf[b] = buf[b], buf[a]
    return buf


def resolve_color_table(buf, color_table):
    color_table = [c for c in chunks(color_table, 4)]
    result = bytearray()
    for b in buf:
        result += color_table[b]
    return result


def resolve_alpha_channel(buf, alpha_channel):
    result = bytearray()
    if len(alpha_channel) > 0:
        for i, chunk in enumerate(chunks(buf, 4)):
            chunk[3] = alpha_channel[i]
            result += chunk
    else:
        for chunk in chunks(buf, 4):
            chunk[3] = 0xFF
            result += chunk
    return result


def add_alpha_channel(buf):
    result = bytearray()
    for chunk in chunks(buf, 3):
        result += chunk + b"\xFF"
    return result


def convert_image(filename, seeds):
    gyu = Gyu.from_file(filename)
    if gyu.mt_seed == 0:
        id = int(os.path.basename(filename).replace(".gyu", ""))
        gyu.mt_seed = seeds[id]
    gyu.data = decrypt_with_mt(gyu.data, gyu.mt_seed)
    padded_width = (gyu.bpp // 8 * gyu.width + 3) & 0xFF_FF_FF_FC

    alpha_channel = bitmap_to_png_with_padding(
        decompress0(gyu.alpha_channel, ((gyu.width + 3) & 0xFF_FF_FF_FC) * gyu.height),
        ((gyu.width + 3) & 0xFF_FF_FF_FC),
        ((gyu.width + 3) & 0xFF_FF_FF_FC) - gyu.width,
    )
    data = decompress(
        gyu.data,
        padded_width * gyu.height,
        gyu.version,
    )
    data = bitmap_to_png_with_padding(
        data, padded_width, padded_width - (gyu.bpp // 8 * gyu.width)
    )

    if gyu.bpp == 8 and gyu.color_table_size != 0:
        data = resolve_color_table(data, gyu.color_table)
    elif gyu.bpp == 24:
        data = add_alpha_channel(data)
    data = bgra_to_rgba(resolve_alpha_channel(data, alpha_channel))

    i = Image.frombytes(
        "RGBA",
        (gyu.width, gyu.height),
        bytes(data),
    )
    return i


if __name__ == "__main__":
    for filename in sys.argv[1:]:
        i = convert_image(filename, [])
        path, _ = os.path.splitext(filename)
        i.save(path + ".png", "PNG")
