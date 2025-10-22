# レッスン08：AI統合 - OllamaによるローカルAI

## テーマ：「知性の増幅 - AIをパートナーとして活用する」

## 学習目標
このレッスンを終えるまでに、あなたは以下のことができるようになります。
- 大規模言語モデル（LLM）の基本を理解する
- ローカルAIのためにOllamaをセットアップし、設定する
- さまざまなLLMモデルとその特性について学ぶ
- Ollamaをチャットボットのバックエンドと統合する
- プロンプトエンジニアリングの基本を理解する
- AIからのストリーミング応答を処理する

## 今週学習すること

### 技術コンセプト
-   **大規模言語モデル（Large Language Models）**: 応答を生成するためにテキストで学習されたAI
-   **ローカルAI vs クラウドAI**: トレードオフと使用例
-   **Ollama**: LLMをローカルで実行するためのツール
-   **モデル選択**: ニーズに合ったモデルを選ぶ
-   **プロンプトエンジニアリング**: 効果的なプロンプトを作成する
-   **ストリーミング応答**: リアルタイムのAI出力を処理する
-   **API統合**: OllamaのHTTP APIへの接続

### AIと統合のコンセプトに焦点を当てる
- Ollama CLIコマンド
- Ollama HTTP APIエンドポイント (`/api/generate`, `/api/chat`)
- モデル管理（pull, list, remove）
- ストリーミング応答と非ストリーミング応答
- システムプロンプトと会話コンテキスト
- トークン制限と応答品質

## 今週のタスク

### 1. Ollamaのセットアップと探索
- [ ] Ollamaをインストールする
- [ ] 小さなモデル（テスト用にqwen2.5:0.5b）をプルする
- [ ] CLI経由でモデルをテストする
- [ ] モデルのサイズと速度のトレードオフを理解する
- [ ] Ollama APIドキュメントを探索する

### 2. バックエンド統合
- [ ] server.jsにOllamaへのプロキシエンドポイントを作成する
- [ ] ユーザーメッセージをOllamaに送信する
- [ ] AIの応答を受信し、フォーマットする
- [ ] エラーとタイムアウトを処理する
- [ ] リクエストに会話コンテキストを追加する

### 3. チャットボットAIの強化
- [ ] フロントエンドを新しいAIエンドポイントに接続する
- [ ] AIが生成した応答を表示する
- [ ] AIが思考中のローディング状態を追加する
- [ ] ストリーミング応答を処理する（オプションの上級者向け）
- [ ] ユーザーメッセージとAI応答の両方をデータベースに保存する

## キャリアレッスン：「AIがゲームを変えている - AIに逆らうのではなく、AIと共に働くためにスキルを適応させよう」

### なぜこれが重要なのか
AIはソフトウェア開発を根本的に変えています。
- AIコーディングアシスタントは今や標準的なツールです
- 多くのルーチンなコーディングタスクは自動化されています
- 開発者の役割は急速に進化しています
- AIへの抵抗はキャリアの成長を制限するでしょう

### 実世界での応用

**AIをツールとして受け入れる**:
- AIコーディングアシスタント（GitHub Copilot、Cursorなど）を使用する
- 定型的なコードや反復的なコードはAIに任せる
- アーキテクチャ、設計、複雑な問題解決に注力する
- AIを使用してより速く学び、新しい技術を探索する

**今、より重要になるスキル**:
-   **批判的思考**: AIの提案の正確性を評価する
-   **アーキテクチャ**: AIが実装を支援できるシステムを設計する
-   **コミュニケーション**: 要求をプロンプトに変換する
-   **ドメイン知識**: 問題領域を深く理解する
-   **コードレビュー**: AIが生成したコードを検証し、改善する

**AIが代替できないスキル（まだ）**:
- ビジネス要件とユーザーニーズの理解
- トレードオフを伴うアーキテクチャ上の意思決定
- 複雑なシステム間でのデバッグ
- チームコラボレーションとメンターシップ
- 新しい状況に対する創造的な問題解決
- 倫理的考慮事項とセキュリティ意識

**適応する方法**:
-   **プロンプトエンジニアリングを学ぶ**: AIからより良い結果を得る
-   **AIの限界を理解する**: いつAIを信頼すべきかを知る
-   **人間的なスキルに焦点を当てる**: 共感、創造性、判断力
-   **抽象化レベルを上げる**: 詳細な作業はAIに任せる
-   **力の増幅器になる**: AIを使って生産性を10倍にする

**マインドセットの転換**:
- 「私はコードを書く」から「私はソリューションを設計する」へ
- 「AIが私の仕事を奪うだろう」から「AIは私の価値を高める」へ
- 「私は全てを知っている」から「私は答えを見つける方法を知っている」へ
- 「孤独なコーダー」から「AI拡張型開発者」へ

### 未来は協調的
最高の開発者とは、人間とAIシステムの両方と効果的に協力できる人になるでしょう。このレッスンは、その協力関係を学ぶための第一歩です。

## このレッスン後のプロジェクトの状態
```
chatbot-project/
├── public/
│   ├── index.html
│   ├── styles.css
│   └── script.js (UPDATED: real AI responses)
├── src/
│   ├── server.js (UPDATED: Ollama proxy endpoints)
│   └── database.js
├── scripts/
│   └── pull-model.sh (NEW: helper for model management)
├── chatbot.db
├── package.json
├── .env (NEW: OLLAMA_HOST config)
├── README.md
└── .git/
```

あなたのチャットボットは以下の機能を備えています。
- ローカルLLMを搭載したリアルなAI応答
- Ollama APIとの統合
- 会話コンテキストの維持
- 環境変数によるモデル設定
- ユーザーとAIのメッセージの両方をデータベースに保存

## その他のリソース

### 必読
- [Ollama 公式ドキュメント](https://github.com/ollama/ollama/blob/main/docs/api.md)
- [Ollama モデルライブラリ](https://ollama.com/library)
- [プロンプトエンジニアリングガイド](https://www.promptingguide.ai/)

### ビデオチュートリアル
- 「大規模言語モデルとは？」
- 「OllamaでLLMをローカルで実行する」
- 「プロンプトエンジニアリングのベストプラクティス」

### モデルの推奨
-   **小規模/高速**（テスト用）：qwen2.5:0.5b (0.4GB)
-   **バランス**: llama3.2:1b (1.3GB), phi3:3.8b (2.2GB)
-   **高品質**（RAM/GPUがある場合）：llama3.1:8b (4.7GB)

### 練習課題
1.  **マルチモデル比較**: 3つの異なるモデルを試して、応答を比較する
2.  **システムプロンプト**: AIに異なるペルソナ（教師、コメディアン、専門家）を与える
3.  **プロンプトテンプレート**: 再利用可能なプロンプト形式を作成する
4.  **ストリーミング実装**: リアルタイムのストリーミング応答を追加する

## 避けるべき一般的な間違い
- ハードウェアに対して大きすぎるモデルを使用する
- Ollama接続エラーを処理しない
- 会話コンテキストを維持し忘れる
- トークン使用量を制限しない（コスト/パフォーマンス）
- 同意なしに機密データをクラウドAIに送信する
- 表示する前にAIの応答を検証しない

## よくある問題のトラブルシューティング

### Ollama接続失敗
```bash
# Check if Ollama is running
ollama list

# Start Ollama if needed
ollama serve

# Check Ollama host in .env
OLLAMA_HOST=127.0.0.1:11434
```

### モデルが見つからない
```bash
# List available models
ollama list

# Pull required model
ollama pull qwen2.5:0.5b
```

### 応答が遅い
- より小さなモデルを試す
- システムリソース（RAM/CPU使用率）を確認する
- リクエストのmax_tokensを減らす
- 利用可能であればGPUアクセラレーションを検討する

### メモリの問題
```bash
# Remove unused models
ollama rm <model-name>

# Check model sizes before pulling
ollama show <model-name>
```

## コード例の構造

.env設定:
```bash
OLLAMA_HOST=127.0.0.1:11434
OLLAMA_MODEL=qwen2.5:0.5b
PORT=3000
```

Server.js Ollama統合:
```javascript
// Proxy to Ollama chat endpoint
if (req.url === '/api/chat' && req.method === 'POST') {
  try {
    const body = await parseBody(req)

    const ollamaReq = http.request(`http://${OLLAMA_HOST}/api/chat`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' }
    }, (ollamaRes) => {
      res.statusCode = ollamaRes.statusCode
      res.setHeader('Content-Type', 'application/json')
      ollamaRes.pipe(res)
    })

    ollamaReq.on('error', (error) => {
      res.statusCode = 500
      res.end(JSON.stringify({
        error: 'Ollama connection failed',
        details: error.message
      }))
    })

    ollamaReq.write(JSON.stringify(body))
    ollamaReq.end()
  } catch (error) {
    res.statusCode = 400
    res.end(JSON.stringify({ error: error.message }))
  }
  return
}
```

フロントエンドAPI呼び出し:
```javascript
const response = await fetch('/api/chat', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({
    model: 'qwen2.5:0.5b',
    messages: conversationHistory,
    stream: false
  })
})

const data = await response.json()
const aiMessage = data.message
```

## プロンプトエンジニアリングのヒント

### 基本構造
```
[System Prompt] You are a helpful assistant...
[User Message] Explain quantum computing
[Context] Previous conversation...
```

### 効果的なプロンプト
- 具体的に、かつ明確にする
- 必要に応じてコンテキストを提供する
- 例を使用する（少数ショット学習）
- 希望する形式を指定する
- 繰り返し洗練させる

### システムプロンプトの例
```
"You are a helpful coding assistant. Provide clear, concise answers."
"You are a patient teacher explaining concepts to beginners."
"You are an expert in [domain]. Give detailed technical responses."
```

## 来週のプレビュー
レッスン09では、会話履歴サイドバー、会話管理、より良いUXなど、チャットボットにプロフェッショナルな機能を追加し、アプリケーション全体を洗練させます。状態管理、UIパターン、そして完全なユーザーエクスペリエンスの作成について学びます。

## 宿題
1. Ollamaをインストールし、qwen2.5:0.5bモデルをプルする
2. Ollama CLI経由でモデルをテストする
3. Ollama用のプロキシエンドポイントをサーバーに作成する
4. フロントエンドを実際のAI応答に接続する
5. AI応答をデータベースに保存する
6. Ollama接続エラーのハンドリングを追加する
7. さまざまなシステムプロンプトを試す
8. 少なくとも2つの異なるモデルでテストする
9. 作業をコミットする
10. AI搭載チャットボットをDiscordで共有する！

**おめでとうございます！** これで、完全にローカルマシン上で動作するAIチャットボットが完成しました！