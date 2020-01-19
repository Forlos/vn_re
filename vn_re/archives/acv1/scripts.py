import zlib
import progressbar

from vn_re.formats.acv1 import Acv1
from vn_re.utils.util import chunks
from os.path import basename
from vn_re.archives.acv1.constants import (
    MAGIC_AND_SIZE,
    ENTRY_SIZE,
    MASTER_KEY,
    SCRIPT_KEY,
    ACV1_FLAGS_TEXTFILE,
)


def extract_scripts(archive, args):
    with open(archive, "rb") as input_file:
        acv = Acv1.from_file(archive)
        with progressbar.ProgressBar(
            max_value=acv.entry_count, redirect_stdout=True
        ) as bar:
            for i, entry in enumerate(acv.entries):
                xor_key = entry.checksum & 0xFFFFFFFF
                input_file.seek(entry.offset ^ xor_key ^ acv.master_key)
                data = decrypt_script(
                    input_file.read(entry.size ^ xor_key), xor_key, acv.script_key
                )
                # file name is a index in archive + checksum as little endian hex string
                file_name = "{:05}_{}".format(
                    i, (entry.checksum).to_bytes(8, "little").hex()
                )

                if args.verbose:
                    print(
                        "Flags: {:4} Xor_key: {:10} Offset: {:10} Size: {:10} Uncompressed: {:10} {}".format(
                            hex(entry.flags ^ xor_key & 0xFF),
                            hex(xor_key),
                            hex(entry.offset ^ xor_key ^ acv.master_key),
                            hex(entry.size ^ xor_key),
                            hex(entry.uncompressed_size ^ xor_key),
                            file_name,
                        )
                    )

                with open(args.out + file_name, "wb") as output_file:
                    output_file.write(zlib.decompress(data))
                bar.update(i + 1)


def decrypt_script(data, xor_key, script_key):
    result = bytes()
    for chunk in chunks(data, 4):
        if len(chunk) != 4:
            result += chunk
        else:
            result += (int.from_bytes(chunk, "little") ^ xor_key ^ script_key).to_bytes(
                4, "little", signed=False
            )
    return result


def encrypt_scripts(data, xor_key, script_key):
    result = bytes()
    for chunk in chunks(data, 4):
        if len(chunk) != 4:
            result += chunk
        else:
            result += (int.from_bytes(chunk, "little") ^ xor_key ^ script_key).to_bytes(
                4, "little", signed=False
            )
    return result


def write_entry(input_file_name, output_file):
    checksum = bytearray.fromhex(basename(input_file_name).split("_")[1])
    xor_key = int.from_bytes(checksum[0:4], "little")
    size = 0
    uncompressed_size = 0
    offset = output_file.tell()
    with open(input_file_name, "rb") as script:
        data = script.read()
        uncompressed_size = len(data)
        size = output_file.write(
            encrypt_scripts(zlib.compress(data), xor_key, SCRIPT_KEY)
        )
    flags = ((ACV1_FLAGS_TEXTFILE | ACV1_FLAGS_TEXTFILE) ^ xor_key & 0xFF).to_bytes(
        1, "little"
    )
    offset = (offset ^ xor_key ^ MASTER_KEY).to_bytes(4, "little")
    size = (size ^ xor_key).to_bytes(4, "little")
    uncompressed_size = (uncompressed_size ^ xor_key).to_bytes(4, "little")
    return checksum + flags + offset + size + uncompressed_size


def pack_scripts(input_files, output_file):
    output_file.write(bytearray(MAGIC_AND_SIZE + len(input_files) * ENTRY_SIZE))
    archive_header = bytes(
        b"ACV1" + (len(input_files) ^ MASTER_KEY).to_bytes(4, "little")
    )
    for i, input_file in enumerate(input_files):
        archive_header += write_entry(input_file, output_file)

    output_file.seek(0)
    output_file.write(archive_header)
