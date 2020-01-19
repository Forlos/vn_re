import argparse

from vn_re.formats.acv1 import Acv1


def init_argparse():
    parser = argparse.ArgumentParser(description="Get hashes from acv1 archives")
    parser.add_argument(
        "lists", help="name lists to merge to one file", type=str, nargs="+",
    )
    parser.add_argument(
        "-o",
        "--out",
        help="output file(default merged_name_list.txt)",
        type=str,
        default="merged_name_list.txt",
        dest="out",
    )
    return parser.parse_args()


def main():
    args = init_argparse()
    merged_set = set()
    for l in args.lists:
        merged_set.update(set(open(l, "r", encoding="cp932").read().splitlines()))
    with open(args.out, "w", encoding="cp932") as merged:
        merged.write("\n".join(n for n in sorted(merged_set)))


if __name__ == "__main__":
    main()
