import os
import argparse
import json

from vn_re.archives.malie.malie import extract_file


def init_argparse():
    parser = argparse.ArgumentParser(
        description="Extract resources from MALIE archives"
    )
    parser.add_argument(
        "archives",
        help="list of archives to extract",
        type=str,
        nargs="+",
    )
    args = parser.parse_args()
    return args


def prompt_for_game():
    games = json.load(open("keys.json"))
    for i, game in enumerate(games.keys()):
        print(f"{game}: {i}")
    num = int(input("Select game(input number): "), 10)
    return list(games.values())[num]


def main():
    args = init_argparse()
    os.makedirs("ext", exist_ok=True)
    for archive in args.archives:
        extract_file(archive, prompt_for_game())


if __name__ == "__main__":
    main()
