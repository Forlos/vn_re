import sys
import os
import zlib

from vn_re.formats.buriko_arc import BurikoArc


def extract_file(filename):
    buriko_arc = BurikoArc.from_file(filename)
    archive = open(filename, "rb")
    for entry in buriko_arc.file_entries:
        entry.name = entry.name.split(b"\x00")[0]
        name = filename.split("/")[-1] + "/" + str(entry.name, "sjis")
        print(name, entry.file_offset, entry.file_size)

        archive.seek(buriko_arc.file_contents_offset + entry.file_offset)
        contents = archive.read(entry.file_size)
        if contents[4:8] == b"bw  ":
            contents = contents[int.from_bytes(contents[0:4], "little") :]
        os.makedirs(os.path.dirname("ext/" + name), exist_ok=True)
        f = open("ext/" + name, "wb")
        f.write(contents)
        f.close()
    return


if __name__ == "__main__":
    for filename in sys.argv[1:]:
        extract_file(filename)
