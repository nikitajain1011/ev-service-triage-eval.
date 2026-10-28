"""
score.py - grade the models' answers against your answer key.

Reads:  ticket_labels.xlsx (your labels) and results.csv (the models' answers)
Writes: scores.csv    - one row per model with every metric
        mistakes.csv  - every ticket a model got wrong, side by side with your label

How to run:  py score.py                                         (grades against ticket_labels.xlsx)
             py score.py ticket_labels_v1_original.xlsx original  (grades against another answer key)
"""

import csv
import statistics
import sys
from collections import defaultdict

import openpyxl

# ---------------------------------------------------------------------------
# PRICES - US dollars per 1 million tokens, from each provider's official pricing page.
# Free tiers cost $0, so cost is estimated at the PAID price: what this would cost in real use.
# Fill these in before reporting cost. Leave as None and cost is shown as "not set".
# ---------------------------------------------------------------------------
PRICES = {
    # gemini-3.5-flash and openai/gpt-oss-120b, as listed by the Maxim LLM cost calculator
    # (updated Oct 23-26, 2026). Confirm on the official Gemini API and Groq pricing pages.
    "gemini": {"input": 1.50, "output": 9.00},
    "groq": {"input": 0.15, "output": 0.60},
}

CATEGORIES = ["Charging", "High-voltage battery & drive", "Chassis", "Software & infotainment",
              "Driver assistance", "Electrical (12V)", "Body & cabin", "Other / Unclear"]
PRIORITIES = ["P1", "P2", "P3"]
SAFETY = ["Yes", "No"]
NEXT_STEPS = ["Stop driving + roadside assistance", "Dispatch mobile service",
              "Schedule service center visit", "Remote diagnosis or software fix",
              "Contact customer for more information", "Explain to customer (no repair needed)"]


def clean(value, allowed):
    """Match an answer to an allowed value, ignoring capitals and extra spaces.
    Anything that isn't on the list counts as wrong."""
    if value is None:
        return None
    text = " ".join(str(value).split()).lower()
    for option in allowed:
        if option.lower() == text:
            return option
    return None


def load_answer_key(path):
    sheet = openpyxl.load_workbook(path, data_only=True)["Tickets"]
    key = {}
    for row in sheet.iter_rows(min_row=2, values_only=True):
        ticket_id, category, alt = row[0], row[7], row[8]
        if not ticket_id or not category:
            continue
        key[ticket_id] = {
            "category": clean(category, CATEGORIES),
            "alt_category": clean(alt, CATEGORIES),
            "priority": clean(row[9], PRIORITIES),
            "safety_critical": clean(row[10], SAFETY),
            "next_step": clean(row[11], NEXT_STEPS),
            "text": row[6],
        }
    return key


def pct(part, whole):
    return f"{100 * part / whole:.0f}%" if whole else "n/a"


def main():
    key_file = sys.argv[1] if len(sys.argv) > 1 else "ticket_labels.xlsx"
    suffix = f"_{sys.argv[2]}" if len(sys.argv) > 2 else ""
    print(f"Answer key: {key_file}")
    key = load_answer_key(key_file)
    by_model = defaultdict(list)
    with open("results.csv", encoding="utf-8") as f:
        for row in csv.DictReader(f):
            if row["ticket_id"] in key:
                by_model[(row["provider"], row["model"])].append(row)

    score_rows, mistake_rows = [], []
    for (provider, model), rows in by_model.items():
        n = len(rows)
        right = defaultdict(int)
        safety_yes = caught = safety_no = false_alarms = invalid = 0
        dangerous_misses = []
        for r in rows:
            gold = key[r["ticket_id"]]
            pred = {
                "category": clean(r["category"], CATEGORIES),
                "priority": clean(r["priority"], PRIORITIES),
                "safety_critical": clean(r["safety_critical"], SAFETY),
                "next_step": clean(r["next_step"], NEXT_STEPS),
            }
            if r["error"] or None in pred.values():
                invalid += 1
            ok = {
                "category": pred["category"] in (gold["category"], gold["alt_category"]) and pred["category"] is not None,
                "priority": pred["priority"] == gold["priority"],
                "safety_critical": pred["safety_critical"] == gold["safety_critical"],
                "next_step": pred["next_step"] == gold["next_step"],
            }
            for field, good in ok.items():
                right[field] += good
            right["all_four"] += all(ok.values())

            # Safety recall: of the truly safety-critical tickets, how many did it flag?
            if gold["safety_critical"] == "Yes":
                safety_yes += 1
                if pred["safety_critical"] == "Yes":
                    caught += 1
                else:
                    dangerous_misses.append(r["ticket_id"])
            # False alarm rate: of the safe tickets, how many did it wrongly flag?
            else:
                safety_no += 1
                if pred["safety_critical"] == "Yes":
                    false_alarms += 1

            if not all(ok.values()):
                mistake_rows.append({
                    "model": model, "ticket_id": r["ticket_id"], "customer_message": gold["text"],
                    "wrong_fields": ", ".join(k for k, good in ok.items() if not good),
                    "your_label": f'{gold["category"]} | {gold["priority"]} | {gold["safety_critical"]} | {gold["next_step"]}',
                    "model_answer": f'{r["category"]} | {r["priority"]} | {r["safety_critical"]} | {r["next_step"]}',
                    "model_reason": r["reason"] or r["error"],
                })

        latencies = [float(r["latency_seconds"]) for r in rows if r["latency_seconds"] and not r["error"]]
        tokens_in = sum(int(r["input_tokens"] or 0) for r in rows)
        tokens_out = sum(int(r["output_tokens"] or 0) for r in rows)
        price = PRICES.get(provider, {})
        if price.get("input") is not None and price.get("output") is not None:
            cost = (tokens_in * price["input"] + tokens_out * price["output"]) / 1_000_000
            cost_text = f"${cost / n:.5f} per ticket (${cost * 1000 / n:.2f} per 1,000 tickets)"
        else:
            cost_text = "not set (fill in PRICES)"

        score_rows.append({
            "model": model, "tickets": n,
            "category_accuracy": pct(right["category"], n),
            "priority_accuracy": pct(right["priority"], n),
            "safety_flag_accuracy": pct(right["safety_critical"], n),
            "next_step_accuracy": pct(right["next_step"], n),
            "all_four_correct": pct(right["all_four"], n),
            "safety_recall": f"{caught} of {safety_yes} ({pct(caught, safety_yes)})",
            "false_alarm_rate": f"{false_alarms} of {safety_no} ({pct(false_alarms, safety_no)})",
            "missed_safety_tickets": " ".join(dangerous_misses) or "none",
            "invalid_or_failed_answers": invalid,
            "median_latency_seconds": f"{statistics.median(latencies):.2f}" if latencies else "n/a",
            "max_latency_seconds": f"{max(latencies):.2f}" if latencies else "n/a",
            "avg_tokens_per_ticket": f"{tokens_in / n:.0f} in, {tokens_out / n:.0f} out",
            "estimated_cost": cost_text,
        })

    for s in score_rows:
        print(f"\n=== {s['model']} ===")
        for k, v in s.items():
            if k != "model":
                print(f"  {k.replace('_', ' '):28} {v}")

    if score_rows:
        with open(f"scores{suffix}.csv", "w", newline="", encoding="utf-8") as f:
            w = csv.DictWriter(f, fieldnames=list(score_rows[0].keys()))
            w.writeheader()
            w.writerows(score_rows)
    with open(f"mistakes{suffix}.csv", "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=["model", "ticket_id", "customer_message", "wrong_fields",
                                          "your_label", "model_answer", "model_reason"])
        w.writeheader()
        w.writerows(mistake_rows)
    print(f"\nSaved scores{suffix}.csv and mistakes{suffix}.csv")


if __name__ == "__main__":
    main()
