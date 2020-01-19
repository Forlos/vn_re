import argparse

from vn_re.archives.acv1.resources import extract_resources


def init_argparse():
    parser = argparse.ArgumentParser(description="Extract resources from ACV1 archives")
    parser.add_argument(
        "archives", help="list of archives to extract", type=str, nargs="+",
    )
    parser.add_argument(
        "-o",
        "--out",
        help="set output directory (default: ext/scripts/)",
        type=str,
        default="ext/",
        dest="out",
    )
    parser.add_argument(
        "--verbose", help="increase output verbosity", action="store_true"
    )
    args = parser.parse_args()
    return args


def main():
    args = init_argparse()
    for archive in args.archives:
        extract_resources(archive, args, "all_file_names.txt")


if __name__ == "__main__":
    main()
