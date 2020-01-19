import os
import zlib
import argparse

from vn_re.archives.acv1.scripts import extract_scripts


def init_argparse():
    parser = argparse.ArgumentParser(description="Extract scripts from ACV1 archives")
    parser.add_argument(
        "archives", help="ist of archives to extract", type=str, nargs="+",
    )
    parser.add_argument(
        "-o",
        "--out",
        help="set output directory (default: ext/scripts/)",
        type=str,
        default="ext/scripts/",
        dest="out",
    )
    parser.add_argument(
        "--verbose", help="increase output verbosity", action="store_true"
    )
    args = parser.parse_args()
    return args


def main():
    args = init_argparse()
    os.makedirs(os.path.dirname(args.out), exist_ok=True)
    for archive in args.archives:
        extract_scripts(archive, args)


if __name__ == "__main__":
    main()
