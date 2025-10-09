import os
from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns


RESULTS_PATH = Path(__file__).resolve().parent / "results.csv"
OUTPUT_DIR = Path(__file__).resolve().parent.parent / "images"
TARGET_SIZES = [4, 8, 10, 12, 15]


def load_results(path: Path) -> pd.DataFrame:
    df = pd.read_csv(path)
    df = df.dropna(subset=["size", "states", "name"])
    df["size"] = pd.to_numeric(df["size"], errors="coerce")
    df["states"] = pd.to_numeric(df["states"], errors="coerce")
    df = df.dropna(subset=["size", "states"])
    df["size"] = df["size"].astype(int)
    return df


def ensure_output_dir(path: Path) -> None:
    os.makedirs(path, exist_ok=True)


def prettify_algorithm_names(df: pd.DataFrame) -> pd.DataFrame:
    mapping = {
        "backtracking": "Backtracking",
        "forward_checking": "Forward Checking",
    }
    df = df.copy()
    df["name"] = df["name"].map(lambda x: mapping.get(x, x))
    return df


def plot_boxplots(df: pd.DataFrame, output_dir: Path) -> None:
    sns.set_style("whitegrid")
    palette = sns.color_palette("Set2", df["name"].nunique())

    for size in TARGET_SIZES:
        subset = df[df["size"] == size]
        if subset.empty:
            continue

        plt.figure(figsize=(6, 4))
        sns.boxplot(
            data=subset,
            x="name",
            y="states",
            hue="name",
            palette=palette,
            legend=False,
            width=0.6,
        )
        sns.stripplot(
            data=subset,
            x="name",
            y="states",
            color="0.35",
            size=3,
            jitter=0.2,
            dodge=False,
        )
        plt.title(f"Expanded States by Algorithm (N={size})")
        plt.xlabel("Algorithm")
        plt.ylabel("States Visited")
        plt.tight_layout()

        filename = output_dir / f"boxplot_states_size_{size}.png"
        plt.savefig(filename, dpi=300)
        plt.close()


def main() -> None:
    ensure_output_dir(OUTPUT_DIR)
    df = load_results(RESULTS_PATH)
    df = prettify_algorithm_names(df)
    plot_boxplots(df, OUTPUT_DIR)


if __name__ == "__main__":
    main()
