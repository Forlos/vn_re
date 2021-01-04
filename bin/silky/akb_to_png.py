import argparse
import progressbar

from vn_re.archives.silky.akb import convert_image


def init_argparse():
    parser = argparse.ArgumentParser(description="Convert AKB images to PNG")
    parser.add_argument(
        "images",
        help="list of images to convert",
        type=str,
        nargs="+",
    )
    args = parser.parse_args()
    return args


def main():
    args = init_argparse()
    with progressbar.ProgressBar(
        max_value=len(args.images), redirect_stdout=True
    ) as bar:
        for i, image in enumerate(args.images):
            img = convert_image(image)
            img.save(image.replace("akb", "png").replace("AKB", "PNG"), "PNG")
            bar.update(i + 1)


if __name__ == "__main__":
    main()
