# レッスン10 - コードリファレンス

このディレクトリには、レッスン10（本番環境とドキュメンテーション）のコードリファレンスが含まれています。

## ファイル

- `package.json` - 完全なプロジェクト設定
- `src/` - サーバーおよびデータベースモジュール
- `public/` - フロントエンドファイル
- `scripts/` - ヘルパースクリプト（Ollamaセットアップ、ライブリロード）
- `.env.example` - 環境変数テンプレート
- `.gitignore` - Git無視ルール

## 学習内容

- 環境変数の設定
- 本番環境と開発環境のセットアップ
- プロジェクトのドキュメンテーション
- ヘルパースクリプトの整理
- セキュリティのベストプラクティス
- パフォーマンスの最適化

## プロジェクトの実行

```bash
# Install dependencies
npm install

# Copy environment template
cp .env.example .env

# Run development server with live reload
npm run dev

# Or run in production mode
npm start
```

## 環境変数

`.env.example` に基づいて `.env` ファイルを作成してください：

```env
PORT=3000
OLLAMA_HOST=127.0.0.1:8081
```

## スクリプト

- `scripts/pull-qwen-0.5b.sh` - AIモデルをダウンロード
- `scripts/start-ollama.sh` - Ollamaサーバーを起動
- `scripts/livereload.sh` - 開発用のライブリロード

## 本番環境チェックリスト

- ✅ 環境変数が設定済み
- ✅ データベーススキーマが初期化済み
- ✅ AIモデルがダウンロード済み
- ✅ すべての依存関係がインストール済み
- ✅ ドキュメンテーションが完了済み
- ✅ Gitリポジトリがクリーン