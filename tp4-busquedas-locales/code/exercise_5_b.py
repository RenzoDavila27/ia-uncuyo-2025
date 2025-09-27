#!/usr/bin/env python3
"""Summarize N-Queens experiment results grouped by algorithm and board size."""
from __future__ import annotations

import argparse
import csv
from collections import defaultdict
from pathlib import Path
from statistics import StatisticsError, mean, stdev
from typing import Iterable, List


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description=(
            "Compute aggregated metrics (success rate, cost/time/state averages) "
            "for each algorithm and board size from an experiment CSV."
        )
    )
    parser.add_argument(
        "input",
        type=Path,
        nargs="?",
        default=Path("results.csv"),
        help="Path to the input CSV produced by the experiments.",
    )
    parser.add_argument(
        "--output",
        type=Path,
        default=None,
        help="Optional path to write the summary table as CSV.",
    )
    return parser.parse_args()


def safe_mean(values: Iterable[float]) -> float | None:
    values = list(values)
    return mean(values) if values else None


def safe_stdev(values: Iterable[float]) -> float | None:
    values = list(values)
    if len(values) >= 2:
        try:
            return stdev(values)
        except StatisticsError:
            return 0.0
    if len(values) == 1:
        return 0.0
    return None


def format_float(value: float | None) -> str:
    return f"{value:.4f}" if value is not None else "NA"


def load_rows(path: Path) -> List[dict]:
    rows: List[dict] = []
    with path.open(encoding="utf-8") as file:
        header = file.readline()
        if not header:
            return rows
        for raw_line in file:
            line = raw_line.strip()
            if not line:
                continue
            try:
                algorithm, seed, board_size, rest = line.split(",", 3)
            except ValueError as exc:
                raise ValueError(f"Formato inesperado en la línea: {raw_line!r}") from exc

            algorithm = algorithm.strip()
            seed = int(seed)
            board_size = int(board_size)

            try:
                board_part, remainder = rest.split("],", 1)
            except ValueError as exc:
                raise ValueError(f"No se pudo aislar la columna board en la línea: {raw_line!r}") from exc

            board_str = f"{board_part.strip()}]"
            remainder = remainder.lstrip(", ")
            try:
                cost_str, states_str, time_str = [segment.strip() for segment in remainder.split(",", 2)]
            except ValueError as exc:
                raise ValueError(f"No se pudieron separar las columnas numéricas en la línea: {raw_line!r}") from exc

            rows.append(
                {
                    "algorithm_name": algorithm,
                    "seed": seed,
                    "board_size": board_size,
                    "board": board_str,
                    "solution_cost": float(cost_str),
                    "states_n": int(states_str),
                    "time": float(time_str),
                }
            )
    return rows


def group_rows(rows: Iterable[dict]) -> dict[tuple[str, int], list[dict]]:
    grouped: dict[tuple[str, int], list[dict]] = defaultdict(list)
    for row in rows:
        key = (row["algorithm_name"], row["board_size"])
        grouped[key].append(row)
    return grouped


def summarize_group(rows: List[dict]) -> dict:
    total_runs = len(rows)
    costs = [row["solution_cost"] for row in rows]
    times = [row["time"] for row in rows]
    states = [row["states_n"] for row in rows]
    successes = [row for row in rows if row["solution_cost"] == 0.0]
    success_count = len(successes)
    success_rate = (success_count / total_runs) * 100 if total_runs else 0.0

    return {
        "runs": total_runs,
        "success_count": success_count,
        "success_rate_pct": success_rate,
        "avg_cost": safe_mean(costs),
        "std_cost": safe_stdev(costs),
        "avg_time": safe_mean(times),
        "std_time": safe_stdev(times),
        "avg_states": safe_mean(states),
        "std_states": safe_stdev(states),
    }


def main() -> None:
    args = parse_args()
    rows = load_rows(args.input)
    grouped = group_rows(rows)
    headers = [
        "algorithm_name",
        "board_size",
        "runs",
        "success_count",
        "success_rate_pct",
        "avg_cost",
        "std_cost",
        "avg_time",
        "std_time",
        "avg_states",
        "std_states",
    ]

    summary_lines = []
    for (algorithm, board_size) in sorted(grouped.keys()):
        stats = summarize_group(grouped[(algorithm, board_size)])
        summary_lines.append({
            "algorithm_name": algorithm,
            "board_size": board_size,
            **stats,
        })

    print("\nAggregated metrics per algorithm and board size\n")
    header_fmt = (
        f"{'Algorithm':<12} {'Size':>4} {'Runs':>4} {'Success%':>9} "
        f"{'Avg H':>10} {'Std H':>10} {'Avg Time':>12} "
        f"{'Std Time':>12} {'Avg States':>13} {'Std States':>13}"
    )
    print(header_fmt)
    print("-" * len(header_fmt))
    for line in summary_lines:
        print(
            f"{line['algorithm_name']:<12} "
            f"{line['board_size']:>4} "
            f"{line['runs']:>4} "
            f"{line['success_rate_pct']:>8.2f}% "
            f"{format_float(line['avg_cost']):>10} "
            f"{format_float(line['std_cost']):>10} "
            f"{format_float(line['avg_time']):>12} "
            f"{format_float(line['std_time']):>12} "
            f"{format_float(line['avg_states']):>13} "
            f"{format_float(line['std_states']):>13}"
        )
    print(
        "\nLos promedios y desviaciones se calculan sobre todas las ejecuciones, "
        "independientemente de si obtuvieron solución óptima."
    )

    if args.output:
        with args.output.open("w", newline="", encoding="utf-8") as file:
            writer = csv.DictWriter(file, fieldnames=headers)
            writer.writeheader()
            for line in summary_lines:
                writer.writerow(line)
        print(f"\nResumen escrito en {args.output}")


if __name__ == "__main__":
    main()
