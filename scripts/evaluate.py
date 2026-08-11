"""Run paired-seat, multi-seed local Kaggriculture evaluation."""

from __future__ import annotations

import argparse
import csv
import json
import statistics
from pathlib import Path

from kaggle_environments import make


def parse_seeds(value: str) -> list[int]:
    if ":" in value:
        start, stop = (int(part) for part in value.split(":", 1))
        return list(range(start, stop))
    return [int(part) for part in value.split(",") if part.strip()]


def play(candidate: str, opponent: str, seed: int, seat: int, steps: int) -> dict:
    agents = [candidate, opponent] if seat == 0 else [opponent, candidate]
    env = make(
        "kaggriculture",
        configuration={"episodeSteps": steps, "seed": seed},
        debug=False,
    )
    env.run(agents)
    final = env.steps[-1]
    mine = final[seat]
    theirs = final[1 - seat]
    mine_reward = float(mine.reward or 0.0)
    their_reward = float(theirs.reward or 0.0)
    return {
        "seed": seed,
        "seat": seat,
        "candidate_reward": mine_reward,
        "opponent_reward": their_reward,
        "margin": mine_reward - their_reward,
        "candidate_status": mine.status,
        "opponent_status": theirs.status,
        "turns": len(env.steps),
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--candidate", default="main.py")
    parser.add_argument("--opponent", default="starter")
    parser.add_argument("--seeds", default="0:10", help="e.g. 0:10 or 1,7,42")
    parser.add_argument("--steps", type=int, default=720)
    parser.add_argument(
        "--output",
        type=Path,
        default=Path("artifacts/reports/baseline_vs_starter.csv"),
    )
    parser.add_argument("--replay", type=Path)
    args = parser.parse_args()

    if args.replay and args.replay.suffix.lower() != ".json":
        parser.error("--replay must use a .json extension")

    candidate = str(Path(args.candidate).resolve())
    seeds = parse_seeds(args.seeds)
    rows = []
    replay_saved = False
    for seed in seeds:
        for seat in (0, 1):
            row = play(candidate, args.opponent, seed, seat, args.steps)
            rows.append(row)
            print(
                f"seed={seed:>4} seat={seat} margin={row['margin']:>10.1f} "
                f"status={row['candidate_status']}"
            )

            if args.replay and not replay_saved:
                agents = (
                    [candidate, args.opponent]
                    if seat == 0
                    else [args.opponent, candidate]
                )
                env = make(
                    "kaggriculture",
                    configuration={"episodeSteps": args.steps, "seed": seed},
                    debug=False,
                )
                env.run(agents)
                args.replay.parent.mkdir(parents=True, exist_ok=True)
                args.replay.write_text(
                    json.dumps(env.toJSON(), ensure_ascii=False), encoding="utf-8"
                )
                replay_saved = True

    args.output.parent.mkdir(parents=True, exist_ok=True)
    with args.output.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0]))
        writer.writeheader()
        writer.writerows(rows)

    margins = [row["margin"] for row in rows]
    wins = sum(margin > 0 for margin in margins)
    draws = sum(margin == 0 for margin in margins)
    failures = [row for row in rows if row["candidate_status"] != "DONE"]
    print("\nsummary")
    print(f"games={len(rows)} wins={wins} draws={draws} losses={len(rows)-wins-draws}")
    print(f"win_rate={wins / len(rows):.3f}")
    print(f"mean_margin={statistics.fmean(margins):.2f}")
    print(f"median_margin={statistics.median(margins):.2f}")
    print(f"min_margin={min(margins):.2f} max_margin={max(margins):.2f}")
    print(f"failures={len(failures)}")
    print(f"report={args.output}")
    if failures:
        raise SystemExit("Candidate did not finish every game")


if __name__ == "__main__":
    main()
