"""
run_eval.py - send every ticket to both AI models and save their answers.

What it does, step by step:
  1. Reads the tickets from ticket_labels.xlsx (only columns A-G, the part the AI is allowed to see).
  2. Reads the instructions from prompt_v1.txt.
  3. Sends each ticket to Gemini (Google AI Studio) and to an open model on Groq.
  4. Records each answer, how many tokens it used (for cost), and how long it took (latency).
  5. Saves everything to results.csv. score.py grades that file afterwards.

How to run (in a terminal, inside this folder):
  py run_eval.py --list-models     # shows which model names your keys can use
  py run_eval.py --limit 3         # quick test on 3 tickets
  py run_eval.py                   # full run on every ticket
  py run_eval.py --only groq       # run just one model (gemini or groq)
  py run_eval.py --fresh           # throw away earlier answers and start over

Re-running is safe: answers already saved in results.csv are kept, and only the
missing or failed tickets are sent again. That's how a run continues after a
free-tier daily limit resets.

Your API keys are typed in when the script starts. They are never saved to a file.
"""

import argparse
import csv
import getpass
import json
import os
import re
import time

import openpyxl
import requests

# ---------------------------------------------------------------------------
# SETTINGS - check these before the full run
# ---------------------------------------------------------------------------
# Exact model names. Run `python run_eval.py --list-models` and copy a name from the list.
GEMINI_MODEL = "gemini-3.5-flash"   # 3.8-flash timed out on the free tier on Oct 26, 2026
GROQ_MODEL = "openai/gpt-oss-120b"  # an open model on Groq's free tier

# Seconds to wait between requests, so we stay under the free-tier speed limits.
WAIT_SECONDS = {"gemini": 13, "groq": 3}  # Gemini free tier allows 5 requests per minute

TICKETS_FILE = "ticket_labels.xlsx"
PROMPT_FILE = "prompt_v1.txt"
RESULTS_FILE = "results.csv"
# ---------------------------------------------------------------------------


def load_tickets(path):
    """Read ticket rows. Only the input columns (A-G) are used, never the labels."""
    sheet = openpyxl.load_workbook(path, data_only=True)["Tickets"]
    tickets = []
    for row in sheet.iter_rows(min_row=2, values_only=True):
        ticket_id, channel, year, model, odometer, drivable, text = row[:7]
        if not ticket_id or not text or str(text).startswith("(you write"):
            continue
        tickets.append({
            "ticket_id": ticket_id,
            # This is exactly what the AI sees for one ticket:
            "message": (
                f"Channel: {channel}\n"
                f"Vehicle: {year} {model}, {odometer} miles\n"
                f"Drivable (customer says): {drivable}\n"
                f"Customer message: {text}"
            ),
        })
    return tickets


def ask_gemini(key, prompt, message):
    """Send one ticket to Gemini. Returns (answer text, input tokens, output tokens)."""
    url = f"https://generativelanguage.googleapis.com/v1beta/models/{GEMINI_MODEL}:generateContent"
    body = {
        "systemInstruction": {"parts": [{"text": prompt}]},
        "contents": [{"role": "user", "parts": [{"text": message}]}],
        "generationConfig": {"temperature": 0, "responseMimeType": "application/json"},
    }
    r = requests.post(url, headers={"x-goog-api-key": key}, json=body, timeout=120)
    r.raise_for_status()
    data = r.json()
    text = "".join(p.get("text", "") for p in data["candidates"][0]["content"]["parts"])
    usage = data.get("usageMetadata", {})
    # "Thinking" tokens are billed as output, so they are counted with the answer.
    out_tokens = usage.get("candidatesTokenCount", 0) + usage.get("thoughtsTokenCount", 0)
    return text, usage.get("promptTokenCount", 0), out_tokens


def ask_groq(key, prompt, message):
    """Send one ticket to Groq. Returns (answer text, input tokens, output tokens)."""
    url = "https://api.groq.com/openai/v1/chat/completions"
    body = {
        "model": GROQ_MODEL,
        "messages": [{"role": "system", "content": prompt}, {"role": "user", "content": message}],
        "temperature": 0,
        "response_format": {"type": "json_object"},
    }
    r = requests.post(url, headers={"Authorization": f"Bearer {key}"}, json=body, timeout=120)
    r.raise_for_status()
    data = r.json()
    usage = data.get("usage", {})
    return (data["choices"][0]["message"]["content"],
            usage.get("prompt_tokens", 0), usage.get("completion_tokens", 0))


def parse_answer(text):
    """Pull the JSON object out of the model's reply. Returns a dict, or None if it can't."""
    try:
        return json.loads(text)
    except (json.JSONDecodeError, TypeError):
        match = re.search(r"\{.*\}", text or "", re.DOTALL)  # model wrapped it in extra text
        if match:
            try:
                return json.loads(match.group(0))
            except json.JSONDecodeError:
                pass
    return None


class QuotaUsedUp(Exception):
    """The free tier's daily allowance is used up. Retrying won't help until it resets."""


def call_with_retry(ask, key, prompt, message, tries=4):
    """Free tiers sometimes say 'too many requests' (error 429). Wait and try again."""
    for attempt in range(tries):
        try:
            start = time.time()
            text, tokens_in, tokens_out = ask(key, prompt, message)
            # Latency = how long the answer that worked took. Time spent waiting to retry is not counted.
            return text, tokens_in, tokens_out, round(time.time() - start, 2)
        except requests.HTTPError as e:
            status = e.response.status_code
            if status == 429 and "quota" in e.response.text.lower():
                raise QuotaUsedUp(e.response.text[:300])
            if status in (429, 500, 503) and attempt < tries - 1:
                wait = 20 * (attempt + 1)
                print(f"    busy or rate-limited ({status}), waiting {wait}s and retrying...")
                time.sleep(wait)
            else:
                raise RuntimeError(f"HTTP {status}: {e.response.text[:300]}")
        except (requests.Timeout, requests.ConnectionError):
            # No answer in time (the server is overloaded). Treat it like "busy" and try again.
            if attempt < tries - 1:
                wait = 20 * (attempt + 1)
                print(f"    no answer in time, waiting {wait}s and retrying...")
                time.sleep(wait)
            else:
                raise RuntimeError("timed out on every try")


def list_models(gemini_key, groq_key):
    r = requests.get("https://generativelanguage.googleapis.com/v1beta/models",
                     headers={"x-goog-api-key": gemini_key}, timeout=60)
    print("Gemini models:" if r.ok else f"Gemini error {r.status_code}: {r.text[:200]}")
    for m in r.json().get("models", []) if r.ok else []:
        if "generateContent" in m.get("supportedGenerationMethods", []):
            print("  ", m["name"].replace("models/", ""))
    r = requests.get("https://api.groq.com/openai/v1/models",
                     headers={"Authorization": f"Bearer {groq_key}"}, timeout=60)
    print("Groq models:" if r.ok else f"Groq error {r.status_code}: {r.text[:200]}")
    for m in r.json().get("data", []) if r.ok else []:
        print("  ", m["id"])


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--limit", type=int, help="only run the first N tickets")
    parser.add_argument("--list-models", action="store_true", help="show available model names and stop")
    parser.add_argument("--only", choices=["gemini", "groq"], help="run just one model")
    parser.add_argument("--fresh", action="store_true", help="ignore earlier answers and start over")
    args = parser.parse_args()

    gemini_key = groq_key = ""
    if args.only != "groq":
        gemini_key = getpass.getpass("Paste your Google AI Studio key (it won't show): ").strip()
    if args.only != "gemini":
        groq_key = getpass.getpass("Paste your Groq key (it won't show): ").strip()

    if args.list_models:
        list_models(gemini_key, groq_key)
        return

    prompt = open(PROMPT_FILE, encoding="utf-8").read()
    tickets = load_tickets(TICKETS_FILE)[: args.limit]
    all_models = [
        ("gemini", GEMINI_MODEL, ask_gemini, gemini_key),
        ("groq", GROQ_MODEL, ask_groq, groq_key),
    ]
    models = [m for m in all_models if args.only in (None, m[0])]
    current = {(provider, name) for provider, name, _, _ in all_models}

    # Keep good answers from earlier runs (same models only), so we never pay for them twice.
    kept = []
    if not args.fresh and os.path.exists(RESULTS_FILE):
        with open(RESULTS_FILE, encoding="utf-8") as f:
            for row in csv.DictReader(f):
                if not row.get("error"):  # good answers from any model are kept; score.py grades each model separately
                    kept.append(row)
    done = {(r["provider"], r["model"], r["ticket_id"]) for r in kept}
    print(f"Running {len(tickets)} tickets on {', '.join(m[1] for m in models)}"
          f" ({len(done)} answers already saved will be skipped)\n")

    fields = ["provider", "model", "ticket_id", "category", "priority", "safety_critical",
              "next_step", "reason", "input_tokens", "output_tokens", "latency_seconds",
              "error", "raw_answer"]
    with open(RESULTS_FILE, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fields)
        writer.writeheader()
        writer.writerows(kept)
        for provider, model_name, ask, key in models:
            for t in tickets:
                if (provider, model_name, t["ticket_id"]) in done:
                    continue
                row = {"provider": provider, "model": model_name, "ticket_id": t["ticket_id"]}
                start = time.time()
                try:
                    text, tokens_in, tokens_out, latency = call_with_retry(ask, key, prompt, t["message"])
                    row["latency_seconds"] = latency
                    row.update(input_tokens=tokens_in, output_tokens=tokens_out, raw_answer=text)
                    answer = parse_answer(text)
                    if answer is None:
                        row["error"] = "could not read JSON"
                    else:
                        for k in ("category", "priority", "safety_critical", "next_step", "reason"):
                            row[k] = answer.get(k, "")
                except QuotaUsedUp:
                    print(f"  {provider}: today's free quota is used up. Skipping the rest for {provider}.")
                    print(f"  Run again after it resets (midnight Pacific) to finish: py run_eval.py --only {provider}")
                    break
                except Exception as e:  # keep going; the error is recorded and scored as a miss
                    row["latency_seconds"] = round(time.time() - start, 2)
                    row["error"] = str(e)[:300]
                writer.writerow(row)
                f.flush()
                status = row.get("error") or f"{row.get('category')} | {row.get('priority')} | safety {row.get('safety_critical')}"
                print(f"  {provider:6} {t['ticket_id']}: {status}")
                time.sleep(WAIT_SECONDS[provider])

    print(f"\nDone. Answers saved to {RESULTS_FILE}. Next: py score.py")


if __name__ == "__main__":
    main()
