import sys
import os

from vn_re.formats.gxp import Gxp
from vn_re.utils.util import wrapping_sub

PASSWORD = [
    0x40,
    0x21,
    0x28,
    0x38,
    0xA6,
    0x6E,
    0x43,
    0xA5,
    0x40,
    0x21,
    0x28,
    0x38,
    0xA6,
    0x43,
    0xA5,
    0x64,
    0x3E,
    0x65,
    0x24,
    0x20,
    0x46,
    0x6E,
    0x74,
]


def xor_data_with_password(data, size, offset):
    for i in range(size):
        al = offset & 0xFF
        al += i & 0xFF
        al &= 0xFF
        al ^= PASSWORD[(i + offset) % len(PASSWORD)]
        data[offset + i] ^= al


def decrypt_file_entries(gxp):
    raw_data = bytearray(gxp.file_entries)
    file_entries = list()
    if gxp.header.unk_14 != 0:
        if gxp.header.file_entries_count != 0:
            for i in range(gxp.header.file_entries_count):
                xor_data_with_password(raw_data, 4, 0)
                entry_size = int.from_bytes(raw_data[0:4], "little")
                xor_data_with_password(raw_data, entry_size - 4, 4)
                entry = Gxp.FileEntry.from_bytes(raw_data[:entry_size])

                file_entries.append(entry)
                raw_data = raw_data[entry_size:]

    return file_entries


def extract_file(filename):
    gxp = Gxp.from_file(filename)
    file_entries = decrypt_file_entries(gxp)
    for entry in file_entries:
        # print(entry.file_name, entry.entry_size, entry.file_size, entry.file_offset)
        contents = bytearray(
            gxp.raw_file_data[entry.file_offset : entry.file_offset + entry.file_size]
        )
        xor_data_with_password(contents, entry.file_size, 0)
        name = entry.file_name
        while name.encode("UTF-16LE").endswith(b"\x00\x00"):
            name = name.encode("UTF-16LE")[:-2].decode("UTF-16LE")
        print(name)
        os.makedirs(os.path.dirname("ext/" + name), exist_ok=True)
        f = open("ext/" + name, "wb")
        f.write(contents)
        f.close()

    return


if __name__ == "__main__":
    for filename in sys.argv[1:]:
        extract_file(filename)
