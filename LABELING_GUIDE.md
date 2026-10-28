# Service Ticket Labeling Guide

**Version 1, frozen Oct 26, 2026.** All 30 pilot labels follow this version. New rules only if a ticket truly can't be labeled; any change becomes version 2, and the test is rerun to compare.

The categories and rules are my own, modeled on public information about EV service. They are not any manufacturer's internal process.

## How to use this guide

Every ticket gets exactly one of 8 categories. Category says which vehicle system the problem is in; danger is tracked separately by the safety-critical flag.

**Tie-breaker rule:** when a ticket could fit two categories, label it by the system most likely broken (the cause). If the cause isn't clear from the description, label it by where the customer notices the problem (the symptom).

This guide grows as you label. When you hesitate on a ticket, decide, then add a "Not this" line here and a row to the decision log. A one-page version is at the end: [Cheat sheet](#cheat-sheet).

## Categories

### 1. Charging

**In:** Getting power into the car: charge port, cable, adapter, charging station connection, slow charging.

**Not this:**

- Car charges fine but range is low → High-voltage battery & drive
- Won't charge and the car is also dead or won't wake up → Electrical (12V)
- A charging schedule set in the app doesn't start → Software & infotainment

### 2. High-voltage battery & drive

**In:** The main battery and the motors that move the car: range loss, battery warnings, overheating, unexpected charge drops, loss of power while driving, noise that happens only when accelerating or slowing under power. Range dropping when the heater runs also goes here (often expected behavior; the next step is usually explaining it to the customer).

**Not this:**

- Trouble starting a charge or with the port → Charging
- A noise that changes with speed even while coasting → Chassis

### 3. Chassis

**In:** Brakes, steering, suspension, tires, and wheels: pulling to one side, vibration through the steering wheel, flat tires, clunks over bumps, noise that changes with speed even while coasting.

**Not this:**

- A lane-keep or automatic emergency braking problem → Driver assistance
- A noise only when accelerating or slowing under power → High-voltage battery & drive

### 4. Software & infotainment

**In:** The center screen, phone app, maps, music, Bluetooth, software updates, digital key, charging schedules, climate controls that don't respond because the screen is frozen, and requests to change a setting (for example, turning off brake hold).

**Not this:**

- Camera or sensor driving features → Driver assistance
- Car completely dead or won't wake up → Electrical (12V)
- Screen responds but the air temperature doesn't change → Body & cabin

### 5. Driver assistance

**In:** Features that use cameras and sensors to help drive: lane-keep, adaptive cruise, automatic emergency braking, parking sensors, and their warnings.

**Not this:**

- A general screen freeze that also affects these features → Software & infotainment

### 6. Electrical (12V)

**In:** The car's regular low-voltage power: won't wake up or unlock, exterior lights out (including a single headlight), 12V battery dying, power windows dead, wipers that stop moving.

**Not this:**

- Main battery or range problems → High-voltage battery & drive
- Car is awake and working but won't take a charge → Charging

### 7. Body & cabin

**In:** Physical parts you see and touch: doors, panels, paint, glass, leaks, seats, climate control hardware (air doesn't get hot or cold), accessories like racks or the tonneau cover, worn or streaking wiper blades.

**Not this:**

- Door won't unlock with the phone → Software & infotainment
- Climate controls unresponsive because the screen is frozen → Software & infotainment
- A light is out → Electrical (12V)

### 8. Other / Unclear

**In:** Only when the description doesn't point to any one system ("something feels off").

**Not this:**

- If you can reasonably guess a system, pick that system.

## Priority

Priority says how fast someone must act. It covers danger and disruption; the safety flag covers danger only. Response times are assumptions for this project, not any manufacturer's actual standards.

| Level | What it means | Response | Example |
| --- | --- | --- | --- |
| P1 | Unsafe to drive, or the customer is stranded | Same day; tell the customer to stop driving if unsafe | "Brake pedal went soft." / "Car won't wake up and I'm at work." |
| P2 | Safe and drivable, but the problem seriously limits use or could get worse | Within a few days | "Car won't charge at home." / "Water leaking into the footwell." |
| P3 | Comfort, cosmetic, or convenience | Normal scheduling | "Paint chip on the door." / "Bluetooth drops sometimes." |

**Rules:**

- Every ongoing safety-critical problem is P1, except a taillight, brake light, or backup camera out, which is P2.
- A stranded customer is P1, even when the car is safe.
- A safety problem that has stopped: brakes, steering, loss of power, or fire risk (burning smell, smoke, overheating) stay P1; other safety issues that have stopped (for example, a warning light that cleared) are P2. The safety flag stays on either way.
- The customer's tone doesn't change priority. Label by the facts of the problem.
- P3 only if all three answers are no: Does it stop the customer from using the car normally? Could it cause more damage if it waits? Is it getting worse?

## Safety-critical flag

A ticket is safety-critical if the problem could make the car unsafe to drive or injure someone, in any of these five areas:

1. **Loss of control:** steering, brakes (including worn pads), wheels or tires failing (flat or losing air quickly), suspension parts breaking
2. **Loss of power while driving**
3. **Fire risk:** burning smell, smoke, battery overheating warnings
4. **Visibility:** wipers failing, any headlight out, a taillight or brake light out, backup camera not working
5. **Crash protection:** airbag warnings, seat belts, seats that won't lock in place

**Also safety-critical:** driver assistance acting unexpectedly, such as sudden hard braking with nothing ahead; and any problem that can lead to one of the five areas, such as a range or charge display reading too high, which can lead to loss of power. NHTSA treats inaccurate fuel gauges the same way ([GM fuel gauge recall, PBS](https://www.pbs.org/newshour/nation/gm-recalls-51640-suvs-defective-fuel-gauges)).

**Not safety-critical:** infotainment, cosmetic damage, comfort and convenience problems, a driver assistance feature that only shows "unavailable," and a tire pressure warning for a slightly low tire.

**Source and how it's adapted:** the five areas follow NHTSA's published examples of safety-related problems ([NHTSA, Nov 2024](https://www.nhtsa.gov/document/motor-vehicle-safety-defects-and-recalls)). NHTSA defines defects for recalls across many vehicles; this flag judges one customer's car right now. That's why worn brake pads count here even though NHTSA treats ordinary wear as not a defect.

## Next step

Each ticket gets exactly one next step: the best first action. These options are modeled on common EV service practice, not any manufacturer's internal process.

1. **Stop driving + roadside assistance:** the car is unsafe to drive, or can't move and is stuck somewhere unsafe (such as a road shoulder). A dead car at home or in a parking lot → Dispatch mobile service.
2. **Dispatch mobile service:** a technician comes to the customer; repairs that don't need a lift (tire, 12V battery, glass, small trim).
3. **Schedule service center visit:** repairs needing a lift or major work (suspension, high-voltage battery, motors, brakes).
4. **Remote diagnosis or software fix:** checked remotely or fixed by a software update.
5. **Contact customer for more information:** not enough detail to decide.
6. **Explain to customer (no repair needed):** the car is working as designed.

**Rules:**

- Stop driving + roadside assistance is for brakes going soft, a car that is hard to control, loss of power, smoke or fire, or a car stuck somewhere unsafe. A mild ongoing safety problem where the driver still has control (a slight pull, a range display reading too high) → P1 + same-day remote diagnosis or service center visit, whichever can fix it. Exception: a taillight, brake light, or backup camera out → Schedule service center visit.
- A safety problem that has stopped but is still P1 → Schedule service center visit, same day.
- Mobile vs. service center: mobile service if the parts and tools can travel in a van; service center if the repair needs a lift or heavy equipment. Based on Tesla's public criteria (its service manual marks each procedure as mobile-capable by whether the part can be transported safely and the tools are in the van; [Tesla Service Manual](https://service.tesla.com/docs/ModelS/ServiceManual/en-us/GUID-FA4D8FAA-9481-4E2A-B98C-D51CAE717FF1.html)). Still a working assumption to validate with technicians.

## Special cases

- **Two problems in one ticket:** label the most serious one. Category, priority, and safety flag all come from it.
- **Not a vehicle problem** (rescheduling, pricing, general questions): out of scope; these tickets are not included. This eval covers vehicle problems only.
- **Not enough information to judge** ("a warning light came on"): P2, safety flag off, next step is contacting the customer for more information.
- **Accident or collision damage:** Body & cabin. Safety-critical only if driving is affected (a bent wheel, a light out, the car pulling).
- **Setting requests:** if the customer only wants to change how a working feature behaves, label it Software & infotainment, P3, safety No, next step Explain to customer. This rule never overrides safety rules: if the feature failed or acted unexpectedly (brake hold won't release, the car rolled), it is a fault, and the normal category and safety rules apply.
- **Two categories honestly fit:** record the second in `alt_category`; the model gets credit for either. Use sparingly.

## How the labels are scored

| Metric | Question it answers |
| --- | --- |
| Accuracy | How often the model matches the label, reported separately for category, priority, and next step (alt_category also counts for category) |
| Safety recall | Of the truly safety-critical tickets, how many the model flagged. Reported as X of Y. |
| False alarm rate | Of the tickets that are not safety-critical, how many the model wrongly flagged. A model that flags everything is noisy, not safe. |
| Cost | Cost per ticket at each model's published paid price |
| Latency | Seconds per ticket |

The AI is strict about flagging; a human advisor decides how to handle the customer.

## Decision log

Every judgment call, newest first.

| Date | Decision | Why |
| --- | --- | --- |
| Oct 28, 2026 | After the first run, three labels corrected where both models disagreed and guide v1 supports the change: T-007 next step roadside → service center; T-008 P2 → P3; T-010 alt_category Electrical (12V) added. T-017 kept. The guide itself was not changed. | T-007's label predated the mild-safety rule; T-008 failed the three-question test; T-010 sits between the collision and light rules. Scores are reported against both keys. |
| Oct 26, 2026 | Guide frozen as version 1 after the 30-ticket pilot | In the last batch, 3 of 4 label differences involved rules added the previous day; rules were changing faster than they could be applied |
| Oct 26, 2026 | A problem that can lead to a safety failure is safety-critical; roadside only for problems that make the car unsafe to keep driving; mild ongoing safety problems get same-day remote diagnosis or service center (from T-021, T-023) | A range display reading too high can strand the driver, as with inaccurate fuel gauges; a tow is too much for a slight pull |
| Oct 25, 2026 | Backup camera out → safety Yes, but P2 and service center, like lights. False alarm rate added to the metrics. | NHTSA lists it; drivers can still use mirrors. A model shouldn't score well on safety by flagging everything. |
| Oct 25, 2026 | Roadside only when the car is unsafe or stuck somewhere unsafe; dead car at home → mobile service. Wipers that stop moving → Electrical (12V); worn blades → Body & cabin (from T-015, T-020). | A dead 12V battery at home isn't dangerous; label wipers by likely cause |
| Oct 25, 2026 | Setting requests → Software & infotainment, only when the feature works as designed (from T-002) | Any failure follows the safety rules |
| Oct 25, 2026 | Taillight or brake light out → safety Yes, but P2 and service center (from T-010) | Towing a car for a broken taillight is too much; the light still matters to the driver behind |
| Oct 23, 2026 | Two problems → label the most serious; non-vehicle tickets out of scope; too little information → P2 and contact customer; collision damage → Body & cabin | Settle common cases before labeling |
| Oct 23, 2026 | Tire pressure warning → safety-critical only if flat or losing air quickly | A slightly low tire doesn't make the car unsafe to drive |
| Oct 23, 2026 | Driver assistance acting unexpectedly → safety-critical; only "unavailable" → not | The driver can still drive normally when a feature is off |
| Oct 23, 2026 | Worn brake pads → safety-critical | One car's worn brakes are dangerous, even though NHTSA doesn't call wear a defect |
| Oct 23, 2026 | One headlight out → safety-critical | NHTSA lists loss of lighting |
| Oct 23, 2026 | Safety-critical definition based on NHTSA's examples, five areas | A public, citable source rather than guesswork |
| Oct 23, 2026 | Customer tone doesn't change priority | Label by facts; also a good trick case for testing the AI |
| Oct 23, 2026 | Safety problem that stopped: brakes, steering, loss of power, fire risk → P1; others → P2 | Some intermittent risks can wait a few days; these four can't |
| Oct 23, 2026 | Stranded but safe customer → P1 | A stranded customer needs same-day help; keeps priority distinct from the safety flag |
| Oct 23, 2026 | Ongoing safety-critical → always P1 | No dangerous ticket should wait |
| Oct 23, 2026 | Noise only under acceleration → Battery & drive; noise that changes with speed while coasting → Chassis | Coasting takes the motor out of the picture, so the noise must come from wheels or suspension |
| Oct 23, 2026 | Range drop with heater → Battery & drive | It's a range concern; usually expected behavior, so the next step is explaining it |
| Oct 23, 2026 | Climate unresponsive due to frozen screen → Software; air won't heat or cool → Body & cabin | Label by cause: screen problem vs. climate hardware |
| Oct 23, 2026 | Single headlight out → Electrical (12V) | Consistent with exterior lights already listed there |
| Oct 23, 2026 | Won't charge + car dead → Electrical (12V); app schedule fails → Software | The car not waking, or the app, is the cause, not the charging hardware |
| Oct 23, 2026 | Tie-breaker: label by cause; if unclear, by symptom | Cause routes the ticket to the right technician skill set |
| Oct 21, 2026 | Phone-key unlock failure → Software & infotainment | The lock works; the digital key is the failing part |
| Oct 21, 2026 | Climate control → Body & cabin | No separate bucket after cutting to 8 categories |
| Oct 21, 2026 | Emergency braking problems → Driver assistance | Usually a sensor problem, not brake hardware |
| Oct 21, 2026 | "Won't wake up" → Electrical (12V) | Most often a low-voltage power problem |
| Oct 21, 2026 | Motors added to battery bucket ("High-voltage battery & drive") | Propulsion had no home; kept the count at 8 |
| Oct 21, 2026 | Cut from 12 to 8 categories | About 15 tickets per category at 120 tickets; danger is tracked by a separate safety flag |
| Oct 21, 2026 | Removed Noise / vibration; added Other / Unclear | Noise is a symptom that overlaps every system; Unclear avoids forced guesses |

---

## Cheat sheet

Decide in this order: safety first, because it drives priority and next step. Unsure on any ticket? Mark **?**.

### 1. Safety-critical?

**Yes:** steering, brakes (including worn pads), a flat or fast-leaking tire, cracked wheel, broken suspension · loss of power while driving · burning smell, smoke, overheating · wipers, any headlight, taillight or brake light, backup camera · airbags, seat belts, seats that won't lock · driver assistance acting unexpectedly · anything that can lead to these (a range display reading too high).

**No:** infotainment, cosmetic, comfort, a feature showing "unavailable," a slightly low tire.

### 2. Priority

| Level | Use when |
| --- | --- |
| P1 | Ongoing safety problem · customer stranded · a stopped problem in brakes, steering, loss of power, or fire risk |
| P2 | Taillight, brake light, or backup camera out · other safety problems that stopped · seriously limits use (can't charge at home) · could get worse (leak, louder noise) · not enough information |
| P3 | Comfort, cosmetic, convenience, settings, expected behavior |

Ignore the customer's tone. "URGENT!!!" doesn't change the level.

### 3. Next step

| Situation | Next step |
| --- | --- |
| Brakes going soft, hard to control, loss of power, smoke or fire, or stuck somewhere unsafe | Stop driving + roadside assistance |
| Problem stopped but still P1 · mild ongoing safety problem, driver still in control (slight pull) · taillight, brake light, or backup camera out · needs a lift or heavy equipment | Schedule service center visit |
| Parts and tools fit in a van · dead car at home or in a parking lot | Dispatch mobile service |
| Screen, app, or software (same day if safety-critical, such as a range display reading too high) | Remote diagnosis or software fix |
| Not enough information | Contact customer for more information |
| Working as designed | Explain to customer (no repair needed) |

### 4. Category

Label by the most likely cause; if the cause is unclear, by the symptom. Two problems in one ticket → label the more serious one. A setting request is Software only if the feature works; if it failed, use the safety rules.

| If the ticket says… | Category |
| --- | --- |
| Home charging fails but public chargers work · charge port or cable | Charging |
| Range drop (including in cold or with the heater) · battery warning · lost power · noise only under power | High-voltage battery & drive |
| Noise while coasting · pulling · vibration · brakes, tires, wheels | Chassis |
| Screen frozen · app · phone key · Bluetooth · maps · wants to change a setting | Software & infotainment |
| Lane-keep · adaptive cruise · emergency braking · parking sensors | Driver assistance |
| Won't wake up · dead car · any light out · wipers stop moving | Electrical (12V) |
| Doors, paint, leaks, seats, seat heater, worn wiper blades · air won't heat or cool · collision damage | Body & cabin |
| Doesn't point to any system | Other / Unclear |
