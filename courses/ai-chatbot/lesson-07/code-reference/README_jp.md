# レッスン 07 - コードリファレンス

このディレクトリには、レッスン 07 (SQLite を使用したデータベース統合) のコードリファレンスが含まれています。

## ファイル

- `package.json` - Node.js プロジェクト設定
- `src/server.js` - API エンドポイントを持つ HTTP サーバー
- `src/database.js` - SQLite データベース操作
- `public/` - フロントエンドファイル (HTML, CSS, JS)
- `.gitignore` - Git 無視ルール (データベースファイルを除外)

## 学習内容

- SQLite データベースのセットアップ
- テーブルとスキーマの作成
- CRUD 操作 (作成、読み取り、更新、削除)
- プリペアドステートメントを使用した SQL クエリ
- データベース操作のための API エンドポイント
- 外部キーとリレーションシップ

## プロジェクトの実行

```bash
# 開発サーバーを実行
npm run dev
```

データベースファイル `chatbot.db` は、サーバーを初めて実行したときに自動的に作成されます。

## API エンドポイント

- `GET /api/health` - ヘルスチェック
- `GET /api/conversations` - すべての会話を取得
- `POST /api/conversations` - 新しい会話を作成
- `GET /api/conversations/:id` - ID で会話を取得
- `PUT /api/conversations/:id` - 会話のタイトルを更新
- `DELETE /api/conversations/:id` - 会話を削除
- `POST /api/messages` - 会話にメッセージを追加