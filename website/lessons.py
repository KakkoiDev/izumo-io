"""Lesson content for KakkoiSchool."""

LESSONS = {
    'T01': {
        'en': """
<h1>T01: Hello World</h1>
<p class="lesson-intro">Every journey starts with a single step. In web development, that step is creating your first HTML file and watching it come alive in a browser. Think of it like writing a letter - you write it, then hand it to someone who reads it aloud.</p>

<h2>Your First Web Page</h2>
<p>Create a file called <code>index.html</code>. This is the conventional name for the main page of any website. The browser reads this file and renders it visually for the user.</p>
<pre><code>&lt;!DOCTYPE html&gt;
&lt;html lang="en"&gt;
&lt;head&gt;
    &lt;meta charset="UTF-8"&gt;
    &lt;title&gt;My First Page&lt;/title&gt;
&lt;/head&gt;
&lt;body&gt;
    &lt;h1&gt;Hello World&lt;/h1&gt;
    &lt;p&gt;This is my first web page.&lt;/p&gt;
&lt;/body&gt;
&lt;/html&gt;</code></pre>

<h2>How It Works</h2>
<p>When you double-click the file or drag it into your browser, the browser reads the raw text, interprets the HTML tags, and paints the result on screen. No server needed for this step.</p>

<div class="mermaid">
flowchart LR
    A[index.html file] -->|open in| B[Browser]
    B -->|reads HTML| C[Parser]
    C -->|builds structure| D[Render Engine]
    D -->|paints| E[Screen Output]
</div>

<h2>The DOCTYPE Declaration</h2>
<p>The <code>&lt;!DOCTYPE html&gt;</code> line tells the browser to use modern HTML5 standards. Without it, the browser may fall back to older, quirky rendering modes.</p>

<div class="takeaways">
<h2>Key Takeaways</h2>
<ul>
<li>An HTML file is just a plain text file with a .html extension</li>
<li>The browser is your interpreter - it reads HTML and displays the result</li>
<li>Always include DOCTYPE, html, head, and body tags</li>
<li>index.html is the default filename for a website's main page</li>
</ul>
</div>
""",
        'ja': """
<h1>T01: Hello World - はじめの一歩</h1>
<p class="lesson-intro">全ての旅は一歩から始まります。Web開発では、最初のHTMLファイルを作成してブラウザで表示することがその一歩です。手紙を書いて誰かに渡すようなものです。あなたが書き、ブラウザが読み上げてくれます。</p>

<h2>最初のWebページ</h2>
<p><code>index.html</code>というファイルを作成します。これはWebサイトのメインページの慣習的な名前です。ブラウザがこのファイルを読み取り、ユーザーに視覚的に表示します。</p>
<pre><code>&lt;!DOCTYPE html&gt;
&lt;html lang="en"&gt;
&lt;head&gt;
    &lt;meta charset="UTF-8"&gt;
    &lt;title&gt;My First Page&lt;/title&gt;
&lt;/head&gt;
&lt;body&gt;
    &lt;h1&gt;Hello World&lt;/h1&gt;
    &lt;p&gt;This is my first web page.&lt;/p&gt;
&lt;/body&gt;
&lt;/html&gt;</code></pre>

<h2>仕組み</h2>
<p>ファイルをダブルクリックするかブラウザにドラッグすると、ブラウザがテキストを読み取り、HTMLタグを解釈し、結果を画面に描画します。この段階ではサーバーは不要です。</p>

<div class="mermaid">
flowchart LR
    A[index.html file] -->|open in| B[Browser]
    B -->|reads HTML| C[Parser]
    C -->|builds structure| D[Render Engine]
    D -->|paints| E[Screen Output]
</div>

<h2>DOCTYPE宣言</h2>
<p><code>&lt;!DOCTYPE html&gt;</code>はブラウザにHTML5標準を使用するよう指示します。これがないと、ブラウザは古い互換モードで表示する場合があります。</p>

<div class="takeaways">
<h2>まとめ</h2>
<ul>
<li>HTMLファイルは.html拡張子を持つプレーンテキストファイルです</li>
<li>ブラウザはインタプリタです。HTMLを読み取って結果を表示します</li>
<li>DOCTYPE、html、head、bodyタグを必ず含めてください</li>
<li>index.htmlはWebサイトのメインページのデフォルトファイル名です</li>
</ul>
</div>
""",
    },
    'T02': {
        'en': """
<h1>T02: HTML Tags</h1>
<p class="lesson-intro">HTML tags are like labels on boxes. Each tag tells the browser what kind of content is inside. A heading tag says "this is a title," a paragraph tag says "this is a block of text." The browser uses these labels to display content appropriately.</p>

<h2>Headings and Text</h2>
<p>HTML provides six levels of headings, from <code>&lt;h1&gt;</code> (most important) to <code>&lt;h6&gt;</code> (least). Paragraphs use the <code>&lt;p&gt;</code> tag.</p>
<pre><code>&lt;h1&gt;Main Title&lt;/h1&gt;
&lt;h2&gt;Section Title&lt;/h2&gt;
&lt;h3&gt;Subsection&lt;/h3&gt;
&lt;p&gt;A paragraph of text goes here.&lt;/p&gt;</code></pre>

<h2>Links and Images</h2>
<p>The anchor tag <code>&lt;a&gt;</code> creates clickable links. The image tag <code>&lt;img&gt;</code> embeds pictures. Note that img is a self-closing tag.</p>
<pre><code>&lt;a href="https://example.com"&gt;Visit Example&lt;/a&gt;
&lt;img src="photo.jpg" alt="A description"&gt;</code></pre>

<h2>Lists</h2>
<p>Unordered lists use <code>&lt;ul&gt;</code> with <code>&lt;li&gt;</code> items (bullet points). Ordered lists use <code>&lt;ol&gt;</code> (numbered items).</p>
<pre><code>&lt;ul&gt;
    &lt;li&gt;First item&lt;/li&gt;
    &lt;li&gt;Second item&lt;/li&gt;
&lt;/ul&gt;</code></pre>

<div class="mermaid">
graph TD
    A[html] --> B[head]
    A --> C[body]
    B --> D[title]
    C --> E[h1]
    C --> F[p]
    C --> G[ul]
    G --> H[li]
    G --> I[li]
    C --> J[a]
    C --> K[img]
</div>

<div class="takeaways">
<h2>Key Takeaways</h2>
<ul>
<li>Headings h1-h6 create a content hierarchy - use them in order</li>
<li>Links use the a tag with an href attribute for the destination URL</li>
<li>Images use the img tag with src and alt attributes</li>
<li>Lists come in two flavors: ul for bullets, ol for numbers</li>
</ul>
</div>
""",
        'ja': """
<h1>T02: HTMLタグ - 基本要素</h1>
<p class="lesson-intro">HTMLタグは箱に貼るラベルのようなものです。各タグがブラウザにコンテンツの種類を伝えます。見出しタグは「これはタイトル」、段落タグは「これはテキストブロック」と伝えます。ブラウザはこれらのラベルを使って適切に表示します。</p>

<h2>見出しとテキスト</h2>
<p>HTMLには<code>&lt;h1&gt;</code>(最重要)から<code>&lt;h6&gt;</code>(最小)まで6段階の見出しがあります。段落には<code>&lt;p&gt;</code>タグを使います。</p>
<pre><code>&lt;h1&gt;Main Title&lt;/h1&gt;
&lt;h2&gt;Section Title&lt;/h2&gt;
&lt;h3&gt;Subsection&lt;/h3&gt;
&lt;p&gt;A paragraph of text goes here.&lt;/p&gt;</code></pre>

<h2>リンクと画像</h2>
<p>アンカータグ<code>&lt;a&gt;</code>はクリック可能なリンクを作成します。画像タグ<code>&lt;img&gt;</code>は写真を埋め込みます。imgは自己閉じタグです。</p>
<pre><code>&lt;a href="https://example.com"&gt;Visit Example&lt;/a&gt;
&lt;img src="photo.jpg" alt="A description"&gt;</code></pre>

<h2>リスト</h2>
<p>順序なしリストは<code>&lt;ul&gt;</code>と<code>&lt;li&gt;</code>を使います(箇条書き)。順序付きリストは<code>&lt;ol&gt;</code>を使います(番号付き)。</p>
<pre><code>&lt;ul&gt;
    &lt;li&gt;First item&lt;/li&gt;
    &lt;li&gt;Second item&lt;/li&gt;
&lt;/ul&gt;</code></pre>

<div class="mermaid">
graph TD
    A[html] --> B[head]
    A --> C[body]
    B --> D[title]
    C --> E[h1]
    C --> F[p]
    C --> G[ul]
    G --> H[li]
    G --> I[li]
    C --> J[a]
    C --> K[img]
</div>

<div class="takeaways">
<h2>まとめ</h2>
<ul>
<li>見出しh1-h6はコンテンツの階層を作ります。順番に使いましょう</li>
<li>リンクはaタグとhref属性でリンク先URLを指定します</li>
<li>画像はimgタグとsrc属性、alt属性を使います</li>
<li>リストは2種類: ulは箇条書き、olは番号付き</li>
</ul>
</div>
""",
    },
    'T03': {
        'en': """
<h1>T03: HTML Forms and Blocks</h1>
<p class="lesson-intro">Forms are the bridge between users and your application. Like a paper form at a doctor's office, HTML forms collect information from users and send it somewhere for processing. Block elements like details/summary add interactive disclosure without JavaScript.</p>

<h2>Form Elements</h2>
<p>The <code>&lt;form&gt;</code> tag wraps input elements. Each input has a type that controls its behavior. The <code>required</code> attribute forces the user to fill in a field before submitting.</p>
<pre><code>&lt;form action="/submit" method="POST"&gt;
    &lt;label for="name"&gt;Name:&lt;/label&gt;
    &lt;input type="text" id="name" name="name" required&gt;

    &lt;label for="email"&gt;Email:&lt;/label&gt;
    &lt;input type="email" id="email" name="email" required&gt;

    &lt;label for="role"&gt;Role:&lt;/label&gt;
    &lt;select id="role" name="role"&gt;
        &lt;option value="dev"&gt;Developer&lt;/option&gt;
        &lt;option value="design"&gt;Designer&lt;/option&gt;
    &lt;/select&gt;

    &lt;textarea name="message" rows="4"&gt;&lt;/textarea&gt;
    &lt;button type="submit"&gt;Send&lt;/button&gt;
&lt;/form&gt;</code></pre>

<div class="mermaid">
flowchart LR
    A[User fills form] --> B{Valid?}
    B -->|Yes| C[Browser sends data]
    C --> D[Server receives]
    D --> E[Process and respond]
    B -->|No| F[Show error message]
    F --> A
</div>

<h2>Details and Summary</h2>
<p>The <code>&lt;details&gt;</code> and <code>&lt;summary&gt;</code> elements create expandable sections with zero JavaScript.</p>
<pre><code>&lt;details&gt;
    &lt;summary&gt;Click to expand&lt;/summary&gt;
    &lt;p&gt;Hidden content revealed on click.&lt;/p&gt;
&lt;/details&gt;</code></pre>

<div class="takeaways">
<h2>Key Takeaways</h2>
<ul>
<li>Forms use action and method attributes to control where and how data is sent</li>
<li>Input types include text, email, password, number, and more</li>
<li>The required attribute provides built-in browser validation</li>
<li>Details/summary gives you interactive disclosure without JavaScript</li>
</ul>
</div>
""",
        'ja': """
<h1>T03: HTMLフォームとブロック要素</h1>
<p class="lesson-intro">フォームはユーザーとアプリケーションの架け橋です。病院の問診票のように、HTMLフォームはユーザーから情報を収集し、処理のために送信します。details/summaryなどのブロック要素はJavaScriptなしでインタラクティブな開閉機能を追加します。</p>

<h2>フォーム要素</h2>
<p><code>&lt;form&gt;</code>タグは入力要素を囲みます。各入力にはtypeがあり動作を制御します。<code>required</code>属性は送信前にフィールドの入力を強制します。</p>
<pre><code>&lt;form action="/submit" method="POST"&gt;
    &lt;label for="name"&gt;Name:&lt;/label&gt;
    &lt;input type="text" id="name" name="name" required&gt;

    &lt;label for="email"&gt;Email:&lt;/label&gt;
    &lt;input type="email" id="email" name="email" required&gt;

    &lt;label for="role"&gt;Role:&lt;/label&gt;
    &lt;select id="role" name="role"&gt;
        &lt;option value="dev"&gt;Developer&lt;/option&gt;
        &lt;option value="design"&gt;Designer&lt;/option&gt;
    &lt;/select&gt;

    &lt;textarea name="message" rows="4"&gt;&lt;/textarea&gt;
    &lt;button type="submit"&gt;Send&lt;/button&gt;
&lt;/form&gt;</code></pre>

<div class="mermaid">
flowchart LR
    A[User fills form] --> B{Valid?}
    B -->|Yes| C[Browser sends data]
    C --> D[Server receives]
    D --> E[Process and respond]
    B -->|No| F[Show error message]
    F --> A
</div>

<h2>DetailsとSummary</h2>
<p><code>&lt;details&gt;</code>と<code>&lt;summary&gt;</code>要素はJavaScriptゼロで展開可能なセクションを作成します。</p>
<pre><code>&lt;details&gt;
    &lt;summary&gt;Click to expand&lt;/summary&gt;
    &lt;p&gt;Hidden content revealed on click.&lt;/p&gt;
&lt;/details&gt;</code></pre>

<div class="takeaways">
<h2>まとめ</h2>
<ul>
<li>フォームはaction属性とmethod属性でデータの送信先と方法を制御します</li>
<li>入力タイプにはtext、email、password、numberなどがあります</li>
<li>required属性はブラウザ組み込みのバリデーションを提供します</li>
<li>details/summaryはJavaScriptなしでインタラクティブな開閉を実現します</li>
</ul>
</div>
""",
    },
    'T04': {
        'en': """
<h1>T04: CSS Basics</h1>
<p class="lesson-intro">If HTML is the skeleton of a web page, CSS is the skin, clothing, and makeup. CSS (Cascading Style Sheets) controls how elements look - their colors, fonts, spacing, and size. The "cascading" part means styles can override each other in a predictable order.</p>

<h2>Selectors and Properties</h2>
<p>CSS rules consist of a selector (which elements to style) and declarations (how to style them). Selectors can target tags, classes, or IDs.</p>
<pre><code>/* Tag selector */
h1 { color: navy; }

/* Class selector */
.highlight { background-color: yellow; }

/* ID selector */
#main-title { font-size: 2rem; }

/* Combined */
p.intro { font-style: italic; }</code></pre>

<h2>Colors and Fonts</h2>
<p>Colors can be specified by name, hex code, or rgb values. Font properties control the typeface, size, weight, and line height.</p>
<pre><code>body {
    font-family: Arial, sans-serif;
    font-size: 16px;
    line-height: 1.5;
    color: #333333;
    background-color: rgb(245, 245, 245);
}</code></pre>

<h2>The Box Model</h2>
<p>Every HTML element is a rectangular box. From inside out: content, padding, border, margin. Understanding this model is essential to controlling layout.</p>

<div class="mermaid">
graph TD
    A["Margin (outer spacing)"] --> B["Border (visible edge)"]
    B --> C["Padding (inner spacing)"]
    C --> D["Content (text, images)"]
    style A fill:#f9f,stroke:#333
    style B fill:#f66,stroke:#333
    style C fill:#6f6,stroke:#333
    style D fill:#66f,stroke:#333
</div>

<div class="takeaways">
<h2>Key Takeaways</h2>
<ul>
<li>CSS selectors target elements by tag name, class (.name), or ID (#name)</li>
<li>The box model has four layers: content, padding, border, margin</li>
<li>Use box-sizing: border-box to make width include padding and border</li>
<li>Specificity determines which CSS rule wins when multiple rules conflict</li>
</ul>
</div>
""",
        'ja': """
<h1>T04: CSS基礎 - スタイルの世界</h1>
<p class="lesson-intro">HTMLがWebページの骨格なら、CSSは肌、服、化粧です。CSS(カスケーディングスタイルシート)は要素の見た目を制御します。色、フォント、余白、サイズなど。「カスケーディング」とは、スタイルが予測可能な順序で上書きされることを意味します。</p>

<h2>セレクタとプロパティ</h2>
<p>CSSルールはセレクタ(どの要素をスタイルするか)と宣言(どうスタイルするか)で構成されます。セレクタはタグ、クラス、IDを対象にできます。</p>
<pre><code>/* Tag selector */
h1 { color: navy; }

/* Class selector */
.highlight { background-color: yellow; }

/* ID selector */
#main-title { font-size: 2rem; }

/* Combined */
p.intro { font-style: italic; }</code></pre>

<h2>色とフォント</h2>
<p>色は名前、16進コード、rgb値で指定できます。フォントプロパティは書体、サイズ、太さ、行の高さを制御します。</p>
<pre><code>body {
    font-family: Arial, sans-serif;
    font-size: 16px;
    line-height: 1.5;
    color: #333333;
    background-color: rgb(245, 245, 245);
}</code></pre>

<h2>ボックスモデル</h2>
<p>全てのHTML要素は長方形のボックスです。内側から外側へ: content、padding、border、margin。このモデルの理解はレイアウト制御に不可欠です。</p>

<div class="mermaid">
graph TD
    A["Margin (outer spacing)"] --> B["Border (visible edge)"]
    B --> C["Padding (inner spacing)"]
    C --> D["Content (text, images)"]
    style A fill:#f9f,stroke:#333
    style B fill:#f66,stroke:#333
    style C fill:#6f6,stroke:#333
    style D fill:#66f,stroke:#333
</div>

<div class="takeaways">
<h2>まとめ</h2>
<ul>
<li>CSSセレクタはタグ名、クラス(.name)、ID(#name)で要素を対象にします</li>
<li>ボックスモデルは4層構造: content、padding、border、margin</li>
<li>box-sizing: border-boxでwidthにpaddingとborderを含められます</li>
<li>詳細度(specificity)が複数のルールが競合した時にどちらが勝つかを決定します</li>
</ul>
</div>
""",
    },
    'T05': {
        'en': """
<h1>T05: CSS Layout</h1>
<p class="lesson-intro">Placing elements on a page used to be painful. Flexbox and Grid changed everything. Think of Flexbox as arranging items in a single line (like books on a shelf), and Grid as organizing items in rows and columns (like a spreadsheet).</p>

<h2>Flexbox</h2>
<p>Flexbox works in one dimension at a time. Set <code>display: flex</code> on a container, then control how children align and distribute space.</p>
<pre><code>.nav {
    display: flex;
    justify-content: space-between;
    align-items: center;
    gap: 1rem;
}

.nav-item {
    flex: 1;
}</code></pre>

<h2>CSS Grid</h2>
<p>Grid works in two dimensions simultaneously. Define rows and columns, then place items into the grid cells.</p>
<pre><code>.layout {
    display: grid;
    grid-template-columns: 250px 1fr;
    grid-template-rows: auto 1fr auto;
    gap: 1rem;
    min-height: 100vh;
}</code></pre>

<h2>Responsive Design</h2>
<p>Media queries let you apply different styles based on screen size. Mobile-first means writing base styles for small screens and adding complexity for larger ones.</p>
<pre><code>@media (min-width: 768px) {
    .layout { grid-template-columns: 250px 1fr; }
}</code></pre>

<div class="mermaid">
flowchart TB
    subgraph Flexbox
        direction LR
        F1[Item] --- F2[Item] --- F3[Item]
    end
    subgraph Grid
        G1[Header] --- G2[Header]
        G3[Sidebar] --- G4[Main]
        G5[Footer] --- G6[Footer]
    end
</div>

<div class="takeaways">
<h2>Key Takeaways</h2>
<ul>
<li>Flexbox is for one-dimensional layouts (row or column)</li>
<li>Grid is for two-dimensional layouts (rows and columns together)</li>
<li>Use media queries for responsive design that adapts to screen size</li>
<li>Mobile-first approach: start small, add complexity for larger screens</li>
</ul>
</div>
""",
        'ja': """
<h1>T05: CSSレイアウト - 配置の技術</h1>
<p class="lesson-intro">かつてページ上の要素配置は大変でした。FlexboxとGridが全てを変えました。Flexboxは一列に並べること(本棚の本のように)、Gridは行と列で整理すること(スプレッドシートのように)と考えてください。</p>

<h2>Flexbox</h2>
<p>Flexboxは一度に一方向で動作します。コンテナに<code>display: flex</code>を設定し、子要素の配置と余白の配分を制御します。</p>
<pre><code>.nav {
    display: flex;
    justify-content: space-between;
    align-items: center;
    gap: 1rem;
}

.nav-item {
    flex: 1;
}</code></pre>

<h2>CSS Grid</h2>
<p>Gridは二方向を同時に扱います。行と列を定義し、グリッドセルにアイテムを配置します。</p>
<pre><code>.layout {
    display: grid;
    grid-template-columns: 250px 1fr;
    grid-template-rows: auto 1fr auto;
    gap: 1rem;
    min-height: 100vh;
}</code></pre>

<h2>レスポンシブデザイン</h2>
<p>メディアクエリで画面サイズに応じた異なるスタイルを適用できます。モバイルファーストとは小さい画面用の基本スタイルを書き、大きい画面用に複雑さを加えるアプローチです。</p>
<pre><code>@media (min-width: 768px) {
    .layout { grid-template-columns: 250px 1fr; }
}</code></pre>

<div class="mermaid">
flowchart TB
    subgraph Flexbox
        direction LR
        F1[Item] --- F2[Item] --- F3[Item]
    end
    subgraph Grid
        G1[Header] --- G2[Header]
        G3[Sidebar] --- G4[Main]
        G5[Footer] --- G6[Footer]
    end
</div>

<div class="takeaways">
<h2>まとめ</h2>
<ul>
<li>Flexboxは一次元レイアウト向け(行または列)</li>
<li>Gridは二次元レイアウト向け(行と列を同時に)</li>
<li>メディアクエリで画面サイズに適応するレスポンシブデザインを実現</li>
<li>モバイルファースト: 小さく始めて、大きい画面向けに拡張する</li>
</ul>
</div>
""",
    },
    'T06': {
        'en': """
<h1>T06: CSS to the Limit</h1>
<p class="lesson-intro">CSS can do far more than change colors. With transitions, animations, and clever selectors, you can build interactive components without a single line of JavaScript. It is like discovering that your paintbrush can also sculpt.</p>

<h2>Transitions</h2>
<p>Transitions smoothly animate property changes. Specify which property to animate, how long it takes, and the easing function.</p>
<pre><code>.button {
    background: #3498db;
    transition: background 0.3s ease, transform 0.2s ease;
}
.button:hover {
    background: #2980b9;
    transform: scale(1.05);
}</code></pre>

<h2>Keyframe Animations</h2>
<p>For more complex motion, define keyframes with specific states at different points in time.</p>
<pre><code>@keyframes fadeIn {
    from { opacity: 0; transform: translateY(-10px); }
    to { opacity: 1; transform: translateY(0); }
}
.card { animation: fadeIn 0.5s ease-out; }</code></pre>

<h2>Pure CSS Accordion</h2>
<p>The <code>:target</code> pseudo-class lets you toggle visibility based on URL hash, creating interactive components without JavaScript.</p>
<pre><code>.panel { max-height: 0; overflow: hidden; transition: max-height 0.3s; }
.panel:target { max-height: 500px; }</code></pre>

<div class="mermaid">
stateDiagram-v2
    [*] --> Default
    Default --> Hover: mouse enter
    Hover --> Default: mouse leave
    Default --> Active: click
    Active --> Animated: transition starts
    Animated --> NewState: transition ends
</div>

<div class="takeaways">
<h2>Key Takeaways</h2>
<ul>
<li>Transitions animate changes between two states smoothly</li>
<li>Keyframe animations allow multi-step, complex motion sequences</li>
<li>The :target pseudo-class enables JS-free interactive patterns</li>
<li>Always consider performance - animate transform and opacity, not width or height</li>
</ul>
</div>
""",
        'ja': """
<h1>T06: CSSの限界に挑戦</h1>
<p class="lesson-intro">CSSは色を変えるだけではありません。トランジション、アニメーション、賢いセレクタで、JavaScriptなしにインタラクティブなコンポーネントを構築できます。絵筆が彫刻もできると気づくようなものです。</p>

<h2>トランジション</h2>
<p>トランジションはプロパティの変化を滑らかにアニメーションします。どのプロパティを、どれくらいの時間で、どのイージングで変化させるかを指定します。</p>
<pre><code>.button {
    background: #3498db;
    transition: background 0.3s ease, transform 0.2s ease;
}
.button:hover {
    background: #2980b9;
    transform: scale(1.05);
}</code></pre>

<h2>キーフレームアニメーション</h2>
<p>より複雑な動きには、時間の異なるポイントでの状態を定義するキーフレームを使います。</p>
<pre><code>@keyframes fadeIn {
    from { opacity: 0; transform: translateY(-10px); }
    to { opacity: 1; transform: translateY(0); }
}
.card { animation: fadeIn 0.5s ease-out; }</code></pre>

<h2>純粋CSSアコーディオン</h2>
<p><code>:target</code>擬似クラスでURLハッシュに基づいて表示を切り替え、JavaScriptなしのインタラクティブなコンポーネントを作成できます。</p>
<pre><code>.panel { max-height: 0; overflow: hidden; transition: max-height 0.3s; }
.panel:target { max-height: 500px; }</code></pre>

<div class="mermaid">
stateDiagram-v2
    [*] --> Default
    Default --> Hover: mouse enter
    Hover --> Default: mouse leave
    Default --> Active: click
    Active --> Animated: transition starts
    Animated --> NewState: transition ends
</div>

<div class="takeaways">
<h2>まとめ</h2>
<ul>
<li>トランジションは2つの状態間の変化を滑らかにアニメーションします</li>
<li>キーフレームアニメーションで複数ステップの複雑な動きを実現できます</li>
<li>:target擬似クラスでJavaScriptなしのインタラクティブパターンが可能です</li>
<li>パフォーマンスを考慮し、transformとopacityをアニメーションしましょう</li>
</ul>
</div>
""",
    },
    'T07': {
        'en': """
<h1>T07: JavaScript Intro</h1>
<p class="lesson-intro">JavaScript is the programming language of the web. If HTML is the structure and CSS is the style, JavaScript is the behavior. It makes pages interactive - responding to clicks, processing data, and updating content dynamically. Think of it as teaching your web page to think.</p>

<h2>Console and Variables</h2>
<p>The browser console is your playground. Use <code>console.log()</code> to print values and debug. Variables store data for later use.</p>
<pre><code>// Variables
let name = "Alice";
const age = 25;
let isStudent = true;

console.log("Hello, " + name);
console.log("Age:", age);</code></pre>

<h2>Data Types</h2>
<p>JavaScript has several core types: strings for text, numbers for math, booleans for true/false, null for intentional emptiness, and undefined for unset values.</p>

<h2>Functions</h2>
<p>Functions are reusable blocks of code. Define once, call many times.</p>
<pre><code>function greet(name) {
    return "Hello, " + name + "!";
}

const add = (a, b) =&gt; a + b;

console.log(greet("Bob"));
console.log(add(3, 4));</code></pre>

<div class="mermaid">
graph TD
    A[JavaScript Types] --> B[String]
    A --> C[Number]
    A --> D[Boolean]
    A --> E[null]
    A --> F[undefined]
    A --> G[Object]
    A --> H[Array]
    B --> I["'hello'"]
    C --> J["42, 3.14"]
    D --> K["true, false"]
</div>

<div class="takeaways">
<h2>Key Takeaways</h2>
<ul>
<li>Use let for variables that change, const for values that stay the same</li>
<li>console.log() is your best friend for debugging</li>
<li>Functions encapsulate reusable logic - define once, use many times</li>
<li>Arrow functions provide a shorter syntax for simple functions</li>
</ul>
</div>
""",
        'ja': """
<h1>T07: JavaScript入門</h1>
<p class="lesson-intro">JavaScriptはWebのプログラミング言語です。HTMLが構造、CSSがスタイルなら、JavaScriptは振る舞いです。ページをインタラクティブにし、クリックに応答し、データを処理し、コンテンツを動的に更新します。Webページに考えることを教えるようなものです。</p>

<h2>コンソールと変数</h2>
<p>ブラウザコンソールは練習場です。<code>console.log()</code>で値を表示しデバッグします。変数はデータを保存します。</p>
<pre><code>// Variables
let name = "Alice";
const age = 25;
let isStudent = true;

console.log("Hello, " + name);
console.log("Age:", age);</code></pre>

<h2>データ型</h2>
<p>JavaScriptにはいくつかの基本型があります。文字列(テキスト)、数値(計算)、真偽値(true/false)、null(意図的な空)、undefined(未設定)です。</p>

<h2>関数</h2>
<p>関数は再利用可能なコードブロックです。一度定義して何度でも呼び出せます。</p>
<pre><code>function greet(name) {
    return "Hello, " + name + "!";
}

const add = (a, b) =&gt; a + b;

console.log(greet("Bob"));
console.log(add(3, 4));</code></pre>

<div class="mermaid">
graph TD
    A[JavaScript Types] --> B[String]
    A --> C[Number]
    A --> D[Boolean]
    A --> E[null]
    A --> F[undefined]
    A --> G[Object]
    A --> H[Array]
    B --> I["'hello'"]
    C --> J["42, 3.14"]
    D --> K["true, false"]
</div>

<div class="takeaways">
<h2>まとめ</h2>
<ul>
<li>変更する変数にはlet、変わらない値にはconstを使います</li>
<li>console.log()はデバッグの最良の味方です</li>
<li>関数は再利用可能なロジックをカプセル化します</li>
<li>アロー関数はシンプルな関数の短い構文を提供します</li>
</ul>
</div>
""",
    },
    'T08': {
        'en': """
<h1>T08: DOM Manipulation</h1>
<p class="lesson-intro">The DOM (Document Object Model) is the browser's live representation of your HTML page. Think of it as a tree made of building blocks - JavaScript lets you add, remove, and rearrange those blocks while the user watches. Every element is a node you can reach and modify.</p>

<h2>Selecting Elements</h2>
<p>Before you can change an element, you need to find it. The <code>querySelector</code> method uses CSS selector syntax to grab elements.</p>
<pre><code>const title = document.querySelector("h1");
const items = document.querySelectorAll(".item");
const form = document.querySelector("#signup-form");</code></pre>

<h2>Creating and Modifying Elements</h2>
<p>Create new elements with <code>createElement</code>, set their content, and append them to the page.</p>
<pre><code>const card = document.createElement("div");
card.className = "card";
card.textContent = "New card content";
document.querySelector(".container").appendChild(card);</code></pre>

<h2>Event Handling</h2>
<p>Events let your page respond to user actions. Click, hover, type - each triggers an event you can listen for.</p>
<pre><code>const button = document.querySelector("#submit");
button.addEventListener("click", function(event) {
    event.preventDefault();
    console.log("Button was clicked!");
});</code></pre>

<div class="mermaid">
graph TD
    A[document] --> B[html]
    B --> C[head]
    B --> D[body]
    D --> E[h1]
    D --> F[div.container]
    F --> G[p]
    F --> H[button]
    H -->|click event| I[Event Handler]
    I -->|modifies| F
</div>

<div class="takeaways">
<h2>Key Takeaways</h2>
<ul>
<li>querySelector and querySelectorAll find elements using CSS selector syntax</li>
<li>createElement and appendChild let you build new DOM nodes dynamically</li>
<li>addEventListener connects user actions to your JavaScript functions</li>
<li>Always use event.preventDefault() when you want to stop default browser behavior</li>
</ul>
</div>
""",
        'ja': """
<h1>T08: DOM操作</h1>
<p class="lesson-intro">DOM(ドキュメントオブジェクトモデル)はHTMLページのブラウザ内でのライブ表現です。積み木で作った木のようなもので、JavaScriptでユーザーが見ている間にブロックを追加、削除、並べ替えできます。全ての要素はアクセスして変更できるノードです。</p>

<h2>要素の選択</h2>
<p>要素を変更するには、まず見つける必要があります。<code>querySelector</code>メソッドはCSSセレクタ構文で要素を取得します。</p>
<pre><code>const title = document.querySelector("h1");
const items = document.querySelectorAll(".item");
const form = document.querySelector("#signup-form");</code></pre>

<h2>要素の作成と変更</h2>
<p><code>createElement</code>で新しい要素を作成し、内容を設定してページに追加します。</p>
<pre><code>const card = document.createElement("div");
card.className = "card";
card.textContent = "New card content";
document.querySelector(".container").appendChild(card);</code></pre>

<h2>イベント処理</h2>
<p>イベントでページがユーザーの操作に応答します。クリック、ホバー、入力、それぞれがリッスンできるイベントを発火します。</p>
<pre><code>const button = document.querySelector("#submit");
button.addEventListener("click", function(event) {
    event.preventDefault();
    console.log("Button was clicked!");
});</code></pre>

<div class="mermaid">
graph TD
    A[document] --> B[html]
    B --> C[head]
    B --> D[body]
    D --> E[h1]
    D --> F[div.container]
    F --> G[p]
    F --> H[button]
    H -->|click event| I[Event Handler]
    I -->|modifies| F
</div>

<div class="takeaways">
<h2>まとめ</h2>
<ul>
<li>querySelectorとquerySelectorAllはCSSセレクタ構文で要素を検索します</li>
<li>createElementとappendChildで新しいDOMノードを動的に構築できます</li>
<li>addEventListenerでユーザー操作とJavaScript関数を接続します</li>
<li>デフォルトのブラウザ動作を止めたい時はevent.preventDefault()を使います</li>
</ul>
</div>
""",
    },
    'T09': {
        'en': """
<h1>T09: Forms and Dialog</h1>
<p class="lesson-intro">HTML forms collect data, but JavaScript validates and processes it. The dialog element gives you native modal windows without any library. Together they create a smooth data collection experience - like a smart receptionist who checks your paperwork before filing it.</p>

<h2>JavaScript Form Validation</h2>
<p>While HTML has built-in validation (required, type), JavaScript gives you full control over validation logic and custom error messages.</p>
<pre><code>const form = document.querySelector("#myForm");
form.addEventListener("submit", function(event) {
    const email = form.querySelector("#email").value;
    if (!email.includes("@")) {
        event.preventDefault();
        showError("Please enter a valid email address.");
    }
});

function showError(message) {
    const errorDiv = document.querySelector(".error");
    errorDiv.textContent = message;
    errorDiv.style.display = "block";
}</code></pre>

<h2>The Dialog Element</h2>
<p>The <code>&lt;dialog&gt;</code> element provides native modal and non-modal dialogs. Use <code>showModal()</code> for modals with backdrop, or <code>show()</code> for non-modal.</p>
<pre><code>&lt;dialog id="confirm"&gt;
    &lt;p&gt;Are you sure?&lt;/p&gt;
    &lt;button id="yes"&gt;Yes&lt;/button&gt;
    &lt;button id="no"&gt;No&lt;/button&gt;
&lt;/dialog&gt;

&lt;script&gt;
const dialog = document.querySelector("#confirm");
dialog.showModal();
dialog.querySelector("#no").addEventListener("click", () =&gt; dialog.close());
&lt;/script&gt;</code></pre>

<div class="mermaid">
flowchart TD
    A[User submits form] --> B{JS Validation}
    B -->|Invalid| C[Show error message]
    C --> A
    B -->|Valid| D{Needs confirmation?}
    D -->|Yes| E[Open dialog]
    E --> F{User confirms?}
    F -->|Yes| G[Process data]
    F -->|No| A
    D -->|No| G
</div>

<div class="takeaways">
<h2>Key Takeaways</h2>
<ul>
<li>JavaScript validation gives you custom logic beyond HTML5 built-in validation</li>
<li>The dialog element provides native modal windows without external libraries</li>
<li>Use showModal() for modal dialogs and show() for non-modal ones</li>
<li>Always provide clear error messages that tell users how to fix the problem</li>
</ul>
</div>
""",
        'ja': """
<h1>T09: フォームとダイアログ</h1>
<p class="lesson-intro">HTMLフォームはデータを収集しますが、JavaScriptがそれを検証・処理します。dialog要素はライブラリなしでネイティブモーダルウィンドウを提供します。この組み合わせでスムーズなデータ収集体験を作れます。書類を提出する前にチェックしてくれる賢い受付のようなものです。</p>

<h2>JavaScriptフォームバリデーション</h2>
<p>HTMLには組み込みバリデーション(required, type)がありますが、JavaScriptはバリデーションロジックとカスタムエラーメッセージを完全に制御できます。</p>
<pre><code>const form = document.querySelector("#myForm");
form.addEventListener("submit", function(event) {
    const email = form.querySelector("#email").value;
    if (!email.includes("@")) {
        event.preventDefault();
        showError("Please enter a valid email address.");
    }
});

function showError(message) {
    const errorDiv = document.querySelector(".error");
    errorDiv.textContent = message;
    errorDiv.style.display = "block";
}</code></pre>

<h2>Dialog要素</h2>
<p><code>&lt;dialog&gt;</code>要素はネイティブのモーダル/非モーダルダイアログを提供します。<code>showModal()</code>で背景付きモーダル、<code>show()</code>で非モーダルを表示します。</p>
<pre><code>&lt;dialog id="confirm"&gt;
    &lt;p&gt;Are you sure?&lt;/p&gt;
    &lt;button id="yes"&gt;Yes&lt;/button&gt;
    &lt;button id="no"&gt;No&lt;/button&gt;
&lt;/dialog&gt;

&lt;script&gt;
const dialog = document.querySelector("#confirm");
dialog.showModal();
dialog.querySelector("#no").addEventListener("click", () =&gt; dialog.close());
&lt;/script&gt;</code></pre>

<div class="mermaid">
flowchart TD
    A[User submits form] --> B{JS Validation}
    B -->|Invalid| C[Show error message]
    C --> A
    B -->|Valid| D{Needs confirmation?}
    D -->|Yes| E[Open dialog]
    E --> F{User confirms?}
    F -->|Yes| G[Process data]
    F -->|No| A
    D -->|No| G
</div>

<div class="takeaways">
<h2>まとめ</h2>
<ul>
<li>JavaScriptバリデーションはHTML5組み込みバリデーション以上のカスタムロジックを提供します</li>
<li>dialog要素は外部ライブラリなしでネイティブモーダルウィンドウを提供します</li>
<li>モーダルにはshowModal()、非モーダルにはshow()を使います</li>
<li>ユーザーに問題の修正方法を伝える明確なエラーメッセージを必ず提供しましょう</li>
</ul>
</div>
""",
    },
    'T10': {
        'en': """
<h1>T10: Data Structures</h1>
<p class="lesson-intro">Data structures are containers for organizing information. Arrays are like numbered lists where order matters. Objects are like labeled filing cabinets where you look up information by name. Choosing the right structure makes your code simpler and faster.</p>

<h2>Arrays</h2>
<p>Arrays store ordered collections. Access items by their index (starting from 0). Arrays have powerful built-in methods for transforming data.</p>
<pre><code>const fruits = ["apple", "banana", "cherry"];
console.log(fruits[0]); // "apple"
fruits.push("date");

// Transform with map, filter, reduce
const prices = [10, 20, 30, 40];
const expensive = prices.filter(p =&gt; p &gt; 15);
const doubled = prices.map(p =&gt; p * 2);
const total = prices.reduce((sum, p) =&gt; sum + p, 0);</code></pre>

<h2>Objects</h2>
<p>Objects store key-value pairs. Keys are strings (or symbols), values can be anything.</p>
<pre><code>const user = {
    name: "Alice",
    age: 25,
    skills: ["HTML", "CSS", "JS"],
    greet() {
        return "Hi, I am " + this.name;
    }
};
console.log(user.name);
console.log(user["age"]);</code></pre>

<h2>Loops</h2>
<p>Iterate over arrays with <code>for...of</code> and objects with <code>for...in</code> or <code>Object.entries()</code>.</p>
<pre><code>for (const fruit of fruits) { console.log(fruit); }
for (const [key, value] of Object.entries(user)) { console.log(key, value); }</code></pre>

<div class="mermaid">
graph LR
    subgraph Array
        A0["[0] apple"] --> A1["[1] banana"] --> A2["[2] cherry"]
    end
    subgraph Object
        O1["name: Alice"] --- O2["age: 25"] --- O3["skills: [...]"]
    end
</div>

<div class="takeaways">
<h2>Key Takeaways</h2>
<ul>
<li>Arrays are ordered lists accessed by numeric index starting at 0</li>
<li>Objects are key-value stores accessed by string keys</li>
<li>Use map, filter, and reduce to transform arrays without mutating them</li>
<li>for...of iterates array values, for...in iterates object keys</li>
</ul>
</div>
""",
        'ja': """
<h1>T10: データ構造</h1>
<p class="lesson-intro">データ構造は情報を整理するための入れ物です。配列は順序が重要な番号付きリストです。オブジェクトは名前で情報を検索するラベル付きファイルキャビネットです。適切な構造を選ぶことでコードがシンプルかつ高速になります。</p>

<h2>配列</h2>
<p>配列は順序付きコレクションを格納します。インデックス(0から開始)でアイテムにアクセスします。配列にはデータ変換のための強力な組み込みメソッドがあります。</p>
<pre><code>const fruits = ["apple", "banana", "cherry"];
console.log(fruits[0]); // "apple"
fruits.push("date");

// Transform with map, filter, reduce
const prices = [10, 20, 30, 40];
const expensive = prices.filter(p =&gt; p &gt; 15);
const doubled = prices.map(p =&gt; p * 2);
const total = prices.reduce((sum, p) =&gt; sum + p, 0);</code></pre>

<h2>オブジェクト</h2>
<p>オブジェクトはキーと値のペアを格納します。キーは文字列(またはシンボル)、値は何でも可能です。</p>
<pre><code>const user = {
    name: "Alice",
    age: 25,
    skills: ["HTML", "CSS", "JS"],
    greet() {
        return "Hi, I am " + this.name;
    }
};
console.log(user.name);
console.log(user["age"]);</code></pre>

<h2>ループ</h2>
<p>配列は<code>for...of</code>で、オブジェクトは<code>for...in</code>や<code>Object.entries()</code>で反復処理します。</p>
<pre><code>for (const fruit of fruits) { console.log(fruit); }
for (const [key, value] of Object.entries(user)) { console.log(key, value); }</code></pre>

<div class="mermaid">
graph LR
    subgraph Array
        A0["[0] apple"] --> A1["[1] banana"] --> A2["[2] cherry"]
    end
    subgraph Object
        O1["name: Alice"] --- O2["age: 25"] --- O3["skills: [...]"]
    end
</div>

<div class="takeaways">
<h2>まとめ</h2>
<ul>
<li>配列は0から始まるインデックスでアクセスする順序付きリストです</li>
<li>オブジェクトは文字列キーでアクセスするキーバリューストアです</li>
<li>map、filter、reduceで配列を変更せずに変換できます</li>
<li>for...ofは配列の値を、for...inはオブジェクトのキーを反復処理します</li>
</ul>
</div>
""",
    },
    'T11': {
        'en': """
<h1>T11: Persistence</h1>
<p class="lesson-intro">Web pages forget everything when you close them. LocalStorage is like a notebook the browser keeps for your website - data persists even after closing the tab. JSON is the universal format for converting JavaScript objects into storable strings and back.</p>

<h2>localStorage API</h2>
<p>LocalStorage stores key-value pairs as strings. It persists across page reloads and browser restarts, with about 5MB of space per domain.</p>
<pre><code>// Save data
localStorage.setItem("username", "Alice");

// Read data
const name = localStorage.getItem("username");

// Remove data
localStorage.removeItem("username");

// Clear all
localStorage.clear();</code></pre>

<h2>Working with JSON</h2>
<p>Since localStorage only stores strings, use <code>JSON.stringify()</code> to save objects and <code>JSON.parse()</code> to read them back.</p>
<pre><code>const tasks = [
    { id: 1, text: "Learn HTML", done: true },
    { id: 2, text: "Learn CSS", done: false }
];

// Save
localStorage.setItem("tasks", JSON.stringify(tasks));

// Load
const saved = JSON.parse(localStorage.getItem("tasks") || "[]");</code></pre>

<div class="mermaid">
flowchart LR
    A[JS Object] -->|JSON.stringify| B[JSON String]
    B -->|setItem| C[localStorage]
    C -->|getItem| D[JSON String]
    D -->|JSON.parse| E[JS Object]
    C -->|persists across| F[Page Reloads]
    C -->|persists across| G[Browser Restart]
</div>

<div class="takeaways">
<h2>Key Takeaways</h2>
<ul>
<li>localStorage persists data across page reloads and browser restarts</li>
<li>All values are stored as strings - use JSON for complex data</li>
<li>JSON.stringify converts objects to strings, JSON.parse converts back</li>
<li>localStorage has a 5MB limit per domain - use it for small data only</li>
</ul>
</div>
""",
        'ja': """
<h1>T11: データの永続化</h1>
<p class="lesson-intro">Webページは閉じると全てを忘れます。localStorageはブラウザがあなたのWebサイト用に保持するノートのようなものです。タブを閉じてもデータは残ります。JSONはJavaScriptオブジェクトを保存可能な文字列に変換し、元に戻すための共通形式です。</p>

<h2>localStorage API</h2>
<p>localStorageはキーバリューペアを文字列として格納します。ページのリロードやブラウザの再起動後も持続し、ドメインあたり約5MBの容量があります。</p>
<pre><code>// Save data
localStorage.setItem("username", "Alice");

// Read data
const name = localStorage.getItem("username");

// Remove data
localStorage.removeItem("username");

// Clear all
localStorage.clear();</code></pre>

<h2>JSONの活用</h2>
<p>localStorageは文字列のみ格納するため、<code>JSON.stringify()</code>でオブジェクトを保存し、<code>JSON.parse()</code>で読み戻します。</p>
<pre><code>const tasks = [
    { id: 1, text: "Learn HTML", done: true },
    { id: 2, text: "Learn CSS", done: false }
];

// Save
localStorage.setItem("tasks", JSON.stringify(tasks));

// Load
const saved = JSON.parse(localStorage.getItem("tasks") || "[]");</code></pre>

<div class="mermaid">
flowchart LR
    A[JS Object] -->|JSON.stringify| B[JSON String]
    B -->|setItem| C[localStorage]
    C -->|getItem| D[JSON String]
    D -->|JSON.parse| E[JS Object]
    C -->|persists across| F[Page Reloads]
    C -->|persists across| G[Browser Restart]
</div>

<div class="takeaways">
<h2>まとめ</h2>
<ul>
<li>localStorageはページリロードやブラウザ再起動後もデータを保持します</li>
<li>全ての値は文字列として格納されます。複雑なデータにはJSONを使います</li>
<li>JSON.stringifyでオブジェクトを文字列に、JSON.parseで元に戻します</li>
<li>localStorageはドメインあたり5MB制限があります。小さなデータ専用です</li>
</ul>
</div>
""",
    },
    'T12': {
        'en': """
<h1>T12: Fetch API</h1>
<p class="lesson-intro">The Fetch API lets your JavaScript talk to servers. It is like sending a letter and waiting for a reply - you make a request, the server processes it, and sends back a response. The async/await syntax makes this asynchronous communication read like synchronous code.</p>

<h2>HTTP Basics</h2>
<p>HTTP is the protocol browsers use to communicate with servers. Every request has a method (GET, POST, PUT, DELETE) and every response has a status code (200 OK, 404 Not Found, 500 Error).</p>

<h2>Making Requests</h2>
<p>The <code>fetch()</code> function returns a Promise. Use <code>async/await</code> for clean, readable asynchronous code.</p>
<pre><code>// GET request
async function getUsers() {
    const response = await fetch("/api/users");
    const data = await response.json();
    return data;
}

// POST request
async function createUser(user) {
    const response = await fetch("/api/users", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(user)
    });
    return await response.json();
}</code></pre>

<h2>Error Handling</h2>
<pre><code>try {
    const data = await getUsers();
    renderUsers(data);
} catch (error) {
    console.error("Failed to fetch:", error);
    showErrorMessage("Could not load users. Try again.");
}</code></pre>

<div class="mermaid">
sequenceDiagram
    participant B as Browser
    participant S as Server
    B->>S: GET /api/users
    S-->>B: 200 OK + JSON data
    B->>S: POST /api/users + body
    S-->>B: 201 Created + new user
    B->>S: GET /api/missing
    S-->>B: 404 Not Found
</div>

<div class="takeaways">
<h2>Key Takeaways</h2>
<ul>
<li>fetch() sends HTTP requests and returns Promises</li>
<li>async/await makes asynchronous code readable and maintainable</li>
<li>Always handle errors with try/catch when making network requests</li>
<li>Use response.json() to parse JSON response bodies</li>
</ul>
</div>
""",
        'ja': """
<h1>T12: Fetch API</h1>
<p class="lesson-intro">Fetch APIはJavaScriptからサーバーと通信する手段です。手紙を送って返事を待つようなもので、リクエストを送り、サーバーが処理し、レスポンスを返します。async/await構文でこの非同期通信を同期的なコードのように読めるようにします。</p>

<h2>HTTPの基本</h2>
<p>HTTPはブラウザがサーバーと通信するプロトコルです。全てのリクエストにはメソッド(GET, POST, PUT, DELETE)があり、全てのレスポンスにはステータスコード(200 OK, 404 Not Found, 500 Error)があります。</p>

<h2>リクエストの送信</h2>
<p><code>fetch()</code>関数はPromiseを返します。<code>async/await</code>でクリーンで読みやすい非同期コードを書けます。</p>
<pre><code>// GET request
async function getUsers() {
    const response = await fetch("/api/users");
    const data = await response.json();
    return data;
}

// POST request
async function createUser(user) {
    const response = await fetch("/api/users", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(user)
    });
    return await response.json();
}</code></pre>

<h2>エラー処理</h2>
<pre><code>try {
    const data = await getUsers();
    renderUsers(data);
} catch (error) {
    console.error("Failed to fetch:", error);
    showErrorMessage("Could not load users. Try again.");
}</code></pre>

<div class="mermaid">
sequenceDiagram
    participant B as Browser
    participant S as Server
    B->>S: GET /api/users
    S-->>B: 200 OK + JSON data
    B->>S: POST /api/users + body
    S-->>B: 201 Created + new user
    B->>S: GET /api/missing
    S-->>B: 404 Not Found
</div>

<div class="takeaways">
<h2>まとめ</h2>
<ul>
<li>fetch()はHTTPリクエストを送信しPromiseを返します</li>
<li>async/awaitで非同期コードが読みやすく保守しやすくなります</li>
<li>ネットワークリクエストではtry/catchで必ずエラー処理をしましょう</li>
<li>response.json()でJSONレスポンスボディをパースします</li>
</ul>
</div>
""",
    },
    'T13': {
        'en': """
<h1>T13: Dynamic Site - Routing</h1>
<p class="lesson-intro">In a traditional website, each page is a separate HTML file. A Single Page Application (SPA) loads once and swaps content dynamically. Hash routing uses the URL fragment (the part after #) to determine which view to show - like chapters in a book that you flip to without getting a new book.</p>

<h2>Hash-Based Routing</h2>
<p>The hash portion of the URL (after #) does not trigger a page reload. We can listen for hash changes and render different content.</p>
<pre><code>const routes = {
    "#/": renderHome,
    "#/about": renderAbout,
    "#/contact": renderContact
};

function router() {
    const hash = window.location.hash || "#/";
    const renderFn = routes[hash] || renderNotFound;
    renderFn();
}

window.addEventListener("hashchange", router);
window.addEventListener("load", router);</code></pre>

<h2>Dynamic Content Rendering</h2>
<pre><code>function renderHome() {
    document.querySelector("#app").innerHTML = `
        &lt;h1&gt;Home&lt;/h1&gt;
        &lt;p&gt;Welcome to the site.&lt;/p&gt;
        &lt;a href="#/about"&gt;About Us&lt;/a&gt;
    `;
}</code></pre>

<div class="mermaid">
flowchart TD
    A[User clicks link] --> B[URL hash changes]
    B --> C[hashchange event fires]
    C --> D{Match route?}
    D -->|Yes| E[Render matched view]
    D -->|No| F[Render 404 page]
    E --> G[Update #app content]
    F --> G
    G --> H[Page stays loaded]
</div>

<div class="takeaways">
<h2>Key Takeaways</h2>
<ul>
<li>SPAs load one HTML file and swap content dynamically via JavaScript</li>
<li>Hash routing uses the URL fragment to determine which view to display</li>
<li>The hashchange event fires whenever the URL hash changes</li>
<li>A route map object connects hash patterns to render functions</li>
</ul>
</div>
""",
        'ja': """
<h1>T13: 動的サイト - ルーティング</h1>
<p class="lesson-intro">従来のWebサイトでは各ページが別々のHTMLファイルです。シングルページアプリケーション(SPA)は一度読み込んでコンテンツを動的に入れ替えます。ハッシュルーティングはURLフラグメント(#の後の部分)でどのビューを表示するか決定します。新しい本を取りに行かずにページをめくるようなものです。</p>

<h2>ハッシュベースルーティング</h2>
<p>URLのハッシュ部分(#の後)はページリロードを引き起こしません。ハッシュの変更をリッスンして異なるコンテンツを描画できます。</p>
<pre><code>const routes = {
    "#/": renderHome,
    "#/about": renderAbout,
    "#/contact": renderContact
};

function router() {
    const hash = window.location.hash || "#/";
    const renderFn = routes[hash] || renderNotFound;
    renderFn();
}

window.addEventListener("hashchange", router);
window.addEventListener("load", router);</code></pre>

<h2>動的コンテンツ描画</h2>
<pre><code>function renderHome() {
    document.querySelector("#app").innerHTML = `
        &lt;h1&gt;Home&lt;/h1&gt;
        &lt;p&gt;Welcome to the site.&lt;/p&gt;
        &lt;a href="#/about"&gt;About Us&lt;/a&gt;
    `;
}</code></pre>

<div class="mermaid">
flowchart TD
    A[User clicks link] --> B[URL hash changes]
    B --> C[hashchange event fires]
    C --> D{Match route?}
    D -->|Yes| E[Render matched view]
    D -->|No| F[Render 404 page]
    E --> G[Update #app content]
    F --> G
    G --> H[Page stays loaded]
</div>

<div class="takeaways">
<h2>まとめ</h2>
<ul>
<li>SPAは1つのHTMLファイルを読み込み、JavaScriptでコンテンツを動的に入れ替えます</li>
<li>ハッシュルーティングはURLフラグメントでどのビューを表示するか決定します</li>
<li>hashchangeイベントはURLハッシュが変わるたびに発火します</li>
<li>ルートマップオブジェクトがハッシュパターンと描画関数を接続します</li>
</ul>
</div>
""",
    },
    'T14': {
        'en': """
<h1>T14: Dynamic Site - Offline</h1>
<p class="lesson-intro">Service Workers are scripts that run in the background, separate from your web page. They intercept network requests and can serve cached responses when offline. Think of a Service Worker as a programmable proxy server living inside the browser - it decides whether to fetch from the network or serve from cache.</p>

<h2>Registering a Service Worker</h2>
<pre><code>// In your main JS file
if ("serviceWorker" in navigator) {
    navigator.serviceWorker.register("/sw.js")
        .then(reg =&gt; console.log("SW registered"))
        .catch(err =&gt; console.error("SW failed:", err));
}</code></pre>

<h2>The Service Worker File</h2>
<pre><code>// sw.js
const CACHE_NAME = "v1";
const ASSETS = ["/", "/index.html", "/style.css", "/app.js"];

self.addEventListener("install", event =&gt; {
    event.waitUntil(
        caches.open(CACHE_NAME)
            .then(cache =&gt; cache.addAll(ASSETS))
    );
});

self.addEventListener("fetch", event =&gt; {
    event.respondWith(
        caches.match(event.request)
            .then(cached =&gt; cached || fetch(event.request))
    );
});</code></pre>

<h2>PWA Manifest</h2>
<p>Add a <code>manifest.json</code> file to make your site installable as an app on mobile devices.</p>

<div class="mermaid">
stateDiagram-v2
    [*] --> Installing: register()
    Installing --> Installed: install event
    Installed --> Activating: activate
    Activating --> Active: activated
    Active --> Active: fetch events
    Active --> Redundant: new SW takes over
    note right of Active: Intercepts all fetch requests
</div>

<div class="takeaways">
<h2>Key Takeaways</h2>
<ul>
<li>Service Workers run in the background and intercept network requests</li>
<li>Cache assets during install to enable offline functionality</li>
<li>The fetch event handler decides: serve from cache or fetch from network</li>
<li>A manifest.json file makes your web app installable on mobile devices</li>
</ul>
</div>
""",
        'ja': """
<h1>T14: 動的サイト - オフライン対応</h1>
<p class="lesson-intro">Service Workerはバックグラウンドで動作するスクリプトで、Webページとは別に実行されます。ネットワークリクエストを傍受し、オフライン時にキャッシュからレスポンスを返せます。ブラウザ内に住むプログラム可能なプロキシサーバーと考えてください。ネットワークから取得するかキャッシュから返すかを判断します。</p>

<h2>Service Workerの登録</h2>
<pre><code>// In your main JS file
if ("serviceWorker" in navigator) {
    navigator.serviceWorker.register("/sw.js")
        .then(reg =&gt; console.log("SW registered"))
        .catch(err =&gt; console.error("SW failed:", err));
}</code></pre>

<h2>Service Workerファイル</h2>
<pre><code>// sw.js
const CACHE_NAME = "v1";
const ASSETS = ["/", "/index.html", "/style.css", "/app.js"];

self.addEventListener("install", event =&gt; {
    event.waitUntil(
        caches.open(CACHE_NAME)
            .then(cache =&gt; cache.addAll(ASSETS))
    );
});

self.addEventListener("fetch", event =&gt; {
    event.respondWith(
        caches.match(event.request)
            .then(cached =&gt; cached || fetch(event.request))
    );
});</code></pre>

<h2>PWAマニフェスト</h2>
<p><code>manifest.json</code>ファイルを追加してモバイルデバイスでアプリとしてインストール可能にします。</p>

<div class="mermaid">
stateDiagram-v2
    [*] --> Installing: register()
    Installing --> Installed: install event
    Installed --> Activating: activate
    Activating --> Active: activated
    Active --> Active: fetch events
    Active --> Redundant: new SW takes over
    note right of Active: Intercepts all fetch requests
</div>

<div class="takeaways">
<h2>まとめ</h2>
<ul>
<li>Service Workerはバックグラウンドで実行され、ネットワークリクエストを傍受します</li>
<li>インストール時にアセットをキャッシュしてオフライン機能を有効にします</li>
<li>fetchイベントハンドラがキャッシュから返すかネットワークから取得するかを決定します</li>
<li>manifest.jsonファイルでWebアプリをモバイルデバイスにインストール可能にします</li>
</ul>
</div>
""",
    },
    'T15': {
        'en': """
<h1>T15: Dynamic Site - Polish</h1>
<p class="lesson-intro">Performance is a feature. Users abandon sites that load slowly. Polishing your site means optimizing what loads, when it loads, and how it loads. Like a restaurant that prepares popular dishes in advance and only cooks rare orders on demand.</p>

<h2>Lazy Loading</h2>
<p>Load images and content only when they enter the viewport. The <code>loading="lazy"</code> attribute handles images natively.</p>
<pre><code>&lt;img src="photo.jpg" loading="lazy" alt="Lazy loaded"&gt;

// For custom lazy loading with Intersection Observer
const observer = new IntersectionObserver((entries) =&gt; {
    entries.forEach(entry =&gt; {
        if (entry.isIntersecting) {
            const img = entry.target;
            img.src = img.dataset.src;
            observer.unobserve(img);
        }
    });
});</code></pre>

<h2>Performance Techniques</h2>
<p>Minimize render-blocking resources. Defer non-critical JavaScript. Use efficient selectors and reduce DOM size.</p>
<pre><code>&lt;!-- Defer non-critical JS --&gt;
&lt;script src="app.js" defer&gt;&lt;/script&gt;

&lt;!-- Preload critical resources --&gt;
&lt;link rel="preload" href="font.woff2" as="font" crossorigin&gt;</code></pre>

<h2>Code Splitting</h2>
<p>Load only the JavaScript needed for the current view. Import additional modules when the user navigates to them.</p>
<pre><code>async function loadModule(name) {
    const module = await import(`./modules/${name}.js`);
    module.init();
}</code></pre>

<div class="mermaid">
sequenceDiagram
    participant B as Browser
    participant S as Server
    B->>S: Initial HTML + critical CSS
    S-->>B: Minimal payload
    B->>B: Render above-the-fold
    B->>S: Lazy load images (on scroll)
    B->>S: Deferred JS modules
    S-->>B: Additional resources
    B->>B: Progressive enhancement
</div>

<div class="takeaways">
<h2>Key Takeaways</h2>
<ul>
<li>Lazy loading defers non-visible content until it enters the viewport</li>
<li>Use defer attribute on script tags to avoid render-blocking</li>
<li>Preload critical resources like fonts to speed up first paint</li>
<li>Code splitting loads only the JavaScript needed for the current view</li>
</ul>
</div>
""",
        'ja': """
<h1>T15: 動的サイト - 仕上げ</h1>
<p class="lesson-intro">パフォーマンスは機能です。読み込みが遅いサイトからユーザーは離脱します。サイトの仕上げとは、何を読み込むか、いつ読み込むか、どう読み込むかの最適化です。人気料理を事前に準備し、珍しい注文だけオンデマンドで調理するレストランのようなものです。</p>

<h2>遅延読み込み</h2>
<p>画像やコンテンツをビューポートに入った時だけ読み込みます。<code>loading="lazy"</code>属性で画像をネイティブに処理できます。</p>
<pre><code>&lt;img src="photo.jpg" loading="lazy" alt="Lazy loaded"&gt;

// For custom lazy loading with Intersection Observer
const observer = new IntersectionObserver((entries) =&gt; {
    entries.forEach(entry =&gt; {
        if (entry.isIntersecting) {
            const img = entry.target;
            img.src = img.dataset.src;
            observer.unobserve(img);
        }
    });
});</code></pre>

<h2>パフォーマンステクニック</h2>
<p>レンダリングをブロックするリソースを最小化します。重要でないJavaScriptを遅延させます。効率的なセレクタを使い、DOMサイズを削減します。</p>
<pre><code>&lt;!-- Defer non-critical JS --&gt;
&lt;script src="app.js" defer&gt;&lt;/script&gt;

&lt;!-- Preload critical resources --&gt;
&lt;link rel="preload" href="font.woff2" as="font" crossorigin&gt;</code></pre>

<h2>コード分割</h2>
<p>現在のビューに必要なJavaScriptだけを読み込みます。ユーザーがナビゲートした時に追加モジュールをインポートします。</p>
<pre><code>async function loadModule(name) {
    const module = await import(`./modules/${name}.js`);
    module.init();
}</code></pre>

<div class="mermaid">
sequenceDiagram
    participant B as Browser
    participant S as Server
    B->>S: Initial HTML + critical CSS
    S-->>B: Minimal payload
    B->>B: Render above-the-fold
    B->>S: Lazy load images (on scroll)
    B->>S: Deferred JS modules
    S-->>B: Additional resources
    B->>B: Progressive enhancement
</div>

<div class="takeaways">
<h2>まとめ</h2>
<ul>
<li>遅延読み込みはビューポートに入るまで非表示コンテンツの読み込みを延期します</li>
<li>scriptタグにdefer属性を使ってレンダリングブロックを回避します</li>
<li>フォントなどの重要リソースをプリロードして初回描画を高速化します</li>
<li>コード分割で現在のビューに必要なJavaScriptだけを読み込みます</li>
</ul>
</div>
""",
    },
    'T16': {
        'en': """
<h1>T16: Node.js Server</h1>
<p class="lesson-intro">Until now, you have been opening HTML files directly in the browser. A web server is a program that listens for requests and sends back responses. Node.js lets you write that server in JavaScript - the same language you already know from the browser. It is like hiring a receptionist who speaks the same language as your entire team.</p>

<h2>Creating an HTTP Server</h2>
<pre><code>const http = require("http");
const fs = require("fs");
const path = require("path");

const server = http.createServer((req, res) =&gt; {
    const filePath = path.join(__dirname, "public", req.url === "/" ? "index.html" : req.url);
    const ext = path.extname(filePath);
    const contentTypes = {
        ".html": "text/html",
        ".css": "text/css",
        ".js": "text/javascript"
    };

    fs.readFile(filePath, (err, content) =&gt; {
        if (err) {
            res.writeHead(404);
            res.end("Not Found");
            return;
        }
        res.writeHead(200, { "Content-Type": contentTypes[ext] || "text/plain" });
        res.end(content);
    });
});

server.listen(3000, () =&gt; console.log("Server on http://localhost:3000"));</code></pre>

<h2>Serving Static Files</h2>
<p>The server reads files from the "public" folder and sends them to the browser with the correct content type header.</p>

<div class="mermaid">
flowchart LR
    A[Browser] -->|HTTP Request| B[Node.js Server]
    B -->|Read file| C[File System]
    C -->|File contents| B
    B -->|HTTP Response| A
    B -->|404| D[Not Found]
</div>

<div class="takeaways">
<h2>Key Takeaways</h2>
<ul>
<li>Node.js runs JavaScript outside the browser on your server</li>
<li>http.createServer creates a server that handles requests and responses</li>
<li>Content-Type headers tell the browser how to interpret the response</li>
<li>Static file serving maps URL paths to files on disk</li>
</ul>
</div>
""",
        'ja': """
<h1>T16: Node.jsサーバー</h1>
<p class="lesson-intro">これまでHTMLファイルをブラウザで直接開いていました。Webサーバーはリクエストを待ち受けてレスポンスを返すプログラムです。Node.jsならブラウザと同じJavaScriptでサーバーを書けます。チーム全員と同じ言語を話す受付を雇うようなものです。</p>

<h2>HTTPサーバーの作成</h2>
<pre><code>const http = require("http");
const fs = require("fs");
const path = require("path");

const server = http.createServer((req, res) =&gt; {
    const filePath = path.join(__dirname, "public", req.url === "/" ? "index.html" : req.url);
    const ext = path.extname(filePath);
    const contentTypes = {
        ".html": "text/html",
        ".css": "text/css",
        ".js": "text/javascript"
    };

    fs.readFile(filePath, (err, content) =&gt; {
        if (err) {
            res.writeHead(404);
            res.end("Not Found");
            return;
        }
        res.writeHead(200, { "Content-Type": contentTypes[ext] || "text/plain" });
        res.end(content);
    });
});

server.listen(3000, () =&gt; console.log("Server on http://localhost:3000"));</code></pre>

<h2>静的ファイルの配信</h2>
<p>サーバーは"public"フォルダからファイルを読み取り、正しいContent-Typeヘッダー付きでブラウザに送信します。</p>

<div class="mermaid">
flowchart LR
    A[Browser] -->|HTTP Request| B[Node.js Server]
    B -->|Read file| C[File System]
    C -->|File contents| B
    B -->|HTTP Response| A
    B -->|404| D[Not Found]
</div>

<div class="takeaways">
<h2>まとめ</h2>
<ul>
<li>Node.jsはブラウザの外でサーバー上のJavaScriptを実行します</li>
<li>http.createServerでリクエストとレスポンスを処理するサーバーを作成します</li>
<li>Content-Typeヘッダーがブラウザにレスポンスの解釈方法を伝えます</li>
<li>静的ファイル配信はURLパスをディスク上のファイルにマッピングします</li>
</ul>
</div>
""",
    },
    'T17': {
        'en': """
<h1>T17: API Endpoints</h1>
<p class="lesson-intro">An API (Application Programming Interface) is a set of endpoints your server exposes for clients to interact with data. REST is a design convention where URLs represent resources and HTTP methods represent actions. Think of it as a menu at a restaurant - the menu lists what you can order and how.</p>

<h2>REST Conventions</h2>
<p>RESTful APIs follow a pattern: resources are nouns in the URL, actions are HTTP methods.</p>
<pre><code>// GET    /api/users      - List all users
// GET    /api/users/1    - Get user with id 1
// POST   /api/users      - Create a new user
// PUT    /api/users/1    - Update user 1
// DELETE /api/users/1    - Delete user 1</code></pre>

<h2>Building Endpoints</h2>
<pre><code>const server = http.createServer((req, res) =&gt; {
    const url = req.url;
    const method = req.method;

    res.setHeader("Content-Type", "application/json");

    if (url === "/api/users" &amp;&amp; method === "GET") {
        res.end(JSON.stringify(users));
    } else if (url === "/api/users" &amp;&amp; method === "POST") {
        let body = "";
        req.on("data", chunk =&gt; body += chunk);
        req.on("end", () =&gt; {
            const user = JSON.parse(body);
            users.push(user);
            res.writeHead(201);
            res.end(JSON.stringify(user));
        });
    } else {
        res.writeHead(404);
        res.end(JSON.stringify({ error: "Not Found" }));
    }
});</code></pre>

<div class="mermaid">
flowchart TD
    A[Client Request] --> B{Route Match}
    B -->|GET /api/users| C[Return user list]
    B -->|POST /api/users| D[Create new user]
    B -->|GET /api/users/:id| E[Return single user]
    B -->|PUT /api/users/:id| F[Update user]
    B -->|DELETE /api/users/:id| G[Remove user]
    B -->|No match| H[404 Not Found]
</div>

<div class="takeaways">
<h2>Key Takeaways</h2>
<ul>
<li>REST uses URLs as resource identifiers and HTTP methods as actions</li>
<li>GET reads, POST creates, PUT updates, DELETE removes</li>
<li>API responses should be JSON with appropriate status codes</li>
<li>Always handle unknown routes with a 404 response</li>
</ul>
</div>
""",
        'ja': """
<h1>T17: APIエンドポイント</h1>
<p class="lesson-intro">API(アプリケーションプログラミングインターフェース)はサーバーがクライアントにデータ操作のために公開するエンドポイントの集合です。RESTはURLがリソースを、HTTPメソッドがアクションを表すデザイン規約です。レストランのメニューのようなものです。何を注文できて、どう注文するかがリストされています。</p>

<h2>REST規約</h2>
<p>RESTful APIはパターンに従います。リソースはURLの名詞、アクションはHTTPメソッドです。</p>
<pre><code>// GET    /api/users      - List all users
// GET    /api/users/1    - Get user with id 1
// POST   /api/users      - Create a new user
// PUT    /api/users/1    - Update user 1
// DELETE /api/users/1    - Delete user 1</code></pre>

<h2>エンドポイントの構築</h2>
<pre><code>const server = http.createServer((req, res) =&gt; {
    const url = req.url;
    const method = req.method;

    res.setHeader("Content-Type", "application/json");

    if (url === "/api/users" &amp;&amp; method === "GET") {
        res.end(JSON.stringify(users));
    } else if (url === "/api/users" &amp;&amp; method === "POST") {
        let body = "";
        req.on("data", chunk =&gt; body += chunk);
        req.on("end", () =&gt; {
            const user = JSON.parse(body);
            users.push(user);
            res.writeHead(201);
            res.end(JSON.stringify(user));
        });
    } else {
        res.writeHead(404);
        res.end(JSON.stringify({ error: "Not Found" }));
    }
});</code></pre>

<div class="mermaid">
flowchart TD
    A[Client Request] --> B{Route Match}
    B -->|GET /api/users| C[Return user list]
    B -->|POST /api/users| D[Create new user]
    B -->|GET /api/users/:id| E[Return single user]
    B -->|PUT /api/users/:id| F[Update user]
    B -->|DELETE /api/users/:id| G[Remove user]
    B -->|No match| H[404 Not Found]
</div>

<div class="takeaways">
<h2>まとめ</h2>
<ul>
<li>RESTはURLをリソース識別子、HTTPメソッドをアクションとして使います</li>
<li>GETは読取、POSTは作成、PUTは更新、DELETEは削除</li>
<li>APIレスポンスは適切なステータスコード付きのJSONにすべきです</li>
<li>未知のルートは必ず404レスポンスで処理しましょう</li>
</ul>
</div>
""",
    },
    'T18': {
        'en': """
<h1>T18: JSON Database</h1>
<p class="lesson-intro">Before learning a real database, you can use a JSON file as a simple data store. Read the file, parse it, modify the data, and write it back. It is like a notebook where you write down and cross out entries - simple but effective for small applications.</p>

<h2>Reading and Writing db.json</h2>
<pre><code>const fs = require("fs");
const DB_PATH = "./db.json";

function readDB() {
    const raw = fs.readFileSync(DB_PATH, "utf-8");
    return JSON.parse(raw);
}

function writeDB(data) {
    fs.writeFileSync(DB_PATH, JSON.stringify(data, null, 2));
}</code></pre>

<h2>CRUD Operations</h2>
<pre><code>// Create
function addUser(user) {
    const db = readDB();
    user.id = Date.now();
    db.users.push(user);
    writeDB(db);
    return user;
}

// Read
function getUsers() { return readDB().users; }

// Update
function updateUser(id, updates) {
    const db = readDB();
    const index = db.users.findIndex(u =&gt; u.id === id);
    if (index === -1) return null;
    db.users[index] = { ...db.users[index], ...updates };
    writeDB(db);
    return db.users[index];
}

// Delete
function deleteUser(id) {
    const db = readDB();
    db.users = db.users.filter(u =&gt; u.id !== id);
    writeDB(db);
}</code></pre>

<div class="mermaid">
flowchart LR
    subgraph CRUD
        C[Create] -->|push + write| DB[(db.json)]
        R[Read] -->|parse| DB
        U[Update] -->|find + modify + write| DB
        D[Delete] -->|filter + write| DB
    end
    API[API Endpoint] --> CRUD
</div>

<div class="takeaways">
<h2>Key Takeaways</h2>
<ul>
<li>A JSON file can serve as a simple database for small projects</li>
<li>CRUD stands for Create, Read, Update, Delete - the four basic data operations</li>
<li>Always read the full file, modify in memory, then write back</li>
<li>JSON databases do not scale - use a real database for production</li>
</ul>
</div>
""",
        'ja': """
<h1>T18: JSONデータベース</h1>
<p class="lesson-intro">本格的なデータベースを学ぶ前に、JSONファイルをシンプルなデータストアとして使えます。ファイルを読み取り、パースし、データを変更し、書き戻します。エントリを書いたり消したりするノートのようなものです。シンプルですが小さなアプリケーションには効果的です。</p>

<h2>db.jsonの読み書き</h2>
<pre><code>const fs = require("fs");
const DB_PATH = "./db.json";

function readDB() {
    const raw = fs.readFileSync(DB_PATH, "utf-8");
    return JSON.parse(raw);
}

function writeDB(data) {
    fs.writeFileSync(DB_PATH, JSON.stringify(data, null, 2));
}</code></pre>

<h2>CRUD操作</h2>
<pre><code>// Create
function addUser(user) {
    const db = readDB();
    user.id = Date.now();
    db.users.push(user);
    writeDB(db);
    return user;
}

// Read
function getUsers() { return readDB().users; }

// Update
function updateUser(id, updates) {
    const db = readDB();
    const index = db.users.findIndex(u =&gt; u.id === id);
    if (index === -1) return null;
    db.users[index] = { ...db.users[index], ...updates };
    writeDB(db);
    return db.users[index];
}

// Delete
function deleteUser(id) {
    const db = readDB();
    db.users = db.users.filter(u =&gt; u.id !== id);
    writeDB(db);
}</code></pre>

<div class="mermaid">
flowchart LR
    subgraph CRUD
        C[Create] -->|push + write| DB[(db.json)]
        R[Read] -->|parse| DB
        U[Update] -->|find + modify + write| DB
        D[Delete] -->|filter + write| DB
    end
    API[API Endpoint] --> CRUD
</div>

<div class="takeaways">
<h2>まとめ</h2>
<ul>
<li>JSONファイルは小さなプロジェクトのシンプルなデータベースとして機能します</li>
<li>CRUDはCreate、Read、Update、Deleteの4つの基本データ操作の略です</li>
<li>常にファイル全体を読み取り、メモリ上で変更してから書き戻します</li>
<li>JSONデータベースはスケールしません。本番では本格的なDBを使いましょう</li>
</ul>
</div>
""",
    },
    'T19': {
        'en': """
<h1>T19: SQLite</h1>
<p class="lesson-intro">SQLite is a real database engine that stores data in a single file. SQL (Structured Query Language) is the language you use to talk to it. If a JSON file is a notebook, SQLite is a proper filing cabinet with labels, categories, and cross-references. It handles concurrent access and data integrity for you.</p>

<h2>Creating Tables</h2>
<pre><code>CREATE TABLE users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    email TEXT UNIQUE NOT NULL,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE posts (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL,
    title TEXT NOT NULL,
    body TEXT,
    FOREIGN KEY (user_id) REFERENCES users(id)
);</code></pre>

<h2>CRUD with SQL</h2>
<pre><code>-- Create
INSERT INTO users (name, email) VALUES ('Alice', 'alice@example.com');

-- Read
SELECT * FROM users WHERE name = 'Alice';
SELECT u.name, p.title FROM users u JOIN posts p ON u.id = p.user_id;

-- Update
UPDATE users SET name = 'Bob' WHERE id = 1;

-- Delete
DELETE FROM users WHERE id = 1;</code></pre>

<h2>Using SQLite in Node.js</h2>
<pre><code>const Database = require("better-sqlite3");
const db = new Database("app.db");

const users = db.prepare("SELECT * FROM users").all();
db.prepare("INSERT INTO users (name, email) VALUES (?, ?)").run("Alice", "a@b.com");</code></pre>

<div class="mermaid">
erDiagram
    USERS ||--o{ POSTS : writes
    USERS {
        int id PK
        text name
        text email
        datetime created_at
    }
    POSTS {
        int id PK
        int user_id FK
        text title
        text body
    }
</div>

<div class="takeaways">
<h2>Key Takeaways</h2>
<ul>
<li>SQLite stores a full relational database in a single file</li>
<li>SQL provides powerful querying with SELECT, JOIN, WHERE, and more</li>
<li>Foreign keys create relationships between tables and enforce data integrity</li>
<li>Use parameterized queries (?) to prevent SQL injection attacks</li>
</ul>
</div>
""",
        'ja': """
<h1>T19: SQLite</h1>
<p class="lesson-intro">SQLiteは単一ファイルにデータを格納する本格的なデータベースエンジンです。SQL(構造化問合せ言語)はそれと対話する言語です。JSONファイルがノートなら、SQLiteはラベル、カテゴリ、相互参照を備えた適切なファイルキャビネットです。同時アクセスとデータ整合性を自動的に処理します。</p>

<h2>テーブルの作成</h2>
<pre><code>CREATE TABLE users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    email TEXT UNIQUE NOT NULL,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE posts (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL,
    title TEXT NOT NULL,
    body TEXT,
    FOREIGN KEY (user_id) REFERENCES users(id)
);</code></pre>

<h2>SQLによるCRUD</h2>
<pre><code>-- Create
INSERT INTO users (name, email) VALUES ('Alice', 'alice@example.com');

-- Read
SELECT * FROM users WHERE name = 'Alice';
SELECT u.name, p.title FROM users u JOIN posts p ON u.id = p.user_id;

-- Update
UPDATE users SET name = 'Bob' WHERE id = 1;

-- Delete
DELETE FROM users WHERE id = 1;</code></pre>

<h2>Node.jsでのSQLite使用</h2>
<pre><code>const Database = require("better-sqlite3");
const db = new Database("app.db");

const users = db.prepare("SELECT * FROM users").all();
db.prepare("INSERT INTO users (name, email) VALUES (?, ?)").run("Alice", "a@b.com");</code></pre>

<div class="mermaid">
erDiagram
    USERS ||--o{ POSTS : writes
    USERS {
        int id PK
        text name
        text email
        datetime created_at
    }
    POSTS {
        int id PK
        int user_id FK
        text title
        text body
    }
</div>

<div class="takeaways">
<h2>まとめ</h2>
<ul>
<li>SQLiteは単一ファイルに完全なリレーショナルデータベースを格納します</li>
<li>SQLはSELECT、JOIN、WHEREなどで強力なクエリを提供します</li>
<li>外部キーはテーブル間の関係を作りデータ整合性を強制します</li>
<li>SQLインジェクション攻撃を防ぐためパラメータ化クエリ(?)を使いましょう</li>
</ul>
</div>
""",
    },
    'T20': {
        'en': """
<h1>T20: Authentication</h1>
<p class="lesson-intro">Authentication answers the question "who are you?" It is like a bouncer at a club checking IDs. Sessions, cookies, and password hashing work together to verify users securely. Get this wrong, and you expose your users to real harm.</p>

<h2>Password Hashing</h2>
<p>Never store passwords in plain text. Hash them with a strong algorithm like bcrypt. A hash is a one-way function - you can verify a password against it but cannot reverse it.</p>
<pre><code>const bcrypt = require("bcrypt");

// Hash a password
const hash = await bcrypt.hash("userPassword123", 10);

// Verify a password
const match = await bcrypt.compare("userPassword123", hash);
if (match) { console.log("Access granted"); }</code></pre>

<h2>Sessions and Cookies</h2>
<p>After login, the server creates a session and sends a session ID via a cookie. The browser sends this cookie with every subsequent request to prove identity.</p>
<pre><code>// On login success
const sessionId = crypto.randomUUID();
sessions[sessionId] = { userId: user.id, createdAt: Date.now() };
res.setHeader("Set-Cookie", `sid=${sessionId}; HttpOnly; Path=/`);

// On each request
function authenticate(req) {
    const cookie = parseCookies(req.headers.cookie);
    return sessions[cookie.sid] || null;
}</code></pre>

<div class="mermaid">
sequenceDiagram
    participant U as User
    participant B as Browser
    participant S as Server
    U->>B: Enter credentials
    B->>S: POST /login (email + password)
    S->>S: Hash compare with stored hash
    S-->>B: Set-Cookie: sid=abc123
    B->>S: GET /dashboard (Cookie: sid=abc123)
    S->>S: Validate session
    S-->>B: 200 OK (protected content)
</div>

<div class="takeaways">
<h2>Key Takeaways</h2>
<ul>
<li>Never store plain text passwords - always hash with bcrypt or similar</li>
<li>Sessions track logged-in users via a unique session ID stored in a cookie</li>
<li>Use HttpOnly cookies to prevent JavaScript from reading session tokens</li>
<li>Authentication verifies identity, authorization controls what they can access</li>
</ul>
</div>
""",
        'ja': """
<h1>T20: 認証</h1>
<p class="lesson-intro">認証は「あなたは誰ですか?」という質問に答えます。クラブの入口でIDをチェックするドアマンのようなものです。セッション、Cookie、パスワードハッシュが連携してユーザーを安全に検証します。これを間違えるとユーザーを危険にさらすことになります。</p>

<h2>パスワードハッシュ</h2>
<p>パスワードを平文で保存してはいけません。bcryptのような強力なアルゴリズムでハッシュします。ハッシュは一方向関数です。パスワードを照合できますが、元に戻すことはできません。</p>
<pre><code>const bcrypt = require("bcrypt");

// Hash a password
const hash = await bcrypt.hash("userPassword123", 10);

// Verify a password
const match = await bcrypt.compare("userPassword123", hash);
if (match) { console.log("Access granted"); }</code></pre>

<h2>セッションとCookie</h2>
<p>ログイン後、サーバーはセッションを作成しCookieでセッションIDを送信します。ブラウザはその後の全リクエストでこのCookieを送信して身元を証明します。</p>
<pre><code>// On login success
const sessionId = crypto.randomUUID();
sessions[sessionId] = { userId: user.id, createdAt: Date.now() };
res.setHeader("Set-Cookie", `sid=${sessionId}; HttpOnly; Path=/`);

// On each request
function authenticate(req) {
    const cookie = parseCookies(req.headers.cookie);
    return sessions[cookie.sid] || null;
}</code></pre>

<div class="mermaid">
sequenceDiagram
    participant U as User
    participant B as Browser
    participant S as Server
    U->>B: Enter credentials
    B->>S: POST /login (email + password)
    S->>S: Hash compare with stored hash
    S-->>B: Set-Cookie: sid=abc123
    B->>S: GET /dashboard (Cookie: sid=abc123)
    S->>S: Validate session
    S-->>B: 200 OK (protected content)
</div>

<div class="takeaways">
<h2>まとめ</h2>
<ul>
<li>平文パスワードは絶対に保存しない。必ずbcryptなどでハッシュします</li>
<li>セッションはCookieに保存された一意のセッションIDでログインユーザーを追跡します</li>
<li>HttpOnly Cookieを使ってJavaScriptがセッショントークンを読めないようにします</li>
<li>認証は身元確認、認可はアクセスできる範囲を制御します</li>
</ul>
</div>
""",
    },
    'T21': {
        'en': """
<h1>T21: Ollama and Chat</h1>
<p class="lesson-intro">Large Language Models (LLMs) can now run locally on your machine. Ollama makes it easy to download and serve open-source models. Connecting your web app to a local LLM gives you AI-powered features without sending data to external services - like having a smart assistant living on your own computer.</p>

<h2>Setting Up Ollama</h2>
<p>Install Ollama, pull a model, and it serves an API on localhost:11434.</p>
<pre><code># Install and run
# ollama pull llama3
# ollama serve

# The API is now available at http://localhost:11434</code></pre>

<h2>Chat API Integration</h2>
<pre><code>async function chat(messages) {
    const response = await fetch("http://localhost:11434/api/chat", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
            model: "llama3",
            messages: messages,
            stream: false
        })
    });
    const data = await response.json();
    return data.message.content;
}

// Usage
const reply = await chat([
    { role: "system", content: "You are a helpful assistant." },
    { role: "user", content: "Explain HTML in one sentence." }
]);</code></pre>

<h2>Building a Chat Interface</h2>
<p>Store the conversation history as an array of message objects. Append each new message and send the full history to maintain context.</p>

<div class="mermaid">
sequenceDiagram
    participant U as User
    participant W as Web App
    participant O as Ollama Server
    U->>W: Type message
    W->>W: Append to history
    W->>O: POST /api/chat (full history)
    O->>O: LLM generates response
    O-->>W: Response JSON
    W->>W: Append assistant reply
    W-->>U: Display response
</div>

<div class="takeaways">
<h2>Key Takeaways</h2>
<ul>
<li>Ollama runs open-source LLMs locally with a simple API</li>
<li>The chat API takes an array of messages with role and content fields</li>
<li>Send the full conversation history for context-aware responses</li>
<li>Local LLMs keep your data private - no external API calls needed</li>
</ul>
</div>
""",
        'ja': """
<h1>T21: OllamaとChat</h1>
<p class="lesson-intro">大規模言語モデル(LLM)はローカルマシンで動作できるようになりました。Ollamaはオープンソースモデルのダウンロードと配信を簡単にします。WebアプリをローカルLLMに接続すれば、外部サービスにデータを送らずにAI機能を実現できます。自分のコンピュータに住む賢いアシスタントを持つようなものです。</p>

<h2>Ollamaのセットアップ</h2>
<p>Ollamaをインストールし、モデルをプルすると、localhost:11434でAPIが提供されます。</p>
<pre><code># Install and run
# ollama pull llama3
# ollama serve

# The API is now available at http://localhost:11434</code></pre>

<h2>Chat API統合</h2>
<pre><code>async function chat(messages) {
    const response = await fetch("http://localhost:11434/api/chat", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
            model: "llama3",
            messages: messages,
            stream: false
        })
    });
    const data = await response.json();
    return data.message.content;
}

// Usage
const reply = await chat([
    { role: "system", content: "You are a helpful assistant." },
    { role: "user", content: "Explain HTML in one sentence." }
]);</code></pre>

<h2>チャットインターフェースの構築</h2>
<p>会話履歴をメッセージオブジェクトの配列として保存します。新しいメッセージを追加し、コンテキスト維持のために完全な履歴を送信します。</p>

<div class="mermaid">
sequenceDiagram
    participant U as User
    participant W as Web App
    participant O as Ollama Server
    U->>W: Type message
    W->>W: Append to history
    W->>O: POST /api/chat (full history)
    O->>O: LLM generates response
    O-->>W: Response JSON
    W->>W: Append assistant reply
    W-->>U: Display response
</div>

<div class="takeaways">
<h2>まとめ</h2>
<ul>
<li>OllamaはシンプルなAPIでオープンソースのLLMをローカル実行します</li>
<li>Chat APIはroleとcontentフィールドを持つメッセージの配列を受け取ります</li>
<li>コンテキストを考慮したレスポンスのために完全な会話履歴を送信します</li>
<li>ローカルLLMはデータを非公開に保ちます。外部API呼び出し不要です</li>
</ul>
</div>
""",
    },
    'T22': {
        'en': """
<h1>T22: Full Stack AI App</h1>
<p class="lesson-intro">This is where everything comes together. A full-stack application connects the frontend (what users see) to the backend (server logic and data) to the AI layer (intelligent responses). Think of it as building a complete restaurant - the dining room, the kitchen, and the chef all working in harmony.</p>

<h2>Architecture Overview</h2>
<p>The frontend sends user input to your Node.js server. The server manages sessions, validates data, and forwards prompts to Ollama. Responses flow back through the same chain.</p>

<h2>Connecting the Layers</h2>
<pre><code>// Server: Bridge between frontend and AI
app.post("/api/chat", authenticate, async (req, res) =&gt; {
    const { message } = req.body;
    const userId = req.session.userId;

    // Save to database
    db.prepare("INSERT INTO messages (user_id, role, content) VALUES (?, ?, ?)")
      .run(userId, "user", message);

    // Get conversation history
    const history = db.prepare("SELECT role, content FROM messages WHERE user_id = ? ORDER BY id")
      .all(userId);

    // Call Ollama
    const aiResponse = await chat(history);

    // Save AI response
    db.prepare("INSERT INTO messages (user_id, role, content) VALUES (?, ?, ?)")
      .run(userId, "assistant", aiResponse);

    res.json({ reply: aiResponse });
});</code></pre>

<div class="mermaid">
flowchart TB
    subgraph Frontend
        A[HTML/CSS/JS] --> B[Fetch API]
    end
    subgraph Backend
        C[Node.js Server] --> D[Auth Middleware]
        D --> E[API Routes]
        E --> F[(SQLite DB)]
    end
    subgraph AI
        G[Ollama LLM]
    end
    B -->|HTTP| C
    E -->|Query| F
    E -->|Prompt| G
    G -->|Response| E
    E -->|JSON| B
</div>

<div class="takeaways">
<h2>Key Takeaways</h2>
<ul>
<li>Full-stack apps connect frontend, backend, and data layers into one system</li>
<li>The server acts as a bridge between the user interface and AI model</li>
<li>Store conversation history in a database for persistence across sessions</li>
<li>Authentication protects AI endpoints from unauthorized access</li>
</ul>
</div>
""",
        'ja': """
<h1>T22: フルスタックAIアプリ</h1>
<p class="lesson-intro">ここで全てが繋がります。フルスタックアプリケーションはフロントエンド(ユーザーが見るもの)、バックエンド(サーバーロジックとデータ)、AI層(インテリジェントな応答)を接続します。完全なレストランを建てるようなもので、ダイニング、キッチン、シェフが調和して動きます。</p>

<h2>アーキテクチャ概要</h2>
<p>フロントエンドはユーザー入力をNode.jsサーバーに送信します。サーバーはセッション管理、データ検証を行い、プロンプトをOllamaに転送します。レスポンスは同じ経路を通って戻ります。</p>

<h2>層の接続</h2>
<pre><code>// Server: Bridge between frontend and AI
app.post("/api/chat", authenticate, async (req, res) =&gt; {
    const { message } = req.body;
    const userId = req.session.userId;

    // Save to database
    db.prepare("INSERT INTO messages (user_id, role, content) VALUES (?, ?, ?)")
      .run(userId, "user", message);

    // Get conversation history
    const history = db.prepare("SELECT role, content FROM messages WHERE user_id = ? ORDER BY id")
      .all(userId);

    // Call Ollama
    const aiResponse = await chat(history);

    // Save AI response
    db.prepare("INSERT INTO messages (user_id, role, content) VALUES (?, ?, ?)")
      .run(userId, "assistant", aiResponse);

    res.json({ reply: aiResponse });
});</code></pre>

<div class="mermaid">
flowchart TB
    subgraph Frontend
        A[HTML/CSS/JS] --> B[Fetch API]
    end
    subgraph Backend
        C[Node.js Server] --> D[Auth Middleware]
        D --> E[API Routes]
        E --> F[(SQLite DB)]
    end
    subgraph AI
        G[Ollama LLM]
    end
    B -->|HTTP| C
    E -->|Query| F
    E -->|Prompt| G
    G -->|Response| E
    E -->|JSON| B
</div>

<div class="takeaways">
<h2>まとめ</h2>
<ul>
<li>フルスタックアプリはフロントエンド、バックエンド、データ層を1つのシステムに接続します</li>
<li>サーバーはユーザーインターフェースとAIモデルの間の橋渡しをします</li>
<li>会話履歴をデータベースに保存してセッション間で永続化します</li>
<li>認証でAIエンドポイントを不正アクセスから保護します</li>
</ul>
</div>
""",
    },
    'R01': {
        'en': """
<h1>R01: What is IT?</h1>
<p class="lesson-intro">Information Technology is about four actions: collecting information, sending it somewhere, processing it into something useful, and storing it for later. Every app, website, and system you use is just doing some combination of these four things - from a calculator to a social network.</p>

<h2>The Four Pillars</h2>
<p><strong>Collect:</strong> Keyboards, cameras, sensors, forms - anything that captures information from the world.</p>
<p><strong>Send:</strong> Networks, Wi-Fi, cables, APIs - moving information from point A to point B.</p>
<p><strong>Process:</strong> CPUs, algorithms, code - transforming raw data into useful output.</p>
<p><strong>Store:</strong> Hard drives, databases, cloud storage - keeping information for future use.</p>

<h2>Real-World Example</h2>
<p>When you post a photo on social media: your phone camera collects the image, the network sends it to a server, the server processes it (resizes, compresses), and the database stores it. All four pillars at work.</p>

<div class="mermaid">
flowchart LR
    A[Collect] -->|keyboard, camera, sensor| B[Send]
    B -->|network, API, cable| C[Process]
    C -->|CPU, algorithm, code| D[Store]
    D -->|database, disk, cloud| E[Retrieve]
    E -->|query, request| C
    C -->|output| F[Display to User]
</div>

<div class="takeaways">
<h2>Key Takeaways</h2>
<ul>
<li>IT boils down to four actions: collect, send, process, store</li>
<li>Every application is a combination of these four operations</li>
<li>Understanding these pillars helps you see the big picture in any system</li>
<li>Web development touches all four: forms collect, HTTP sends, servers process, databases store</li>
</ul>
</div>
""",
        'ja': """
<h1>R01: ITとは何か</h1>
<p class="lesson-intro">情報技術は4つのアクションで成り立ちます: 情報を集める、どこかに送る、有用なものに加工する、後で使うために保存する。あなたが使う全てのアプリ、Webサイト、システムはこの4つの組み合わせです。電卓からSNSまで全て同じです。</p>

<h2>4つの柱</h2>
<p><strong>収集:</strong> キーボード、カメラ、センサー、フォーム。世界から情報を取り込むもの全て。</p>
<p><strong>送信:</strong> ネットワーク、Wi-Fi、ケーブル、API。情報をAからBに移動すること。</p>
<p><strong>処理:</strong> CPU、アルゴリズム、コード。生データを有用な出力に変換すること。</p>
<p><strong>保存:</strong> ハードドライブ、データベース、クラウドストレージ。将来の使用のために情報を保持すること。</p>

<h2>実例</h2>
<p>SNSに写真を投稿する時: スマホのカメラが画像を収集し、ネットワークがサーバーに送信し、サーバーが処理(リサイズ、圧縮)し、データベースが保存します。4つの柱全てが動いています。</p>

<div class="mermaid">
flowchart LR
    A[Collect] -->|keyboard, camera, sensor| B[Send]
    B -->|network, API, cable| C[Process]
    C -->|CPU, algorithm, code| D[Store]
    D -->|database, disk, cloud| E[Retrieve]
    E -->|query, request| C
    C -->|output| F[Display to User]
</div>

<div class="takeaways">
<h2>まとめ</h2>
<ul>
<li>ITは4つのアクションに集約されます: 収集、送信、処理、保存</li>
<li>全てのアプリケーションはこの4つの操作の組み合わせです</li>
<li>これらの柱を理解すると、どんなシステムでも全体像が見えます</li>
<li>Web開発は4つ全てに関わります: フォームが収集、HTTPが送信、サーバーが処理、DBが保存</li>
</ul>
</div>
""",
    },
    'R02': {
        'en': """
<h1>R02: Web Architecture</h1>
<p class="lesson-intro">The web works like a restaurant. The client (your browser) is the customer sitting at a table. The server is the kitchen. HTTP is the waiter carrying orders back and forth. The customer never enters the kitchen, and the kitchen never sits at the table. Each has a clear role.</p>

<h2>Client-Server Model</h2>
<p>The client makes requests and displays responses. The server receives requests, processes them, and sends back data. This separation of concerns is fundamental to web architecture.</p>

<h2>How a Web Request Works</h2>
<p>When you type a URL: the browser looks up the server's address (DNS), opens a connection (TCP), sends a request (HTTP), and the server responds with HTML, CSS, JS, or data.</p>
<pre><code>Client: "GET /menu please"
Server: "Here is the menu page (200 OK)"

Client: "POST /order with {item: 'pasta'}"
Server: "Order received (201 Created)"</code></pre>

<h2>Beyond Simple Pages</h2>
<p>Modern web apps add layers: CDNs cache content closer to users, load balancers distribute traffic across multiple servers, and databases persist the data.</p>

<div class="mermaid">
flowchart LR
    A[Client / Browser] -->|HTTP Request| B[Server]
    B -->|HTTP Response| A
    B -->|Query| C[(Database)]
    C -->|Data| B
    subgraph "Restaurant Analogy"
        D[Customer] -->|Order| E[Waiter]
        E -->|Order| F[Kitchen]
        F -->|Food| E
        E -->|Food| D
    end
</div>

<div class="takeaways">
<h2>Key Takeaways</h2>
<ul>
<li>The web follows a client-server model with clear separation of roles</li>
<li>HTTP is the protocol that defines how clients and servers communicate</li>
<li>The browser handles display, the server handles logic and data</li>
<li>DNS translates domain names into server IP addresses</li>
</ul>
</div>
""",
        'ja': """
<h1>R02: Webアーキテクチャ</h1>
<p class="lesson-intro">Webはレストランのように動きます。クライアント(ブラウザ)はテーブルに座る客です。サーバーはキッチンです。HTTPは注文を運ぶウェイターです。客はキッチンに入らず、キッチンはテーブルに座りません。それぞれ明確な役割があります。</p>

<h2>クライアント-サーバーモデル</h2>
<p>クライアントはリクエストを送りレスポンスを表示します。サーバーはリクエストを受け取り、処理し、データを返します。この関心の分離はWebアーキテクチャの基本です。</p>

<h2>Webリクエストの仕組み</h2>
<p>URLを入力すると: ブラウザがサーバーのアドレスを検索し(DNS)、接続を開き(TCP)、リクエストを送信し(HTTP)、サーバーがHTML、CSS、JS、またはデータで応答します。</p>
<pre><code>Client: "GET /menu please"
Server: "Here is the menu page (200 OK)"

Client: "POST /order with {item: 'pasta'}"
Server: "Order received (201 Created)"</code></pre>

<h2>シンプルなページを超えて</h2>
<p>モダンWebアプリは層を追加します。CDNがユーザーに近い場所でコンテンツをキャッシュし、ロードバランサーが複数サーバーにトラフィックを分散し、データベースがデータを永続化します。</p>

<div class="mermaid">
flowchart LR
    A[Client / Browser] -->|HTTP Request| B[Server]
    B -->|HTTP Response| A
    B -->|Query| C[(Database)]
    C -->|Data| B
    subgraph "Restaurant Analogy"
        D[Customer] -->|Order| E[Waiter]
        E -->|Order| F[Kitchen]
        F -->|Food| E
        E -->|Food| D
    end
</div>

<div class="takeaways">
<h2>まとめ</h2>
<ul>
<li>Webは明確な役割分離を持つクライアント-サーバーモデルに従います</li>
<li>HTTPはクライアントとサーバーの通信方法を定義するプロトコルです</li>
<li>ブラウザは表示を担当し、サーバーはロジックとデータを担当します</li>
<li>DNSはドメイン名をサーバーのIPアドレスに変換します</li>
</ul>
</div>
""",
    },
    'R03': {
        'en': """
<h1>R03: Problem Solving</h1>
<p class="lesson-intro">Programming is problem solving with a keyboard. Before writing any code, you must understand the problem, find a solution strategy, and then implement it step by step. Jumping straight to code is like building a house without a blueprint - you will waste time and materials.</p>

<h2>Step 1: Understand</h2>
<p>Restate the problem in your own words. Identify the inputs, the expected outputs, and the constraints. Ask questions until you are certain you understand what is being asked.</p>

<h2>Step 2: Plan</h2>
<p>Break the problem into smaller sub-problems. Write pseudocode or draw a diagram. Identify patterns you have seen before. Start with the simplest case.</p>
<pre><code>// Problem: Find the most frequent word in a text
// Plan:
// 1. Split text into words
// 2. Count occurrences of each word
// 3. Find the word with highest count
// 4. Return that word</code></pre>

<h2>Step 3: Implement</h2>
<p>Write code for each sub-problem one at a time. Test each piece before moving on. When stuck, go back to Step 1 - you probably do not fully understand the problem yet.</p>

<div class="mermaid">
flowchart TD
    A[Problem] --> B[Understand]
    B --> C{Clear?}
    C -->|No| D[Ask questions]
    D --> B
    C -->|Yes| E[Plan solution]
    E --> F[Break into sub-problems]
    F --> G[Implement step by step]
    G --> H{Works?}
    H -->|No| I[Debug]
    I --> B
    H -->|Yes| J[Solution]
</div>

<div class="takeaways">
<h2>Key Takeaways</h2>
<ul>
<li>Understand the problem completely before writing any code</li>
<li>Break complex problems into smaller, manageable sub-problems</li>
<li>Write pseudocode as a bridge between thinking and coding</li>
<li>When stuck, revisit your understanding - the bug is often in your assumptions</li>
</ul>
</div>
""",
        'ja': """
<h1>R03: 問題解決</h1>
<p class="lesson-intro">プログラミングはキーボードを使った問題解決です。コードを書く前に、問題を理解し、解決戦略を見つけ、段階的に実装する必要があります。いきなりコードを書くのは設計図なしに家を建てるようなもので、時間と材料を無駄にします。</p>

<h2>ステップ1: 理解する</h2>
<p>問題を自分の言葉で言い換えます。入力、期待される出力、制約を特定します。何を求められているか確信できるまで質問しましょう。</p>

<h2>ステップ2: 計画する</h2>
<p>問題をより小さなサブ問題に分解します。擬似コードを書くか図を描きます。以前見たパターンを特定します。最もシンプルなケースから始めます。</p>
<pre><code>// Problem: Find the most frequent word in a text
// Plan:
// 1. Split text into words
// 2. Count occurrences of each word
// 3. Find the word with highest count
// 4. Return that word</code></pre>

<h2>ステップ3: 実装する</h2>
<p>各サブ問題のコードを一つずつ書きます。次に進む前に各部分をテストします。行き詰まったらステップ1に戻りましょう。おそらく問題を完全に理解していません。</p>

<div class="mermaid">
flowchart TD
    A[Problem] --> B[Understand]
    B --> C{Clear?}
    C -->|No| D[Ask questions]
    D --> B
    C -->|Yes| E[Plan solution]
    E --> F[Break into sub-problems]
    F --> G[Implement step by step]
    G --> H{Works?}
    H -->|No| I[Debug]
    I --> B
    H -->|Yes| J[Solution]
</div>

<div class="takeaways">
<h2>まとめ</h2>
<ul>
<li>コードを書く前に問題を完全に理解しましょう</li>
<li>複雑な問題をより小さく管理しやすいサブ問題に分解しましょう</li>
<li>擬似コードは思考とコーディングの橋渡しとして書きましょう</li>
<li>行き詰まったら理解を見直しましょう。バグは仮定の中にあることが多いです</li>
</ul>
</div>
""",
    },
    'R04': {
        'en': """
<h1>R04: The 20/80 Rule</h1>
<p class="lesson-intro">The Pareto Principle says that roughly 80% of results come from 20% of efforts. In programming, 20% of the features deliver 80% of the value. Learning to identify and focus on that critical 20% is the difference between productive developers and busy developers.</p>

<h2>Applying 20/80 to Learning</h2>
<p>You do not need to master every CSS property or know every JavaScript method. Focus on the core concepts that appear in 80% of real-world code. Master flexbox before learning grid animations. Master querySelector before learning about the Shadow DOM.</p>

<h2>Applying 20/80 to Building</h2>
<p>When building a product, ship the core feature first. A chat app that sends messages is more valuable than a chat app with custom themes but no messages. Identify the minimum viable functionality and deliver that.</p>

<h2>Identifying the Critical 20%</h2>
<p>Ask yourself: "If I could only keep 20% of this, which parts would deliver the most value?" Apply this to studying, building features, and debugging.</p>

<div class="mermaid">
graph LR
    subgraph "20% Effort"
        A[Core HTML tags]
        B[Flexbox layout]
        C[querySelector + events]
        D[fetch + async/await]
    end
    subgraph "80% Coverage"
        E[Most web pages]
        F[Most layouts]
        G[Most interactions]
        H[Most data operations]
    end
    A --> E
    B --> F
    C --> G
    D --> H
</div>

<div class="takeaways">
<h2>Key Takeaways</h2>
<ul>
<li>80% of results come from 20% of efforts - focus on high-impact work</li>
<li>Master the fundamentals before chasing advanced topics</li>
<li>Ship core features first, polish later</li>
<li>Regularly ask: "Is this in the critical 20% or the optional 80%?"</li>
</ul>
</div>
""",
        'ja': """
<h1>R04: 20/80の法則</h1>
<p class="lesson-intro">パレートの法則は、結果の約80%が努力の20%から生まれると述べています。プログラミングでは、機能の20%が価値の80%を提供します。その重要な20%を見極めて集中できるかが、生産的な開発者と忙しいだけの開発者の違いです。</p>

<h2>学習への20/80適用</h2>
<p>全てのCSSプロパティをマスターしたり、全てのJavaScriptメソッドを知る必要はありません。実際のコードの80%に登場するコアコンセプトに集中しましょう。グリッドアニメーションの前にflexboxをマスター。Shadow DOMの前にquerySelectorをマスター。</p>

<h2>構築への20/80適用</h2>
<p>プロダクトを作る時は、まずコア機能をリリースします。メッセージが送れないカスタムテーマ付きチャットアプリより、メッセージが送れるシンプルなチャットアプリの方が価値があります。最小限の実用機能を特定して提供しましょう。</p>

<h2>重要な20%の特定</h2>
<p>自問しましょう: 「20%しか残せないなら、どの部分が最も価値を提供するか?」これを学習、機能構築、デバッグに適用します。</p>

<div class="mermaid">
graph LR
    subgraph "20% Effort"
        A[Core HTML tags]
        B[Flexbox layout]
        C[querySelector + events]
        D[fetch + async/await]
    end
    subgraph "80% Coverage"
        E[Most web pages]
        F[Most layouts]
        G[Most interactions]
        H[Most data operations]
    end
    A --> E
    B --> F
    C --> G
    D --> H
</div>

<div class="takeaways">
<h2>まとめ</h2>
<ul>
<li>結果の80%は努力の20%から生まれます。高インパクトな作業に集中しましょう</li>
<li>高度なトピックを追う前に基礎をマスターしましょう</li>
<li>コア機能を先にリリースし、改良は後からしましょう</li>
<li>定期的に問いかけましょう: 「これは重要な20%か、任意の80%か?」</li>
</ul>
</div>
""",
    },
    'R05': {
        'en': """
<h1>R05: Consistency Beats Passion</h1>
<p class="lesson-intro">Motivation gets you started, but consistency gets you there. A developer who codes 30 minutes every day will outpace one who does 10-hour marathons once a month. Skill builds through repetition and daily practice, not through occasional bursts of energy.</p>

<h2>The Compound Effect</h2>
<p>Small daily improvements add up exponentially over time. Just 1% improvement per day means you are 37 times better after one year. But 1% decline means you are nearly at zero. The math of daily habits is powerful.</p>

<h2>Building a Practice Habit</h2>
<p>Start small. Commit to 20 minutes a day, not 4 hours. Attach coding to an existing habit (after morning coffee, before dinner). Track your streak - the fear of breaking it becomes motivation itself.</p>

<h2>When Motivation Fades</h2>
<p>Passion fluctuates. Systems persist. Do not rely on feeling motivated. Instead, build a system: same time, same place, same minimum commitment. On bad days, just show up and write one line of code. That counts.</p>

<div class="mermaid">
graph LR
    subgraph "Passion-Driven"
        P1["Week 1: 10hrs"] --> P2["Week 2: 0hrs"]
        P2 --> P3["Week 3: 8hrs"]
        P3 --> P4["Week 4: 0hrs"]
    end
    subgraph "Consistency-Driven"
        C1["Week 1: 3.5hrs"] --> C2["Week 2: 3.5hrs"]
        C2 --> C3["Week 3: 3.5hrs"]
        C3 --> C4["Week 4: 3.5hrs"]
    end
</div>

<div class="takeaways">
<h2>Key Takeaways</h2>
<ul>
<li>Daily practice beats occasional marathon sessions</li>
<li>Small consistent improvements compound into massive results over time</li>
<li>Build systems, not goals - same time, same place, minimum commitment</li>
<li>On bad days, just show up - one line of code still counts</li>
</ul>
</div>
""",
        'ja': """
<h1>R05: 継続は情熱に勝る</h1>
<p class="lesson-intro">モチベーションは始めるきっかけですが、継続が目的地に連れて行きます。毎日30分コードを書く開発者は、月に一度10時間マラソンする人を追い越します。スキルは反復と毎日の練習で構築され、時折のエネルギー爆発では得られません。</p>

<h2>複利効果</h2>
<p>小さな日々の改善は時間とともに指数的に積み上がります。1日1%の改善で1年後には37倍になります。しかし1%の低下はほぼゼロに近づきます。日々の習慣の数学は強力です。</p>

<h2>練習の習慣を作る</h2>
<p>小さく始めましょう。4時間ではなく1日20分にコミットします。コーディングを既存の習慣に結びつけます(朝のコーヒーの後、夕食の前)。連続記録を追跡しましょう。途切れさせたくないという気持ちがモチベーションになります。</p>

<h2>モチベーションが消えた時</h2>
<p>情熱は変動します。システムは持続します。モチベーションに頼らないでください。代わりにシステムを構築します: 同じ時間、同じ場所、同じ最低限のコミットメント。調子の悪い日でも、とりあえず座って1行のコードを書きましょう。それで十分です。</p>

<div class="mermaid">
graph LR
    subgraph "Passion-Driven"
        P1["Week 1: 10hrs"] --> P2["Week 2: 0hrs"]
        P2 --> P3["Week 3: 8hrs"]
        P3 --> P4["Week 4: 0hrs"]
    end
    subgraph "Consistency-Driven"
        C1["Week 1: 3.5hrs"] --> C2["Week 2: 3.5hrs"]
        C2 --> C3["Week 3: 3.5hrs"]
        C3 --> C4["Week 4: 3.5hrs"]
    end
</div>

<div class="takeaways">
<h2>まとめ</h2>
<ul>
<li>毎日の練習は時折のマラソンセッションに勝ります</li>
<li>小さな一貫した改善が時間とともに大きな成果に複利します</li>
<li>目標ではなくシステムを作りましょう。同じ時間、同じ場所、最低限のコミットメント</li>
<li>調子の悪い日でもとりあえず座りましょう。1行のコードでもカウントされます</li>
</ul>
</div>
""",
    },
    'R06': {
        'en': """
<h1>R06: Path of Least Resistance</h1>
<p class="lesson-intro">People and systems naturally follow the easiest path. Water flows downhill. Users choose the simplest option. Code gets written in the framework with the best docs. Understanding this principle helps you design systems people will actually use and choose tools that reduce friction.</p>

<h2>In User Experience</h2>
<p>If signing up requires 10 fields, users leave. If it requires one click (sign in with Google), they stay. Every extra step is a chance for the user to give up. Reduce friction to increase adoption.</p>

<h2>In Development</h2>
<p>Developers adopt tools that are easy to start with. Node.js won because JavaScript was already known. React won because components made sense. The technology with the lowest barrier to entry gets the most adoption.</p>

<h2>In Learning</h2>
<p>Make learning easy for yourself. Keep your development environment ready. Have a project you can open in seconds. Remove obstacles between you and practice. If setup takes 30 minutes, you will not practice on a tired evening.</p>

<div class="mermaid">
flowchart TD
    A[New Tool / Feature] --> B{Easy to start?}
    B -->|Yes| C[High adoption]
    C --> D[Community grows]
    D --> E[Better docs and tools]
    E --> F[Even easier to start]
    B -->|No| G[Low adoption]
    G --> H[Small community]
    H --> I[Poor docs]
    I --> J[Harder to start]
</div>

<div class="takeaways">
<h2>Key Takeaways</h2>
<ul>
<li>Adoption follows the path of least resistance - reduce friction everywhere</li>
<li>Every extra step in a process is a chance for users to drop off</li>
<li>Choose tools and frameworks with low barriers to entry</li>
<li>Make it easy to practice - remove obstacles between you and your code</li>
</ul>
</div>
""",
        'ja': """
<h1>R06: 最も抵抗の少ない道</h1>
<p class="lesson-intro">人もシステムも自然と最も簡単な道を選びます。水は下に流れます。ユーザーは最もシンプルな選択肢を選びます。コードは最も良いドキュメントのあるフレームワークで書かれます。この原則を理解すれば、人が実際に使うシステムを設計し、摩擦を減らすツールを選べます。</p>

<h2>ユーザー体験において</h2>
<p>サインアップに10項目必要なら、ユーザーは離脱します。ワンクリック(Googleでサインイン)なら留まります。余分なステップは全てユーザーが諦める機会です。摩擦を減らして採用率を上げましょう。</p>

<h2>開発において</h2>
<p>開発者は始めやすいツールを採用します。Node.jsはJavaScriptが既に知られていたから勝ちました。Reactはコンポーネントが理にかなっていたから勝ちました。参入障壁が最も低い技術が最も多く採用されます。</p>

<h2>学習において</h2>
<p>学習を自分にとって簡単にしましょう。開発環境を常に準備しておきます。数秒で開けるプロジェクトを持ちましょう。あなたと練習の間の障害を取り除きます。セットアップに30分かかるなら、疲れた夜には練習しないでしょう。</p>

<div class="mermaid">
flowchart TD
    A[New Tool / Feature] --> B{Easy to start?}
    B -->|Yes| C[High adoption]
    C --> D[Community grows]
    D --> E[Better docs and tools]
    E --> F[Even easier to start]
    B -->|No| G[Low adoption]
    G --> H[Small community]
    H --> I[Poor docs]
    I --> J[Harder to start]
</div>

<div class="takeaways">
<h2>まとめ</h2>
<ul>
<li>採用は最も抵抗の少ない道に従います。あらゆる場所で摩擦を減らしましょう</li>
<li>プロセスの余分なステップは全てユーザーが離脱する機会です</li>
<li>参入障壁が低いツールとフレームワークを選びましょう</li>
<li>練習を簡単にしましょう。あなたとコードの間の障害を取り除きます</li>
</ul>
</div>
""",
    },
    'R07': {
        'en': """
<h1>R07: Keep Things Super Simple</h1>
<p class="lesson-intro">Complexity is the enemy of reliability. Every line of code you write is a line that can break. The best code is code you did not have to write. Simple solutions are easier to understand, debug, test, and maintain. When in doubt, choose the simpler approach.</p>

<h2>Signs of Unnecessary Complexity</h2>
<p>If you need a diagram to explain your file structure, it is too complex. If a new developer cannot understand your code in 10 minutes, it is too complex. If you have more abstraction layers than features, it is too complex.</p>

<h2>Simplicity in Practice</h2>
<pre><code>// Complex: over-engineered
class UserServiceFactory {
    createService(type) {
        return new UserServiceAdapter(new UserRepository(type));
    }
}

// Simple: just a function
function getUser(id) {
    return db.users.find(u =&gt; u.id === id);
}</code></pre>

<h2>When to Add Complexity</h2>
<p>Add complexity only when the simple solution fails under real requirements. Not imagined future requirements. Solve today's problem today. Refactor tomorrow if needed.</p>

<div class="mermaid">
flowchart LR
    subgraph Simple
        S1[1 file] --> S2[3 functions]
        S2 --> S3[Works]
    end
    subgraph Complex
        C1[5 files] --> C2[3 classes]
        C2 --> C3[2 interfaces]
        C3 --> C4[1 factory]
        C4 --> C5[Works the same]
    end
</div>

<div class="takeaways">
<h2>Key Takeaways</h2>
<ul>
<li>The best code is code you did not have to write</li>
<li>Simple solutions are easier to understand, debug, and maintain</li>
<li>Add complexity only when simple solutions fail under real requirements</li>
<li>If a new developer cannot understand it in 10 minutes, simplify</li>
</ul>
</div>
""",
        'ja': """
<h1>R07: とにかくシンプルに</h1>
<p class="lesson-intro">複雑さは信頼性の敵です。書いた全てのコード行は壊れ得る行です。最良のコードは書く必要がなかったコードです。シンプルな解決策は理解、デバッグ、テスト、保守が容易です。迷ったらシンプルなアプローチを選びましょう。</p>

<h2>不必要な複雑さの兆候</h2>
<p>ファイル構造を説明するのに図が必要なら、複雑すぎます。新しい開発者が10分でコードを理解できないなら、複雑すぎます。機能より抽象化レイヤーの方が多いなら、複雑すぎます。</p>

<h2>実践におけるシンプルさ</h2>
<pre><code>// Complex: over-engineered
class UserServiceFactory {
    createService(type) {
        return new UserServiceAdapter(new UserRepository(type));
    }
}

// Simple: just a function
function getUser(id) {
    return db.users.find(u =&gt; u.id === id);
}</code></pre>

<h2>複雑さを加えるタイミング</h2>
<p>シンプルな解決策が実際の要件で失敗した時だけ複雑さを加えます。想像上の将来の要件ではありません。今日の問題を今日解決し、必要なら明日リファクタリングしましょう。</p>

<div class="mermaid">
flowchart LR
    subgraph Simple
        S1[1 file] --> S2[3 functions]
        S2 --> S3[Works]
    end
    subgraph Complex
        C1[5 files] --> C2[3 classes]
        C2 --> C3[2 interfaces]
        C3 --> C4[1 factory]
        C4 --> C5[Works the same]
    end
</div>

<div class="takeaways">
<h2>まとめ</h2>
<ul>
<li>最良のコードは書く必要がなかったコードです</li>
<li>シンプルな解決策は理解、デバッグ、保守が容易です</li>
<li>実際の要件でシンプルな解決策が失敗した時だけ複雑さを加えましょう</li>
<li>新しい開発者が10分で理解できないなら、シンプルにしましょう</li>
</ul>
</div>
""",
    },
    'R08': {
        'en': """
<h1>R08: Code Quality</h1>
<p class="lesson-intro">Good code has three levels: it runs correctly, it runs fast enough, and it is easy to change. Most beginners stop at level one. Professionals aim for all three. Think of it as a pyramid - correctness at the base, performance in the middle, and maintainability at the top.</p>

<h2>Level 1: It Runs</h2>
<p>The code produces correct output for all expected inputs. It handles edge cases and errors gracefully. This is the minimum requirement - code that does not work is not code.</p>

<h2>Level 2: It is Fast</h2>
<p>The code performs well enough for its use case. A function that takes 10 seconds for 10 items is fine for a personal todo app but unacceptable for a search engine. Context determines what "fast enough" means.</p>

<h2>Level 3: It is Easy to Change</h2>
<p>This is the hardest level. Code is read far more often than it is written. Clear names, small functions, consistent style, and good structure make code that others (and future you) can understand and modify.</p>
<pre><code>// Hard to change
function p(d) { return d.filter(x =&gt; x.a &gt; 5).map(x =&gt; x.b * 2); }

// Easy to change
function getExpensiveItemPrices(products) {
    const expensive = products.filter(product =&gt; product.price &gt; 5);
    return expensive.map(product =&gt; product.price * 2);
}</code></pre>

<div class="mermaid">
graph TD
    A["Maintainability (easy to change)"] --> B["Performance (fast enough)"]
    B --> C["Correctness (it works)"]
    style A fill:#4CAF50,stroke:#333
    style B fill:#2196F3,stroke:#333
    style C fill:#FF9800,stroke:#333
</div>

<div class="takeaways">
<h2>Key Takeaways</h2>
<ul>
<li>Code quality has three levels: correct, fast enough, easy to change</li>
<li>Correctness is non-negotiable - code that does not work has no value</li>
<li>Performance depends on context - optimize for your actual use case</li>
<li>Maintainability is the hardest but most valuable quality for long-lived code</li>
</ul>
</div>
""",
        'ja': """
<h1>R08: コード品質</h1>
<p class="lesson-intro">良いコードには3つのレベルがあります: 正しく動く、十分に速い、変更しやすい。多くの初心者はレベル1で止まります。プロフェッショナルは3つ全てを目指します。ピラミッドと考えてください。正確性が土台、パフォーマンスが中間、保守性が頂上です。</p>

<h2>レベル1: 動く</h2>
<p>コードが全ての期待される入力に対して正しい出力を生成します。エッジケースとエラーを適切に処理します。これは最低限の要件です。動かないコードはコードではありません。</p>

<h2>レベル2: 速い</h2>
<p>コードがそのユースケースに十分なパフォーマンスを発揮します。10アイテムに10秒かかる関数は個人のTodoアプリには問題ありませんが、検索エンジンには許容できません。コンテキストが「十分に速い」の意味を決定します。</p>

<h2>レベル3: 変更しやすい</h2>
<p>これが最も難しいレベルです。コードは書かれるよりも遥かに多く読まれます。明確な名前、小さな関数、一貫したスタイル、良い構造が、他の人(そして将来の自分)が理解し修正できるコードを作ります。</p>
<pre><code>// Hard to change
function p(d) { return d.filter(x =&gt; x.a &gt; 5).map(x =&gt; x.b * 2); }

// Easy to change
function getExpensiveItemPrices(products) {
    const expensive = products.filter(product =&gt; product.price &gt; 5);
    return expensive.map(product =&gt; product.price * 2);
}</code></pre>

<div class="mermaid">
graph TD
    A["Maintainability (easy to change)"] --> B["Performance (fast enough)"]
    B --> C["Correctness (it works)"]
    style A fill:#4CAF50,stroke:#333
    style B fill:#2196F3,stroke:#333
    style C fill:#FF9800,stroke:#333
</div>

<div class="takeaways">
<h2>まとめ</h2>
<ul>
<li>コード品質には3つのレベルがあります: 正しい、十分に速い、変更しやすい</li>
<li>正確性は譲れません。動かないコードには価値がありません</li>
<li>パフォーマンスはコンテキスト次第です。実際のユースケースに最適化しましょう</li>
<li>保守性は最も難しいですが、長寿命のコードにとって最も価値ある品質です</li>
</ul>
</div>
""",
    },
    'R09': {
        'en': """
<h1>R09: How to Learn</h1>
<p class="lesson-intro">Learning a skill goes through predictable stages. First you do not know what you do not know (unconscious incompetence). Then you realize how much you do not know (conscious incompetence). Then you can do it with effort (conscious competence). Finally, it becomes automatic (unconscious competence). Understanding where you are helps you learn more effectively.</p>

<h2>The Four Stages</h2>
<p><strong>Stage 1 - Unconscious Incompetence:</strong> You do not know HTML exists. You cannot miss what you have never seen.</p>
<p><strong>Stage 2 - Conscious Incompetence:</strong> You know HTML exists but cannot write it well. This stage feels frustrating but is actually progress.</p>
<p><strong>Stage 3 - Conscious Competence:</strong> You can write HTML by thinking through each step. It works but requires concentration.</p>
<p><strong>Stage 4 - Unconscious Competence:</strong> You write HTML without thinking about it. Your hands just type the right tags.</p>

<h2>Learning Strategies</h2>
<p>Build projects, not tutorials. Reading about swimming does not make you a swimmer. Write code every day. Explain what you learned to someone else - teaching is the best way to solidify understanding.</p>

<div class="mermaid">
graph TD
    A["Stage 1: Don't know what you don't know"] -->|exposure| B["Stage 2: Know what you don't know"]
    B -->|practice| C["Stage 3: Can do it with effort"]
    C -->|repetition| D["Stage 4: Automatic skill"]
    style A fill:#ff6b6b,stroke:#333
    style B fill:#ffa726,stroke:#333
    style C fill:#66bb6a,stroke:#333
    style D fill:#42a5f5,stroke:#333
</div>

<div class="takeaways">
<h2>Key Takeaways</h2>
<ul>
<li>Learning progresses through four stages from unconscious incompetence to unconscious competence</li>
<li>The frustrating Stage 2 (knowing what you do not know) is actually a sign of progress</li>
<li>Build real projects instead of only following tutorials</li>
<li>Teaching others is the most effective way to deepen your own understanding</li>
</ul>
</div>
""",
        'ja': """
<h1>R09: 学び方</h1>
<p class="lesson-intro">スキルの学習には予測可能な段階があります。最初は知らないことを知らない(無意識の無能)。次に知らないことの多さに気づく(意識的な無能)。次に努力すればできる(意識的な有能)。最後に自動的にできる(無意識の有能)。自分がどこにいるか理解すれば、より効果的に学べます。</p>

<h2>4つの段階</h2>
<p><strong>段階1 - 無意識の無能:</strong> HTMLの存在を知りません。見たことのないものは見逃せません。</p>
<p><strong>段階2 - 意識的な無能:</strong> HTMLの存在は知っていますが上手く書けません。この段階はフラストレーションを感じますが、実際には前進しています。</p>
<p><strong>段階3 - 意識的な有能:</strong> 各ステップを考えながらHTMLを書けます。動きますが集中が必要です。</p>
<p><strong>段階4 - 無意識の有能:</strong> 考えずにHTMLを書けます。手が自然に正しいタグを打ちます。</p>

<h2>学習戦略</h2>
<p>チュートリアルではなくプロジェクトを作りましょう。水泳について読んでも泳げるようにはなりません。毎日コードを書きましょう。学んだことを誰かに説明しましょう。教えることは理解を固める最良の方法です。</p>

<div class="mermaid">
graph TD
    A["Stage 1: Don't know what you don't know"] -->|exposure| B["Stage 2: Know what you don't know"]
    B -->|practice| C["Stage 3: Can do it with effort"]
    C -->|repetition| D["Stage 4: Automatic skill"]
    style A fill:#ff6b6b,stroke:#333
    style B fill:#ffa726,stroke:#333
    style C fill:#66bb6a,stroke:#333
    style D fill:#42a5f5,stroke:#333
</div>

<div class="takeaways">
<h2>まとめ</h2>
<ul>
<li>学習は無意識の無能から無意識の有能まで4段階で進みます</li>
<li>フラストレーションを感じる段階2(知らないことを知る)は実際には進歩の証です</li>
<li>チュートリアルだけでなく実際のプロジェクトを作りましょう</li>
<li>他の人に教えることが自分の理解を深める最も効果的な方法です</li>
</ul>
</div>
""",
    },
    'R10': {
        'en': """
<h1>R10: Izumo.io Case Study</h1>
<p class="lesson-intro">The best way to understand web development is to analyze a real project. Izumo.io - the very course you are taking - is itself a full-stack web application. Let us examine how it applies every concept you have learned: HTML for structure, CSS for design, JavaScript for interactivity, a server for delivery, and a build system to tie it all together.</p>

<h2>Course Architecture</h2>
<p>The course website is built with a Python build system that generates static HTML pages from templates and lesson content. This approach combines the simplicity of static files with the power of a templating engine.</p>

<h2>How Lessons Are Delivered</h2>
<p>Lesson content is stored as Python data structures (the file you are reading about right now). A build script processes each lesson, wraps it in a template with navigation and styling, and outputs static HTML files. No server needed at runtime - just files served by any web host.</p>

<h2>Design Decisions</h2>
<p>Static site generation was chosen over a dynamic server because: simpler hosting (any file server works), faster load times (no server processing), and better reliability (no server to crash). This is the 20/80 rule and KISS principle in action.</p>

<div class="mermaid">
flowchart TB
    subgraph "Build Time"
        A[lessons.py] --> B[build.py]
        C[templates/] --> B
        D[static/css] --> B
        B --> E[Generated HTML files]
    end
    subgraph "Runtime"
        E --> F[Web Server]
        F --> G[Browser]
    end
    subgraph "Concepts Used"
        H[HTML structure]
        I[CSS styling]
        J[Mermaid diagrams]
        K[Responsive design]
    end
</div>

<div class="takeaways">
<h2>Key Takeaways</h2>
<ul>
<li>Real projects apply multiple concepts together - HTML, CSS, JS, build tools</li>
<li>Static site generation offers simplicity, speed, and reliability</li>
<li>Architecture decisions should follow the principles you have learned (KISS, 20/80)</li>
<li>Analyzing existing projects is one of the best ways to deepen your understanding</li>
</ul>
</div>
""",
        'ja': """
<h1>R10: Izumo.ioケーススタディ</h1>
<p class="lesson-intro">Web開発を理解する最良の方法は実際のプロジェクトを分析することです。Izumo.io、つまりあなたが受講しているこのコース自体がフルスタックWebアプリケーションです。学んだ全てのコンセプトがどう適用されているか見てみましょう: 構造のHTML、デザインのCSS、対話性のJavaScript、配信のサーバー、全てを結ぶビルドシステム。</p>

<h2>コースアーキテクチャ</h2>
<p>コースのWebサイトはPythonビルドシステムで構築されており、テンプレートとレッスンコンテンツから静的HTMLページを生成します。このアプローチは静的ファイルのシンプルさとテンプレートエンジンの力を組み合わせています。</p>

<h2>レッスンの配信方法</h2>
<p>レッスンコンテンツはPythonデータ構造として格納されています(まさに今読んでいるこのファイルです)。ビルドスクリプトが各レッスンを処理し、ナビゲーションとスタイリングを含むテンプレートで包み、静的HTMLファイルを出力します。実行時にサーバーは不要で、どのWebホストでもファイルを配信するだけです。</p>

<h2>設計上の決定</h2>
<p>動的サーバーではなく静的サイト生成を選んだ理由: より簡単なホスティング(どのファイルサーバーでも動く)、より速い読み込み(サーバー処理なし)、より高い信頼性(クラッシュするサーバーなし)。これは20/80ルールとKISSの原則の実践です。</p>

<div class="mermaid">
flowchart TB
    subgraph "Build Time"
        A[lessons.py] --> B[build.py]
        C[templates/] --> B
        D[static/css] --> B
        B --> E[Generated HTML files]
    end
    subgraph "Runtime"
        E --> F[Web Server]
        F --> G[Browser]
    end
    subgraph "Concepts Used"
        H[HTML structure]
        I[CSS styling]
        J[Mermaid diagrams]
        K[Responsive design]
    end
</div>

<div class="takeaways">
<h2>まとめ</h2>
<ul>
<li>実際のプロジェクトは複数のコンセプトを組み合わせます。HTML、CSS、JS、ビルドツール</li>
<li>静的サイト生成はシンプルさ、速度、信頼性を提供します</li>
<li>アーキテクチャの決定は学んだ原則(KISS、20/80)に従うべきです</li>
<li>既存プロジェクトの分析は理解を深める最良の方法の一つです</li>
</ul>
</div>
""",
    },
}
