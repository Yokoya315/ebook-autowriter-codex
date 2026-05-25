# eBook AutoWriter for Codex

電子書籍（25,000字・5章構成）をテキスト執筆 → 高品質DOCX → 出版メタデータ → 表紙JPEG → A+画像4枚 → Kindle申請データを一括生成する量産向けスキル。

## 言語

- 日本語で応答する
- プロンプト・技術用語は英語OK

## 全体フロー（10フェーズ）

```
Phase 1  → 参考資料の受け取り
Phase 2  → 5層ディープリサーチ（並列推奨）
Phase 2.5 → タイトル10案提案 & 基本情報確定（★唯一のユーザー確認）
Phase 3  → 構成設計（目次）
Phase 4  → 原稿執筆 25,000字（並列推奨）
Phase 5  → DOCX変換 + 後処理スクリプト
Phase 6  → 出版メタデータ生成（listing.txt）
Phase 7  → 表紙プロンプト生成（cover_prompt.txt）
Phase 8  → 表紙JPEG生成（gpt-image-2）
Phase 9  → A+コンテンツ画像4枚生成（gpt-image-2）
Phase 10 → Kindle申請TXT出力
```

## 自動進行ルール

Phase 2.5（タイトル確定）のみユーザー確認を行う。他のPhaseはすべて確認なしで自動進行する。

## 6点セット出力

```
output/{slug}/
├── manuscript.md             # Markdown原稿
├── manuscript.docx           # Word原稿（句点改行処理済み）
├── listing.txt               # 出版メタデータ
├── cover_prompt.txt          # 表紙プロンプト（YAML）
├── kindle_application.txt    # Kindle申請データ
├── research.md               # リサーチ結果
├── book_meta.md              # 確定メタ情報
└── images/
    ├── cover.jpg             # 表紙画像 1600×2560px
    ├── aplus_1.png           # A+ 問題提起 970×600px
    ├── aplus_2.png           # A+ 煽り・共感
    ├── aplus_3.png           # A+ 解決策
    └── aplus_4.png           # A+ CTA
```

## ビルド・テストコマンド

```bash
# DOCX変換
pip install python-docx Pillow
pandoc manuscript.md -o manuscript.docx --from markdown --to docx --standalone

# DOCX後処理
python scripts/docx_postprocess.py output/{slug}/manuscript.docx

# 画像リサイズ（A+コンテンツ）
python scripts/resize_aplus.py output/{slug}/images/
```

---

## Phase 1: 参考資料の受け取り

ユーザーからテーマと参考資料を受け取る。

受け取れる形式:
- ファイル（PDF、テキスト、Markdown、DOCX）
- URL（Web検索で内容取得）
- テキスト（直接貼り付け）
- 複数資料の組み合わせ

資料を受け取ったら即座にPhase 2へ進む。

---

## Phase 2: 5層ディープリサーチ

参考資料からテーマ・キーワードを抽出し、以下の5層リサーチを実行する。
可能であれば並列で実行して高速化する。

### Layer 1: YouTube専門家の知見
- 「{テーマ} やり方 解説」「{テーマ} プロ 実践」等で検索
- 再生回数が多い動画・専門チャンネルを5〜10本特定
- 各動画の要点・独自ノウハウ・具体的手法を抽出

### Layer 2: note専門家の記事
- 「{テーマ} site:note.com」で検索
- 上位5〜10記事の内容を取得
- 著者の専門性、独自フレームワーク、具体的数値を抽出

### Layer 3: SNS/ショート動画トレンド
- Instagram、TikTokのバズキーワード・切り口を調査
- インフルエンサーの推しポイント、Z世代に響く表現を抽出

### Layer 4: 市場・競合・書籍分析
- Amazon上位書籍5冊の目次構成・レビュー分析
- 星1-2レビューから読者の不満・期待を抽出
- 競合にない切り口・空白地帯を特定

### Layer 5: 読者の悩み・ニーズ
- Yahoo知恵袋、Q&Aサイトで10件以上の悩みを収集
- 初心者がぶつかる壁、「こういう本があれば」という要望を抽出

### リサーチ品質基準
- YouTube: 最低5本
- note: 最低5記事
- SNSトレンド: バズワード3つ以上
- 競合書籍: 最低3冊
- 読者の声: 最低10件

結果を `output/{slug}/research.md` に保存。

---

## Phase 2.5: タイトル提案 & 基本情報確定（★唯一のユーザー確認ポイント）

### このフェーズだけはユーザー確認を行う

1. リサーチ結果から「次が読みたくなる」書籍構成案を1つ提案
2. 売れるタイトル/サブタイトル案を**10個**生成（以下の型を必ず混ぜる）

| # | 型 | 例 |
|---|---|---|
| 1 | ベネフィット直球型 | 「3日で身につく〇〇」 |
| 2 | 数字提示型 | 「7つの〇〇ルール」 |
| 3 | 問いかけ型 | 「なぜ〇〇は××なのか？」 |
| 4 | 否定・常識破り型 | 「〇〇をやめなさい」 |
| 5 | ターゲット限定型 | 「初心者のための〇〇入門」 |
| 6 | ストーリー型 | 「ゼロから〇〇になった話」 |
| 7 | 比較・選択型 | 「AとBどっちがいい？」 |
| 8 | 完全ガイド型 | 「〇〇完全攻略ガイド」 |
| 9 | 時短・効率型 | 「最短で〇〇する方法」 |
| 10 | 権威・最新型 | 「2026年最新版 〇〇のすべて」 |

3. ユーザーに確定してもらう:
   - タイトル + サブタイトル（10案から選択 or 改変 or 新規）
   - 著者名（必須・空欄不可）

4. 確定情報を `output/{slug}/book_meta.md` に保存

**確定するまで次のPhaseに進まない。確定後は自動進行を再開。**

---

## Phase 3: 構成設計

`book_meta.md` が確定済みであることを確認し、目次を詳細化する。

### 目次テンプレート

```
書籍タイトル: {確定タイトル}
想定読者: {テーマから推定}
読者のゴール: {この本を読んで何ができるようになるか}

はじめに（1,200〜1,500字）
  - この本の目的 / 読者への約束 / 本書の使い方

第1章: {章タイトル}（4,000〜5,000字）
  1.1〜1.5 各節

第2章〜第5章: 同上の形式

おわりに（1,200〜1,500字）
```

### 構成ルール
- 章の順序: 基礎 → 応用 → 実践
- 各章は独立して読んでも価値がある
- 章をまたいで内容が行き来しない
- 読者が「次に何をすればいいか」がわかる

確認なしでPhase 4へ進む。

---

## Phase 4: 原稿執筆（25,000字）

### 並列執筆推奨

```
Agent 1: はじめに + 第1章 + 第2章
Agent 2: 第3章 + 第4章
Agent 3: 第5章 + おわりに
```

各エージェントに渡す情報: 目次全体、参考資料の該当部分、リサーチ結果、執筆ルール、他エージェントの担当範囲。

### 執筆ルール（厳守）

- 総文字数: 約25,000字
- 1章あたり: 4,000〜5,000字
- はじめに/おわりに: 各1,200〜1,500字
- 文体: **です・ます調で統一**
  - NG: 「〜だ」「〜である」
  - OK: 「〜です」「〜になります」「〜してみましょう」「〜してください」
- 段落: 3〜4文ごとに改行
- 具体例: 各章に最低2つ
- **画像タグ禁止**: `<!-- [IMAGE] -->` 等は一切使用しない
- **表（テーブル）禁止**: 比較情報は箇条書きで
- **コードブロック禁止**: コマンドは通常テキストで
- **ASCII図禁止**: 罫線文字は使わない
- **ユーザー名禁止**: 「読者の皆さん」等を使用
- **著者情報禁止**: 原稿本文に著者名・プロフィールを入れない
- **文字数厳守**: 各章の執筆後に文字数カウントし、4,000字未満は加筆

### 改ページ・整形ルール

- 各章（`##`）の直前に `\newpage`
- 各節（`###`）の直前に `\newpage`
- はじめに・おわりにの直前にも `\newpage`
- 見出しの前後に空行1行
- 段落間に空行1行
- 箇条書きの前後に空行1行

### 見出しレベル

- `#`: 書籍タイトル（冒頭1回のみ）
- `##`: 章タイトル（はじめに、第1章〜第5章、おわりに）
- `###`: 節タイトル（1.1, 1.2, ...）
- `####`: 小見出し（必要に応じて）

完成原稿を `output/{slug}/manuscript.md` に保存。確認なしでPhase 5へ。

---

## Phase 5: DOCX変換 + 後処理

### DOCX整形3大ルール

1. 目次（TOC）を入れない
2. 段落間にスペース（空行）を入れる
3. 見出し・章の前に改ページを入れる

### 手順

1. manuscript.md の整形チェック（チェックリスト下記）
2. 不備は自動修正
3. Pandocで変換（--tocは使わない）
4. python scripts/docx_postprocess.py で後処理

### 変換前チェックリスト

- 各章の直前に \newpage がある
- 各節の直前に \newpage がある
- 見出しの前後に空行がある
- 段落間に空行がある
- テーブル記法が使われていない
- コードブロックが使われていない
- ASCII図が使われていない
- 画像タグが混入していない

### Pandocコマンド

```bash
cd output/{slug}
pandoc manuscript.md -o manuscript.docx --from markdown --to docx --standalone
```

### 後処理

```bash
python scripts/docx_postprocess.py output/{slug}/manuscript.docx
```

スクリプトが行う処理:
1. 見出し・章前の改ページ挿入
2. 句点改行（「。」→ 「。」+ 段落区切り）
3. 段落間の空行挿入（空の `w:p` 要素を挿入）

確認なしでPhase 6へ。

---

## Phase 6: 出版メタデータ生成

### 手順

1. manuscript.md からテーマ・ターゲット・キーコンセプトを抽出
2. Web検索でキーワードリサーチ
3. メタデータを生成して `listing.txt` に出力

### 生成内容

#### タイトル・副タイトル（3案）

```
【提案N：コンセプト】
タイトル: {30文字以内、メインキーワード必須}
副タイトル: {関連キーワード×接続 + ベネフィット文}
```

最重要ルール: メインキーワードは**必ずタイトルに入れる**。副タイトルだけは禁止。

3案の方向性: 1=網羅性、2=好奇心、3=簡単さ・具体的成果

#### 著者名

```
{メインKW}（{テーマ1}×{テーマ2}）活用研究室
```

#### キーワード（7行 × 各50文字以内）

- タイトルに含まれるKWは除外
- メインKW 2-3個、関連KW 2-3個、ロングテール 1-2個
- 各行内は半角スペース区切り

#### フリガナ

タイトル・副タイトル・著者名のカタカナ・ローマ字を生成。
変換ルール: ひらがな→カタカナ / ×→カケル / 漢字→読み / 数字→読み

#### 紹介文（3,000〜4,000文字厳守）

- emoji禁止、区切り線禁止、装飾記号禁止、HTMLタグ禁止
- プレーンテキストのみ（`・` `--` `「」` 数字 括弧はOK）
- 目次を含める（SEO対策）
- トーンに合わせて4タイプから自動選択:
  - A: おだやか共感型（初心者向け）
  - B: 成果アピール型（副業・稼ぐ系）
  - C: BtoB戦略型（マーケ・戦略）
  - D: 技術入門型（IT・ツール）

確認なしでPhase 7へ。

---

## Phase 7: 表紙プロンプト生成

### 手順

1. manuscript.md からジャンル・テーマを自動抽出
2. スタイルを自動選択（A〜E）
3. カラーパレットを自動選択
4. YAMLプロンプトを生成
5. `cover_prompt.txt` に出力

### スタイル自動選択

```
ビジネス/自己啓発/話し方/時間術 → A（テキストインパクト型）
料理/健康/ダイエット/生活改善 → B（イラスト＋テキスト型）
マンガ解説/AI活用/テック入門 → C（マンガ・アニメ型）
投資/金融/経営戦略/不動産 → D（ダーク・プレミアム型）
副業/ハウツー → E（ハイブリッド型）
```

### カラーパレット

| ジャンル | メイン | アクセント | ハイライト |
|---------|--------|----------|-----------|
| ビジネス | #FFFFFF | #1A1A2E | #E74C3C |
| 自己啓発 | #FFF3CD | #E74C3C | #FFD700 |
| 投資・マネー | #1B2A4A | #D4AF37 | #FFFFFF |
| 健康・ダイエット | #E8F5E9 | #FF6B6B | #2E7D32 |
| AI・テック | #1A73E8 | #FFD700 | #FF5252 |
| 副業・稼ぐ系 | #FFF9C4 | #1565C0 | #FF5722 |
| 心理学 | #0D1B2A | #E8872A | #D4AF37 |

### YAMLプロンプト設計原則

- フラット構造: text_elements に全テキスト集約
- 簡潔記述: 1要素 = 2-3行
- 色はHEX値+色名: `#1A73E8 blue`
- portrait 2:3 比率
- **著者名は絶対に入れない**
- constraintsに `"DO NOT include any author name"` を必ず含める

確認なしでPhase 8へ。

---

## Phase 8: 表紙JPEG生成（gpt-image-2）

### 画像生成にはgpt-image-2を使用する

cover_prompt.txt のYAMLプロンプトを元に、gpt-image-2で表紙画像を生成する。

### 生成指示

```
Professional Kindle book cover, portrait orientation 2:3 ratio (1600x2560px).
Title: "{確定タイトル}" in large bold Japanese text, centered upper area.
Subtitle: "{確定サブタイトル}" in smaller Japanese text below title.
Style: {選択スタイル}
Color palette: {メイン} / {アクセント} / {ハイライト}
Background: {テーマに合った背景}
Design:
- Z-pattern eye flow: title → visual → subtitle
- Title text clearly readable
- Professional modern Kindle cover aesthetic
- High contrast between text and background
- DO NOT include any author name on the cover
- No watermarks, no logos
High resolution, 4K quality.
```

生成した画像を `output/{slug}/images/cover.jpg` に保存。

確認なしでPhase 9へ。

---

## Phase 9: A+コンテンツ画像4枚生成（gpt-image-2）

サイズ: 970×600px（横長）、形式: PNG、枚数: 4枚

### 各画像の役割と生成指示

#### aplus_1.png（問題提起）

```
Wide landscape banner 970x600px. {テーマに関連する読者の悩みや問題状況を視覚化}.
Dark muted tones suggesting difficulty. Emotional relatable scene.
Professional advertising banner, modern illustration, no composition labels, no watermarks, 4K.
NO text labels like "問題提起" inside the image.
```

#### aplus_2.png（煽り・共感）

```
Wide landscape banner 970x600px. {問題が深刻化した状況、読者への共感}.
Dramatic contrast, intense colors amplifying urgency.
Professional banner, strong emotional impact, no composition labels, 4K.
```

#### aplus_3.png（解決策）

```
Wide landscape banner 970x600px. {本書の解決策、変化後の明るい状況}.
Bright optimistic colors, vivid fresh hopeful tones. Transformative uplifting scene.
Professional banner, aspirational mood, no composition labels, 4K.
```

#### aplus_4.png（CTA）

```
Wide landscape banner 970x600px. {本書を手に取る行動を促すビジュアル}.
Energetic accent colors. Book cover or reading device featured.
Professional banner, call-to-action focused, no composition labels, 4K.
```

### リサイズ（生成後必須）

```bash
python scripts/resize_aplus.py output/{slug}/images/
```

確認なしでPhase 10へ。

---

## Phase 10: Kindle申請TXT出力

### 生成内容

1. タイトル・サブタイトル・著者名（漢字・カタカナ・ローマ字）
2. 書籍説明文（PASONA法則 / HTML / 3,000〜4,000字厳守）
3. カテゴリー5つ（各カテゴリー横に1位書籍の総合ランキング順位を併記）
4. キーワード40個以上（7マス × 各50文字以内）

### PASONA法則

P: 問題 → A: 煽り・親近感 → S: 解決策 → O: 提案 → N: 絞り込み → A: 行動

- HTML形式（`<p>`, `<strong>` タグ使用）
- PASONA項目名は本文に出さない
- 3,000字未満は必ず加筆

### カテゴリー

- Web検索でAmazon Kindleカテゴリーを調査
- 1位書籍の総合ランキングが5,000位以上のジャンルを優先
- 必ず5つ提案

出力先: `output/{slug}/kindle_application.txt`

---

## 完了時の報告

全Phase完了後、以下を表示:

```
電子書籍の制作が完了しました。

成果物一覧:
1. manuscript.docx — 原稿Word（約{N}字）
2. listing.txt — 出版メタデータ
3. cover_prompt.txt — 表紙プロンプト
4. kindle_application.txt — Kindle申請データ
5. images/cover.jpg — 表紙画像
6. images/aplus_1〜4.png — A+コンテンツ画像
```

---

## 制約事項

- Markdown表（テーブル）を原稿内で使わない
- コードブロックを原稿内で使わない
- 著者情報を原稿本文に入れない
- 表紙に著者名を入れない
- 画像タグを原稿に入れない
- ASCII罫線図を使わない
