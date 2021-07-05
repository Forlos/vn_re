import sys
import os

from vn_re.formats.pna import Pna

def extract_file(filename):
    pna = Pna.from_file(filename)
    path = os.path.splitext(os.path.basename(filename))[0]

    index = 0
    images = {}
    for entry in pna.data.entries:
        if entry.size == 0:
            continue

        image_data = pna.image_data[index: index + entry.size]
        index += entry.size

        images[entry.id] = image_data

    for i, image_data in enumerate(images.values()):
        image_magic = image_data[:4]
        extension = "png"
        if image_magic == b"RIFF":
            extension = "webp"
        output_path = f"ext/{path}_{i}.{extension}"

        os.makedirs("ext", exist_ok=True)
        f = open(output_path, "wb")
        f.write(image_data)

if __name__ == "__main__":
    for filename in sys.argv[1:]:
        try:
            extract_file(filename)
        except Exception as e:
            print(filename, e)

