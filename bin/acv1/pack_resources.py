import argparse

from os import walk
from os.path import join
from vn_re.archives.acv1.resources import pack_resources


def init_argparse():
    parser = argparse.ArgumentParser(description="Pack resources to ACV1 archive")
    parser.add_argument(
        "output", help="name of output file", type=str,
    )
    parser.add_argument(
        "input",
        help="directory containing resources(directory not included)",
        type=str,
    )
    parser.add_argument(
        "-e",
        "--encrypt",
        help="encrypt files in target archive(by default they are left unencrypted)",
        action="store_true",
        dest="encrypt",
    )
    return parser.parse_args()


def main():
    args = init_argparse()
    input_files = []
    for root_path, _, file_names in walk(args.input):
        for filename in file_names:
            input_files.append(join(root_path, filename))
    input_files.sort()
    with open(args.output, "wb") as output_file:
        pack_resources(input_files, output_file, args.encrypt)


if __name__ == "__main__":
    main()
