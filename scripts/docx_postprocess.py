#!/usr/bin/env python3
"""
DOCX後処理スクリプト for eBook AutoWriter

3つの処理を一括実行:
1. 見出し・章前の改ページ挿入
2. 句点改行（「。」→「。」+ 段落区切り）
3. 段落間の空行挿入（空の w:p 要素を挿入）

使い方:
    python scripts/docx_postprocess.py output/{slug}/manuscript.docx
"""

import sys
from pathlib import Path

try:
    from docx import Document
    from docx.oxml.ns import qn
    from docx.oxml import OxmlElement
    from copy import deepcopy
except ImportError:
    print("python-docx が必要です。インストールしてください:")
    print("  pip install python-docx")
    sys.exit(1)


def postprocess_docx(filepath: str) -> None:
    doc = Document(filepath)

    # === 処理1: 見出し・章前の改ページ ===
    heading_styles = {"Heading 1", "Heading 2", "Heading 3"}
    for para in doc.paragraphs:
        style_name = para.style.name if para.style else ""
        if style_name in heading_styles:
            pPr = para._element.get_or_add_pPr()
            existing = pPr.find(qn("w:pageBreakBefore"))
            if existing is None:
                pb = OxmlElement("w:pageBreakBefore")
                pPr.append(pb)

    # === 処理2: 句点改行 + 段落の切れ目に空行挿入 ===
    paras = list(doc.paragraphs)
    for para in paras:
        style_name = para.style.name if para.style else ""
        text = para.text.strip()

        # 見出しはスキップ
        if style_name.startswith("Heading"):
            continue

        # 画像段落の検出
        ns_wp = "{http://schemas.openxmlformats.org/drawingml/2006/wordprocessingDrawing}"
        has_drawing = bool(
            para._element.findall(f".//{ns_wp}inline")
            or para._element.findall(f".//{ns_wp}anchor")
        )

        if has_drawing:
            p_element = para._element
            parent = p_element.getparent()
            idx = list(parent).index(p_element)
            if idx > 0:
                prev = parent[idx - 1]
                prev_runs = prev.findall(qn("w:r"))
                prev_is_empty = len(prev_runs) == 0
                if not prev_is_empty:
                    empty_before = OxmlElement("w:p")
                    parent.insert(idx, empty_before)
                    idx += 1
            empty_after = OxmlElement("w:p")
            parent.insert(idx + 1, empty_after)
            continue

        if not text:
            continue

        if style_name == "Image Caption":
            continue

        if "。" not in text:
            p_element = para._element
            parent = p_element.getparent()
            idx = list(parent).index(p_element)
            empty_p = OxmlElement("w:p")
            parent.insert(idx + 1, empty_p)
            continue

        sentences = [s for s in text.split("。") if s.strip()]
        if len(sentences) <= 1:
            p_element = para._element
            parent = p_element.getparent()
            idx = list(parent).index(p_element)
            empty_p = OxmlElement("w:p")
            parent.insert(idx + 1, empty_p)
            continue

        p_element = para._element
        parent = p_element.getparent()
        idx = list(parent).index(p_element)
        new_elements = []

        for i, sentence in enumerate(sentences):
            st = sentence.strip()
            if not st:
                continue
            if i < len(sentences) - 1 or text.rstrip().endswith("。"):
                st += "。"

            new_p = deepcopy(p_element)
            for r in new_p.findall(qn("w:r")):
                new_p.remove(r)
            new_r = OxmlElement("w:r")
            if para.runs:
                rPr = para.runs[0]._element.find(qn("w:rPr"))
                if rPr is not None:
                    new_r.append(deepcopy(rPr))
            new_t = OxmlElement("w:t")
            new_t.set(qn("xml:space"), "preserve")
            new_t.text = st
            new_r.append(new_t)
            new_p.append(new_r)
            new_elements.append(new_p)

        # 最後に空行
        empty_p = OxmlElement("w:p")
        new_elements.append(empty_p)

        for j, new_el in enumerate(new_elements):
            parent.insert(idx + j, new_el)
        parent.remove(p_element)

    doc.save(filepath)
    print(f"DOCX後処理完了: {filepath}")
    print("  - 改ページ挿入")
    print("  - 句点改行")
    print("  - 空行挿入")


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("使い方: python scripts/docx_postprocess.py <path/to/manuscript.docx>")
        sys.exit(1)

    docx_path = sys.argv[1]
    if not Path(docx_path).exists():
        print(f"ファイルが見つかりません: {docx_path}")
        sys.exit(1)

    postprocess_docx(docx_path)
