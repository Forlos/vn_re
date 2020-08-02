import sys
import os
import hashlib

from vn_re.formats.pfs import Pfs
from vn_re.utils.util import chunks


def decrypt_file(contents, password):
    for i in range(len(contents)):
        contents[i] ^= password[i % len(password)]
    return


def extract_file(filename):
    pfs = Pfs.from_file(filename)

    s = hashlib.sha1()
    s.update(pfs.raw_archive_data)
    digest = s.digest()
    for entry in pfs.entries:
        print(entry.file_name, entry.file_size, entry.file_offset)
        archive = open(filename, "rb")
        archive.seek(entry.file_offset)

        contents = bytearray(archive.read(entry.file_size))
        decrypt_file(contents, digest)

        name = entry.file_name.decode("utf8").replace("\\", "/")
        os.makedirs(os.path.dirname("ext/" + name), exist_ok=True)
        f = open("ext/" + name, "wb")
        f.write(contents)
        f.close()

    return


if __name__ == "__main__":
    for filename in sys.argv[1:]:
        extract_file(filename)
