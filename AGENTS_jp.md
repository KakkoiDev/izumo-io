# プロジェクトエージェントメモリ

このファイルは、プロジェクト固有のエージェント知識を永続的に記録するためのものです：ビルド、テスト、リリース、アーキテクチャ、およびコードと共に保持すべき注意点など。

- 実際の作業を通じて発見された、永続的なプロジェクト固有のメモをここに追加してください。

## レッスンは3言語対応で、翻訳はCIで管理されています

`content/ai/aNN.md` が英語のソースです。`aNN.ja.md` と `aNN.pt.md` (ブラジルポルトガル語) がその兄弟ファイルです。
`scripts/translate_content.py` (Geminiを使用し、`.github/workflows/translate-content.yml` によって実行されます) は、兄弟ファイルのうち
不足しているか空のものを埋め、さらにフロントマターの`source_sha`が
`sha1(english_source)[:12]` と異なる兄弟ファイルを再翻訳します。

結果として：英語のレッスンを編集した後、両方の翻訳ファイルで`source_sha`を再スタンプしないと、ボットが
次回の実行時に手書きの翻訳を上書きしてしまいます。フロントマターに `translate: false` を記述すると、そのファイルは翻訳対象から除外されます。

ゲームレッスンの慣例 (a09以降)：「`## The prompt`」のフェンスで囲まれたブロックは、すべての言語で
英語のまま保持されます。レッスンa01からa08では翻訳されます。Mermaidブロック、コード、パス、画像の代替テキストはそのまま保持されます。

## docs/以下のサイトは生成されます

`make build` は `website/build.py` を実行します。これは一時ディレクトリに書き込み、そのディレクトリ名を `docs/` に変更します。
これは決定論的であるため、コンテンツの変更がない再ビルドでは差分は発生しません。再生成された `docs/` を
いかなる `content/` の変更とともにコミットしてください。

## テスト：シナリオが最初、各機能に1つのe2eテスト

Pi Workbench および test-core と同じプロトコルです。サイト、ビルド、翻訳ツールのすべての機能には、
`SCENARIOS.md` に Given/When/Then シナリオ (`### Scenario: <title>`) があり、それぞれに1つのエンドツーエンドテストが
`tests/e2e/` 内にタイトル (`def test_<title in snake case>` に `@pytest.mark.scenario("<title>")`) にちなんで名付けられています。Playwright は
サイト向け、ビルドおよび翻訳ツール向けにはスクラッチコピー上での実際のコマンドを使用します。まずシナリオを書き、テストが失敗することを確認してから、コードを変更します。
機能を削除する場合、同じコミットでそのシナリオとテストも削除します。
テストはオフラインです（外部リクエストにはスタンドインが使用されます。Geminiクライアントは `tests/e2e/stand_ins/` です）、状態変化を待つだけで時間を待つことはありません、
そしてすべてのChromium起動時には `--use-mock-keychain --password-store=basic` (`tests/e2e/conftest.py`) が渡されます。

ゲートは、`.github/workflows/test.yml` が実行するように（`pip install -r requirements-dev.txt` を一度実行し、ブラウザは
`python -m playwright install chromium` から取得するか、既存のChromiumをPLAYWRIGHT_CHROMIUMに指定します）：

```sh
python tools/test-core/flaky_lint.py tests
python tools/test-core/e2e_coverage.py --pages 'website/pages/*.html' 'website/templates/*.html' --tests 'tests/e2e/*.py'
python -m pytest --junitxml=.test-output/pytest-junit.xml
python tools/test-core/scenarios.py check SCENARIOS.md --tests tests/e2e/test_*.py --junit .test-output/pytest-junit.xml
```

テンプレートに新しいコントロールを追加する場合、e2eステップが必要です。`docs/` は、クリーンな `make build` の結果と一致している必要があります（これはテストで確認されます）。

## テスト：シナリオが最初、各機能に1つのe2eテスト

Pi Workbench および test-core と同じプロトコルです。サイト、ビルド、翻訳ツールのすべての機能には、
`SCENARIOS.md` に Given/When/Then シナリオ (`### Scenario: <title>`) があり、それぞれに1つのエンドツーエンドテストが
`tests/e2e/` 内にタイトル (`def test_<title in snake case>` に `@pytest.mark.scenario("<title>")`) にちなんで名付けられています。Playwright は
サイト向け、ビルドおよび翻訳ツール向けにはスクラッチコピー上での実際のコマンドを使用します。まずシナリオを書き、テストが失敗することを確認してから、コードを変更します。
機能を削除する場合、同じコミットでそのシナリオとテストも削除します。
テストはオフラインです（外部リクエストにはスタンドインが使用されます。Geminiクライアントは `tests/e2e/stand_ins/` です）、状態変化を待つだけで時間を待つことはありません、
そしてすべてのChromium起動時には `--use-mock-keychain --password-store=basic` (`tests/e2e/conftest.py`) が渡されます。

ゲートは、`.github/workflows/test.yml` が実行するように（`pip install -r requirements-dev.txt` を一度実行し、ブラウザは
`python -m playwright install chromium` から取得するか、既存のChromiumをPLAYWRIGHT_CHROMIUMに指定します）：

```sh
python tools/test-core/flaky_lint.py tests
python tools/test-core/e2e_coverage.py --pages 'website/pages/*.html' 'website/templates/*.html' --tests 'tests/e2e/*.py'
python -m pytest --junitxml=.test-output/pytest-junit.xml
python tools/test-core/scenarios.py check SCENARIOS.md --tests tests/e2e/test_*.py --junit .test-output/pytest-junit.xml
```

テンプレートに新しいコントロールを追加する場合、e2eステップが必要です。`docs/` は、クリーンな `make build` の結果と一致している必要があります（これはテストで確認されます）。

## このファイルの保守

このファイルは、本プロジェクトにおける今後のほとんどすべてのエージェントセッションに役立つ知識を保持するために使用してください。
コードベースが既に示していることを繰り返さないでください。代わりに、信頼できるファイルやコマンドを指し示してください。
新しいエントリを追加するよりも、既存のエントリを書き換えたり、整理したりすることを推奨します。
このファイルを更新する際は、すべてのエージェントのためにこの基準を維持し、エントリを簡潔に保ってください。