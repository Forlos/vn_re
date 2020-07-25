import os
import zlib
import progressbar

from vn_re.utils.util import chunks
from vn_re.utils.crc64 import crc64
from vn_re.formats.acv1 import Acv1
from vn_re.archives.acv1.constants import (
    MAGIC_AND_SIZE,
    ENTRY_SIZE,
    MASTER_KEY,
    ACV1_FLAGS_ENCRYPTED,
    ACV1_FLAGS_PLAIN,
)


def decrypt_entry(data, file_name, size, flags, xor_key):
    if flags == Acv1.AcvFlags.plain.value:
        return data

    if flags & Acv1.AcvFlags.compressed.value == 0:
        return_data = bytearray(data)
        result = size // len(file_name)
        index = 0
        name_index = 0
        while index <= size and name_index < (len(file_name) - 1):
            for i in range(0, result):
                return_data[index] ^= file_name[name_index]
                index += 1
            name_index += 1
        return return_data

    return_data = bytearray()
    for chunk in chunks(data, 4):
        if len(chunk) != 4:
            return_data += chunk
        else:
            return_data += (int.from_bytes(chunk, "little") ^ xor_key).to_bytes(
                4, "little", signed=False
            )
    return zlib.decompress(return_data)


def parse_entry(entry, master_key, file_name, archive, args):
    xor_key = entry.checksum & 0xFFFFFFFF
    offset = entry.offset ^ xor_key ^ master_key
    size = entry.size ^ xor_key
    flags = entry.flags ^ xor_key & 0xFF
    uncompressed_size = entry.uncompressed_size ^ xor_key
    if flags & Acv1.AcvFlags.compressed.value == 0:
        offset ^= file_name[len(file_name) >> 1]
        size ^= file_name[len(file_name) >> 2]
        uncompressed_size ^= file_name[len(file_name) >> 3]

    if args.verbose:
        print(
            "Flags: {:4} Xor_key: {:10} Offset: {:10} Size: {:10} Uncompressed: {:10} {}".format(
                hex(flags),
                hex(xor_key),
                hex(offset),
                hex(size),
                hex(uncompressed_size),
                str(file_name, encoding="cp932"),
            )
        )
    os.makedirs(
        os.path.dirname(args.out + str(file_name, encoding="cp932")), exist_ok=True
    )
    f = open(args.out + str(file_name, encoding="cp932"), "wb")
    archive.seek(offset, 0)
    f.write(decrypt_entry(archive.read(size), file_name, size, flags, xor_key))


def extract_resources(resources_file_name, args, file_name_list):
    extracted = 0

    archive = open(resources_file_name, "rb")
    names = open(file_name_list, "r", encoding="cp932")
    file_names = names.read().splitlines()
    hashes = dict()
    for name in file_names:
        hashes[crc64(name.encode("cp932"))] = name

    acv = Acv1.from_file(resources_file_name)

    with progressbar.ProgressBar(
        max_value=acv.entry_count, redirect_stdout=True
    ) as bar:
        for entry in acv.entries:
            if entry.checksum in hashes.keys():
                parse_entry(
                    entry,
                    acv.master_key,
                    hashes[entry.checksum].encode("cp932"),
                    archive,
                    args,
                )
                extracted += 1
                bar.update(extracted)

    if extracted == acv.entry_count:
        print("{}: Extracted all files!".format(resources_file_name))
    else:
        print(
            "{}: Extracted {} out of {} files.".format(
                resources_file_name, extracted, acv.entry_count
            )
        )


def encrypt_resources(data, flags, file_name, xor_key):
    if flags == Acv1.AcvFlags.plain.value:
        return data

    return_data = bytearray(data)
    if flags & Acv1.AcvFlags.compressed.value:
        for chunk in chunks(data, 4):
            if len(chunk) != 4:
                return_data += chunk
            else:
                return_data += (int.from_bytes(chunk, "little") ^ xor_key).to_bytes(
                    4, "little"
                )
        return zlib.decompress(return_data)

    result = len(data) // len(file_name)
    index = 0
    name_index = 0
    while index <= len(data) and name_index < (len(file_name) - 1):
        for i in range(0, result):
            return_data[index] ^= file_name[name_index]
            index += 1
        name_index += 1
    return return_data


def write_entry(input_file_name, output_file, encrypt):
    file_name = "/".join(input_file_name.split("/")[1:]).encode("cp932")
    print(str(file_name, encoding="cp932"))
    checksum = crc64(file_name).to_bytes(8, "little")
    xor_key = int.from_bytes(checksum[0:4], "little")
    flags = ACV1_FLAGS_PLAIN
    if encrypt:
        flags ^= ACV1_FLAGS_ENCRYPTED
    offset = output_file.tell()
    size = 0
    uncompressed_size = 0
    with open(input_file_name, "rb") as script:
        data = script.read()
        uncompressed_size = len(data)
        size = output_file.write(encrypt_resources(data, flags, file_name, xor_key))

    if flags & Acv1.AcvFlags.compressed.value == 0:
        offset ^= file_name[len(file_name) >> 1]
        size ^= file_name[len(file_name) >> 2]
        uncompressed_size ^= file_name[len(file_name) >> 3]
    flags = (flags ^ xor_key & 0xFF).to_bytes(1, "little")
    offset = (offset ^ xor_key ^ MASTER_KEY).to_bytes(4, "little")
    size = (size ^ xor_key).to_bytes(4, "little")
    uncompressed_size = (uncompressed_size ^ xor_key).to_bytes(4, "little")
    return checksum + flags + offset + size + uncompressed_size


def pack_resources(input_files, output_file, encrypt):
    output_file.write(bytearray(MAGIC_AND_SIZE + len(input_files) * ENTRY_SIZE))
    archive_header = bytes(
        b"ACV1" + (len(input_files) ^ MASTER_KEY).to_bytes(4, "little")
    )
    for i, input_file in enumerate(input_files):
        archive_header += write_entry(input_file, output_file, encrypt)

    output_file.seek(0)
    output_file.write(archive_header)
