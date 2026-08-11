# 参照元と採用判断

## 公式仕様

- Competition: https://www.kaggle.com/competitions/kaggriculture
- Official environment: https://github.com/Kaggle/kaggle-environments/tree/master/kaggle_environments/envs/kaggriculture
- 取得時の公式リポジトリcommit: `bded87b0d7879078c726a93a4884d044f79c4eed`
- ローカルに保存した仕様: `docs/official/README.md`, `docs/official/AGENTS.md`
- 使用するシミュレータ: `kaggle-environments==1.32.6`

ゲームルール、観測値、行動形式、提出物の条件は公式仕様を正本とする。

## 採用した公開ベースライン

- Notebook: https://www.kaggle.com/code/prvsiyan/kaggriculture-baseline
- Author: `prvsiyan`
- ローカル保存: `notebooks/public/prvsiyan-kaggriculture-baseline.ipynb`
- 展開後の提出コード: `agents/public_baseline/main.py`
- SHA-256: `97e5de08ed8f43f7fd2c196dd943e13bb71278477fcdeaec8e0ad8f1357ac515`

採用理由:

- `main.py` 1ファイルで完結する。
- 外部通信、非公開Dataset、リプレイ、pickle、`/kaggle/input`への依存がない。
- 公開されている観測情報だけを使う。
- 公式シミュレータ1.32.6で検証されている。
- Notebook記載では380シナリオを両席で比較した計760対戦を使っている。
- 親方策から初手の5人目の`HIRE`だけを除き、初手後の現金を13から26へ増やしている。

注意:

- 公開Notebookに記載された検証値は作者の報告であり、このリポジトリでは別途ローカル再評価する。
- エージェント内部には圧縮された複数方策が入っている。難読化ではあるが、展開した内側も通信・ファイル読込・リプレイ依存がないことを確認済み。
- 公開方策に対する過学習の可能性は残るため、今後はseed、席順、相手方策を変えた評価を必須とする。

## 比較用公式スターター

- 出典: `kaggle-environments`の`starter_agent`
- 保存先: `agents/official_starter/main.py`

Carrotを1枚のタイルで繰り返す最小方策であり、提出本命ではなく動作確認と最低比較線に使う。

