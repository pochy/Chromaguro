# Chromaguro

Chroma を RAG / AI エージェント向けの検索基盤として学ぶための実践チュートリアルです。

単に `add` と `query` の API を覚えるのではなく、検索単位の設計、metadata filtering、chunking、hybrid search、RAG context、検索評価、本番運用までを Level 0 から Level 9 まで順番に扱います。

初心者はまず [START_HERE.md](START_HERE.md) から始めてください。用語が不安な場合は [glossary.md](glossary.md) を参照します。全体設計の詳しい背景は [TUTORIAL.md](TUTORIAL.md) にあります。

## Why Chroma, not SQLite?

SQLite や PostgreSQL は、正確な構造化データ、transaction、join、集計、source of truth に向いています。Chroma はそれとは別の役割を持ちます。

```text
RDB / SQLite:
  ユーザー、権限、請求、原本メタデータ、監査ログを正確に管理する。

Chroma:
  chunked document、embedding、metadata、full-text 条件を使って、
  LLM や agent に渡す context 候補を取り出す。
```

この教材では Chroma を「AI のための retrieval index」として扱います。保存できること自体ではなく、質問に役立つ情報をどう検索し、どう評価し、どう運用するかを学びます。

## ゴール

この教材の最終目標は、次を自分で設計・実装・説明できるようになることです。

```text
ユーザーの質問を受け取る
必要な文書を Chroma から検索する
metadata / keyword / reranking で検索結果を改善する
LLM に渡す context と source を組み立てる
検索品質を評価して改善する
```

Chroma は「LLM の記憶装置」ではなく、LLM に読ませる context を選ぶための検索基盤として扱います。

## 必要な環境

- Python 3.11 以上を推奨
- `pip`
- macOS / Linux / WSL などのターミナル環境

標準のサンプルコードは API キー不要です。教材用 helper が簡易 embedding を明示的に渡すため、最初の学習ルートでは外部 embedding API や Chroma のデフォルト embedding runtime に依存しません。

## セットアップ

リポジトリのルートで実行します。

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

最初に動かすコマンド:

```bash
python levels/level_01_intro/examples/01_hello_chroma.py
```

`coffee_intro_001` や `tea_intro_001` のような ID が表示されれば成功です。

## 学習ロードマップ

| Level | テーマ | できるようになること |
| --- | --- | --- |
| 0 | 検索基盤としての哲学 | Chroma を RAG の context 選択基盤として説明する |
| 1 | Chroma 入門 | 文書を追加し、質問で検索する |
| 2 | CRUD と metadata | record の更新・削除・metadata filter を使う |
| 3 | chunking と embedding | 検索しやすい単位に文書を分割する |
| 4 | 検索改善 | vector search の弱点を keyword / hybrid で補う |
| 5 | RAG | LLM に渡す context と source を組み立てる |
| 6 | 評価 | recall@k / precision@k / MRR で検索品質を測る |
| 7 | API / UI 連携 | `/search` と `/rag` の API を作る |
| 8 | 本番設計 | collection naming、reindex、versioning を考える |
| 9 | 高度な pipeline | query expansion、hybrid fusion、reranking、A/B testing を組み合わせる |

各 Level は同じ流れで進めます。

```text
1. levels/<level>/README.md を読む
2. examples/ のコードを実行する
3. 出力の意味を確認する
4. exercises.md に取り組む
5. 進級条件を満たしたら次の Level へ進む
```

## 完全ローカル方針と Cloud 機能

標準ルートは API キー不要・完全ローカルで動きます。Cloud 専用機能は実行必須にしませんが、設計判断として理解できるように付録で扱います。

| 種類 | 標準ルート | 付録 / Advanced Labs |
| --- | --- | --- |
| `query`, `get`, `where`, `where_document` | 実行する | 詳細比較 |
| `PersistentClient` | 実行する | 運用設計 |
| `HttpClient` / local server | 任意 | `advanced_labs/local_server_http` |
| local / OSS coverage | 付録で確認 | `appendices/local_chroma_coverage.md` |
| Search API / Schema / sparse vector | 疑似実験 | `appendices/cloud_search_api_schema.md` |
| LangChain / LlamaIndex / MCP | 任意 | `advanced_labs/integrations` |

## よく使うコマンド

Level 1 の基本例:

```bash
python levels/level_01_intro/examples/01_hello_chroma.py
python levels/level_01_intro/examples/02_persistent_client.py
```

metadata filtering:

```bash
python levels/level_02_crud_metadata/examples/02_metadata_filtering.py
```

retrieval evaluation:

```bash
python levels/level_06_evaluation/examples/01_retrieval_evaluation.py
```

final project starter:

```bash
python levels/level_09_professional/examples/04_final_project_starter.py
python levels/level_09_professional/examples/05_final_project_api.py
python levels/level_09_professional/examples/06_final_project_api_probe.py
```

API サーバー:

```bash
uvicorn levels.level_07_application.examples.api_server:app --reload
uvicorn levels.level_09_professional.capstone_api:app --reload
```

起動後に確認する endpoint:

```text
GET  /health
GET  /search?q=検索したい内容
POST /rag
```

全 example を確認する場合:

```bash
scripts/validate_tutorial.sh
```

任意の integration lab まで確認する場合:

```bash
pip install -r requirements-integrations.txt
scripts/validate_tutorial.sh --optional-integrations
```

`HttpClient` / local server lab まで確認する場合:

```bash
scripts/validate_tutorial.sh --http --port 9010
```

## メンテナ向け検証

リリース前や大きな教材変更の後は、手元の既存 `.venv` だけでなく fresh clone / fresh venv 相当でも確認します。

```bash
git clone <this-repo-url> /tmp/chromaguro-fresh
cd /tmp/chromaguro-fresh
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python levels/level_01_intro/examples/01_hello_chroma.py
scripts/validate_tutorial.sh
```

任意ラボまで確認する場合は、追加で次を実行します。

```bash
pip install -r requirements-integrations.txt
scripts/validate_tutorial.sh --optional-integrations
scripts/validate_tutorial.sh --http --port 9010
```

## フォルダ構成

```text
README.md                   このファイル
START_HERE.md               初心者向けの進め方
TUTORIAL.md                 教材全体の設計背景
glossary.md                 用語集
requirements.txt            Python 依存関係
requirements-integrations.txt 任意 integration lab 用の依存関係
shared/                     教材用の共通 helper
levels/                     Level 0-9 の教材本体
appendices/                 Chroma 機能マップ・Cloud専用機能・運用・連携の付録
advanced_labs/              local server / integration / agent memory の任意演習
scripts/                    教材の検証スクリプト
```

各 Level の主な構成:

```text
levels/level_xx_*/
  README.md                 その Level の解説
  examples/                 実行できるサンプル
  exercises.md              演習と進級チェック
  data/                     サンプルデータ
```

## 注意点

- コマンドは必ずリポジトリのルートで実行してください。
- `TUTORIAL.md` 内のコード片は設計説明用です。標準の実行ルートでは `levels/*/examples` を使います。
- 永続化のサンプルは各 example ディレクトリ配下に `chroma_db` を作ることがあります。
- 外部 embedding model や LLM を使う発展課題では、各サービスの API キー設定が別途必要です。

## 次に読むもの

初めての場合は [START_HERE.md](START_HERE.md) に進み、Level 0 を短く読んでから Level 1 の Hello Chroma を実行してください。
