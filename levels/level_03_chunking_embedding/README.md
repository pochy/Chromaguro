# Level 3: Chunking と Embedding

## この Level でできるようになること

長い文書を検索しやすい単位に分け、各 chunk に metadata を付けて Chroma に入れられるようになります。

## まず知るべき言葉

- **chunk**: 長い文書を分割した検索単位。
- **chunking**: chunk を作ること。
- **embedding**: 文章を数値のリストに変換したもの。
- **parent document**: chunk の元になった文書。
- **chunker_version**: どのルールで chunk を作ったかを表す版。

## なぜこれを学ぶのか

検索される単位はファイルではありません。ユーザーの質問に答えられる意味単位です。

悪い例:

```text
1 つの PDF 全体を 1 record にする
```

良い例:

```text
見出し単位
段落単位
FAQ 単位
コードの関数単位
仕様書の節単位
```

長すぎる document を 1 つの embedding にすると、複数の話題が混ざって検索がぼやけます。

## 手順 1: Markdown を chunk にする

```bash
python levels/level_03_chunking_embedding/examples/01_chunk_markdown.py
```

出力では、次を確認します。

```text
created chunks
  Markdown から何個の chunk ができたか

section
  どの見出しから作られた chunk か

chunk_index
  元文書内の何番目の chunk か
```

## 手順 2: version 情報を見る

```bash
python levels/level_03_chunking_embedding/examples/02_embedding_versions.py
```

`embedding_version` と `chunker_version` が metadata に入っていることを確認します。

```text
embedding model を変えた
chunking ルールを変えた
```

この場合、検索結果が変わるので、どの版で作ったデータか追跡できる必要があります。

## 手順 3: chunk metadata を読む

最低限、次のような metadata を持たせます。

```json
{
  "source": "manual.md",
  "section": "PersistentClient",
  "chunk_index": 2,
  "parent_id": "manual",
  "lang": "ja",
  "chunker_version": "heading-v1"
}
```

## よくあるつまずき

```text
Q. chunk size の正解は？
A. 文書種類と質問の粒度で変わります。最初は見出し・段落・FAQ など自然な単位で始めます。

Q. embedding model を変えたら何が起きる？
A. 距離の意味が変わるので、基本的には再 embedding / 再 index が必要です。
```

## 次の Level に進む条件

次ができたら Level 4 に進みます。

```text
なぜ全文を 1 record にしないのか説明できる
chunk に source / section / chunk_index を付ける理由を言える
embedding model や chunker を変えたら評価し直す必要があると説明できる
```

## 公式 docs で確認する箇所

- [Embedding Functions](https://docs.trychroma.com/docs/embeddings/embedding-functions): Chroma の embedding function の考え方。
- [Add Data](https://docs.trychroma.com/docs/collections/add-data): document / metadata / embedding を追加する流れ。

## 発展: code chunking

追加で次を実行します。

```bash
python levels/level_03_chunking_embedding/examples/03_code_chunking.py
```

Markdown は見出しや段落で分けやすいですが、コードは関数・class・method を単位にすることが多いです。この example では Python の AST を使い、`ClassDef` / `FunctionDef` を chunk にします。

見る場所:

```text
symbol
  検索された関数名・class 名。

start_line / end_line
  UI や source 表示で参照できる位置情報。

chunker_version
  chunking ルールを変えた時に比較できるようにする版。
```

## 発展: collection-owned embedding function

追加で次を実行します。

```bash
python levels/level_03_chunking_embedding/examples/04_custom_embedding_function.py
```

これまでの多くの example では、教材用 helper が `embeddings` と `query_embeddings` を明示的に渡していました。この example では、Chroma collection に `embedding_function` を設定し、`collection.add(documents=...)` と `collection.query(query_texts=...)` で Chroma 側から embedding function が呼ばれる流れを確認します。

見る場所:

```text
documents だけを add している
query_texts だけで query している
それでも embedding function により検索できている
```
