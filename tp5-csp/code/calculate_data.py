import csv
import json
import math
import statistics
from collections import defaultdict


RESULTS_PATH = "tp5-csp/code/results.csv"
OUTPUT_PATH = "tp5-csp/code/data_obtained.csv"


def parse_results(path):
    aggregates = defaultdict(
        lambda: {
            "total": 0,
            "success": 0,
            "durations": [],
            "states": [],
        }
    )

    with open(path, newline="", encoding="utf-8") as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            if not row:
                continue

            algorithm = row.get("name", "").strip()
            size_value = row.get("size", "").strip()

            if not algorithm or not size_value:
                continue

            try:
                size = int(size_value)
            except ValueError:
                continue

            key = (algorithm, size)
            bucket = aggregates[key]
            bucket["total"] += 1

            final_board_raw = row.get("final_board", "").strip()
            if final_board_raw.lower() == "null" or final_board_raw == "":
                continue

            bucket["success"] += 1

            try:
                duration = float(row.get("duration", "0") or 0.0)
            except ValueError:
                duration = 0.0
            bucket["durations"].append(duration)

            try:
                states = int(float(row.get("states", "0") or 0))
            except ValueError:
                states = 0
            bucket["states"].append(states)

    return aggregates


def compute_metrics(aggregates):
    records = []
    for (algorithm, size), bucket in sorted(aggregates.items()):
        total = bucket["total"]
        success = bucket["success"]
        success_rate = (success / total * 100) if total else 0.0

        durations = bucket["durations"]
        states = bucket["states"]

        if durations:
            avg_time = statistics.mean(durations)
            std_time = statistics.pstdev(durations) if len(durations) > 1 else 0.0
        else:
            avg_time = ""
            std_time = ""

        if states:
            avg_state = statistics.mean(states)
            std_state = statistics.pstdev(states) if len(states) > 1 else 0.0
        else:
            avg_state = ""
            std_state = ""

        records.append(
            {
                "algorithm_name": algorithm,
                "size": size,
                "success_rate": round(success_rate, 2),
                "avg_time": avg_time if avg_time == "" else round(avg_time, 6),
                "std_time": std_time if std_time == "" else round(std_time, 6),
                "avg_state": avg_state if avg_state == "" else round(avg_state, 2),
                "std_state": std_state if std_state == "" else round(std_state, 2),
            }
        )

    return records


def write_output(records, path):
    fieldnames = [
        "algorithm_name",
        "size",
        "success_rate",
        "avg_time",
        "std_time",
        "avg_state",
        "std_state",
    ]

    with open(path, "w", newline="", encoding="utf-8") as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        for record in records:
            writer.writerow(record)


def main():
    aggregates = parse_results(RESULTS_PATH)
    records = compute_metrics(aggregates)
    write_output(records, OUTPUT_PATH)


if __name__ == "__main__":
    main()
