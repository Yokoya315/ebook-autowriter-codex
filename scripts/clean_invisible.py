#!/usr/bin/env python3
"""不可視文字クリーニングスクリプト（stdlib only）

Codex生成テキストに混入する不可視文字を除去する:
- ZWNJ (U+200C): ゼロ幅非結合子
- ZWS (U+200B): ゼロ幅スペース
- BOM (U+FEFF): バイトオーダーマーク
- Tags (U+E0000-U+E01FF): タグ文字・異体字セレクタ補助

混入するとKindle変換時に「??」として表示される。
"""
import sys
import os
import re


TARGET_FILES = [
    "manuscript.md",
    "manuscript.html",
    "research.md",
    "book_meta.md",
    "listing.txt",
    "kindle_application.txt",
    "cover_prompt.txt",
]


def clean_file(filepath):
    """ファイルから不可視文字を除去し、除去数を返す"""
    if not os.path.exists(filepath):
        return 0

    with open(filepath, "r", encoding="utf-8") as f:
        content = f.read()

    original_len = len(content)

    # Tags + Variation Selectors Supplement (U+E0000-U+E01FF)
    cleaned = re.sub(r"[\U000E0000-\U000E01FF]", "", content)

    # ZWNJ, ZWS, BOM
    cleaned = cleaned.replace("\u200c", "")
    cleaned = cleaned.replace("\u200b", "")
    cleaned = cleaned.replace("\ufeff", "")

    removed = original_len - len(cleaned)

    if removed > 0:
        with open(filepath, "w", encoding="utf-8") as f:
            f.write(cleaned)

    return removed


def clean_all(slug_dir):
    total_removed = 0

    for filename in TARGET_FILES:
        filepath = os.path.join(slug_dir, filename)
        removed = clean_file(filepath)
        if removed > 0:
            print(f"  {filename}: {removed} chars removed")
        total_removed += removed

    if total_removed == 0:
        print("PASS: 不可視文字は検出されませんでした")
    else:
        print(f"CLEANED: 合計 {total_removed} 文字の不可視文字を除去しました")

    return 0


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python clean_invisible.py <output/slug_dir>")
        sys.exit(1)
    sys.exit(clean_all(sys.argv[1]))
