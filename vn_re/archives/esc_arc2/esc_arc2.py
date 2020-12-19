import sys
import os

from vn_re.formats.esc_arc2 import EscArc2
from vn_re.utils.util import chunks, wrapping_add


def decrypt_file_entries(file_entries, file_entry_key, key):
    decrypted_file_entries = bytearray()
    for chunk in chunks(file_entries, 4):
        file_entry_key ^= key
        d = wrapping_add(file_entry_key, file_entry_key)
        d ^= file_entry_key
        c = file_entry_key
        c >>= 1
        d = wrapping_add(d, d)
        c ^= file_entry_key
        d = wrapping_add(d, d)
        c >>= 3
        d = wrapping_add(d, d)
        c ^= d
        file_entry_key ^= c
        decrypted_file_entries += (
            int.from_bytes(chunk, "little") ^ file_entry_key
        ).to_bytes(4, "little")
    result = list()
    for chunk in chunks(decrypted_file_entries, 12):
        result.append(EscArc2.FileEntry.from_bytes(chunk))
    return result


def extract_file(filename):
    arc = EscArc2.from_file(filename)
    archive_file = open(filename, "rb")
    unk0 = arc.unk0
    file_count = arc.file_count

    unk0 ^= arc.key
    file_name_table_size = ((unk0 >> 1) ^ unk0) >> 3
    d = wrapping_add(unk0, unk0) ^ unk0
    d = wrapping_add(d, d)
    d = wrapping_add(d, d)
    d = wrapping_add(d, d)
    file_name_table_size ^= d ^ unk0
    file_count ^= file_name_table_size
    file_name_table_size ^= arc.key
    unk0 = (
        wrapping_add(file_name_table_size, file_name_table_size) ^ file_name_table_size
    )
    unk0 = wrapping_add(unk0, unk0)
    unk0 = wrapping_add(unk0, unk0)
    unk0 = wrapping_add(unk0, unk0)
    file_entry_key = ((file_name_table_size >> 1) ^ file_name_table_size) >> 3
    file_entry_key ^= unk0 ^ file_name_table_size
    file_name_table_size = arc.unk2 ^ file_entry_key
    file_count_in_bytes = file_count * arc.file_entry_size

    archive_file.seek(20)
    file_entries = decrypt_file_entries(
        archive_file.read(file_count_in_bytes), file_entry_key, arc.key
    )
    file_names = archive_file.read(file_name_table_size)

    for file in file_entries:
        name = str(
            file_names[file.file_name_table_offset :].split(b"\x00")[0], "ascii"
        ).replace("\\", "/")
        print(
            name,
            file.file_name_table_offset,
            file.file_offset,
            file.file_size,
        )
        archive_file.seek(file.file_offset)
        d = archive_file.read(file.file_size)
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
