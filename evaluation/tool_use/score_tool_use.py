"""Score tool-use accuracy (scoring logic of the original analyze_results.py).

A prediction is correct only if the tool name AND the full argument dictionary
match the ground truth exactly. Run: python evaluation/tool_use/score_tool_use.py
"""
import json
import os

from scipy.stats import beta

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
RESULTS_PATH = os.path.join(SCRIPT_DIR, "tool_use_results.json")


def main():
    with open(RESULTS_PATH, "r", encoding="utf-8") as f:
        results = json.load(f)

    tasks = [r for r in results if r.get("type") == "TOOL"]
    correct = 0
    for r in tasks:
        gt = r["ground_truth"]
        pred = r.get("predicted_output", {}).get("tool_call")
        if not pred:
            continue
        same_args = (
            pred.get("arguments") is not None and gt.get("arguments") is not None
            and json.dumps(pred["arguments"], sort_keys=True) == json.dumps(gt["arguments"], sort_keys=True)
        )
        if pred.get("tool_name") == gt.get("tool_name") and same_args:
            correct += 1

    n = len(tasks)
    lo = beta.ppf(0.025, correct, n - correct + 1) if correct > 0 else 0.0
    hi = beta.ppf(0.975, correct + 1, n - correct) if correct < n else 1.0
    print(f"Tool-use accuracy: {100 * correct / n:.2f}% ({correct}/{n}); "
          f"95% Clopper-Pearson CI [{100 * lo:.1f}%, {100 * hi:.1f}%]")


if __name__ == "__main__":
    main()
