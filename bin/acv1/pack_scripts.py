import argparse

from os import listdir
from os.path import isfile, join
from vn_re.archives.acv1.scripts import pack_scripts


def init_argparse():
    parser = argparse.ArgumentParser(description="Pack scripts to ACV1 archive")
    parser.add_argument(
        "output", help="name of output file", type=str,
    )
    parser.add_argument(
        "input", help="directory containing script files", type=str,
    )
    return parser.parse_args()


def main():
    args = init_argparse()
    input_files = sorted(
        [
            join(args.input, f)
            for f in listdir(args.input)
            if isfile(join(args.input, f))
        ]
    )
    with open(args.output, "wb") as output_file:
        pack_scripts(input_files, output_file)


if __name__ == "__main__":
    main()
