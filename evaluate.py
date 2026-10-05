"""
Compares results.json (the output) to expected.json ("answer key") and reports
precision, recall, and each mistake. Run after flagger.py.

use by running: python evaluate.py
"""

import json
from pathlib import Path

HERE = Path(__file__).parent


def evaluate(expected: dict, results: dict) -> dict:
    true_pos = false_pos = false_neg = 0
    mistakes = []

    for note, expected_flags in expected.items():
        output = results.get(note, [])
        predicted = {f["criterion"] for f in output} if isinstance(output, list) else set()
        actual = set(expected_flags)

        true_pos += len(predicted & actual)
        for extra in predicted - actual:
            false_pos += 1
            mistakes.append(f"{note}: false positive -> {extra}")
        for missed in actual - predicted:
            false_neg += 1
            mistakes.append(f"{note}: missed -> {missed}")

    precision = true_pos / (true_pos + false_pos) if (true_pos + false_pos) else 0.0
    recall = true_pos / (true_pos + false_neg) if (true_pos + false_neg) else 0.0
    return {"precision": precision, "recall": recall, "mistakes": mistakes}


def main() -> None:
    expected = json.loads((HERE / "expected.json").read_text(encoding="utf-8"))
    results = json.loads((HERE / "results.json").read_text(encoding="utf-8"))
    report = evaluate(expected, results)

    print(f"Precision: {report['precision']:.0%}  (of flags raised, how many were right)")
    print(f"Recall:    {report['recall']:.0%}  (of real opportunities, how many were caught)")
    print("\nMistakes:" if report["mistakes"] else "\nNo mistakes!")
    for m in report["mistakes"]:
        print(f"  - {m}")


if __name__ == "__main__":
    main()