import sys
import os

from vn_re.formats.g00 import G00
from vn_re.utils.image import bgra_to_rgba, resolve_color_table
from PIL import Image

from hexdump import hexdump


def decompress(src, dest_len, version):
    if version == 0:
        return decompress0(src, dest_len)
    elif version == 1:
        return decompress2(src, dest_len)
    elif version == 2:
        return decompress2(src, dest_len)
    else:
        raise Exception(f"Version not supported {version}")


def decompress0(src, dest_len):
    dest = bytearray(dest_len)
    src_index = 0
    dest_index = 0
    start = True
    dl = 0
    d = 0
    while dest_index != dest_len:
        if start:
            dl = src[src_index]
            src_index += 1
            d = 8
            start = False
        if dest_index == dest_len:
            return dest
        if (dl & 1) == 0:
            a = int.from_bytes(src[src_index : src_index + 2], "little")
            src_index += 2
            counter = a & 0x0F
            counter += 1
            a >>= 4
            a <<= 2
            temp_index = dest_index - a
            for _ in range(counter):
                dest[dest_index : dest_index + 4] = dest[temp_index : temp_index + 4]
                dest_index += 4
                temp_index += 4
        else:
            dest[dest_index : dest_index + 3] = src[src_index : src_index + 3]
            src_index += 3
            dest_index += 3
            dest[dest_index] = 0xFF
            dest_index += 1
        dl >>= 1
        d -= 1
        if d == 0:
            start = True
    return dest


def decompress2(src, dest_len):
    dest = bytearray(dest_len)
    src_index = 0
    dest_index = 0
    start = True
    dl = 0
    d = 0
    while dest_index != dest_len:
        if start:
            dl = src[src_index]
            src_index += 1
            d = 8
            start = False
        if dest_index == dest_len:
            return dest
        if (dl & 1) == 0:
            a = int.from_bytes(src[src_index : src_index + 2], "little")
            src_index += 2
            counter = a & 0x0F
            counter += 2
            a >>= 4
            temp_index = dest_index - a
            for _ in range(counter):
                dest[dest_index] = dest[temp_index]
                dest_index += 1
                temp_index += 1
                if dest_index == dest_len:
                    return dest
        else:
            dest[dest_index] = src[src_index]
            src_index += 1
            dest_index += 1
        dl >>= 1
        d -= 1
        if d == 0:
            start = True
    return dest


def read_chunk(src, dest, dest_index, padding, counter, line):
    src_index = 0
    for _ in range(counter):
        for _ in range(line):
            dest[dest_index : dest_index + 4] = src[src_index : src_index + 4]
            src_index += 4
            dest_index += 4
        dest_index += padding
    return dest


def convert_image(filename):
    g00 = G00.from_file(filename)
    print(g00.version, filename)
    data = decompress(
        g00.pixel_data.data, g00.pixel_data.uncompressed_image_size, g00.version
    )

    if g00.version == 0:
        data = bgra_to_rgba(data)
        i = Image.frombytes(
            "RGBA",
            (g00.width, g00.height),
            bytes(data),
        )
        return [i]

    elif g00.version == 1:
        color_table = G00.ColorTable.from_bytes(data)
        color_index_table = data[color_table.size * 4 + 2 :]
        data = bgra_to_rgba(resolve_color_table(color_index_table, color_table.data))
        i = Image.frombytes(
            "RGBA",
            (g00.width, g00.height),
            bytes(data),
        )
        return [i]

    elif g00.version == 2:
        header_data = data[4 : 4 + g00.header_count * 8]
        headers = list()
        for i in range(g00.header_count):
            offset = int.from_bytes(header_data[i * 8 : i * 8 + 4], "little")
            size = int.from_bytes(header_data[i * 8 + 4 : i * 8 + 8], "little")
            if size != 0:
                headers.append(offset)
        sprites = dict()
        for h in headers:
            sprite = G00.Sprite.from_bytes(data[h : h + 36])
            chunks = list()
            chunk_index = 0
            for _ in range(sprite.chunk_count):
                chunk = G00.Chunk.from_bytes(
                    data[h + 0x74 + chunk_index : h + 0x74 + chunk_index + 10]
                )
                chunk.data_offset = h + 0xD0 + chunk_index
                chunk_index += chunk.width * chunk.height * 4 + 0x5C
                chunks.append(chunk)
            sprites[sprite] = chunks
        g00.headers.headers = [
            header
            for header in g00.headers.headers
            if header.right != 0 and header.bottom != 0
        ]
        images = list()
        for header, (sprite, chunks) in zip(g00.headers.headers, sprites.items()):
            width = header.right - header.left + 1
            height = header.bottom - header.top + 1
            dest = bytearray(width * height * 4)
            for chunk in chunks:
                padding = (width - chunk.width) * 4
                dest_index = (chunk.top * width * 4) + chunk.left * 4
                dest = read_chunk(
                    data[
                        chunk.data_offset : chunk.data_offset
                        + (chunk.width * chunk.height * 4)
                    ],
                    dest,
                    dest_index,
                    padding,
                    chunk.height,
                    chunk.width,
                )
            images.append(
                Image.frombytes(
                    "RGBA",
                    (width, height),
                    bytes(bgra_to_rgba(dest)),
                )
            )
        return images


if __name__ == "__main__":
    for filename in sys.argv[1:]:
        try:
            images = convert_image(filename)
            if len(images) == 1:
                img = images[0]
                path, _ = os.path.splitext(filename)
                img.save(f"{path}.png", "PNG")
            else:
                for i, img in enumerate(images):
                    path, _ = os.path.splitext(filename)
                    img.save(f"{path}_{i}.png", "PNG")
        except Exception as e:
            print(e)
