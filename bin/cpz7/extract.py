import os
import argparse

from vn_re.archives.cpz7.cpz7 import extract_file


def init_argparse():
    parser = argparse.ArgumentParser(description="Extract resources from CPZ7 archives")
    parser.add_argument(
        "archives", help="list of archives to extract", type=str, nargs="+",
    )
    args = parser.parse_args()
    return args


def prompt_for_game():
    games = {1: "aoitori.txt", 2: "realive.txt", 3: "seishun.txt"}
    print("Aoi Tori(アオイトリ): 1")
    print("Realive(リアライブ):  2")
    print("Seishun:  3")
    num = int(input("Select game(input number): "), 10)
    with open(games[num], "r") as f:
        data = {
            line.split(" ")[0]: [int(v, 16) for v in line.split(" ")[1:]]
            for line in f.readlines()
        }
        return data


def main():
    args = init_argparse()
    os.makedirs("ext", exist_ok=True)
    for archive in args.archives:
        filename = os.path.basename(archive)
        extract_file(archive, prompt_for_game()[filename])


if __name__ == "__main__":
    main()
