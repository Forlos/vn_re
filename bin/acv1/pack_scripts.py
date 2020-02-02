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
    parser.add_argument(
        "-k",
        "--script-key",
        help="script key to use when decrypting",
        type=int,
        default=None,
        dest="script_key",
    )
    return parser.parse_args()


def prompt_for_game():
    with open("script_keys.txt", "r") as script_keys:
        keys = [
            [k.strip() for k in line.split("|")] for line in script_keys.readlines()
        ]
        for i, key in enumerate(keys):
            print("[{}] {} {}".format(i, key[0], key[1]))
        num = int(input("Select game(input number): "), 10)
        return int(keys[num][2], 16)


def main():
    args = init_argparse()
    if args.script_key is None:
        args.script_key = prompt_for_game()
    input_files = sorted(
        [
            join(args.input, f)
            for f in listdir(args.input)
            if isfile(join(args.input, f))
        ]
    )
    with open(args.output, "wb") as output_file:
        pack_scripts(input_files, output_file, args.script_key)


if __name__ == "__main__":
    main()
