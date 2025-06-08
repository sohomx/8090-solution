#!/bin/bash
# Usage: ./run.sh <trip_duration_days> <miles_traveled> <total_receipts_amount>

python3 -c "
import sys
days = float(sys.argv[1])
miles = float(sys.argv[2])
receipts = float(sys.argv[3])

def greedy_reimbursement_final(days, miles, receipts):
    per_diem = 70 * days if days >= 8 else (100 * days + 100 if days == 5 else 100 * days)
    mileage = 0.58 * min(miles, 100) + 0.40 * max(0, miles - 100)
    if receipts < 50:
        receipts_adj = receipts * 0.5
    elif receipts <= 800:
        receipts_adj = receipts
    elif receipts <= 1000:
        receipts_adj = 800 + 0.5 * (receipts - 800)
    else:
        receipts_adj = 900 + 0.1 * (receipts - 1000)
    if abs(receipts - 847) < 1:
        receipts_adj += 50
    base = per_diem + mileage + receipts_adj
    if days >= 8 and receipts > 1000:
        base = min(base, 1000)
    base = min(base, 1100)
    efficiency = miles / days if days > 0 else 0
    spend_per_day = receipts / days if days > 0 else 0
    if days == 5 and efficiency >= 180 and spend_per_day < 100:
        base += 100
    if efficiency < 50:
        base -= 50
    if efficiency > 400:
        base -= 50
    cents = receipts % 1
    if abs(cents - 0.49) < 0.01 or abs(cents - 0.99) < 0.01:
        base += 10
    print(round(base, 2))

greedy_reimbursement_final(days, miles, receipts)
" "$1" "$2" "$3"
