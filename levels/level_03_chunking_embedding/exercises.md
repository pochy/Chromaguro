# Level 3 Exercises

## 1. Chunk 単位を変える

`examples/01_chunk_markdown.py` の chunking を見出し単位から段落単位に変えてください。

比較すること:

```text
検索結果の chunk は短くなったか
質問に対する答えが直接含まれやすくなったか
source / section は追跡できるか
```

## 2. overlap を考える

次の文書では、どこで chunk を切ると情報が失われるか考えてください。

```text
料金プランは Basic, Pro, Enterprise です。
Enterprise の SLA は 99.9% です。
この SLA は個別契約で変更される場合があります。
```

## 3. embedding model 変更の影響

`embedding_model` を metadata に入れる理由を、次の観点で説明してください。

```text
再 index
A/B testing
rollback
検索評価
```

## 提出物

次の内容をメモしてください。

```text
1. 01_chunk_markdown.py で作られた chunk 数
2. 検索結果 1 位の section
3. chunk に source / section / chunk_index が必要な理由
4. 自分の文書ならどの単位で chunk するか
```

## 進級チェック

次の質問に答えられたら Level 4 へ進みます。

```text
なぜ PDF 全体を 1 record にしないほうがよいのか？
chunker_version を metadata に残す理由は何か？
embedding model を変えたらなぜ評価し直すのか？
```
