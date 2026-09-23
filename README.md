# Kaggriculture

Kaggleの対戦型農場経営シミュレーション「Kaggriculture」用リポジトリです。

競技ページ: https://www.kaggle.com/competitions/kaggriculture

## このコンペでやること

通常のKaggleのようにCSVを予測するのではなく、毎ターンの農場操作を返すPythonエージェントを提出します。

- 1試合は標準で30日、1日24ターン、合計720ターン
- 2人のエージェントが同時に農場を経営
- 種・動物・土地を買い、作物を育て、商品を市場で売る
- 最終的に銀行残高が多い側が勝つ
- 提出物のルートには`main.py`が必要で、その中に`agent(obs)`関数を置く

`obs`はobservationの略で、現在の農場、所持金、市場価格、作物、相手の公開農場などの観測情報です。`agent(obs)`は、その情報を受け取り、農夫、雇用した作業員、市場注文の行動を返します。

## 現在の最高スコア

ルートの`main.py`は、公開Notebook [The 2965 Master Hybrid Engine](https://www.kaggle.com/code/haideptry/the-2965-master-hybrid-engine) を監査し、複数の強い公開エージェントとのローカル対戦を通過した提出版です。

- Public Score: `2562.8`
- Kaggle提出ID: `56464426`
- 提出タイトル: `2965 Hybrid broad pool 36-4`
- SHA-256: `93831c18a43c49312a71fa67171224681c52c3fade0259403e8d8fae7973565f`
- ローカル検証: Pipe18、V56、Fieldcraft、V45に対して両席合計`36勝4敗`

このエージェントは、終盤の不要な種購入を抑える処理、最終日前の肥料購入停止、価格を見た売却タイミング調整、在庫上限への対処を組み合わせています。提出物は`main.py`だけで完結し、外部通信や実行時の外部データ読み込みはありません。

再現用ファイルは`agents/hybrid2965/main.py`、Kaggleへ送ったアーカイブは`submissions/hybrid2965-2562.8.tar.gz`、ローカル対戦結果は`artifacts/reports/hybrid2965_broad_pool_20260922.csv`です。

## 初期ベースライン

ルートの`main.py`は、公開Notebook [Kaggriculture Baseline](https://www.kaggle.com/code/prvsiyan/kaggriculture-baseline) から正確に展開したベースラインです。

この方策は、複数の決定的な経営方策を内部に持ち、試合中に見える状態から使う方策を選びます。外部通信、非公開データ、過去リプレイには依存しません。詳しい出典と監査内容は`docs/SOURCES.md`にあります。

## フォルダ構成

```text
Kaggriculture/
├─ main.py                         現在選択中の提出エージェント
├─ agents/
│  ├─ public_baseline/main.py      採用した公開ベースライン
│  └─ official_starter/main.py     公式の最小Carrot方策
├─ scripts/
│  ├─ setup.ps1                    環境構築
│  ├─ evaluate.py                  複数seed・両席でローカル対戦
│  ├─ build_submission.py          submission.tar.gz作成
│  └─ select_agent.ps1             main.pyの切り替え
├─ notebooks/public/               参照した公開Notebook
├─ docs/official/                  Kaggle公式ルールとAgentガイド
├─ artifacts/reports/              ローカル対戦結果
├─ artifacts/replays/              リプレイJSON
├─ submissions/                    提出用tar.gz
└─ tests/                           構造・依存・再現性テスト
```

## 1. Python環境を作る

このPCにcondaがある場合は`kagri`環境を作ります。ない場合はPython 3.12の`.venv`を作ります。公式環境の依存パッケージとの互換性のため、Python 3.12を使用します。

```powershell
cd C:\kaggle\Kaggriculture
powershell -ExecutionPolicy Bypass -File .\scripts\setup.ps1
```

condaの場合:

```powershell
conda activate kagri
```

venvの場合:

```powershell
.\.venv\Scripts\Activate.ps1
```

## 2. ローカル対戦する

まず5seedを両方の席で実行し、計10試合を公式starterと戦わせます。

```powershell
python scripts\evaluate.py --candidate main.py --opponent starter --seeds 0:5
```

より安定して比較する場合:

```powershell
python scripts\evaluate.py --candidate main.py --opponent starter --seeds 0:50
```

同じseedでも先手・後手の影響があるため、必ず両席で実行します。評価結果は`artifacts/reports/baseline_vs_starter.csv`へ保存されます。

初期構築時の確認では、seed 0から4までを両席で戦わせた10試合をすべて完走し、公式starterに10勝0敗でした。平均marginは`+142,851.9`、最小marginは`+117,632`です。ただしstarterは最小構成の相手なので、この結果だけでLeaderboard性能が保証されるわけではありません。

## 3. テストする

```powershell
python -m pytest -q
```

ここでは、公開ベースラインと完全に同じSHA-256か、`agent`関数が読み込めるか、外部通信や外部ファイル依存がないか、提出archiveが`main.py`だけを含むかを検証します。

## 4. 提出ファイルを作る

```powershell
python scripts\build_submission.py
```

作成されるファイル:

```text
submissions/submission.tar.gz
```

tar.gzの直下に`main.py`が1つだけ入ります。

## 5. Kaggleへ提出する

Web画面を使う場合は、`submissions/submission.tar.gz`を提出します。

CLIの場合:

```powershell
python -m kaggle competitions submit kaggriculture `
  -f submissions\submission.tar.gz `
  -m "public baseline exact repro"
```

提出タイトル案:

```text
public baseline exact repro
```

## 方策を切り替える

公開ベースラインへ戻す:

```powershell
powershell -ExecutionPolicy Bypass -File .\scripts\select_agent.ps1 public_baseline
```

公式starterへ切り替える:

```powershell
powershell -ExecutionPolicy Bypass -File .\scripts\select_agent.ps1 official_starter
```

## 開発方針

1. `main.py`を基準に新しい方策を別フォルダへ作る
2. 複数seed、両席、複数相手でローカル評価する
3. 平均勝率だけでなく、最悪marginと異常終了も確認する
4. Kaggleスコアが上がるまではローカルに保留する
5. スコアが上がった方策だけGitへ残す

ここでの`margin`は「自分の最終所持金 - 相手の最終所持金」です。正なら勝ち、負なら負けです。
