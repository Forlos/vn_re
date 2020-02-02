import os
import zlib
import argparse

from vn_re.archives.acv1.scripts import extract_scripts


def init_argparse():
    parser = argparse.ArgumentParser(description="Extract scripts from ACV1 archives")
    parser.add_argument(
        "archives", help="list of archives to extract", type=str, nargs="+",
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
    parser.add_argument(
        "-k",
        "--script-key",
        help="script key to use when decrypting",
        type=int,
        default=None,
        dest="script_key",
    )
    args = parser.parse_args()
    return args


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
    os.makedirs(os.path.dirname(args.out), exist_ok=True)
    for archive in args.archives:
        extract_scripts(archive, args, args.script_key)


if __name__ == "__main__":
    main()
