import os
import argparse

from vn_re.archives.silky.silky import extract_file


def init_argparse():
    parser = argparse.ArgumentParser(
        description="Extract resources from SILKY archives"
    )
    parser.add_argument(
        "archives",
        help="list of archives to extract",
        type=str,
        nargs="+",
    )
    args = parser.parse_args()
    return args


def main():
    args = init_argparse()
    os.makedirs("ext", exist_ok=True)
    for archive in args.archives:
        extract_file(archive)


if __name__ == "__main__":
    main()
