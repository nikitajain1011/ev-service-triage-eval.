# EV Service Ticket Triage: Two-Model Eval

**What this project is.** When an electric vehicle owner reports a problem, someone has to read the message and make four decisions: what kind of problem it is, how urgent it is, whether it's dangerous, and what should happen first. I tested whether AI can make those decisions reliably. I created 30 realistic customer messages, wrote the correct answers by hand, gave the same messages to two AI models, and graded their answers.

**What I found.** I compared Google's Gemini 3.5 Flash with gpt-oss-120b, a free, open-source model that I ran through a service called Groq.

- **Both models caught all 14 dangerous tickets,** including ones written in calm, everyday words, like a brake pedal "going almost to the floor" without the word "brakes."
- **Gemini was more accurate overall:** it got all four decisions right on 70% of tickets, versus 57% for gpt-oss-120b.
- **gpt-oss-120b was about 19 times cheaper and nearly 3 times faster:** $0.47 versus $8.81 per 1,000 tickets, and 2.9 versus 7.8 seconds per answer.
- **Both models were weakest at choosing the next step** (right 70–77% of the time), such as whether to send a mobile technician or book a service center visit.

**What I recommend.** Neither model is ready to make these decisions on its own. The next step is a **shadow pilot** with gpt-oss-120b: for a few weeks, the AI reads real incoming tickets and makes its suggestions quietly in the background, while service advisors keep working exactly as they do today. No one acts on the AI's answers; they're only compared with what the advisors decided. I chose gpt-oss-120b because it was just as good at catching dangerous tickets at a fraction of the cost, and its weaker area, the next step, is exactly the decision an advisor would confirm anyway.

## Results

Both models answered all 30 tickets with the same prompt (`prompt_v1.txt`). Accuracy is shown against the corrected answer key, with the original key in brackets.

| Metric | Gemini 3.5 Flash | gpt-oss-120b (Groq) |
| --- | --- | --- |
| Safety recall | 14 of 14 (100%) | 14 of 14 (100%) |
| False alarm rate | 1 of 16 (6%) | 1 of 16 (6%) |
| Category accuracy | 100% [97%] | 97% [93%] |
| Priority accuracy | 87% [83%] | 87% [83%] |
| Safety flag accuracy | 97% [97%] | 97% [97%] |
| Next step accuracy | 77% [73%] | 70% [67%] |
| All four correct | 70% [63%] | 57% [47%] |
| Median response time | 7.8 s | 2.9 s |
| Average tokens per ticket (in / out) | 1,175 / 783 | 1,230 / 470 |
| Estimated cost per 1,000 tickets | $8.81 | $0.47 |
| Availability during the test | Free-tier daily limit hit; one outage; newer 3.8 Flash timed out | No failures |

Cost uses each model's paid price per million tokens (Gemini 3.5 Flash $1.50 in / $9.00 out; gpt-oss-120b on Groq $0.15 in / $0.60 out), as listed by a third-party price tracker on Oct 26, 2026. The test ran on free tiers.

## Where the models went wrong

Every miss is in `mistakes.csv` (corrected key) and `mistakes_original.csv` (original key), with the model's one-line reason.

| Pattern | Example |
| --- | --- |
| Under-escalating an active safety problem | T-013: the truck braked hard on its own. Both models flagged it as safety-critical and P1, but neither told the driver to stop. |
| Sending working cars to service | T-024 (humming under acceleration), T-009 for Groq (range drop in cold weather): normal behavior routed to a service center. |
| Defaulting to a service center visit | Groq chose a service center on 4 tickets where the key said mobile service, remote diagnosis, or explain. |
| Reading the situation, not the rule | Gemini missed a stranded customer at home (T-015). Groq flagged a dead car with children aboard as safety-critical (T-030). |

## Recommendation and pilot plan

Test gpt-oss-120b in **shadow mode**: it triages real incoming tickets, advisors work as they do today and never see its answers, and the two are compared weekly. Nothing reaches a customer until the pilot meets its exit criteria.

| Review level | Tickets | Who decides |
| --- | --- | --- |
| Human decides | Safety-flagged, any P1, any "stop driving" instruction, Other / Unclear | Advisor, with the AI's suggestion and reason shown |
| Human confirms | P2 | AI pre-fills all four fields; advisor accepts or edits |
| Spot-checked | P3 settings questions and expected-behavior explanations | AI drafts the reply; a sample is reviewed weekly |

Proposed exit criteria: safety recall of at least 99% on a few hundred real safety-critical tickets with no missed "stop driving" cases; next-step agreement with advisors of at least 85%; false alarm rate under 10%; measured advisor time saved per ticket.

## Limits

- **Small sample.** 14 of 14 is consistent with a true catch rate as low as about 80% (95% confidence).
- **Rules and tickets grew together.** The labeling guide was refined on these same 30 tickets before it was frozen, so results may be optimistic. Version 2 adds 30 held-out tickets.
- **Synthetic tickets.** 25 of 30 were drafted with Claude (a different model family from both models tested); 5 were written by hand.
- **One human labeler,** with an AI as second labeler. The rules have not yet been checked by a service technician.
- **Three labels corrected after the run,** where both models disagreed and the frozen guide supported the change. Results are shown both ways.
- **Free-tier conditions** and third-party prices; one run per model at temperature 0.

The categories and rules are my own, modeled on public information about EV service. They are not any manufacturer's internal process, and no real customer data was used.

## Files

| File | What it is |
| --- | --- |
| `LABELING_GUIDE.md` | The labeling rules (version 1, frozen Oct 26, 2026), cheat sheet, and dated decision log |
| `ticket_labels.xlsx` | The 30 tickets and the corrected answer key (notes column explains every revision) |
| `ticket_labels_v1_original.xlsx` | The answer key before the three post-run corrections |
| `prompt_v1.txt` | The prompt both models received |
| `run_eval.py` | Sends each ticket to both models; records answers, tokens, and latency in `results.csv` |
| `score.py` | Grades `results.csv` against an answer key; writes `scores*.csv` and `mistakes*.csv` |
| `results.csv` | Every model answer, with its reason, token counts, and latency |
| `scores.csv`, `scores_original.csv` | Metrics against the corrected and original keys |
| `mistakes.csv`, `mistakes_original.csv` | Every ticket a model got wrong, side by side with the label |
| `HOW_TO_RUN.md` | Step-by-step instructions to rerun the eval |

## How it was built

1. Defined the four decisions and wrote a labeling guide. Cut 12 draft categories to 8; kept danger as a separate safety flag based on NHTSA's examples of safety-related defects.
2. Ran a 30-ticket labeling pilot. It produced 7 new rules and showed where my own labels drifted from my rules.
3. Added an automatic consistency check to the label sheet and froze the guide as version 1.
4. Built the prompt only from the guide, ran both models, and adjudicated: three labels corrected where both models disagreed and the guide supported the change.

Claude (Anthropic) was my collaborator for drafting tickets, the prompt, and the Python scripts, and as a second labeler. The labels, rule decisions, and recommendation are mine.

## Sources

- [NHTSA, Motor Vehicle Safety Defects and Recalls (Nov 2024)](https://www.nhtsa.gov/document/motor-vehicle-safety-defects-and-recalls)
- [Tesla Service Manual, Mobile Service Indicator](https://service.tesla.com/docs/ModelS/ServiceManual/en-us/GUID-FA4D8FAA-9481-4E2A-B98C-D51CAE717FF1.html)
- [PBS NewsHour, GM recalls 51,640 SUVs for defective fuel gauges](https://www.pbs.org/newshour/nation/gm-recalls-51640-suvs-defective-fuel-gauges)
- [Maxim LLM cost calculator: Gemini 3.5 Flash](https://www.getmaxim.ai/bifrost/llm-cost-calculator/provider/gemini/model/gemini-3.5-flash) and [gpt-oss-120b on Groq](https://www.getmaxim.ai/bifrost/llm-cost-calculator/provider/groq/model/gpt-oss-120b)
