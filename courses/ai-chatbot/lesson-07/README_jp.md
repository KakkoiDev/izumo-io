# レッスン07: SQLiteを使ったデータベース統合

## テーマ: 「記憶は重要 — 情報を保存し整理する」

## 学習目標
このレッスンの終わりまでに、あなたは以下のことができるようになります。
- データベースの概念と、なぜそれらが必要なのかを理解する
- SQLの基本（SELECT、INSERT、UPDATE、DELETE）を学ぶ
- Node.jsでSQLiteをセットアップする
- チャットアプリケーションのデータベーススキーマを設計する
- 永続的なチャット履歴の保存を実装する
- サーバーからCRUD操作を実行する

## 今週学ぶこと

### 技術的コンセプト
- **データベース**: 永続的なデータ保存
- **リレーショナルデータベース**: テーブル、行、列、リレーションシップ
- **SQL**: データベース操作のための構造化クエリ言語
- **SQLite**: 軽量なファイルベースのデータベース
- **スキーマ設計**: データベース構造の計画
- **CRUD操作**: 作成、読み取り、更新、削除
- **データベース統合**: Node.jsとSQLiteの接続

### SQLとデータベースの概念に焦点を当てる
- `CREATE TABLE` - データベース構造を定義する
- `INSERT INTO` - 新しいレコードを追加する
- `SELECT` - データをクエリする
- `UPDATE` - 既存のレコードを変更する
- `DELETE` - レコードを削除する
- `WHERE`句 - データのフィルタリング
- 主キーとリレーションシップ

## 今週のタスク

### 1. データベースの基礎
- [ ] データベースが何を解決するかを理解する（ファイルへの保存と比較して）
- [ ] 基本的なSQL構文を学ぶ
- [ ] DBeaverまたは他のデータベースビューアをインストールする
- [ ] データベース設計の原則を理解する

### 2. SQLiteのセットアップ
- [ ] Node.js組み込みのsqliteモジュールを使用する（Node 22.5+）
- [ ] データベースファイルを作成する
- [ ] 会話とメッセージのスキーマを設計する
- [ ] 適切な列を持つテーブルを作成する

### 3. チャットボットのデータベース統合
- [ ] database.jsモジュールを作成する
- [ ] 関数を実装する: createConversation, saveMessage, getMessages
- [ ] データベースを使用するようにAPIエンドポイントを更新する
- [ ] ページ読み込み時にチャット履歴を読み込む
- [ ] データ永続性をテストする（サーバー再起動後も履歴が保持されること）

## キャリアレッスン: 「陳腐化しないために毎日学び続ける — テクノロジーの状況は急速に変化する」

### なぜこれが重要なのか
テクノロジーは猛烈な速さで進化しています:
- 新しいフレームワークやツールが常に登場する
- 昨日のベストプラクティスは時代遅れになる
- スキルは維持しなければ陳腐化する
- AIは開発の状況を急速に変化させている

### 実世界での応用

**学習を習慣にする**:
- 定期的に時間を割く（1日20分でもよい）
- テックニュースやリリースノートを追う
- 他の人が書いたコードを読む
- オープンソースプロジェクトに貢献する

**戦略的に学ぶ**:
- テクノロジーをまたいで通用する基礎に焦点を当てる
- 隣接するスキルを学ぶ（バックエンド開発者がDevOpsを学ぶなど）
- 一つの分野で深い知識、他の分野で幅広い知識
- 好奇心に従いつつもキャリア目標と合わせる

**学習ソース**:
- 公式ドキュメント（最も正確）
- 技術ブログやチュートリアル
- カンファレンストークやポッドキャスト
- 深い理解のための書籍
- ハンズオンプロジェクト（最高の学習方法）

**広さと深さのバランス**:
- **T字型スキル**: 一つの分野で深く、他の分野で広く理解する
- あらゆる新しいトレンドを追いかけない
- 新しいテクノロジーが実際の問題を解決するか評価する
- 新しいツールに飛びつく前に現在のツールを習得する

**AIで関連性を保つ**:
- AIツール（GitHub Copilot, Claude, ChatGPT）と共に働くことを学ぶ
- AIが置き換えられないスキル（アーキテクチャ、コミュニケーション、批判的思考）に焦点を当てる
- AIの能力と限界を理解する
- AIを学習を加速させるために使い、置き換えるために使わない

### 遅れをとっている兆候
- 求人情報が持っていないスキルを要求している
- 若い開発者が聞いたことのないツールを知っている
- あなたのソリューションが現代のプラクティスと比較して時代遅れに感じる
- 新しいテクノロジーへの恐れや抵抗

### 継続的な学習は任意ではない
これはプレッシャーではありません。急速に進化する分野でのキャリアの生存と成長にかかわる話です。学習を持続可能で楽しい日常の一部にしましょう。

## このレッスン後のプロジェクトの状態
```
chatbot-project/
├── public/
│   ├── index.html
│   ├── styles.css
│   └── script.js (UPDATED: load history)
├── src/
│   ├── server.js (UPDATED: database endpoints)
│   └── database.js (NEW: database operations)
├── chatbot.db (NEW: SQLite database file)
├── package.json
├── README.md
└── .git/
```

あなたのチャットボットは以下の機能を備えています:
- SQLiteに保存された永続的なチャット履歴
- サーバー再起動後も会話が保持される
- 以前の会話を閲覧する機能
- メッセージと会話のためのデータベーススキーマ
- チャットデータを管理するためのCRUD操作

## 追加リソース

### 必須読書
- [SQLite Official Docs](https://www.sqlite.org/docs.html)
- [SQL Tutorial - W3Schools](https://www.w3schools.com/sql/)
- [Node.js sqlite module](https://nodejs.org/api/sqlite.html)
- [Database Design Basics](https://www.guru99.com/database-design.html)

### ツール
- **DBeaver**: ユニバーサルデータベースビューア（無料、オープンソース）
- **DB Browser for SQLite**: SQLite専用GUIツール

### ビデオチュートリアル
- 「100秒でわかるSQL」
- 「データベース設計チュートリアル」
- 「Node.jsとSQLite」

### 練習課題
1. **TodoアプリDB**: SQLite永続化機能を持つTodoリストを作成する
2. **ユーザー管理**: CRUD操作を持つusersテーブルを作成する
3. **データリレーションシップ**: 外部キーでテーブルをリンクする
4. **検索機能**: メッセージに全文検索を実装する

## 避けるべき一般的な間違い
- データベース接続を適切に閉じない
- SQLインジェクションの脆弱性（パラメーター化されたクエリを使用！）
- データベースエラーを処理しない
- 大規模なリファクタリングが必要となる貧弱なスキーマ設計
- .dbファイルを.gitignoreに追加し忘れる
- データベースファイルをバックアップしない

## 一般的な問題のトラブルシューティング

### データベースがロックされている
- データベースにアクセスしている他のアプリケーションを閉じる
- 以前の接続が閉じられていることを確認する
- 未コミットのトランザクションがないか確認する

### テーブルがすでに存在する
```javascript
// Use IF NOT EXISTS
CREATE TABLE IF NOT EXISTS messages (...)
```

### SQL構文エラー
- SQL構文を注意深く確認する
- 適切な引用符を使用する（文字列にはシングルクォート、数値にはなし）
- 列名がスキーマと一致することを確認する
- 安全のためにパラメーター化されたクエリを使用する

## コード例の構造

database.js:
```javascript
import { DatabaseSync } from 'node:sqlite'

const db = new DatabaseSync('./chatbot.db')

// Create tables
db.exec(`
  CREATE TABLE IF NOT EXISTS conversations (
    id TEXT PRIMARY KEY,
    title TEXT NOT NULL,
    created_at INTEGER DEFAULT (strftime('%s', 'now'))
  )
`)

db.exec(`
  CREATE TABLE IF NOT EXISTS messages (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    conversation_id TEXT NOT NULL,
    role TEXT NOT NULL,
    content TEXT NOT NULL,
    created_at INTEGER DEFAULT (strftime('%s', 'now')),
    FOREIGN KEY (conversation_id) REFERENCES conversations(id)
  )
`)

// Database operations
export const conversations = {
  create(id, title) {
    const stmt = db.prepare('INSERT INTO conversations (id, title) VALUES (?, ?)')
    stmt.run(id, title)
    return { id, title }
  },

  getAll() {
    return db.prepare('SELECT * FROM conversations ORDER BY created_at DESC').all()
  }
}

export const messages = {
  create(conversationId, role, content) {
    const stmt = db.prepare(
      'INSERT INTO messages (conversation_id, role, content) VALUES (?, ?, ?)'
    )
    stmt.run(conversationId, role, content)
  },

  getByConversation(conversationId) {
    return db.prepare(
      'SELECT * FROM messages WHERE conversation_id = ? ORDER BY created_at'
    ).all(conversationId)
  }
}
```

## データベーススキーマ設計

```sql
-- Conversations table
CREATE TABLE conversations (
  id TEXT PRIMARY KEY,           -- Unique conversation ID
  title TEXT NOT NULL,           -- Conversation title
  created_at INTEGER             -- Unix timestamp
)

-- Messages table
CREATE TABLE messages (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  conversation_id TEXT NOT NULL, -- Links to conversations.id
  role TEXT NOT NULL,            -- 'user' or 'assistant'
  content TEXT NOT NULL,         -- Message text
  created_at INTEGER,            -- Unix timestamp
  FOREIGN KEY (conversation_id) REFERENCES conversations(id)
)
```

## 来週のプレビュー
レッスン08では、実際のAIを統合します！チャットボットをOllamaに接続してローカルAI応答を実現し、LLMモデル、プロンプトエンジニアリング、AI統合パターンについて学びます。

## 宿題
1. conversationsおよびmessagesテーブルを含むSQLiteデータベースをセットアップする
2. database.jsにすべてのCRUD操作を実装する
3. データベースを使用するようにサーバーエンドポイントを更新する
4. サーバー再起動後もデータが永続化されることをテストする
5. ページ読み込み時に以前の会話を読み込む
6. DBeaverを使用してデータベースを閲覧する
7. 作業をコミットする
8. Discordであなたの永続的なチャットボットを共有する
