# Security Template

セキュリティチェック用のGitHub Actionsと、動作確認用の最小限のPython HTTPアプリです。
DB・外部API・環境変数の設定は不要です。

## ローカルで起動

[uv](https://docs.astral.sh/uv/getting-started/installation/)をインストールし、リポジトリのルートで実行します。Python 3.12と開発用依存はuvが取得します。

```sh
uv sync --locked
uv run --no-sync python app.py
```

別のターミナルから応答を確認できます。終了は`Ctrl+C`です。

```sh
curl http://127.0.0.1:8000/
# {"message": "Hello, world!"}
curl http://127.0.0.1:8000/health
# {"status": "ok"}
```

`--port 8080`でポートを変更できます。未定義のパスにはJSON形式の404を返します。
Python標準ライブラリのHTTPサーバーを使ったデモです。

## テスト

```sh
uv run --locked pytest
```

実際にHTTPサーバーを起動して、応答のステータス・ヘッダー・JSONを確認します。
開発用依存のpytestはTakumi Guard経由で取得します。`pyproject.toml`と`uv.lock`の取得先をそろえ、ローカルとCIで同じロックファイルを利用します。
依存を変更したら`uv lock`でロックファイルを更新してください。

## コンテナで起動

```sh
docker build -t security-template-demo .
docker run --rm -p 127.0.0.1:8000:8000 security-template-demo
```

アプリの実行時依存は標準ライブラリのみなので、イメージにはuv・pytestをインストールしません。

## GitHub Actions

`main`へのpushやPRで、シークレット検査・依存インストールとテスト・コンテナの脆弱性検査を実行します。
Claude Security Reviewのみ、`CLAUDE_API_KEY`の登録と手動実行が必要です。
各チェックの内容・制限は[GitHub Actionsの説明](docs/repository-setup/github-actions.md)を参照してください。

## Dependabot

`.github/dependabot.yml`をデフォルトブランチに反映すると、uv・Docker・GitHub Actions・pre-commitのバージョン更新PRを週1回チェックして自動作成します。
脆弱性修正PRも自動作成するには、リポジトリの **Settings → Code security** で **Dependency graph**・**Dependabot alerts**・**Dependabot security updates** を有効にしてください。脆弱性修正は週次スケジュールとは別に実行されます。
