# Level 9 Exercises

## 1. Pipeline を削る

`examples/01_advanced_pipeline.py` から query expansion を外し、検索結果がどう変わるか確認してください。

## 2. tenant 分離を強化する

`examples/02_multi_tenant_ab_test.py` を organization ごとに collection を分ける設計へ書き換えてください。

## 3. A/B testing を追加する

chunker_version `v1` と `v2` の recall@3 を比較する評価データを追加してください。

## 4. agentic memory を設計する

次を実行してください。

```bash
python levels/level_09_professional/examples/03_agentic_memory.py
```

semantic / procedural / episodic memory のどれを保存すべきか、自分のアプリで 3 つ例を書いてください。

## 5. final project starter を自分の文書に近づける

次を実行してください。

```bash
python levels/level_09_professional/examples/04_final_project_starter.py
python levels/level_09_professional/examples/05_final_project_api.py
python levels/level_09_professional/examples/06_final_project_api_probe.py
```

`data/final_project_docs/` の Markdown を 1 つ追加する想定で、次を設計してください。

```text
source に何を入れるか
section をどう決めるか
doc_type をどう分類するか
tenant_id をどこで決めるか
gold question をどう追加するか
API response の sources に何を含めるか
diagnostics をユーザーに見せるか、内部ログだけにするか
```

## 提出物

次の内容をメモしてください。

```text
1. advanced pipeline の rewritten query
2. expanded query
3. fused context の上位 3 件
4. tenant_a と tenant_b の検索結果の違い
5. final project starter の selected context と source 表示
6. final project で最初に作る最小構成
```

## 進級チェック

次の質問に答えられたら、このチュートリアルの基礎からプロフェッショナル編までの流れを完了です。

```text
query expansion はいつ必要か？
hybrid search は何を補うのか？
reranking は Chroma の代わりに何をしているのか？
evaluation logging はなぜ必要か？
自分のアプリで最初に測る指標は何か？
```
