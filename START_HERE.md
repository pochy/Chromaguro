# START HERE: 初心者のための進め方

この教材は、Chroma を使って「質問に役立つ情報を探し、RAG や AI エージェントに渡す検索基盤」を作れるようになるためのチュートリアルです。

最初から公式ドキュメントを全部読む必要はありません。まずこの教材で手を動かし、各 Level の最後に公式ドキュメントで同じ概念を確認します。

## まず今日やること

初心者なら、初日は `START_HERE.md` を読み、Level 0 を 10 分だけ確認し、Level 1 の `Hello Chroma` を動かせば十分です。

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python levels/level_01_intro/examples/01_hello_chroma.py
```

出力に `coffee_intro_001` や `tea_intro_001` が表示されれば成功です。意味が全部わからなくても構いません。最初の目的は「文書を入れて、質問で取り出す」体験をすることです。

Level 0 は思想の入口です。全部を完璧に理解しようとせず、「Chroma は LLM に読ませる文書を選ぶ道具」という一文だけ持って Level 1 に進んでください。

## この教材の読み方

各 Level は同じ順番で進めます。

```text
1. README.md を読む
2. まず知るべき言葉を確認する
3. examples/ のコードを実行する
4. 出力のどこを見るか確認する
5. exercises.md の提出物を作る
6. 進級チェックに答えられたら次の Level へ進む
7. 公式ドキュメントで該当箇所だけ確認する
```

読み物だけで理解しようとしないでください。Chroma は「出力を見ながら少しずつ意味がわかる」タイプの道具です。

## Level 別ロードマップ

| Level | 何をする | 次へ進む条件 |
| --- | --- | --- |
| 0 | Chroma を検索基盤として考える | Chroma は LLM の記憶ではなく context を選ぶ仕組みだと言える |
| 1 | 文書を入れて質問で取り出す | `ids`, `documents`, `metadatas`, `distances` の意味がざっくり言える |
| 2 | 更新・削除・metadata filter を使う | `where` で検索範囲を絞れる |
| 3 | chunking と embedding を学ぶ | なぜ長文を 1 record にしないのか説明できる |
| 4 | vector search の弱点を補う | keyword / full-text が必要な場面を判別できる |
| 5 | 最小 RAG の context を作る | LLM に渡す context と source を組み立てられる |
| 6 | 検索品質を測る | recall@k / precision@k / MRR を使って比較できる |
| 7 | API として使う | `/search` と `/rag` の request / response を説明できる |
| 8 | 本番運用を考える | reindex / versioning / tenant filter の方針を説明できる |
| 9 | 高度な retrieval pipeline を設計する | query expansion, hybrid, reranking, evaluation を組み合わせられる |

## 公式ドキュメントとの付き合い方

公式ドキュメントは正確ですが、初心者には前提が多いです。この教材では、まず手元の例を動かし、その後に公式ドキュメントで「同じことを公式はどう説明しているか」を確認します。

最初に見るのはこの 3 つだけです。

- [Getting Started](https://docs.trychroma.com/docs/overview/getting-started): install, client, collection, add, query の流れを見る。
- [Chroma Clients](https://docs.trychroma.com/docs/run-chroma/clients): `Client()` と `PersistentClient()` の違いを見る。
- [Query and Get](https://docs.trychroma.com/docs/querying-collections/query-and-get): `query`, `get`, `where`, `where_document` の位置づけを見る。

Level 2 以降で必要になったら、metadata filtering や full-text search のページを読みます。

## 「永続化」がわからない人へ

永続化とは、プログラムを終了してもデータが消えないように、ディスクに保存することです。

```text
chromadb.Client()
  メモ帳に一時的に書くようなもの。
  プログラムが終わると消える。

chromadb.PersistentClient(path="./chroma_db")
  ノートに保存するようなもの。
  次にプログラムを動かしても残っている。
```

最初は `Client()` で構いません。Level 1 の後半で `PersistentClient()` を動かし、「2 回実行しても collection が残る」ことを確認します。

## 詰まった時

まず次を確認してください。

```bash
pwd
python3 --version
source .venv/bin/activate
python --version
pip install -r requirements.txt
```

実行コマンドは必ずリポジトリのルート、つまり `TUTORIAL.md` があるディレクトリで打ちます。

Python のエラーが出たら、いきなり全部理解しようとせず、次の順で見ます。

```text
ModuleNotFoundError
  依存関係が入っていない。pip install -r requirements.txt を実行する。

No such file or directory
  コマンドを打つ場所が違う。pwd を確認する。

collection already exists
  同じ名前の collection を作ろうとしている。教材コードでは基本的に回避済み。

embedding runtime returned status 400
  Chroma のデフォルト embedding runtime や外部 embedding API が呼ばれて失敗している可能性があります。
  この教材では、まず levels/*/examples のコードを使ってください。教材用 helper は embeddings と query_embeddings を明示しているため、標準ルートでは外部 embedding runtime を使いません。
  TUTORIAL.md 内の公式ドキュメント風スニペットを直接実行する場合は、embedding function や API key の設定が別途必要になることがあります。
```

## 学習ペースの目安

```text
Level 0-2: 1-2日
Level 3-4: 2-3日
Level 5-6: 2-4日
Level 7: 1-2日
Level 8-9: 3日以上
```

急がなくて構いません。各 Level の進級チェックに答えられることを優先してください。
