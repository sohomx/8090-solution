# Black Box Reimbursement System: Rules Cheat Sheet

---

## 1. System Context & Known Unknowns

- Logic is undocumented, buggy, and only partly understood. (PRD.md:5)
- Unpredictable reimbursement, inconsistent receipt handling, strange trip-length/mileage effects, conflicting folk theories. (PRD.md:7)
- Replica must match all current quirks and bugs, not just logic. (PRD.md:23)
- Inputs: 
    - trip_duration_days (integer)
    - miles_traveled (integer)
    - total_receipts_amount (float)  
  Output: single numeric reimbursement. (PRD.md:17–19, 35)
- Output believed to use a mix of per diem, mileage, receipts, and unknown factors. (PRD.md:21)
- Employee interviews are a primary source for reconstructing rules. (PRD.md:42)

---

## Key Thresholds and Cutoffs

- **Base per diem:** $100/day (INTERVIEWS.md:107)
- **Mileage tier:** First 100 miles @ $0.58/mile, then rate drops (nonlinear curve) (INTERVIEWS.md:123, 125)
- **Receipts:**
    - $600–$800: best reimbursement (INTERVIEWS.md:145)
    - >$1000: diminishing returns (INTERVIEWS.md:141, 145)
    - <~$50 (on multi-day): penalized (INTERVIEWS.md:147, 151, 255)
    - **Worked examples:**
        - $847 receipt total: sometimes triggers an unusually good reimbursement (the "magic number") [oai_citation:0‡raw_rules_candidates.txt](file-service://file-V9SkVXZLo7VtXT97AgcYgq)
        - $1,000 receipts → $800 reimbursed (not proportional) (INTERVIEWS.md:141)
        - $1,200 receipts → $850 reimbursed (not proportional) (INTERVIEWS.md:141)
        - $2,000 in expenses can get less reimbursement than $1,200 (INTERVIEWS.md:53)
- **Spending per day by trip type:**
    - Short trip (<4d): < $75/day
    - Medium (4–6d): < $120/day
    - Long (7+d): < $90/day (INTERVIEWS.md:427)
- **Efficiency bonus:** 180–220 miles/day = max bonus (INTERVIEWS.md:415)
- **Special combos:**
    - 5 days + 180+ mi/day + <$100/day spend = guaranteed bonus (INTERVIEWS.md:489)
    - 8+ days + high spend = "vacation penalty" (INTERVIEWS.md:491)

---

## 3. Actionable If/Then Patterns

- If receipts in $600–$800, maximize reimbursement.
- If receipts > $1000, each extra dollar matters less ("soft cap").
- If receipts < $50 (multi-day), penalize.
- If trip is 5 days **and** >180 miles/day **and** <$100/day spend, grant bonus.
- If trip is 8+ days **and** high spending, apply penalty ("vacation penalty").
- If efficiency (miles/day) between 180–220, grant bonus; <180 or >220, less/no bonus.
- If low mileage/high spending, penalize; if high mileage/low spend, reward.
- If receipts end in .49 or .99, possible double rounding bug, add extra (needs data check).
- If submit no receipts, get base per diem. If submit tiny receipts, could get less than per diem (INTERVIEWS.md:255).

---

## 4. Patterns, Interactions, and Branching

- Sweet spot for trip length is 4–6 days ("best payout"); longer or shorter often worse. (INTERVIEWS.md:339)
- System likely branches calculation path based on trip type:  
    - Quick high-mileage,  
    - Long low-mileage,  
    - Medium balanced trips (INTERVIEWS.md:465, 469, 473)
- Efficiency bonus is real; 180–220 mi/day sweet spot, >400 mi/day may lose bonus ("not real business"). (INTERVIEWS.md:415, 417)
- Significant interaction effects:  
    - Trip length × efficiency  
    - Spending per day × total mileage  
    - Certain combinations trigger bonuses/penalties ("decision tree") (INTERVIEWS.md:481, 485)
- High mileage + low spending = good; low mileage + high spending = bad (INTERVIEWS.md:493)
- "Magic number": $847 receipt total sometimes gets special treatment (flagged, needs data check). (INTERVIEWS.md:77)
- Moderate daily expense ($60/day) favored; $90/day can trigger penalty. (INTERVIEWS.md:59)

---

## 5. Noise, Exceptions, and Non-coded Effects

- Rounding bug: receipts ending in .49 or .99 can trigger extra payout, possible double rounding (needs data check for exact logic). (INTERVIEWS.md:81, 181)
- Tuesday/Thursday submission day often best, Friday worst (submission day bonus/penalty—**only code if confirmed in data**). (INTERVIEWS.md:443, 447)
- Department (e.g. sales vs ops), moon phases, and user history may affect outcome, but should only be coded if a clear public data pattern exists. (INTERVIEWS.md:349, 455, 507–509)
- Employees forced to learn system quirks to optimize; "expense optimization as a game." (INTERVIEWS.md:367)
- New employees may get lower reimbursement due to lack of optimization skill. (INTERVIEWS.md:325)
- Randomness/noise: Even for same person/same trip, expect 5–10% variation. (INTERVIEWS.md:189)

---

## 6. Ambiguities and "Needs Data Check"

- Amount of 5-day bonus is unclear, needs data check.
- Value of "vacation penalty" for 8+ days with high spend: needs data check.
- Double rounding for .49/.99 receipt bug: needs data check.
- Confirm if Tuesday/Friday submission day effect exists in public_cases.json before using.
- All "combo" bonuses/penalties—quantify with actual data (public_cases.json) in Phase 2.

---

## 7. Data-Driven Next Steps

- Validate all thresholds and patterns above with public_cases.json:  
    - Visualize residuals after applying base rules  
    - Tweak/quantify ambiguous values  
    - Identify remaining edge cases/outliers for manual mapping  
- Cluster trips by days/miles/receipts and check if distinct logic emerges as interviews suggest.

---