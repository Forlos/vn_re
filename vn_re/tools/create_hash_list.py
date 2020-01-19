import argparse

from vn_re.formats.acv1 import Acv1


def init_argparse():
    parser = argparse.ArgumentParser(description="Get hashes from acv1 archives")
    parser.add_argument(
        "archives", help="acv1 archives to get hashes from", type=str, nargs="+",
    )
    return parser.parse_args()


def main():
    args = init_argparse()
    hash_set = set()
    for archive in args.archives:
        acv = Acv1.from_file(archive)
        for entry in acv.entries:
            hash_set.add(entry.checksum)

    with open("hash_list.txt", "w") as hash_file:
        hash_file.write("\n".join((s).to_bytes(8, "big").hex() for s in hash_set))


if __name__ == "__main__":
    main()
