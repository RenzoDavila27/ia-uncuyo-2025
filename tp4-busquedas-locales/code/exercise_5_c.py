#!/usr/bin/env python3
"""Generate boxplots per board size using raw experiment runs."""
from __future__ import annotations

import argparse
from pathlib import Path
from typing import Sequence

import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns


DEFAULT_METRICS: tuple[str, ...] = ("states_n", "time", "solution_cost")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description=(
            "Lee las ejecuciones de results.csv y genera boxplots por tamaño de tablero "
            "para las métricas seleccionadas."
        )
    )
    parser.add_argument(
        "input",
        type=Path,
        nargs="?",
        default=Path("results.csv"),
        help="CSV con los resultados crudos (por defecto results.csv).",
    )
    parser.add_argument(
        "--metrics",
        nargs="*",
        default=list(DEFAULT_METRICS),
        help=(
            "Métricas a graficar (columnas numéricas del CSV). "
            f"Por defecto: {', '.join(DEFAULT_METRICS)}"
        ),
    )
    parser.add_argument(
        "--output-dir",
        type=Path,
        default=Path("../images"),
        help="Directorio donde guardar las figuras (se crea si no existe).",
    )
    parser.add_argument(
        "--style",
        default="whitegrid",
        help="Estilo de Seaborn a utilizar (default whitegrid).",
    )
    return parser.parse_args()


def load_results(path: Path) -> pd.DataFrame:
    if not path.exists():
        raise FileNotFoundError(f"No se encontró el archivo {path}")

    rows: list[dict[str, object]] = []
    with path.open(encoding="utf-8") as file:
        header = file.readline()
        if not header:
            return pd.DataFrame()
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
                    "seed": int(seed),
                    "board_size": board_size,
                    "board": f"{board_part.strip()}]",
                    "solution_cost": float(cost_str),
                    "states_n": int(states_str),
                    "time": float(time_str),
                }
            )

    df = pd.DataFrame(rows)
    if df.empty:
        return df
    required_columns = {"algorithm_name", "board_size"}
    missing = required_columns - set(df.columns)
    if missing:
        raise ValueError(f"El CSV no contiene las columnas requeridas: {', '.join(sorted(missing))}")
    return df


def validate_metrics(df: pd.DataFrame, metrics: Sequence[str]) -> list[str]:
    available = set(df.columns)
    invalid = [metric for metric in metrics if metric not in available]
    if invalid:
        raise ValueError(
            "Las métricas solicitadas no existen en el CSV: "
            f"{', '.join(invalid)}"
        )
    numeric_metrics = [metric for metric in metrics if pd.api.types.is_numeric_dtype(df[metric])]
    if not numeric_metrics:
        raise ValueError("Ninguna de las métricas seleccionadas es numérica")
    return numeric_metrics


def plot_boxplots(
    df: pd.DataFrame,
    board_size: int,
    metrics: Sequence[str],
    output_dir: Path,
) -> None:
    subset = df[df["board_size"] == board_size]
    if subset.empty:
        return

    n_metrics = len(metrics)
    fig, axes = plt.subplots(1, n_metrics, figsize=(6 * n_metrics, 5), constrained_layout=True)
    if n_metrics == 1:
        axes = [axes]

    palette = sns.color_palette("Set2", subset["algorithm_name"].nunique())

    for ax, metric in zip(axes, metrics):
        sns.boxplot(
            data=subset,
            x="algorithm_name",
            y=metric,
            hue="algorithm_name",
            palette=palette,
            legend=False,
            ax=ax,
            width=0.6,
        )
        legend = ax.get_legend()
        if legend is not None:
            legend.remove()
        sns.stripplot(
            data=subset,
            x="algorithm_name",
            y=metric,
            ax=ax,
            color="0.25",
            size=2,
            jitter=True,
            dodge=False,
        )
        ax.set_title(f"{metric.replace('_', ' ').title()} (N={board_size})")
        ax.set_xlabel("Algoritmo")
        ax.set_ylabel(metric.replace('_', ' ').title())
        ax.tick_params(axis="x", rotation=20)

    fig.suptitle(f"Distribución por algoritmo - Tablero {board_size}")
    output_dir.mkdir(parents=True, exist_ok=True)
    output_path = output_dir / f"exercise_5_c_size_{board_size}.png"
    fig.savefig(output_path, dpi=200)
    plt.close(fig)


def main() -> None:
    args = parse_args()
    sns.set_style(args.style)
    df = load_results(args.input)
    metrics = validate_metrics(df, args.metrics)

    for size in sorted(df["board_size"].unique()):
        plot_boxplots(df, size, metrics, args.output_dir)


if __name__ == "__main__":
    main()
