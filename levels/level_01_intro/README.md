# Level 1: Chroma に触る

## この Level でできるようになること

Chroma に文書を入れて、質問で取り出せるようになります。さらに、一時的に保存する場合と、ディスクに残す場合の違いを理解します。

## まず知るべき言葉

- **client**: Chroma に命令を送る入口。
- **collection**: 検索対象を入れる箱。
- **document**: 検索したい本文。
- **id**: document を識別する名前。
- **metadata**: source や category などの説明情報。
- **distance**: query と document の距離。基本的には小さいほど近い。

## なぜこれを学ぶのか

Chroma の最初の体験はとても単純です。

```text
client を作る
collection を作る
document を入れる
query する
結果を見る
```

公式 Getting Started もこの順番です。この教材では日本語の例で、出力の読み方まで確認します。

## 手順 1: Hello Chroma を実行する

リポジトリのルートで実行します。

```bash
source .venv/bin/activate
python levels/level_01_intro/examples/01_hello_chroma.py
```

期待する出力はこのような形です。

```text
## Hello Chroma
1. coffee_intro_001 distance=...
   metadata={...}
   エスプレッソは...
```

ここで見るのは、まだ 4 つだけです。

```text
id
  どの record が返ったか

document
  検索で見つかった本文

metadata
  source や category などの説明

distance
  query との近さ
```

## 手順 2: 永続化を確認する

永続化とは、プログラムを終了してもデータが残ることです。

```text
chromadb.Client()
  実験用。終了すると消える。

chromadb.PersistentClient(path="./chroma_db")
  ローカル保存用。次回も残る。
```

次を 2 回実行してください。

```bash
python levels/level_01_intro/examples/02_persistent_client.py
```

2 回目も `collection count: 2` のように表示されれば、保存されたデータを再利用できています。

## 手順 3: コードを少しだけ読む

`examples/01_hello_chroma.py` の中で、まず次だけ見ます。

```python
client = chromadb.Client()
collection = recreate_collection(client, "level01_hello")
add_records(collection, records)
result = query_records(collection, query="エスプレッソに使う豆について知りたい")
```

今は `shared/chroma_helpers.py` の中身を全部読む必要はありません。教材用に、embedding などの面倒な部分を隠しています。

## よくあるつまずき

```text
Q. embedding がわからない。
A. 文章を数値に変換したものです。Level 3 で詳しく扱います。

Q. distance が小さいのに、答えとして微妙な文書が出ることがある。
A. 正常です。「近い」と「役に立つ」は違います。Level 4 で改善します。
```

## 次の Level に進む条件

次ができたら Level 2 に進みます。

```text
01_hello_chroma.py を実行できた
02_persistent_client.py を 2 回実行できた
ids / documents / metadatas / distances が何を表すか言える
Client と PersistentClient の違いを言える
```

## 公式 docs で確認する箇所

- [Getting Started](https://docs.trychroma.com/docs/overview/getting-started): install, client, collection, add, query, results の流れ。
- [Chroma Clients](https://docs.trychroma.com/docs/run-chroma/clients): In-Memory Client と Persistent Client の違い。

## 発展: query と get と include

追加で次を実行します。

```bash
python levels/level_01_intro/examples/03_query_vs_get.py
```

見る場所:

```text
get
  ID や filter で record を取り出す。similarity ranking はしない。

query
  embedding 距離で近い順に探す。

include
  documents / metadatas / embeddings / distances のどれを返すか選ぶ。
```

Chroma の結果は column-major な形で返ります。`ids`, `documents`, `metadatas`, `distances` が同じ順番で並んでいることを確認してください。
