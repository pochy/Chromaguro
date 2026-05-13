# Chroma Clients

## PersistentClient

ローカル開発で Chroma のデータを残す場合は `PersistentClient` を使います。`path` に保存先ディレクトリを指定すると、プログラムを終了しても collection と record が残ります。

RDB を source of truth として使い、Chroma は検索用 index として再構築できる状態にしておくと、embedding model や chunker を変更しやすくなります。

## HttpClient

本番構成に近づける場合は Chroma server を別プロセスで起動し、アプリケーションから `HttpClient` で接続します。アプリ process と Chroma process を分けることで、API server、worker、batch job から同じ検索基盤を利用できます。

## Collection Versioning

embedding model や chunking strategy を変えると、距離の意味が変わります。同じ collection を直接上書きする前に、`docs_embed_v1` と `docs_embed_v2` のように version を分けて評価します。
