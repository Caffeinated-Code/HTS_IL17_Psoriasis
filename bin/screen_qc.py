#!/usr/bin/env python3
import csv
import sys


def as_float(value):
    return float(value)


with open(sys.argv[1], newline="") as handle, open(sys.argv[2], "w", newline="") as out:
    reader = csv.DictReader(handle, delimiter="\t")
    fields = reader.fieldnames + ["selectivity_score", "screen_qc_score", "screen_qc_call"]
    writer = csv.DictWriter(out, fieldnames=fields, delimiter="\t")
    writer.writeheader()
    for row in reader:
        primary = as_float(row["primary_activity_score"])
        counter = as_float(row["counterscreen_activity_score"])
        selectivity = max(0.0, primary - counter)
        artifact = row["artifact_flag"].lower() == "true"
        qc = max(0.0, min(1.0, 0.65 * primary + 0.35 * selectivity - (0.25 if artifact else 0.0)))
        if artifact:
            call = "artifact_risk"
        elif qc >= 0.75:
            call = "strong_screen_support"
        elif qc >= 0.55:
            call = "moderate_screen_support"
        else:
            call = "weak_screen_support"
        row["selectivity_score"] = f"{selectivity:.3f}"
        row["screen_qc_score"] = f"{qc:.3f}"
        row["screen_qc_call"] = call
        writer.writerow(row)
