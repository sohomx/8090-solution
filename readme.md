MIT License

Copyright (c) 2024 [Your Name or Username]

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.


# Black Box Reimbursement Challenge – Solution

## Overview

This repository contains my solution for the **Black Box Reimbursement Challenge**.  
The goal: predict reimbursement amounts for trips using only provided features (`trip_duration_days`, `miles_traveled`, `total_receipts_amount`), by reverse-engineering the logic of an unknown reimbursement system.

- **Public cases:** Used for rule discovery (`public_cases.json`)
- **Private cases:** Blind test set (`private_cases.json`)
- **Submission:** Your predictions (`submission.csv`)

---

## How To Run

1. **Install requirements**
    ```sh
    pip install -r requirements.txt
    ```

2. **Generate predictions**
    ```sh
    python predict.py
    ```
    - This script reads `private_cases.json` and outputs `submission.csv`.

3. **Submission format:**  
   `submission.csv` should look like:
    ```
    case_id,prediction
    0,XXX.XX
    1,YYY.YY
    ...
    ```

---

## Approach

**Summary:**  
- Analyze public data & interviews, look for repeated formulas and exception patterns.
- Iteratively construct a rule-based formula to match the black box system.
- Manually review outliers and patch logic for "magic numbers," hard caps, and bonus/penalty cases.
- Apply hard system caps and clear rules to avoid overfitting.

Core logic is in [`predict.py`](predict.py).  
For detailed exploration, see [`visualize_fit.ipynb`](visualize_fit.ipynb).

---

## Files

| File                          | Description                                 |
|-------------------------------|---------------------------------------------|
| `predict.py`                  | Main script for generating predictions      |
| `submission.csv`              | Final output for submission                 |
| `private_cases.json`          | (Do not include if not allowed)             |
| `public_cases.json`           | Public data                                 |
| `requirements.txt`            | Dependencies                                |
| `README.md`                   | This file                                   |
| `rules_cheat_sheet.md`        | (Optional) Notes from challenge             |
| `PRD.md` / `INTERVIEWS.md`    | (Optional) Background docs                  |
| `visualize_fit.ipynb`         | (Optional) Analysis and rule development    |

---

## Key Rules Discovered

- **Per-diem:** $100/day (plus bonuses/penalties for certain trip lengths)
- **Mileage:** $0.58 per mile (first 100 mi), $0.40 after that
- **Receipts:** Piecewise, capped; diminishing returns above thresholds
- **Long trip penalty:** Hard cap for 8+ day trips with high receipts
- **"Magic numbers":** Rounding bug for .49/.99 receipts, etc
- **Efficiency bonus:** For "sweet spot" trips (5d, 180+ miles, sub-$100/day)
- **Hard cap:** $1,100 system-wide

---

## Usage Notes

- `submission.csv` can be uploaded directly for leaderboard evaluation.
- To sanity-check your predictions, run `predict.py` on `public_cases.json` and compare against known outputs.

---

## Notes

- All business rules were reverse-engineered from provided data and documentation.
- Exception logic was only added for repeatable, justified patterns—not overfitted.
- For full EDA and rule derivation, see `visualize_fit.ipynb` and the CSVs under phase6.

