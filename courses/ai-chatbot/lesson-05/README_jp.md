# レッスン05：高度なJavaScriptとAPIの概念

## テーマ：「つながる思考 - システムがどのように連携するかを理解する」

## 学習目標
このレッスンの終わりまでに、あなたは以下のことができるようになります。
- Promisesとasync/awaitを使った非同期プログラミングを理解する
- APIにHTTPリクエストを行う方法を学ぶ
- JSONデータ形式を扱う
- エラー処理と読み込み状態を実装する
- 外部AIサービスとの統合のためにチャットボットを準備する

## 今週の学習内容

### 技術的な概念
- **非同期プログラミング**: ノンブロッキングコードの理解
- **Promises**: 時間のかかる操作を扱う
- **async/await**: 非同期コードのための現代的な構文
- **fetch() API**: HTTPリクエストを行う
- **JSON**: データ交換のためのJavaScriptオブジェクト記法
- **エラー処理**: `try/catch`ブロックとエラー状態
- **読み込み状態**: 非同期操作中にフィードバックを提供する

### JavaScriptの概念に焦点を当てる
- ``Promise`` - 将来の値を表す
- ``async``/``await`` - 同期的に見える非同期コードを書く
- ``fetch()`` - ネットワークリクエストを行う
- ``JSON.parse()``, ``JSON.stringify()`` - JSONを扱う
- ``try...catch`` - エラーを適切に処理する

## 今週のタスク

### 1. 非同期JavaScriptの基本
- [ ] イベントループと非同期の振る舞いを理解する
- [ ] Promiseとその仕組みを学ぶ
- [ ] async/await構文を習得する
- [ ] try/catchを使ったエラー処理を練習する

### 2. API統合の準備
- [ ] REST APIとHTTPメソッドについて学ぶ
- [ ] リクエスト/レスポンスサイクルを理解する
- [ ] 公開APIでfetch()を練習する
- [ ] JSONデータのパースを扱う

### 3. チャットボットの機能強化
- [ ] モックAPIレスポンス関数を作成する（AIをシミュレートする）
- [ ] 「考えている」間に読み込みインジケーターを追加する
- [ ] モックAIレスポンスをチャットに表示する
- [ ] 失敗したリクエストのエラー処理を実装する
- [ ] 遅いレスポンスのためのタイムアウト処理を追加する

## キャリアレッスン：「職場の裏切り行為への対処 - 職場政治を乗りこなし、自分の仕事を保護する」

### これが重要な理由
職場政治はあらゆる組織に存在します。
- 同僚があなたの仕事を横取りするかもしれません
- 昇進のための競争は醜くなることがあります
- 情報共有が武器として使われることがあります
- 信頼は獲得されるものであり、自動的なものではありません

### 実世界での応用

**自分を保護する**：
- 貢献を文書化する（コミットメッセージ、メール、プロジェクトノート）
- 重要な連絡には関連する人物をCCに入れる
- 成果を記録する仕事日誌をつける
- チーム会議で自分の仕事を発表する

**同盟を築く**：
- 同僚と真の関係を築く
- 他者の成功を助ける（互恵関係が重要です）
- あなたを擁護するメンターを見つける
- 一貫した品質を通じて評判を築く

**政治を乗りこなす**：
- うわさ話や裏切り行為には関わらない
- 結果と測定可能な影響に焦点を当てる
- 自慢することなく成果を伝える
- 問題を管理職にエスカレートすべき時を知る

**危険信号**：
- 誰かが常にチームの仕事を横取りする
- あなたのアイデアが他者の提案として現れる
- あなたが共有した情報があなたに対して使われる
- 明らかな貢献にもかかわらず、認識されない

**退職を検討する時**：
- 政治を成果よりも評価する有害な文化
- あなたの精神衛生が損なわれている
- 努力にもかかわらず、前進の道がない
- あなたの価値観に合ったより良い機会がある

## このレッスン後のプロジェクトの状態
```
chatbot-project/
├── index.html
├── styles.css
├── script.js (強化済み: async, fetch, モックAIレスポンス)
├── README.md
└── .git/
```

あなたのチャットボットは以下のようになるはずです。
- 処理中に「考えています...」インジケーターを表示する
- モックデータでAI応答をシミュレートする
- 非同期操作を適切に処理する
- ユーザーに読み込み状態を表示する
- エラーを適切に処理する
- JSONデータ構造を扱う

## 追加リソース

### 必読書
- [MDN Promises ガイド](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Guide/Using_promises)
- [MDN async/await](https://developer.mozilla.org/en-US/docs/Learn/JavaScript/Asynchronous/Async_await)
- [MDN Fetch API](https://developer.mozilla.org/en-US/docs/Web/API/Fetch_API/Using_Fetch)
- [JSON.org](https://www.json.org/) - JSON形式の理解

### ビデオチュートリアル
- 「100秒でわかる非同期JavaScript」
- 「Promises vs Async/Await」
- 「Fetch API クラッシュコース」
- 「イベントループの理解」

### 練習課題
1. **APIエクスプローラー**: 公開API（dog.ceoや猫の事実など）をテストするインターフェースを構築する
2. **読み込み状態**: さまざまな読み込みアニメーション（スピナー、ドット、スケルトン）を作成する
3. **エラーシナリオ**: さまざまなエラータイプ（ネットワーク、タイムアウト、無効なデータ）を処理する
4. **データ変換**: APIからデータをフェッチし、表示用に変換する

## 避けるべきよくある間違い
- Promiseの拒否を処理しない（未処理のPromiseエラー）
- 非同期関数で`await`キーワードを忘れる
- ユーザーに読み込みフィードバックを提供しない
- `try/catch`なしでJSONをパースする
- コールバックとPromise/async-awaitを混同する
- JSONをパースする前にレスポンスステータスを確認しない

## よくある問題のトラブルシューティング

### Promiseが解決されない
```javascript
// Always handle both success and error
// 成功とエラーの両方を常に処理する
async function getData() {
  try {
    const response = await fetch(url)
    if (!response.ok) throw new Error('Failed')
    return await response.json()
  } catch (error) {
    console.error('Error:', error)
    // Handle error appropriately
    // エラーを適切に処理する
  }
}
```

### CORSエラー
- CORSエラーは、異なるドメインからのAPI呼び出し時に発生します
- 学習目的では、CORSを許可する公開APIを使用してください
- 後で、独自のサーバーを介してリクエストをプロキシします（レッスン06）

### JSONパースエラー
```javascript
// Always validate before parsing
// パースする前に常に検証する
try {
  const data = JSON.parse(responseText)
} catch (error) {
  console.error('Invalid JSON:', error)
}
```

## コード例の構造

強化されたscript.jsには以下が含まれている必要があります。
```javascript
// Mock AI response function (simulates API call)
// モックAI応答関数（API呼び出しをシミュレートする）
async function getMockAIResponse(userMessage) {
  // Simulate network delay
  // ネットワーク遅延をシミュレート
  await new Promise(resolve => setTimeout(resolve, 1000))

  // Return mock response
  // モック応答を返す
  return {
    message: `I received: "${userMessage}". This is a mock response!`
  }
}

// Enhanced send message with async
// asyncで強化されたメッセージ送信
async function sendMessage() {
  const messageText = input.value.trim()
  if (!messageText) return

  // Add user message
  // ユーザーメッセージを追加
  addMessageToChat('user', messageText)
  input.value = ''

  // Show loading indicator
  // 読み込みインジケーターを表示
  showLoadingIndicator()

  try {
    // Get AI response
    // AI応答を取得
    const response = await getMockAIResponse(messageText)

    // Hide loading and show response
    // 読み込みを非表示にし、応答を表示
    hideLoadingIndicator()
    addMessageToChat('assistant', response.message)
  } catch (error) {
    hideLoadingIndicator()
    addMessageToChat('error', 'Sorry, something went wrong!')
    console.error('Error:', error)
  }
}
```

## 来週の予告
レッスン06では、バックエンドロジックを処理するためにNode.jsサーバーをセットアップします。サーバーサイドJavaScript、Express.js、およびチャットボット用のAPIエンドポイントを作成する方法について学びます。

## 宿題
1. async/awaitでモックAI応答を実装する
2. 読み込みインジケーター（「考えています...」またはスピナー）を追加する
3. try/catchでエラーを適切に処理する
4. 公開APIでテストする（オプション：天気、ジョーク、名言）
5. 実際のAPIをシミュレートするために、モック応答に1～2秒の遅延を追加する
6. 作業をコミットする
7. Discordで非同期チャットボットを共有する