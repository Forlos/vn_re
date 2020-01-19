import argparse

from vn_re.utils.crc64 import crc64


def check(hash_set: set, name_set: set) -> set:
    name_hash_set = set([crc64(name.encode("cp932")) for name in name_set])
    name_hash_set.update(
        set([crc64(b"z/" + name.encode("cp932")) for name in name_set])
    )
    name_hash_dict = dict()
    for name in name_set:
        name_hash_dict[crc64(name.encode("cp932"))] = name
        name_hash_dict[crc64(b"z/" + name.encode("cp932"))] = "z/" + name
    print("All hashes:", len(hash_set))
    print("All names:", len(name_hash_set))
    print("Matches found:", len(hash_set & name_hash_set))
    with open("name_list.txt", "w", encoding="cp932") as hash_file:
        hash_file.write(
            "\n".join(name_hash_dict[h] for h in (hash_set & name_hash_set))
        )


def init_argparse():
    parser = argparse.ArgumentParser(description="Extract scripts from ACV1 archives")
    parser.add_argument(
        "hash_list", help="text file containing crc64 hashes", type=str,
    )
    parser.add_argument(
        "name_list", help="text file containing file names", type=str,
    )
    return parser.parse_args()


def main():
    args = init_argparse()
    check(
        set([int(line, 16) for line in open(args.hash_list, "r").read().splitlines()]),
        set(open(args.name_list, "r", encoding="cp932").read().splitlines()),
    )


if __name__ == "__main__":
    main()
