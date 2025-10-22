# レッスン08 - コードリファレンス

このディレクトリには、レッスン08（OllamaによるAI統合）のコードリファレンスが含まれています。

## ファイル

- `package.json` - Ollamaスクリプトを含むNode.jsプロジェクト設定
- `src/server.js` - Ollamaプロキシを備えたHTTPサーバー
- `src/database.js` - SQLiteデータベース操作
- `public/` - AI統合を備えたフロントエンドファイル
- `scripts/` - Ollamaセットアップ用のヘルパースクリプト

## 学習内容

- ローカルLLMのためのOllamaのセットアップ
- サーバーを介したAPIリクエストのプロキシ
- AI応答のストリーミング
- AI出力のマークダウン解析
- AIリクエストのエラー処理
- 環境設定

## プロジェクトの実行

```bash
# Install dependencies
npm install

# Run development server (includes Ollama setup)
npm run dev
```

これにより、以下が実行されます。
1. Node.jsサーバーを起動します
2. ポート8081でOllamaを起動します
3. Qwen2.5:0.5bモデルをダウンロードします

その後、ブラウザで http://localhost:3000 を開きます。

## APIエンドポイント

これまでのすべてのエンドポイントに加えて、以下が含まれます。
- `POST /api/chat` - AIにメッセージを送信し、応答を取得します