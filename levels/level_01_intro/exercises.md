# Level 1 Exercises

## 1. 文書を追加する

`examples/01_hello_chroma.py` に、緑茶に関する record を 1 件追加してください。

確認すること:

```text
query を「日本茶について知りたい」に変える
緑茶の record が上位に出るか見る
distance を他の record と比較する
```

## 2. ID を設計する

次の 2 つの ID のどちらが実務で扱いやすいか考えてください。

```text
id1
coffee_intro_001
```

考える観点:

```text
再取り込み
デバッグ
source 表示
評価データでの指定
```

## 3. PersistentClient を確認する

`examples/02_persistent_client.py` を 2 回実行してください。2 回目も同じ collection を取得できることを確認します。

## 提出物

次の内容をメモしてください。

```text
1. 01_hello_chroma.py の検索結果 1 位の id
2. その document の内容
3. metadata に入っていた source
4. 02_persistent_client.py を 2 回実行した時の collection count
```

## 進級チェック

次の質問に答えられたら Level 2 へ進みます。

```text
collection とは何か？
document と metadata は何が違うか？
Client と PersistentClient は何が違うか？
distance は大きいほうが近いか、小さいほうが近いか？
```
