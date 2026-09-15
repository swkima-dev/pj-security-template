# GitHub Rulesets

## CAUTION: チーム開発時の承認ルールについて

このリポジトリ自体は1人で作業しているため、**Require a pull request before merging** の **Required approvals** を `0` にしています。プルリクエスト（PR）は必須ですが、承認は必須ではありません。複数人のチームで開発する場合は、`1` 以上を推奨します。

必要に応じて、**Require approval of the most recent reviewable push** も有効にしてください。最後のレビュー対象の push に対して、その push を行った人以外の承認を必須にする設定です。現在の `require_last_push_approval` は `false` です。

## 共通設定

- 対象はブランチ（`target: branch`）で、ルールは有効（`enforcement: active`）です。
- 対象から除外するブランチはありません。
- ルールをバイパスできるユーザー・チーム・アプリは指定していません（`bypass_actors: []`）。

## main_branch_protection

設定ファイル: [main_branch_protection.json](../../rulesets/main_branch_protection.json)

`main` ブランチを対象に、変更を PR 経由にし、削除や履歴の強制的な書き換えを防ぎます。

| 設定 | 現在の値・意味 |
| --- | --- |
| `deletion` | ブランチの削除を禁止します。 |
| `non_fast_forward` | force push を禁止します。 |
| `pull_request` | マージ前に PR を必須にします。 |
| `required_approving_review_count` | `0`：必須の承認数です。チーム開発では `1` 以上を推奨します。 |
| `dismiss_stale_reviews_on_push` | `true`：PR の差分を変更するコミットが追加された場合、古い承認を取り消します。 |
| `required_reviewers` | `[]`：特定チームのレビュー要件は指定していません。 |
| `require_code_owner_review` | `false`：CODEOWNERS に指定された担当者の承認は必須にしていません。 |
| `require_last_push_approval` | `false`：最新の push に対する別の人の承認は必須にしていません。 |
| `required_review_thread_resolution` | `true`：マージ前にレビューの会話をすべて解決する必要があります。 |
| `require_extra_approval_for_unattributed_changes` | `true`：人に紐づかない Copilot の PR に追加の承認を要求します。ただし、必須承認数が `0` の現在は効果がありません。 |
| `allowed_merge_methods` | `merge`・`squash`・`rebase` を許可します。実際に使える方法はリポジトリ側の設定にも依存します。 |

## required_status_checks

設定ファイル: [required_status_checks.json](../../rulesets/required_status_checks.json)

すべてのブランチ（`~ALL`）を対象に、指定したステータスチェックを要求するための設定です。

**現在は `required_status_checks` が空のため、必須のチェックはありません。** CI を導入したら、必須にするチェック名を追加してください。

| 設定 | 現在の値・意味 |
| --- | --- |
| `required_status_checks` | `[]`：必須にするチェックの一覧です。現在は未指定です。 |
| `strict_required_status_checks_policy` | `false`：PR ブランチをマージ先の最新状態に追従させることは必須にしていません。 |
| `do_not_enforce_on_create` | `false`：ブランチ作成時もチェックの適用を免除しません。 |

## 参考

- [GitHub Docs: Rulesets で利用できるルール](https://docs.github.com/en/repositories/configuring-branches-and-merges-in-your-repository/managing-rulesets/available-rules-for-rulesets)
- [GitHub Docs: Rules の REST API](https://docs.github.com/en/rest/repos/rules)
