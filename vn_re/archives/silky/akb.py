import sys
from hexdump import hexdump

from PIL import Image

from vn_re.formats.akb import Akb
from vn_re.utils.util import chunks, wrapping_add8


def bgra_to_rgba(buf):
    result = bytearray()
    for chunk in chunks(buf, 4):
        a = int.from_bytes(chunk, "little")
        chunk[2] = a & 0xFF
        chunk[1] = (a >> 8) & 0xFF
        chunk[0] = (a >> 16) & 0xFF
        chunk[3] = (a >> 24) & 0xFF
        result += chunk
    return result


def bitmap_to_png(buf, width):
    result = bytearray()
    for chunk in chunks(buf, width * 4):
        result = chunk + result
    return result


def print_hex(buf, width):
    for chunk in chunks(buf, width * 4):
        hexdump(chunk[:16])


def decompress(buf, akb):
    if akb.compression & 0x40000000 == 0:
        return decompress3(
            buf,
            akb.width * akb.height * 4,
            (akb.right - akb.left) * 4,
            (akb.width - (akb.right - akb.left)) * 4,
            akb.left * 4 + (akb.height - akb.bottom) * 4 * akb.width,
        )
    else:
        return decompress2(
            buf,
            akb.width * akb.height * 4,
            (akb.right - akb.left) * 4,
            (akb.width - (akb.right - akb.left)) * 4,
            akb.left * 4 + (akb.height - akb.bottom) * 4 * akb.width,
        )


def decompress2(buf, dest_len, w_in, w_out, write_index):
    temp_buf = bytearray(4096)
    result = bytearray(dest_len)
    x = 0
    z = 0
    a = 4078
    b = 0
    c = 0
    bytes_read = 0
    bytes_written = write_index
    cur_index = w_in
    while bytes_read < len(buf):
        x >>= 1
        if (x & 0x100) == 0:
            b = buf[bytes_read]
            bytes_read += 1
            b |= 0xFF00
            x = b
        bl = buf[bytes_read]
        bytes_read += 1
        if ((x & 0xFF) & 1) == 0:
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
                counter = c
                while counter != 0:
                    c = s & 0xFFF
                    d = temp_buf[c]
                    result[bytes_written] = d
                    bytes_written += 1
                    cur_index -= 1
                    z = d & 0xFF
                    b = cur_index
                    c = cur_index & 3
                    if c == 1:
                        bytes_written += 1
                        cur_index -= 1
                        if cur_index == 0:
                            bytes_written += w_out
                            cur_index = w_in
                    c = a
                    a += 1
                    a &= 0xFFF
                    temp_buf[c] = z

                    s += 1
                    counter -= 1
        else:
            result[bytes_written] = bl
            bytes_written += 1
            cur_index -= 1
            c = cur_index & 3
            if c == 1:
                bytes_written += 1
                cur_index -= 1
                if cur_index == 0:
                    bytes_written += w_out
                    cur_index = w_in

            c = a
            a += 1
            a &= 0xFFF
            temp_buf[c] = bl

    return result


def decompress3(buf, dest_len, w_in, w_out, write_index):
    temp_buf = bytearray(4096)
    result = bytearray(dest_len)
    x = 0
    z = 0
    a = 4078
    b = 0
    c = 0
    bytes_read = 0
    bytes_written = write_index
    cur_index = w_in
    while bytes_read < len(buf):
        x >>= 1
        if (x & 0x100) == 0:
            b = buf[bytes_read]
            bytes_read += 1
            b |= 0xFF00
            x = b
        bl = buf[bytes_read]
        bytes_read += 1
        if ((x & 0xFF) & 1) == 0:
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
                counter = c
                while counter != 0:
                    c = d & 0xFFF
                    bl = temp_buf[c]
                    result[bytes_written] = bl
                    bytes_written += 1
                    cur_index -= 1
                    if cur_index == 0:
                        bytes_written += w_out
                        cur_index = w_in
                    c = a
                    a += 1
                    a &= 0xFFF
                    temp_buf[c] = bl

                    d += 1
                    counter -= 1
        else:
            result[bytes_written] = bl
            bytes_written += 1
            cur_index -= 1
            if cur_index == 0:
                bytes_written += w_out
                cur_index = w_in

            c = a
            a += 1
            a &= 0xFFF
            temp_buf[c] = bl

    return result


def transform(buf, akb, start_index):
    result = bytearray()
    result += buf[:start_index]
    w_in = akb.right - akb.left
    h_in = akb.bottom - akb.top

    line = buf[start_index : start_index + w_in * 4]
    prev = line[:4]
    result += prev
    for pixel in chunks(line[4:], 4):
        prev = (
            wrapping_add8(pixel[0], prev[0])
            + (wrapping_add8(pixel[1], prev[1]) << 8)
            + (wrapping_add8(pixel[2], prev[2]) << 16)
            + (wrapping_add8(pixel[3], prev[3]) << 24)
        ).to_bytes(4, "little")
        result += prev
    result += buf[start_index + w_in * 4 : start_index + akb.width * 4]

    for line_index, line in enumerate(
        chunks(
            buf[start_index + akb.width * 4 : start_index + h_in * akb.width * 4],
            akb.width * 4,
        )
    ):
        cur_line = line[: w_in * 4]
        prev_line = result[
            start_index
            + (line_index * akb.width * 4) : start_index
            + ((line_index + 1) * akb.width * 4)
        ]
        prev_line = prev_line[: len(cur_line)]
        for pixel, prev in zip(chunks(cur_line, 4), chunks(prev_line, 4)):
            cur = (
                wrapping_add8(pixel[0], prev[0])
                + (wrapping_add8(pixel[1], prev[1]) << 8)
                + (wrapping_add8(pixel[2], prev[2]) << 16)
                + (wrapping_add8(pixel[3], prev[3]) << 24)
            ).to_bytes(4, "little")
            result += cur
        result += line[w_in * 4 :]

    result += buf[len(result) :]
    return result


def apply_filters(buf, akb):
    if akb.compression & 0x40000000 != 0:
        for i in range(akb.height):
            for j in range(akb.width):
                buf[i * akb.width * 4 + j * 4 + 3] = akb.compression & 0xFF
    if akb.compression & 0x80000000 != 0:
        fill = akb.fill
        b = fill & 0xFF
        g = (fill >> 8) & 0xFF
        r = (fill >> 16) & 0xFF
        a = (fill >> 24) & 0xFF

        for i in range(akb.height):
            for j in range(akb.width):
                if i not in range(akb.top, akb.bottom) or j not in range(
                    akb.left, akb.right
                ):
                    buf[i * akb.width * 4 + j * 4] = b
                    buf[i * akb.width * 4 + j * 4 + 1] = g
                    buf[i * akb.width * 4 + j * 4 + 2] = r
                    buf[i * akb.width * 4 + j * 4 + 3] = a
    return buf


def convert_image(filename):
    akb = Akb.from_file(filename)
    d = decompress(
        akb.image_data,
        akb,
    )
    i = Image.frombytes(
        "RGBA",
        (akb.width, akb.height),
        bytes(
            apply_filters(
                bgra_to_rgba(
                    transform(
                        bitmap_to_png(d, akb.width),
                        akb,
                        akb.left * 4 + akb.top * 4 * akb.width,
                    )
                ),
                akb,
            )
        ),
    )
    return i


if __name__ == "__main__":
    for filename in sys.argv[1:]:
        i = convert_image(filename)
        i.save(filename.replace("akb", "png").replace("AKB", "PNG"), "PNG")
