# レッスン06 - コードリファレンス

このディレクトリには、レッスン06 (Node.jsとサーバー開発) のコードリファレンスが含まれています。

## ファイル

- `package.json` - Node.jsプロジェクト設定
- `src/server.js` - 静的ファイル配信用のHTTPサーバー
- `public/index.html` - HTML構造
- `public/styles.css` - CSSスタイル
- `public/script.js` - JavaScript機能

## 学習内容

- Node.js HTTPサーバーの作成
- 静的ファイルの配信 (HTML、CSS、JS)
- ファイルの分離 (HTML、CSS、JSを別々のファイルに)
- MIMEタイプとContent-Typeヘッダー
- public/ディレクトリを使用したプロジェクト構造

## プロジェクトの実行

```bash
# Install dependencies (if any)
npm install

# Run development server (with auto-reload)
npm run dev

# Or run normally
npm start
```

その後、ブラウザで http://localhost:3000 を開きます。