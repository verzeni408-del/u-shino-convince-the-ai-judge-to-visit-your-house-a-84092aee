"""Entry for u-shino-convince-the-ai-judge-to-visit-your-house-a-84092aee.

Copies the pre-rendered summons letter image to /output/entry.png.
Standard library only.
"""

import os
import shutil


def main():
    here = os.path.dirname(os.path.abspath(__file__))
    src = os.path.join(here, "summons.png")
    if not os.path.isfile(src):
        raise SystemExit("missing source image: " + src)
    out_dir = os.environ.get("OUTPUT_DIR", "/output")
    os.makedirs(out_dir, exist_ok=True)
    dst = os.path.join(out_dir, "entry.png")
    shutil.copyfile(src, dst)
    if os.path.getsize(dst) != os.path.getsize(src):
        raise SystemExit("copy size mismatch")
    print("wrote", dst)


if __name__ == "__main__":
    main()
