import sys
import os
from sys import version

from PIL import Image
from hexdump import hexdump

from vn_re.formats.iar import Iar
from vn_re.utils.util import wrapping_add, wrapping_shl
from vn_re.utils.image import (
    bgra_to_rgba,
    add_alpha_channel,
    remove_bitmap_padding,
    bgr_to_rgb,
)


def decompress(src, dest_len):
    src_index = 0
    dest_index = 0
    dest = bytearray(dest_len)
    b = 0
    c = 0
    s = 0
    var_4 = 0
    var_8 = 0
    var_c = 0
    while True:
        while True:
            c >>= 1
            if c <= 0xFFFF:
                c = src[src_index] | (
                    wrapping_shl((src[src_index + 1] | 0xFFFF_FF00), 8)
                )
                src_index += 2
            if c & 1 == 0:
                break
            dest[dest_index] = src[src_index]
            src_index += 1
            dest_index += 1

        c >>= 1
        if c <= 0xFFFF:
            c = src[src_index] | (wrapping_shl((src[src_index + 1] | 0xFFFF_FF00), 8))
            src_index += 2

        if c & 1 == 0:
            c >>= 1
            b = 2
            var_c = b
            if c <= 0xFFFF:
                c = src[src_index] | wrapping_shl((src[src_index + 1] | 0xFFFF_FF00), 8)
                src_index += b

            if c & 1 == 0:
                s = src[src_index] + 1
                src_index += 1
                if s == 256:
                    return dest
            else:
                c >>= 1
                if c <= 0xFFFF:
                    c = src[src_index] | wrapping_shl(
                        (src[src_index + 1] | 0xFFFF_FF00), 8
                    )
                    src_index += 2
                d = wrapping_shl((c & 1), 10)
                c >>= 1
                if c <= 0xFFFF:
                    c = src[src_index] | wrapping_shl(
                        (src[src_index + 1] | 0xFFFF_FF00), 8
                    )
                    src_index += 2
                a = wrapping_shl((c & 1), 9)
                c >>= 1
                d |= a
                if c <= 0xFFFF:
                    c = src[src_index] | wrapping_shl(
                        (src[src_index + 1] | 0xFFFF_FF00), 8
                    )
                    src_index += 2
                s = wrapping_add(((wrapping_shl((c & 1), 8) | src[src_index]) | d), 256)
                src_index += 1
        else:
            c >>= 1
            d = 1
            if c <= 0xFFFF:
                c = src[src_index] | wrapping_shl((src[src_index + 1] | 0xFFFF_FF00), 8)
                src_index += 2
            s = c
            c >>= 1
            s &= d
            if c <= 0xFFFF:
                c = src[src_index] | wrapping_shl((src[src_index + 1] | 0xFFFF_FF00), 8)
                src_index += 2
            if c & 1 == 0:
                c >>= 1
                d = 513
                if c <= 0xFFFF:
                    c = src[src_index] | wrapping_shl(
                        (src[src_index + 1] | 0xFFFF_FF00), 8
                    )
                    src_index += 2
                if c & 1 == 0:
                    c >>= 1
                    d = 1025
                    if c <= 0xFFFF:
                        c = src[src_index] | wrapping_shl(
                            (src[src_index + 1] | 0xFFFF_FF00), 8
                        )
                        src_index += 2
                    a = c & 1
                    c >>= 1
                    s = wrapping_add(s, s)
                    s |= a
                    if c <= 0xFFFF:
                        c = src[src_index] | wrapping_shl(
                            (src[src_index + 1] | 0xFFFF_FF00), 8
                        )
                        src_index += 2
                    if c & 1 == 0:
                        c >>= 1
                        d = 2049
                        if c <= 0xFFFF:
                            c = src[src_index] | wrapping_shl(
                                (src[src_index + 1] | 0xFFFF_FF00), 8
                            )
                            src_index += 2
                        a = c & 1
                        c >>= 1
                        s = wrapping_add(s, s)
                        s |= a
                        if c <= 0xFFFF:
                            c = src[src_index] | wrapping_shl(
                                (src[src_index + 1] | 0xFFFF_FF00), 8
                            )
                            src_index += 2
                        if c & 1 == 0:
                            c >>= 1
                            d = 4097
                            if c <= 0xFFFF:
                                c = src[src_index] | wrapping_shl(
                                    (src[src_index + 1] | 0xFFFF_FF00), 8
                                )
                                src_index += 2
                            s = wrapping_add(s, s)
                            s |= c & 1

            s = wrapping_shl(s, 8) | src[src_index]
            src_index += 1
            c >>= 1
            s = wrapping_add(s, d)
            var_4 = src_index
            if c <= 0xFFFF:
                c = src[src_index] | wrapping_shl((src[src_index + 1] | 0xFFFF_FF00), 8)
                src_index += 2
                var_4 = src_index

            b = 3
            if c & 1 == 0:
                c >>= 1
                if c <= 0xFFFF:
                    c = src[src_index] | (
                        wrapping_shl((src[src_index + 1] | 0xFFFF_FF00), 8)
                    )
                    src_index += 2
                    var_4 = src_index
                b = 4
                if c & 1 == 0:
                    c >>= 1
                    if c <= 0xFFFF:
                        c = src[src_index] | wrapping_shl(
                            (src[src_index + 1] | 0xFFFF_FF00), 8
                        )
                        src_index += 2
                        var_4 = src_index
                    b = 5
                    if c & 1 == 0:
                        c >>= 1
                        if c <= 0xFFFF:
                            c = src[src_index] | wrapping_shl(
                                (src[src_index + 1] | 0xFFFF_FF00), 8
                            )
                            src_index += 2
                            var_4 = src_index
                        b = 6
                        if c & 1 == 0:
                            c >>= 1
                            var_8 = c
                            if c <= 0xFFFF:
                                c = src[src_index] | wrapping_shl(
                                    (src[src_index + 1] | 0xFFFF_FF00), 8
                                )
                                src_index += 2
                                var_8 = c
                                var_4 = src_index
                            if c & 1 == 0:
                                a, var_4, var_8 = some_fn(var_4, var_8, src)
                                if a == 0:
                                    d, var_4, var_8 = some_fn(var_4, var_8, src)
                                    d = wrapping_shl(d, 2)
                                    a, var_4, var_8 = some_fn(var_4, var_8, src)
                                    a = wrapping_add(a, a)
                                    d |= a
                                    a, var_4, var_8 = some_fn(var_4, var_8, src)
                                    src_index = var_4
                                    b = a | d
                                    b = wrapping_add(b, 9)
                                else:
                                    src_index = var_4 + 1
                                    b = src[src_index - 1] + 17
                            else:
                                a, var_4, var_8 = some_fn(var_4, var_8, src)
                                src_index = var_4
                                if a == 0:
                                    b = 7
                                else:
                                    b = 8
                            c = var_8
            var_c = b

        d = dest_index
        d -= s
        var_8 = b
        for _ in range(b):
            dest[d + s] = dest[d]
            d += 1
        if b != 0:
            b = var_c
        dest_index += b


def some_fn(var_4, var_8, src):
    var_8 >>= 1
    if var_8 <= 0xFFFF:
        s = src[var_4] | wrapping_shl((src[var_4 + 1] | 0xFFFF_FF00), 8)
        var_8 = s
        var_4 += 2
    return (var_8 & 1, var_4, var_8)


def calculate_padding(width):
    padding = 4 - ((width * 3) % 4)
    if padding == 4:
        padding = 0
    return padding


def raw_image_data(iar, f, image_index):
    off = iar.entry_index_table[image_index]
    f.seek(off)
    header_data = f.read(72)
    entry = Iar.FileEntry.from_bytes(header_data)
    file_data = bytearray(f.read(entry.file_size))
    if (entry.version >> 24) == 1:
        file_data = decompress(file_data, entry.decompressed_file_size)
    return (file_data, entry)


def get_image_data_by_version(entry, file_data, iar, f):
    mode = "RGBA"
    if (entry.version & 0xFFFF) == 0x3C:
        file_data = bgra_to_rgba(file_data)
    elif (entry.version & 0xFFFF) == 0x83C:
        mode = "RGB"
        file_data, _ = parse_subimage(iar, f, file_data, 4)
        file_data = bgra_to_rgba(file_data)
    elif (entry.version & 0xFFFF) == 0x1C:
        padding = calculate_padding(entry.width)
        file_data = add_alpha_channel(
            remove_bitmap_padding(
                file_data, entry.decompressed_file_size // entry.height, padding
            )
        )
        file_data = bgra_to_rgba(file_data)
    elif (entry.version & 0xFFFF) == 0x81C:
        mode = "RGB"
        file_data, parent_entry = parse_subimage(iar, f, file_data, 3)
        padding = calculate_padding(entry.width)
        file_data = remove_bitmap_padding(
            file_data, parent_entry.decompressed_file_size // entry.height, padding
        )
        file_data = bgr_to_rgb(file_data)
    elif (entry.version & 0xFFFF) == 0x02:
        mode = "L"
    return (file_data, mode)


def versions_to_ignore(entry):
    # This just concatenates two images into one, those images are already extracted no need to double
    if (entry.version & 0xFFFF) == 0x103C:
        return True
    # This just concatenates two images into one, those images are already extracted no need to double
    elif (entry.version & 0xFFFF) == 0x101C:
        return True
    return False


def parse_subimage(iar, f, data, bytes_per_pixel):
    data_index = 12
    sub_image = Iar.SubImage.from_bytes(data)
    parent, parent_entry = raw_image_data(iar, f, sub_image.parent_index)
    padding = calculate_padding(parent_entry.width)
    if bytes_per_pixel == 4:
        padding = 0
    for y in range(sub_image.height):
        writes = int.from_bytes(data[data_index : data_index + 2], "little")
        data_index += 2
        parent_index = (sub_image.top + y) * (
            parent_entry.width * bytes_per_pixel + padding
        )
        for _ in range(writes):
            parent_index += (
                int.from_bytes(data[data_index : data_index + 2], "little")
                * bytes_per_pixel
            )
            pixels_count = (
                int.from_bytes(data[data_index + 2 : data_index + 4], "little")
                * bytes_per_pixel
            )
            data_index += 4
            pixels = data[data_index : data_index + pixels_count]
            parent[parent_index : parent_index + pixels_count] = pixels
            parent_index += pixels_count
            data_index += pixels_count
    return parent, parent_entry


def extract_image(iar, f, image_index):
    file_data, entry = raw_image_data(iar, f, image_index)
    if versions_to_ignore(entry):
        return
    # print(
    #     image_index,
    #     hex(entry.version),
    #     entry.width,
    #     entry.height,
    #     entry.decompressed_file_size,
    #     entry.width * entry.height * 4,
    # )

    file_data, mode = get_image_data_by_version(entry, file_data, iar, f)

    return Image.frombytes(
        mode,
        (entry.width, entry.height),
        bytes(file_data),
    )


def extract_file(filename):
    iar = Iar.from_file(filename)
    f = open(filename, "rb")
    path = os.path.basename(filename) + "_ext/"
    os.makedirs(path, exist_ok=True)
    for i in range(iar.header.entry_count):
        img = extract_image(iar, f, i)
        if img is not None:
            img.save(path + str(i) + ".png", "PNG")
    return


if __name__ == "__main__":
    for filename in sys.argv[1:]:
        extract_file(filename)
