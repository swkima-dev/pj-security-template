# GitHub Actions

## Overview

| ワークフロー | 用途 | 実行条件 |
| --- | --- | --- |
| [Secret Scan](../../.github/workflows/secret-scan.yml) | Betterleaksによるシークレット漏洩の検出 | PR作成・更新時、`main`へのpush時 |
| [Container Vulnerability Scan](../../.github/workflows/container-vulnerability-scan.yml) | Trivyによるコンテナイメージの脆弱性検出 | PR作成・更新時、`main`へのpush時 |
| [Dependency Install Check](../../.github/workflows/dependency-install-check.yml) | Takumi Guard経由の依存インストールとテスト | `main`宛てのPR作成・更新時、`main`へのpush時 |
| [Claude Security Review](../../.github/workflows/claude-security-review.yml) | Claudeによるセキュリティレビュー | `workflow_dispatch`による手動実行 |

## Secret Scan

BetterleaksでGit履歴をスキャンし、APIキーなどのシークレットを検出するとチェックを失敗させます。
結果はSARIF形式で出力し、GitHubのCode scanningへアップロードします。

## Container Vulnerability Scan

アプリ用のDockerfileからイメージをビルドし、TrivyでOS・ライブラリの脆弱性を検査します。修正版がある`HIGH`・`CRITICAL`の脆弱性を検出すると失敗します（未修正の脆弱性は対象外）。
デモアプリの[Dockerfile](../../Dockerfile)を追加して有効化済みです。イメージはCI内でビルド・検査し、レジストリへのログインや公開は不要です。

## Dependency Install Check（Takumi Guard）

uvとPythonを用意し、Takumi Guardのプロキシ経由で`uv sync --locked --no-cache`を行ったあと、`uv run --no-sync pytest`でデモアプリをテストします。
**注意:** 現状は`bot-id`なしの匿名モードのため、監査ログの記録やダッシュボードでのパッケージ利用状況の確認はできません。これらには`bot-id`と`id-token: write`などの認証設定が必要です（[公式ドキュメント](https://github.com/flatt-security/setup-takumi-guard-pypi#setup-modes)）。
`pyproject.toml`と`uv.lock`にもプロキシの取得先を記録し、CIでは依存キャッシュを使わずに取得します。保護の対象はプロキシ経由のインストールで、別ジョブのインストールや未知の悪意あるパッケージの安全性までは保証しません。

## Claude Security Review

Claudeによるセキュリティレビューを実行します。APIコストと、毎回AIレビューが挟まる煩わしさを考慮し、あえて`workflow_dispatch`で必要なときだけ手動実行する運用にしています。
実行前に、リポジトリの **Settings → Secrets and variables → Actions → Repository secrets** に、Anthropic APIキーを`CLAUDE_API_KEY`という名前で登録する必要があります。
