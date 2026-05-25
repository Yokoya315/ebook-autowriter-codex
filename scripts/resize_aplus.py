#!/usr/bin/env python3
"""
A+コンテンツ画像リサイズスクリプト

生成されたA+画像を970x600pxにリサイズする。

使い方:
    python scripts/resize_aplus.py output/{slug}/images/
"""

import sys
from pathlib import Path

try:
    from PIL import Image
except ImportError:
    print("Pillow が必要です。インストールしてください:")
    print("  pip install Pillow")
    sys.exit(1)


def resize_aplus(images_dir: str) -> None:
    target_size = (970, 600)
    images_path = Path(images_dir)

    for i in range(1, 5):
        fname = f"aplus_{i}.png"
        fpath = images_path / fname
        if fpath.exists():
            img = Image.open(fpath)
            img = img.resize(target_size, Image.LANCZOS)
            img.save(fpath)
            print(f"Resized {fname} to {target_size[0]}x{target_size[1]}")
        else:
            print(f"Warning: {fname} not found in {images_dir}")


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("使い方: python scripts/resize_aplus.py <path/to/images/>")
        sys.exit(1)

    resize_aplus(sys.argv[1])
