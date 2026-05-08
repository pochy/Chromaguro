# Chroma DB 実践チュートリアル

このリポジトリは `TUTORIAL.md` の設計に沿って、Chroma を「ベクトル DB の API」ではなく、RAG / AI エージェント向けの検索基盤として学ぶための実践教材です。

初心者はまず [START_HERE.md](START_HERE.md) から始めてください。用語がわからない場合は [glossary.md](glossary.md) を見ます。

## 学び方

Level 0 から Level 9 まで順番に進めます。各 Level は独立したフォルダになっており、`README.md` で設計思想を読み、`examples/` のコードを動かし、`exercises.md` で手を動かします。

```text
Level 0  検索基盤としての哲学
Level 1  Chroma 入門
Level 2  CRUD と metadata
Level 3  chunking と embedding
Level 4  vector search の限界と hybrid search
Level 5  RAG の最小構成
Level 6  retrieval evaluation
Level 7  API / UI 連携
Level 8  production 設計
Level 9  advanced retrieval pipeline
```

## セットアップ

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

この教材の標準コードは API キー不要です。実務用の embedding model や LLM を使う例は、各 Level の発展課題として扱います。

最初に実行するコマンドはこれだけです。

```bash
python levels/level_01_intro/examples/01_hello_chroma.py
```

## 実行例

```bash
python levels/level_01_intro/examples/01_hello_chroma.py
python levels/level_02_crud_metadata/examples/02_metadata_filtering.py
python levels/level_06_evaluation/examples/01_retrieval_evaluation.py
```

Level 7 の API 例は次のように起動します。

```bash
uvicorn levels.level_07_application.examples.api_server:app --reload
```

## この教材の立場

Chroma を学ぶ目的は、単に `add` と `query` を覚えることではありません。重要なのは、ユーザーの質問に対して「役に立つ情報」を取り出せる検索品質を設計することです。

そのため、この教材では次の順番で力を積み上げます。

```text
保存する
↓
絞り込む
↓
検索単位を設計する
↓
vector search の弱点を補う
↓
RAG に渡す context を作る
↓
検索品質を測る
↓
API / UI / 本番運用へ広げる
```

## フォルダ構成

```text
TUTORIAL.md                 元の設計仕様
README.md                   この教材の入口
START_HERE.md               初心者向けの進め方
glossary.md                 用語集
requirements.txt            実行に必要な Python 依存関係
shared/                     教材用の共通ヘルパー
levels/                     Level 0-9 の実教材
```
