import sys
import os

from PIL import Image
import zlib

from vn_re.formats.crx import Crx
from vn_re.utils.util import chunks
from vn_re.utils.image import (
    bgr_to_rgb,
    bgra_to_rgba,
    resolve_color_table,
    resolve_color_table_without_alpha,
)
from hexdump import hexdump


def ver0(src, width, bytes_per_pixel):
    src_index = 0
    dest_index = 0
    dest = bytearray(width * bytes_per_pixel)

    dest[dest_index : dest_index + bytes_per_pixel] = src[
        src_index : src_index + bytes_per_pixel
    ]
    src_index += bytes_per_pixel
    dest_index += bytes_per_pixel

    for _ in range(width - 1):
        if bytes_per_pixel == 4:
            d = dest[dest_index - 4] + src[src_index]
            src_index += 1
            dest[dest_index] = d & 0xFF
            dest_index += 1

            d = dest[dest_index - 4] + src[src_index]
            src_index += 1
            dest[dest_index] = d & 0xFF

            d = dest[dest_index - 3] + src[src_index]
            src_index += 1
            dest_index += 1
            dest[dest_index] = d & 0xFF

            d = dest[dest_index - 3] + src[src_index]
            src_index += 1
            dest[dest_index + 1] = d & 0xFF
            dest_index += 2
        else:
            d = dest[dest_index - 3] + src[src_index]
            src_index += 1
            dest[dest_index] = d & 0xFF
            dest_index += 1

            d = dest[dest_index - 3] + src[src_index]
            src_index += 1
            dest[dest_index] = d & 0xFF

            d = dest[dest_index - 2] + src[src_index]
            src_index += 1
            dest[dest_index + 1] = d & 0xFF
            dest_index += 2

    return dest


def ver1(src, prev_line, width, bytes_per_pixel):
    src_index = 0
    dest_index = 0
    prev_line_index = 0
    dest = bytearray(width * bytes_per_pixel)

    for _ in range(width * bytes_per_pixel):
        dest[dest_index] = (src[src_index] + prev_line[prev_line_index]) & 0xFF
        src_index += 1
        prev_line_index += 1
        dest_index += 1

    return dest


def ver2(src, prev_line, width, bytes_per_pixel):
    src_index = 0
    dest_index = 0
    prev_line_index = 0
    dest = bytearray(width * bytes_per_pixel)

    dest[dest_index : dest_index + bytes_per_pixel] = src[
        src_index : src_index + bytes_per_pixel
    ]
    src_index += bytes_per_pixel
    dest_index += bytes_per_pixel

    for _ in range(width - 1):
        for _ in range(bytes_per_pixel):
            d = (src[src_index] + prev_line[prev_line_index]) & 0xFF
            src_index += 1
            prev_line_index += 1
            dest[dest_index] = d
            dest_index += 1

    return dest


def ver3(src, prev_line, width, bytes_per_pixel):
    src_index = 0
    dest_index = 0
    prev_line_index = bytes_per_pixel
    dest = bytearray(width * bytes_per_pixel)
    for _ in range(width - 1):
        for _ in range(bytes_per_pixel):
            d = (src[src_index] + prev_line[prev_line_index]) & 0xFF
            src_index += 1
            prev_line_index += 1
            dest[dest_index] = d
            dest_index += 1

    dest[dest_index : dest_index + bytes_per_pixel] = src[
        src_index : src_index + bytes_per_pixel
    ]
    src_index += bytes_per_pixel
    dest_index += bytes_per_pixel
    return dest


def ver4(src, width, bytes_per_pixel):
    src_index = 0
    dest_index = 0
    dest = bytearray(width * bytes_per_pixel)
    for _ in range(bytes_per_pixel):
        s = width
        while s > 0:
            b = src[src_index]
            dest[dest_index] = b
            src_index += 1
            dest_index += bytes_per_pixel
            s -= 1
            if s == 0:
                break
            if b == src[src_index]:
                c = src[src_index + 1]
                src_index += 2
                s -= c
                while c > 0:
                    dest[dest_index] = b
                    c -= 1
                    dest_index += bytes_per_pixel
        s = 1
        c = width * bytes_per_pixel
        s -= c
        dest_index += s

    return dest, src_index


def abgr_to_rgba(buf):
    result = bytearray()
    for chunk in chunks(buf, 4):
        a = int.from_bytes(chunk, "little")
        chunk[3] = ~a & 0xFF  # alpha
        chunk[2] = (a >> 8) & 0xFF  # blue
        chunk[1] = (a >> 16) & 0xFF  # green
        chunk[0] = (a >> 24) & 0xFF  # red
        result += chunk
    return result


def parse_pixels(data, width, height, bytes_per_pixel):
    src_index = 0
    data_index = 0
    dest = bytearray()
    prev = bytearray()
    if bytes_per_pixel == 1:
        return data
    for _ in range(height):
        x = data[data_index]
        data_index += 1
        if x == 0:
            prev = ver0(data[data_index:], width, bytes_per_pixel)
            data_index += width * bytes_per_pixel
        if x == 1:
            prev = ver1(data[data_index:], prev, width, bytes_per_pixel)
            data_index += width * bytes_per_pixel
        if x == 2:
            prev = ver2(data[data_index:], prev, width, bytes_per_pixel)
            data_index += width * bytes_per_pixel
        if x == 3:
            prev = ver3(data[data_index:], prev, width, bytes_per_pixel)
            data_index += width * bytes_per_pixel
        if x == 4:
            prev, src_index = ver4(data[data_index:], width, bytes_per_pixel)
            data_index += src_index

        dest += prev
    if bytes_per_pixel == 3:
        dest = bgr_to_rgb(dest)
    elif bytes_per_pixel == 4:
        dest = abgr_to_rgba(dest)
    return dest


def extract_file(filename):
    crx = Crx.from_file(filename)
    f = open(filename, "rb")
    print(
        crx.header.width,
        crx.header.height,
        crx.header.width * crx.header.height * 4,
        hex(crx.header.width * crx.header.height * 4),
    )
    data = zlib.decompress(crx.image_data)
    bytes_per_pixel = 0
    mode = "RGB"
    if crx.header.has_alpha == 0:
        bytes_per_pixel = 3
    elif crx.header.has_alpha == 1:
        mode = "RGBA"
        bytes_per_pixel = 4
    elif crx.header.has_alpha == 0x101:
        mode = "RGB"
        bytes_per_pixel = 1
        data = bgr_to_rgb(resolve_color_table_without_alpha(data, crx.color_table))
    elif crx.header.has_alpha == 0x102:
        mode = "RGBA"
        bytes_per_pixel = 1
        data = bgra_to_rgba(resolve_color_table(data, crx.color_table_with_alpha))

    data = parse_pixels(data, crx.header.width, crx.header.height, bytes_per_pixel)
    print(len(data))
    i = Image.frombytes(mode, (crx.header.width, crx.header.height), bytes(data))
    path = os.path.splitext(os.path.basename(filename))[0]
    os.makedirs("ext", exist_ok=True)
    i.save(f"ext/{path}.png")
    return


if __name__ == "__main__":
    for filename in sys.argv[1:]:
        try:
            extract_file(filename)
        except Exception as e:
            print(filename, e)
