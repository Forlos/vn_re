from vn_re.utils.util import chunks


def bgr_to_rgb(buf):
    result = bytearray()
    for chunk in chunks(buf, 3):
        if len(chunk) != 3:
            break
        a = int.from_bytes(chunk, "little")
        chunk[2] = a & 0xFF
        chunk[1] = (a >> 8) & 0xFF
        chunk[0] = (a >> 16) & 0xFF
        result += chunk
    return result


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
    for chunk in chunks(buf, width):
        result = chunk + result
    return result


def bitmap_to_png_with_padding(buf, width, padding):
    if padding == 0:
        return bitmap_to_png(buf, width)

    result = bytearray()
    for chunk in chunks(buf, width):
        result = chunk[:-padding] + result
    return result


def resolve_color_table(color_index_table, color_table):
    color_table = [c for c in chunks(color_table, 4)]
    result = bytearray()
    for index in color_index_table:
        result += color_table[index]
    return result
