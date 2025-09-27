#!/usr/bin/env python3
"""Generate success-rate bar charts per board size from experiment results."""
from __future__ import annotations

import argparse
from collections import defaultdict
from pathlib import Path
from typing import Dict, Iterable, List

import matplotlib.pyplot as plt

Row = Dict[str, object]


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description=(
            "Calcula el porcentaje de soluciones óptimas por algoritmo y tamaño de tablero, "
            "generando gráficos de barras a partir de un archivo CSV de resultados."
        )
    )
    parser.add_argument(
        "input",
        type=Path,
        nargs="?",
        default=Path("results_5_a.csv"),
        help="CSV con las ejecuciones a analizar (por defecto results_5_a.csv).",
    )
    parser.add_argument(
        "--output-dir",
        type=Path,
        default=Path("../images"),
        help="Directorio donde guardar las imágenes generadas.",
    )
    parser.add_argument(
        "--dpi",
        type=int,
        default=200,
        help="Resolución (dpi) para los gráficos exportados.",
    )
    return parser.parse_args()


def load_rows(path: Path) -> List[Row]:
    if not path.exists():
        raise FileNotFoundError(f"No se encontró el archivo {path}")

    rows: List[Row] = []
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
            board_size = int(board_size)

            try:
                board_part, remainder = rest.split("],", 1)
            except ValueError as exc:
                raise ValueError(f"No se pudo aislar la columna board en la línea: {raw_line!r}") from exc

            remainder = remainder.lstrip(", ")
            try:
                cost_str, states_str, time_str = [segment.strip() for segment in remainder.split(",", 2)]
            except ValueError as exc:
                raise ValueError(f"No se pudieron separar las columnas numéricas en la línea: {raw_line!r}") from exc

            rows.append(
                {
                    "algorithm_name": algorithm,
                    "board_size": board_size,
                    "solution_cost": float(cost_str),
                }
            )
    return rows


def group_by_size(rows: Iterable[Row]) -> Dict[int, List[Row]]:
    grouped: Dict[int, List[Row]] = defaultdict(list)
    for row in rows:
        grouped[int(row["board_size"])].append(row)
    return grouped


def compute_success_rate(rows: List[Row]) -> float:
    total = len(rows)
    if total == 0:
        return 0.0
    successes = sum(1 for row in rows if float(row["solution_cost"]) == 0.0)
    return (successes / total) * 100.0


def ensure_algorithms(rows: Iterable[Row]) -> List[str]:
    algorithms = sorted({str(row["algorithm_name"]) for row in rows})
    if not algorithms:
        raise ValueError("El archivo de resultados no contiene algoritmos.")
    return algorithms


def plot_success_rates(
    board_size: int,
    algorithms: List[str],
    rows_by_algorithm: Dict[str, List[Row]],
    output_dir: Path,
    dpi: int,
) -> None:
    success_rates = [compute_success_rate(rows_by_algorithm.get(algo, [])) for algo in algorithms]

    fig, ax = plt.subplots(figsize=(8, 5))
    bars = ax.bar(range(len(algorithms)), success_rates, color=plt.get_cmap("tab10")(range(len(algorithms))))
    ax.set_title(f"Porcentaje de soluciones óptimas (N={board_size})")
    ax.set_ylabel("Éxitos (%)")
    ax.set_xticks(range(len(algorithms)), algorithms)
    ax.set_ylim(0, 100)
    ax.grid(axis="y", linestyle="--", alpha=0.4)
    ax.bar_label(bars, fmt="%.1f%%", padding=3)

    output_dir.mkdir(parents=True, exist_ok=True)
    output_path = output_dir / f"success_size_{board_size}.png"
    fig.savefig(output_path, dpi=dpi, bbox_inches="tight")
    plt.close(fig)


def main() -> None:
    args = parse_args()
    rows = load_rows(args.input)
    if not rows:
        raise ValueError("El archivo de resultados está vacío.")

    algorithms = ensure_algorithms(rows)
    rows_by_size = group_by_size(rows)

    for board_size in sorted(rows_by_size):
        grouped = defaultdict(list)
        for row in rows_by_size[board_size]:
            grouped[str(row["algorithm_name"])].append(row)
        plot_success_rates(board_size, algorithms, grouped, args.output_dir, args.dpi)


if __name__ == "__main__":
    main()
