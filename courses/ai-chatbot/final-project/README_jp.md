# AIチャットボット - 最終プロジェクト

ローカルLLM統合、会話履歴、および永続ストレージを備えたフルスタックのAIチャットボットアプリケーション。

## 機能

### 主要機能
- **チャットインターフェース**: 最新のUIを備えた、クリーンで直感的なメッセージングインターフェース
- **AI統合**: Ollama (qwen2.5:0.5bモデル) を介したローカルAI応答
- **会話管理**: 会話の作成、名前変更、削除
- **永続ストレージ**: 全チャットデータ用のSQLiteデータベース
- **自動生成タイトル**: AIによる会話タイトル
- **コンテキストメニュー**: 会話アクションのための最新のPopover API + CSSアンカーポジショニング

### 技術的ハイライト
- **ゼロフレームワークバックエンド**: 素のNode.js HTTPサーバー (Expressなし)
- **組み込みSQLite**: Node.jsの実験的なSQLiteを使用 (ネイティブ依存関係なし)
- **モダンCSS**: Popover API、CSSアンカーポジショニング (Chrome 125+ / Safari TP)
- **ホットリロード**: 開発用のネイティブ `node --watch`
- **環境設定**: dotenvによる構成管理

## 技術スタック

- **フロントエンド**: HTML5, CSS3, Vanilla JavaScript (ES6+)
- **バックエンド**: 素のNode.js HTTPサーバー (フレームワークなし)
- **データベース**: Node.js組み込みSQLite (`node:sqlite`)
- **AI/ML**: Ollama (ローカルLLM - qwen2.5:0.5b)
- **開発ツール**: node --watch, concurrently

## 前提条件

- **Node.js**: v24+ (組み込みSQLiteサポートのため)
- **Ollama**: ローカルにインストールされ、実行されていること
- **ブラウザ**: Chrome 125+ または Safari Technology Preview (Popover APIのため)

## インストール

### 1. 依存関係のインストール

```bash
npm install
```

これにより、以下の2つの依存関係のみがインストールされます。
- `concurrently` - 複数の開発プロセスを実行
- `dotenv` - 環境変数管理

### 2. 環境設定

```bash
cp .env.example .env
```

カスタム設定が必要な場合は、`.env` を編集してください。

```env
PORT=3000                    # サーバーポート
OLLAMA_HOST=127.0.0.1:8081  # Ollamaサーバーアドレス
OLLAMA_MODEL=qwen2.5:0.5b   # 使用するAIモデル
DB_PATH=./chatbot.db        # データベースファイルパス
```

### 3. AIモデルのセットアップ (一度のみ)

```bash
npm run setup
```

これはOllamaからqwen2.5:0.5bモデルをプルします。一度だけ実行する必要があります。

### 4. 開発の開始

**オプションA - Nodeサーバーのみ** (Ollamaがすでにシステム全体で実行されている場合):
```bash
npm run dev
```

**オプションB - すべてを一緒に** (Node + Ollama):
```bash
npm run dev:all
```

**オプションC - Ollamaサーバーのみ**:
```bash
npm run ollama
```

### 5. アプリケーションを開く

次のURLにアクセスしてください: **http://localhost:3000**

## 使用方法

### 会話の開始
1. 入力フィールドにメッセージを入力します
2. **Enter**キーを押すか、**送信**をクリックします
3. AIがローカルのOllamaモデルを使用して応答します
4. 最初のやり取りの後、会話タイトルが自動生成されます

### 会話の管理
- **履歴の表示**: **≡** ボタンをクリックしてサイドバーを切り替えます
- **会話の切り替え**: サイドバーで任意の会話をクリックします
- **名前の変更**: **⋮** をクリック → タイトルを選択 → 編集 → Enterキーを押す
- **削除**: **⋮** をクリック → 削除 (確認あり)
- **新しい会話**: サイドバーの **+ 新しいチャット** をクリックします

## プロジェクト構造

```
ai-chatbot/final-project/
├── public/                 # フロントエンドファイル
│   ├── index.html         # メインHTML
│   ├── styles.css         # スタイル (Popover API CSSを含む)
│   └── script.js          # フロントエンドロジック
├── src/                   # バックエンドソース
│   ├── server.js          # HTTPサーバー (120行)
│   └── database.js        # SQLite操作 (93行)
├── .env.example           # 環境テンプレート
├── .env                   # ローカル設定 (gitignored)
├── package.json           # 依存関係とスクリプト
├── chatbot.db             # SQLiteデータベース (自動作成)
└── README.md             # このファイル
```

## APIドキュメント

### RESTエンドポイント

#### 会話

**GET /api/conversations**
```json
Response: {
  "conversations": [
    {
      "id": "string",
      "title": "string",
      "created_at": 1234567890,
      "messages": [
        {"id": 1, "role": "user", "content": "...", "created_at": 1234567890}
      ]
    }
  ]
}
```

**POST /api/conversations**
```json
Request: {"id": "uuid", "title": "Untitled"}
Response: {"conversation": {...}}
```

**GET /api/conversations/:id**
```json
Response: {"conversation": {...}}
```

**PUT /api/conversations/:id**
```json
Request: {"title": "New Title"}
Response: {"success": true}
```

**DELETE /api/conversations/:id**
```json
Response: {"success": true}
```

#### メッセージ

**POST /api/messages**
```json
Request: {
  "conversationId": "uuid",
  "role": "user|assistant",
  "content": "message text"
}
Response: {"message": {...}}
```

#### AIプロキシ

**POST /api/chat** (Ollama proxy)
```json
Request: {
  "model": "qwen2.5:0.5b",
  "messages": [{"role": "user", "content": "..."}],
  "stream": false
}
Response: {
  "message": {"role": "assistant", "content": "..."}
}
```

**POST /api/generate** (Ollama proxy)
```json
Request: {
  "model": "qwen2.5:0.5b",
  "prompt": "...",
  "stream": false
}
Response: {"response": "..."}
```

## データベーススキーマ

### conversations
```sql
CREATE TABLE conversations (
  id TEXT PRIMARY KEY,
  title TEXT NOT NULL,
  created_at INTEGER NOT NULL
)
```

### messages
```sql
CREATE TABLE messages (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  conversation_id TEXT NOT NULL,
  role TEXT NOT NULL,
  content TEXT NOT NULL,
  created_at INTEGER NOT NULL,
  FOREIGN KEY (conversation_id) REFERENCES conversations(id) ON DELETE CASCADE
)
```

## npmスクリプト

- `npm run setup` - AIモデルをプル (一度限りのセットアップ)
- `npm run dev` - Node.jsサーバーのみを起動 (ホットリロード有効)
- `npm run dev:all` - Node.js + Ollamaを一緒に起動
- `npm run start` - Node.jsサーバーを起動 (プロダクションモード)
- `npm run ollama` - Ollamaサーバーのみを起動
- `npm run model:pull` - AIモデルを更新/再プル

## トラブルシューティング

### Ollama接続失敗

**症状**: コンソールに「Ollama connection failed」エラーが表示される

**解決策**:
1. Ollamaが実行されていることを確認します: `ollama list`
2. モデルがインストールされていることを確認します: `ollama pull qwen2.5:0.5b`
3. `.env` の `OLLAMA_HOST` がOllamaサーバーと一致していることを確認します

### ポートが既に使用中

**症状**: `EADDRINUSE: address already in use :::3000`

**解決策**:
```bash
# ポート3000でプロセスを強制終了
lsof -ti:3000 | xargs kill -9

# または.envでPORTを変更
PORT=3001
```

### データベースがロックされています

**症状**: 「database is locked」エラー

**解決策**:
1. `chatbot.db` への他の接続を閉じます
2. サーバーを再起動します
3. `chatbot.db` を削除します (データは失われます)

### Popover APIが機能しない

**症状**: コンテキストメニュー (⋮) が機能しない

**解決策**:
- **Chrome 125+** または **Safari Technology Preview** を使用します
- または、古いブラウザ用にPopover APIポリフィルを追加します

### Unicode文字が正しく表示されない

**症状**: 絵文字が �� またはランダムな文字として表示される

**解決策**: これは修正済みのはずです (MIMEタイプで charset=utf-8)。まだ壊れている場合は、ブラウザのエンコード設定を確認してください。

## 開発メモ

### なぜ素のNode.jsか？

Expressではなく素のNode.jsを選択した理由は次のとおりです。
- **シンプルさ**: 120行 vs Expressでの200行以上
- **ゼロ依存関係**: フレームワークのオーバーヘッドなし (50以上の依存関係を回避)
- **学習**: HTTPの基本を理解する
- **モダン**: Node.jsプラットフォームの機能を活用

### なぜ組み込みSQLiteか？

better-sqlite3ではなくNode.jsの実験的なSQLiteを使用している理由は次のとおりです。
- **ネイティブコンパイルなし**: node-gypのビルド問題を回避
- **ゼロ依存関係**: Node.js v22+に組み込み済み
- **同じAPI**: better-sqlite3と同様
- **ローカルアプリに最適**: 個人的なプロジェクトには十分な安定性

### ブラウザの互換性

このアプリは最新のWeb APIを使用しています:
- **Popover API**: Chrome 125+、Safari TP、Firefox (ポリフィルあり)
- **CSSアンカーポジショニング**: Chrome 125+、Safari TP
- **ES6モジュール**: すべてのモダンブラウザ

古いブラウザの場合は、ポリフィルの追加を検討してください。

## パフォーマンス

- **API応答時間**: 10ミリ秒未満 (AI生成を除く)
- **AI応答時間**: 3〜15秒 (ハードウェアとモデルに依存)
- **データベースクエリ**: 高速検索のためにインデックス付け済み
- **メモリ使用量**: 約50MB (サーバー) + モデルメモリ (Ollama)

## セキュリティに関する注意

⚠️ **このアプリはローカルでのみ使用してください**

- 認証システムなし
- 入力サニタイズなし (ローカルユーザーを信頼)
- SQLiteインジェクションはプリペアドステートメントにより防止
- CORS無効 (同一オリジンのみ)
- 公開展開向けのプロダクション対応ではありません

## 今後の機能強化

潜在的な改善点:
- [ ] AI応答のストリーミング (SSEまたはWebSockets)
- [ ] メッセージの編集と削除
- [ ] 会話の検索とフィルタリング
- [ ] 会話のエクスポート (JSON/Markdown)
- [ ] 複数モデルの選択
- [ ] カスタムシステムプロンプト
- [ ] ダークモードの切り替え
- [ ] メッセージタイムスタンプの表示
- [ ] コード構文のハイライト表示

## 学習成果

このプロジェクトは以下を実証します:
- ✅ フルスタック開発 (フロントエンド + バックエンド + データベース)
- ✅ RESTful APIの設計と実装
- ✅ 外部キーを使用したSQLiteデータベース操作
- ✅ ローカルAI統合 (Ollama)
- ✅ 最新のWeb API (Popover、アンカーポジショニング)
- ✅ 環境ベースの構成
- ✅ エラー処理とエッジケース
- ✅ クリーンなコード構成とドキュメント

## ライセンス

MITライセンス - 教育目的および個人利用は無料です。

## 謝辞

- **Ollama** - ローカルLLMランタイム
- **Qwen2.5** - 高速で効率的な言語モデル
- **Node.jsチーム** - 組み込みSQLiteサポート
- **オープンソースコミュニティ** - 最新のWeb APIに対して

---

**ステータス**: ✅ 完了 (フェーズ1-3)
**最終更新**: 2025-10-05
**Node.jsバージョン**: v24.9.0+