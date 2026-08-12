# 文書索引

学習者が最初に読む正規文書と、過去のレビュー資料を分けています。

## 現在の教材

| 目的 | 文書 |
|---|---|
| 全体像とセットアップ | [ルートREADME](../README.md) |
| 3環境の比較自習 | [複数言語ガイド](../MULTILANGUAGE_GUIDE.md) |
| **180分ワークショップ** | [カリキュラム](../docs/tutorials/WORKSHOP_TEMPLATE_180min.md) <br/> [講師スライド](../docs/tutorials/INSTRUCTOR_SLIDES_180min.md) <br/> [スライド使用ガイド](../docs/tutorials/SLIDES_README.md) |
| 90分授業 | [ワークショップ](../WORKSHOP_TEMPLATE.md) |
| 動画収録 | [動画台本](../VIDEO_TUTORIAL_SCRIPT.md) |
| Python | [Python版README](../sample-compass/README.md) |
| TypeScript | [TypeScript版README](../sample-compass-ts/README.md) |
| MakeCode | [MakeCode版README](../sample-compass-makecode/README.md) |
| HEX生成 | [HEXビルドガイド](../HEX_BUILD_GUIDE.md) |
| Git hooks | [Git hooksガイド](../GIT_HOOKS_GUIDE.md) |

現在の品質状態は文書中の固定件数ではなく、次の実行結果を正とします。

```bash
npm run test:all
npm run lint
npm run build:hex
```

## 過去レビュー（非規範）

次のファイルは改善検討時のスナップショットです。評価、テスト件数、未実装項目は作成時点の情報で、現在仕様ではありません。

- [repository_review_2026-08-10.md](./repository_review_2026-08-10.md) — 最新。品質ゲート・CI・文書の実測レビュー（Critical 3 件）
- [ACTIONABLE_IMPROVEMENTS.md](./ACTIONABLE_IMPROVEMENTS.md)
- [MICROBIT_EDUCATION_REVIEW.md](./MICROBIT_EDUCATION_REVIEW.md)
- [TEST_RESULTS.md](./TEST_RESULTS.md)
- [microbit_curriculum_review_report.md](./microbit_curriculum_review_report.md)
- [microbit_environment_review.md](./microbit_environment_review.md)
- [microbit_learning_review.md](./microbit_learning_review.md)

レビュー資料から現在の教材へ内容を移す場合は、実装とテストで再確認し、上の正規文書を更新します。
