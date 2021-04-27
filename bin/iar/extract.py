import argparse

from vn_re.archives.iar.iar import extract_file


def init_argparse():
    parser = argparse.ArgumentParser(description="Extract resources from IAR archives")
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
    for archive in args.archives:
        extract_file(archive)


if __name__ == "__main__":
    main()
