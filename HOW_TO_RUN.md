# How to run the eval

Everything runs on your computer. Your API keys are typed in when the script starts and are never saved.

## Files in this folder

| File | What it is |
| --- | --- |
| `ticket_labels.xlsx` | The tickets and your answer key |
| `prompt_v1.txt` | The instructions both models get |
| `run_eval.py` | Sends every ticket to both models and saves their answers to `results.csv` |
| `score.py` | Grades `results.csv` against your answer key and writes `scores.csv` and `mistakes.csv` |

## One-time setup

1. Install Python 3 from python.org if you don't have it. On Windows, tick **"Add Python to PATH"** during install.
2. Open a terminal in this folder:
   - **Mac:** open Terminal, type `cd ` (with a space), drag this folder onto the window, press Enter.
   - **Windows:** open the folder in File Explorer, click the address bar, type `cmd`, press Enter.
3. Install the two libraries the scripts use:

   ```
   py -m pip install requests openpyxl
   ```

   These commands are for Windows (`py`). On a Mac, use `python3` and `pip3` instead.

## Each run

1. **Check the model names.** This prints every model your keys can use:

   ```
   py run_eval.py --list-models
   ```

   If `gemini-2.5-flash` or `openai/gpt-oss-120b` isn't in the list, open `run_eval.py` in a text editor and change `GEMINI_MODEL` or `GROQ_MODEL` near the top to a name from the list.

2. **Test on 3 tickets first:**

   ```
   py run_eval.py --limit 3
   ```

   You should see one line per ticket per model. Errors are printed on the line.

3. **Full run.** Takes about 5 to 10 minutes because of the free-tier speed limits:

   ```
   py run_eval.py
   ```

4. **Score it:**

   ```
   py score.py
   ```

   Results print on screen and are saved to `scores.csv`. Every ticket a model got wrong is in `mistakes.csv`, next to your label and the model's one-line reason.

## Useful options

- `py run_eval.py --only groq` (or `--only gemini`) runs one model.
- Rerunning is safe: answers already in `results.csv` are kept, and only missing or failed tickets are sent again. That's how a run continues after a free-tier daily limit resets.
- `py run_eval.py --fresh` starts over.
- `py score.py ticket_labels_v1_original.xlsx original` grades against the original answer key.

## Before reporting cost

Free tiers cost $0, so cost is estimated at each model's **paid** price. `PRICES` near the top of `score.py` holds the input and output price per 1 million tokens. Check them against the Gemini API and Groq pricing pages for the exact models used, and note the date.

## Don't

- Paste your keys into any file, or share them.
- Change `prompt_v1.txt` or your labels after seeing results on these tickets. If you want to try a change, save it as `prompt_v2.txt` and keep the version 1 results.
