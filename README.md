# eBook AutoWriter for Codex

Kindle電子書籍（25,000字・5章構成）を一括生成するChatGPT Codex用ワークフロー。

## 成果物（6点セット）

1. `manuscript.docx` — Word原稿（句点改行処理済み）
2. `listing.txt` — 出版メタデータ（タイトル3案・KW7つ・紹介文）
3. `cover_prompt.txt` — 表紙プロンプト（YAML）
4. `kindle_application.txt` — Kindle申請データ
5. `images/cover.jpg` — 表紙画像（1600x2560px）
6. `images/aplus_1-4.png` — A+コンテンツ画像（970x600px）

## 使い方

Codexで以下のように指示:

```
「AIを使った副業入門」というテーマで電子書籍を作ってください。
```

AGENTS.md に従って10フェーズが自動進行します。

## 必要なツール

- Python 3.8+
- pandoc
- python-docx (`pip install python-docx`)
- Pillow (`pip install Pillow`)
