# Codex出版 導入手順書

AI出版ラボのメンバー向け、OpenAI Codex で電子書籍を自動制作するための導入ガイドです。

初めての方でも、この手順通りに進めれば **約30分でセットアップが完了** します。

---

## 目次

1. [全体の流れ](#1-全体の流れ)
2. [OpenAI アカウント作成と Pro 契約](#2-openai-アカウント作成と-pro-契約)
3. [GitHub アカウント作成](#3-github-アカウント作成)
4. [リポジトリの fork（コピー）](#4-リポジトリの-forkコピー)
5. [Codex Cloud にリポジトリを接続](#5-codex-cloud-にリポジトリを接続)
6. [ローカル環境の準備（後処理用）](#6-ローカル環境の準備後処理用)
7. [動作確認テスト](#7-動作確認テスト)
8. [電子書籍を作る（実践編）](#8-電子書籍を作る実践編)
9. [ローカル後処理の実行](#9-ローカル後処理の実行)
10. [Kindle に出版する](#10-kindle-に出版する)
11. [よくある質問（FAQ）](#11-よくある質問faq)

---

## 1. 全体の流れ

```
Step 1: OpenAI Plus 以上の契約 ← Codex Cloud を使うために必要
Step 2: GitHub アカウント作成  ← リポジトリ（ファイル置き場）の接続に必要
Step 3: リポジトリを fork     ← 自分用のコピーを作る
Step 4: Codex に接続         ← GitHub と Codex をつなぐ
Step 5: ローカル環境準備      ← 後処理ツールのインストール
Step 6: 動作確認テスト        ← 短いテーマで全フロー確認
```

全部で **約30分** です。一度セットアップすれば、あとは「スタート」と入力するだけで何冊でも作れます。

---

## 2. OpenAI アカウント作成と Plus 以上の契約

Codex Cloud を使うには **OpenAI Plus プラン**（月額 $20）以上が必要です。

> **プラン比較:**
> - Plus（$20/月）— Codex 利用可能（基準量）
> - Pro（$100/月）— 5倍の利用枠
> - Pro（$200/月）— 20倍の利用枠
>
> まずは Plus で始めて、利用量が増えたら上位プランに変更するのがおすすめです。

### 2-1. アカウント作成

1. ブラウザで [https://platform.openai.com/](https://platform.openai.com/) を開く
2. 「Sign up」をクリック
3. メールアドレスとパスワードを入力して登録
4. メール認証を完了する

> 既にChatGPTのアカウントがある方は、同じアカウントでログインできます。

### 2-2. Plus プラン以上に変更

1. ログイン後、左下の **歯車アイコン（Settings）** をクリック
2. **「Billing」** を選択
3. **「Upgrade to Plus」**（$20/月）をクリック（より多く使いたい方は Pro を選択）
4. クレジットカード情報を入力して契約完了

### 2-3. Codex が使えることを確認

1. 左メニューに **「Codex」** という項目が表示されていれば OK
2. クリックして Codex Cloud の画面が開くことを確認

> Codex が表示されない場合は、プランの反映に数分かかることがあります。ページを再読み込みしてください。

---

## 3. GitHub アカウント作成

GitHub は「コードやファイルの保管庫」です。Codex がファイルを読み書きするために必要です。

### 3-1. アカウント作成

1. ブラウザで [https://github.com/](https://github.com/) を開く
2. 「Sign up」をクリック
3. メールアドレス、パスワード、ユーザー名を入力
4. メール認証を完了する

> ユーザー名は英数字で自由に設定できます（例: `taro-kindle`）。あとから変更も可能です。

### 3-2. 初期設定

特別な設定は不要です。アカウントが作成できれば次に進みます。

---

## 4. リポジトリの fork（コピー）

「fork」は、元のリポジトリを自分のアカウントにコピーする操作です。

### 4-1. fork する

1. ブラウザで以下のURLを開く:
   **https://github.com/SCHOOGATE/ebook-autowriter-codex**
2. 右上の **「Fork」** ボタンをクリック
3. 「Create fork」をクリック
4. 自分のアカウントにコピーが作成される

> fork 後のURLは `https://github.com/{あなたのユーザー名}/ebook-autowriter-codex` になります。

### 4-2. ローカルにダウンロード（clone）

後処理をパソコンで行うため、ファイルをダウンロードします。

**Windows の場合:**

1. パソコンで「コマンドプロンプト」または「PowerShell」を開く
2. 以下のコマンドを入力:

```bash
cd Desktop
git clone https://github.com/{あなたのユーザー名}/ebook-autowriter-codex.git
```

> `{あなたのユーザー名}` は実際のGitHubユーザー名に置き換えてください。

**git がインストールされていない場合:**

1. [https://git-scm.com/downloads](https://git-scm.com/downloads) からダウンロード
2. インストーラーを実行（すべてデフォルト設定で OK）
3. コマンドプロンプトを**再起動**してから再度 clone を実行

**Mac の場合:**

1. 「ターミナル」を開く
2. 以下のコマンドを入力:

```bash
cd ~/Desktop
git clone https://github.com/{あなたのユーザー名}/ebook-autowriter-codex.git
```

---

## 5. Codex Cloud にリポジトリを接続

### 5-1. Codex を開く

1. [https://platform.openai.com/](https://platform.openai.com/) にログイン
2. 左メニューの **「Codex」** をクリック

### 5-2. リポジトリを接続

1. **「Connect repository」** ボタンをクリック
2. GitHub の認証画面が表示されたら **「Authorize」** をクリック
3. リポジトリ一覧から **`ebook-autowriter-codex`** を選択
4. 「Connect」をクリック

### 5-3. 接続の確認

- Codex の画面上部にリポジトリ名 `ebook-autowriter-codex` が表示されれば OK
- チャット入力欄が表示されていれば準備完了

> 接続がうまくいかない場合は、GitHub で fork したリポジトリが public（公開）になっていることを確認してください。

---

## 6. ローカル環境の準備（後処理用）

Codex で生成された原稿を Word（DOCX）に変換するために、パソコンにツールをインストールします。

### 6-1. Python のインストール

**Windows:**
1. [https://www.python.org/downloads/](https://www.python.org/downloads/) を開く
2. 「Download Python 3.x」をクリック
3. インストーラーを実行
4. **「Add Python to PATH」にチェックを入れてから** Install をクリック

**Mac:**
```bash
# Homebrew がある場合
brew install python
```

**確認:**
```bash
python --version
# Python 3.8 以上が表示されれば OK
```

### 6-2. pandoc のインストール

pandoc は HTML → DOCX の変換ツールです。

**Windows:**
1. [https://pandoc.org/installing.html](https://pandoc.org/installing.html) を開く
2. Windows 用インストーラー（.msi）をダウンロード
3. インストーラーを実行

**Mac:**
```bash
brew install pandoc
```

**確認:**
```bash
pandoc --version
# バージョンが表示されれば OK
```

### 6-3. Python パッケージのインストール

```bash
pip install python-docx Pillow
```

> エラーが出る場合は `pip3 install python-docx Pillow` を試してください。

### 6-4. 全ツールの確認

```bash
python --version      # Python 3.8+
pandoc --version      # pandoc 2.x or 3.x
pip show python-docx  # Name: python-docx が表示
pip show Pillow       # Name: Pillow が表示
```

4つすべて表示されれば準備完了です。

---

## 7. 動作確認テスト

セットアップが完了したら、短いテーマで全フローを確認します。

### 7-1. Codex でテスト実行

1. Codex の画面を開く
2. チャット欄に **「スタート」** と入力して送信
3. 以下の質問に回答:

```
テーマ: 朝5分でできる瞑想入門
著者名: テスト太郎
参考資料: なし
```

4. ★チェックポイントでは **「OK」** と回答して進める
5. 全フロー完了まで待つ（約15〜30分）

### 7-2. 完了の確認

Codex が「完了しました」と表示したら、以下を確認:

- `output/morning-meditation/` フォルダが作成されている
- `manuscript.md` が 25,000字以上ある
- `images/` に表紙＋A+画像がある
- `completion_report.json` の `overall` が `PASS`

### 7-3. ローカル後処理のテスト

```bash
cd Desktop/ebook-autowriter-codex

# 最新の出力を取得
git pull

# 不可視文字の除去
python scripts/clean_invisible.py output/morning-meditation/

# DOCX変換
pandoc output/morning-meditation/manuscript.html -o output/morning-meditation/manuscript.docx

# 改ページ挿入
python scripts/docx_postprocess.py output/morning-meditation/manuscript.docx

# A+画像リサイズ
python scripts/resize_aplus.py output/morning-meditation/images/
```

`manuscript.docx` を Word で開いて、内容が正しく表示されれば成功です。

---

## 8. 電子書籍を作る（実践編）

動作確認が済んだら、本番のテーマで制作を開始します。

### 8-1. テーマを決める

- 自分の専門知識や経験に基づくテーマがおすすめ
- 読者の悩みを解決する内容が売れやすい
- Amazon で類似書籍を検索して、需要があるか確認

### 8-2. Codex で制作開始

1. Codex で **「スタート」** と入力
2. テーマ・著者名・参考資料を回答
3. ★チェックポイントで内容を確認しながら進行

**★確認ポイントでの判断基準:**

| チェックポイント | 確認すべきこと |
|---------------|-------------|
| ★1: タイトル10案 | 読者にとって魅力的か、検索されやすいキーワードが入っているか |
| ★2: 構成（目次） | 論理的な流れか、読者が知りたい内容が網羅されているか |
| ★3: 表紙プロンプト | テーマに合ったデザインか |
| ★4: 表紙画像 | 文字が読めるか、Amazon で目立つか |
| ★5: A+プロンプト | 訴求ポイントが明確か |
| ★6: A+画像 | 購入ページで効果的に見えるか |
| ★7: 最終確認 | 全体の品質に問題がないか |

修正が必要な場合は、具体的な指示を出してください（例:「タイトルの3番をもう少しキャッチーにして」）。

### 8-3. 参考資料の活用

より高品質な書籍を作るには、参考資料を用意すると効果的です:

- **自分のブログ記事やnote記事のURL** — あなたの知見がそのまま反映される
- **PDFやテキストファイル** — セミナー資料、メモなど
- **参考にしたい書籍のAmazon URL** — 構成やトーンの参考に

参考資料は「スタート」時の質問で入力できます。複数の資料を組み合わせることも可能です。

---

## 9. ローカル後処理の実行

Codex での生成が完了したら、パソコンで以下の後処理を行います。

### 9-1. 最新ファイルの取得

```bash
cd Desktop/ebook-autowriter-codex
git pull
```

### 9-2. 後処理コマンド（順番に実行）

```bash
# {slug} はテーマのフォルダ名に置き換えてください
# 例: ai-side-hustle, morning-meditation など

# 1. 不可視文字の除去（必須）
python scripts/clean_invisible.py output/{slug}/

# 2. HTML → DOCX 変換
pandoc output/{slug}/manuscript.html -o output/{slug}/manuscript.docx

# 3. DOCX に章ごとの改ページを挿入
python scripts/docx_postprocess.py output/{slug}/manuscript.docx

# 4. A+画像を規定サイズにリサイズ
python scripts/resize_aplus.py output/{slug}/images/
```

### 9-3. 完成物の確認

後処理が終わったら、以下を確認してください:

- [ ] `manuscript.docx` を Word で開いて、文章が正しく表示されるか
- [ ] 太字（Bold）が正しく反映されているか
- [ ] 章ごとに改ページされているか
- [ ] `images/cover.png` が鮮明か
- [ ] `images/aplus_1〜4.png` が適切なサイズか

---

## 10. Kindle に出版する

### 10-1. KDP にログイン

1. [https://kdp.amazon.co.jp/](https://kdp.amazon.co.jp/) を開く
2. Amazon アカウントでログイン
3. 「本棚」画面を開く

### 10-2. 新しい本を作成

1. **「電子書籍または有料マンガ」** をクリック
2. 「Kindle 本の詳細」画面で以下を入力:

| 項目 | 入力内容 |
|------|---------|
| 本のタイトル | `book_meta.md` の確定タイトル |
| サブタイトル | `book_meta.md` のサブタイトル |
| 著者 | `book_meta.md` の著者名 |
| 内容紹介 | `listing.txt` の「紹介文」セクション |
| キーワード | `kindle_application.txt` の「検索キーワード」（7つまで） |
| カテゴリ | `kindle_application.txt` の「推奨カテゴリ」 |

### 10-3. 原稿のアップロード

1. 「Kindle 本のコンテンツ」画面に進む
2. **「電子書籍の原稿をアップロード」** をクリック
3. `manuscript.docx` を選択してアップロード
4. 変換完了後、**「プレビューア」** で内容を確認

### 10-4. 表紙のアップロード

1. **「表紙をアップロード」** をクリック
2. `images/cover.png` を選択

### 10-5. 価格設定と出版

1. 「Kindle 本の価格設定」画面に進む
2. ロイヤリティ **70%** を選択（推奨）
3. 価格を設定（`kindle_application.txt` の推奨価格を参考に）
4. **「Kindle 本を出版」** をクリック

> 出版後、審査に通常 24〜72時間かかります。

### 10-6. A+コンテンツの設定

出版後、A+コンテンツを設定して商品ページを充実させます:

1. KDP の本棚 → 該当書籍の **「A+コンテンツの管理」**
2. 「コンテンツの作成を開始」をクリック
3. `images/aplus_1〜4.png` を順番にアップロード
4. 審査申請

---

## 11. よくある質問（FAQ）

### Q: Codex Cloud の利用料金は？

A: OpenAI Plus プラン（月額 $20）以上に含まれています。Plus/Pro プラン契約中は追加料金なしで Codex Cloud を利用できます。利用量が多い場合は Pro（$100/月 or $200/月）で枠を拡大できます。

### Q: 1冊の制作にどれくらい時間がかかる？

A: Codex での生成に約15〜30分、ローカル後処理に約5分、合計 **約20〜35分** です。ただし★チェックポイントでの確認・修正時間は含みません。

### Q: 何冊でも作れる？

A: はい。Plus/Pro プラン契約中は何冊でも制作できます。テーマを変えて「スタート」と入力するだけです（利用枠はプランにより異なります）。

### Q: 参考資料なしでも作れる？

A: はい。テーマだけでも 5層ディープリサーチが自動実行されるため、十分な品質の書籍が生成されます。ただし、自分の専門知識を反映したい場合は参考資料を用意することをおすすめします。

### Q: 生成された原稿を自分で編集してもいい？

A: もちろんです。`manuscript.md`（Markdown）または `manuscript.docx`（Word）を自由に編集できます。特に「はじめに」「おわりに」は自分の言葉で書き換えるとオリジナリティが出ます。

### Q: 表紙が気に入らない場合は？

A: ★確認4で「もう少し明るい色で」「文字を大きくして」などの修正指示を出せます。再生成されるまで何度でも修正可能です。

### Q: Codex が途中でエラーになったら？

A: チャット欄で「続けて」と入力すると、中断した箇所から再開します。それでも改善しない場合は、新しいセッションで「スタート」からやり直してください（リサーチ結果は保持されます）。

### Q: Windows でも Mac でも使える？

A: はい。Codex Cloud はブラウザ上で動作するため、OS を問いません。ローカル後処理も Windows / Mac 両対応です。

### Q: pandoc や Python のインストールが難しい場合は？

A: ローカル後処理を省略して、`manuscript.md`（Markdown原稿）を直接 Word にコピー＆ペーストすることも可能です。ただし、改ページの自動挿入と不可視文字の除去は手動で行う必要があります。

---

## 困ったときは

AI出版ラボのコミュニティ内で質問してください。セットアップでつまずいた場合はスクリーンショット付きで共有いただけるとスムーズに解決できます。
