import sys
import os

from vn_re.formats.silky import Silky
from vn_re.utils.util import wrapping_add8


def decompress(buf, dest_len):
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


def extract_file(filename):
    arc = Silky.from_file(filename)
    archive_file = open(filename, "rb")
    for entry in arc.entries.entries:
        entry.name = str(
            bytes(
                [
                    wrapping_add8(b, entry.name_length - i)
                    for i, b in enumerate(entry.name)
                ]
            ),
            "sjis",
        )
        entry.file_size = int.from_bytes(entry.file_size.to_bytes(4, "big"), "little")
        entry.uncompressed_file_size = int.from_bytes(
            entry.uncompressed_file_size.to_bytes(4, "big"), "little"
        )
        entry.file_offset = int.from_bytes(
            entry.file_offset.to_bytes(4, "big"), "little"
        )
        name = entry.name
        print(
            entry.name_length,
            entry.name,
            entry.file_size,
            entry.uncompressed_file_size,
            entry.file_offset,
        )
        archive_file.seek(entry.file_offset)
        d = archive_file.read(entry.file_size)
        if entry.file_size < entry.uncompressed_file_size:
            d = decompress(d, entry.uncompressed_file_size)

        os.makedirs(os.path.dirname("ext/" + name), exist_ok=True)
        output_file = open(
            "ext/" + name,
            "wb",
        )
        output_file.write(d)
        output_file.close()
    return


if __name__ == "__main__":
    for filename in sys.argv[1:]:
        extract_file(filename)
