"""Copy the invitation letter image to the submission path.

The entry image is letter.png (a 1024x1024 PNG) sitting next to this
script; this script only copies it to the absolute path the competition
harness reads. No image processing happens here.
"""

import os
import shutil

HERE = os.path.dirname(os.path.abspath(__file__))
SOURCE = os.path.join(HERE, "letter.png")
DEST = "/output/entry.png"


def main():
    os.makedirs(os.path.dirname(DEST), exist_ok=True)
    shutil.copyfile(SOURCE, DEST)


if __name__ == "__main__":
    main()
