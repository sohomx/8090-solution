import pandas as pd

def greedy_reimbursement_final(days, miles, receipts):
    # --- Per diem logic ---
    if days >= 8:
        per_diem = 70 * days  # Long trip penalty
    elif days == 5:
        per_diem = 100 * days + 100  # 5-day bonus
    else:
        per_diem = 100 * days

    # --- Mileage logic (tiered) ---
    mileage = 0.58 * min(miles, 100) + 0.40 * max(0, miles - 100)

    # --- Receipts logic (piecewise, capped, with magic numbers) ---
    if receipts < 50:
        receipts_adj = receipts * 0.5
    elif receipts <= 800:
        receipts_adj = receipts
    elif receipts <= 1000:
        receipts_adj = 800 + 0.5 * (receipts - 800)
    else:
        receipts_adj = 900 + 0.1 * (receipts - 1000)

    # --- Magic number bonus ---
    if abs(receipts - 847) < 1:
        receipts_adj += 50

    # --- Vacation penalty for long trips with high spend ---
    base = per_diem + mileage + receipts_adj
    if days >= 8 and receipts > 1000:
        base = min(base, 1000)

    # --- Hard system-wide absolute cap ---
    base = min(base, 1100)

    # --- Efficiency Bonus (sweet spot combo) ---
    efficiency = miles / days if days > 0 else 0
    spend_per_day = receipts / days if days > 0 else 0
    if days == 5 and efficiency >= 180 and spend_per_day < 100:
        base += 100

    # --- Efficiency penalty: low miles/day or high miles/day ---
    if efficiency < 50:
        base -= 50
    if efficiency > 400:
        base -= 50

    # --- Rounding bug (receipts end with .49 or .99) ---
    cents = receipts % 1
    if abs(cents - 0.49) < 0.01 or abs(cents - 0.99) < 0.01:
        base += 10

    return round(base, 2)

if __name__ == "__main__":
    # 1. Load input cases (private_cases.json)
    df = pd.read_json('private_cases.json')

    # 2. If case_id exists, use it. If not, create it.
    if 'case_id' in df.columns:
        case_ids = df['case_id']
    else:
        case_ids = range(len(df))

    # 3. Run predictions
    preds = []
    for i, row in df.iterrows():
        pred = greedy_reimbursement_final(
            row['trip_duration_days'],
            row['miles_traveled'],
            row['total_receipts_amount']
        )
        preds.append(pred)

    # 4. Save the file (case_id, prediction)
    out_df = pd.DataFrame({
        'case_id': case_ids,
        'prediction': preds
    })
    out_df.to_csv('submission.csv', index=False)
    print("Saved submission.csv with predictions.")
