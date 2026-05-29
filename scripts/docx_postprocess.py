#!/usr/bin/env python3
"""
DOCX後処理スクリプト for eBook AutoWriter v2

処理内容:
1. 見出し（H1/H2）前の改ページ挿入

※ 句点改行はMarkdown段階で実施済み（1文=1段落）
※ Boldのrun構造を壊す句点分割処理は廃止（v1からの変更点）

使い方:
    python scripts/docx_postprocess.py output/{slug}/manuscript.docx
"""

import sys
from pathlib import Path

try:
    from docx import Document
    from docx.oxml.ns import qn
    from docx.oxml import OxmlElement
except ImportError:
    print("python-docx が必要です。インストールしてください:")
    print("  pip install python-docx")
    sys.exit(1)


def postprocess_docx(filepath: str) -> None:
    doc = Document(filepath)

    # 見出し（H1/H2）前の改ページ挿入
    page_break_count = 0
    for para in doc.paragraphs:
        style_name = para.style.name if para.style else ""
        if style_name in ("Heading 1", "Heading 2"):
            pPr = para._element.get_or_add_pPr()
            if pPr.find(qn("w:pageBreakBefore")) is None:
                pb = OxmlElement("w:pageBreakBefore")
                pPr.append(pb)
                page_break_count += 1

    doc.save(filepath)
    print(f"DOCX後処理完了: {filepath}")
    print(f"  - 改ページ挿入: {page_break_count} 箇所")


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("使い方: python scripts/docx_postprocess.py <path/to/manuscript.docx>")
        sys.exit(1)

    docx_path = sys.argv[1]
    if not Path(docx_path).exists():
        print(f"ファイルが見つかりません: {docx_path}")
        sys.exit(1)

    postprocess_docx(docx_path)
