import sys
import os
import camellia

from vn_re.formats.malie import Malie
from vn_re.utils.util import chunks, rol, ror


def rotate_buffer(buf, n):
    n >>= 4
    n &= 0xF
    n += 0x10
    result = bytearray()
    for i, chunk in enumerate(chunks(buf, 4)):
        if i % 2 == 0:
            result += rol(int.from_bytes(chunk, "little"), n, 32).to_bytes(4, "little")
        else:
            result += ror(int.from_bytes(chunk, "little"), n, 32).to_bytes(4, "little")
    return bytes(result)


def decrypt(buf, n, key):
    buf = rotate_buffer(buf, n)
    cp = camellia.new(key, camellia.MODE_ECB)
    buf = cp.decrypt(buf)
    return buf


def decrypt_file(buf, offset, size, key):
    result = bytearray()
    for i, chunk in enumerate(filter(lambda c: len(c) == 16, chunks(buf, 16))):
        result += decrypt(chunk, offset + i * 0x10, key)
    return result[:size]


def align_size(size):
    if size % 0x10 == 0:
        return size
    else:
        return size + (0x10 - size % 0x10)


def get_path(id, dirs):
    cur = id
    path = ""
    while cur != 0:
        for k, name, r in dirs:
            if cur in r:
                path = f"{name}/{path}"
                cur = k
                break
    return "." + path


def extract_file(filename, key):
    arc = Malie.from_file(filename)
    archive_file = open(filename, "rb")
    archive_file.seek(0x10)
    header = Malie.Header.from_bytes(decrypt(arc.header, 0, key))
    size = (header.file_entries_count * 8 + header.unk2) * 4
    print(header.magic, header.file_entries_count, header.unk2, header.unk3, hex(size))
    file_data_offset = (
        ((header.file_entries_count * 8 + header.unk2) * 4 + 0x10) + 1023
    ) >> 10
    d = [
        decrypt(chunk, (i + 1) * 0x10, key)
        for i, chunk in enumerate(chunks(archive_file.read(align_size(size)), 16))
    ][:size]
    a = bytearray()
    for b in d:
        a += b
    file_entries_size = header.file_entries_count << 5
    file_entries = {
        i: Malie.FileEntry.from_bytes(chunk)
        for i, chunk in enumerate(chunks(a[:file_entries_size], 32))
    }
    file_offset_table = [
        int.from_bytes(chunk, "little") for chunk in chunks(a[file_entries_size:], 4)
    ]
    dirs = [
        (k, v.name, range(v.file_offset, v.file_offset + v.file_size))
        for k, v in file_entries.items()
        if v.type == 0
    ]
    for i, f in filter(lambda f: f[1].type == 1, file_entries.items()):
        name = get_path(i, dirs) + f.name
        print(
            name,
            f.type,
            f.file_offset,
            f.file_size,
            file_offset_table[f.file_offset],
            hex((file_offset_table[f.file_offset] + file_data_offset) << 10),
        )
        off = (file_offset_table[f.file_offset] + file_data_offset) << 10
        archive_file.seek(off)
        d = decrypt_file(
            archive_file.read(align_size(f.file_size)), off, f.file_size, key
        )
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
