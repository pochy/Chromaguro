# Level 5: 最小 RAG を作る

## この Level でできるようになること

Chroma の検索結果を、LLM に渡す context として整えられるようになります。

この Level の標準コードでは外部 LLM を呼びません。まず「何を読ませるか」を作ります。

## まず知るべき言葉

- **RAG**: 検索した文書を LLM に渡して回答させる構成。
- **context**: LLM に読ませる材料。
- **query expansion**: ユーザー質問を検索向けの語彙に広げること。
- **reranking**: 候補を質問に答えている順に並べ替えること。
- **citation / source**: 回答の根拠として表示する参照元。

## なぜこれを学ぶのか

RAG の基本は「LLM に何を読ませるか」です。

悪い RAG:

```text
top 10 をそのまま全部 prompt に貼る
source を表示しない
重複 chunk を除去しない
metadata filter をかけない
```

良い RAG:

```text
検索範囲を metadata で絞る
広めに候補を取得する
reranking で上位を選ぶ
短く具体的な context に圧縮する
source を回答と一緒に表示する
```

## 手順 1: 最小 RAG の流れを見る

```bash
python levels/level_05_rag/examples/01_minimal_rag.py
```

出力では次を見ます。

```text
Retrieved context
  Chroma が取得した候補。

Prompt for LLM
  LLM に渡す形に整えた prompt。

Mock answer
  本物の LLM の代わりに、context から作った回答例。
```

## 手順 2: query expansion を見る

```bash
python levels/level_05_rag/examples/02_query_expansion.py
```

例:

```text
元の質問:
Chroma の保存方法は？

検索向け query:
Chroma の保存方法は？ PersistentClient path persistence local storage 永続化
```

ユーザーの自然文は短く曖昧です。検索前に語彙を足すと、見つかりやすくなる場合があります。

## 手順 3: reranking を見る

```bash
python levels/level_05_rag/examples/03_reranking.py
```

Chroma の順位と、簡易 reranker 後の順位を比較します。

## よくあるつまずき

```text
Q. なぜ LLM を呼ばないの？
A. 初心者が最初に学ぶべきなのは、回答生成より前の context 作りだからです。

Q. source 表示は必要？
A. 必要です。ユーザーが回答の根拠を確認できるようにします。
```

## 次の Level に進む条件

次ができたら Level 6 に進みます。

```text
検索結果を context として prompt に入れられる
source / section / chunk_id を回答と一緒に表示する理由を言える
query expansion と reranking の役割を説明できる
```

## 公式 docs で確認する箇所

- [Query and Get](https://docs.trychroma.com/docs/querying-collections/query-and-get): Chroma から候補を取得する基本。
- [Metadata Filtering](https://docs.trychroma.com/docs/querying-collections/metadata-filtering): RAG の検索範囲を絞るための filter。

