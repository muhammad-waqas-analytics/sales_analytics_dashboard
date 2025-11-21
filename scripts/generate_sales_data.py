#!/usr/bin/env python3
"""Generate a synthetic sales_data_1000.csv file with 1000 rows.

Regions: Punjab, KPK, Balochistan, Sindh
Products: Shirts, Pants, T-Shirts, Jeans (match existing file)
Unit prices follow realistic ranges per product; quantities are random.
"""
import csv
import random
from datetime import datetime, timedelta

OUT_PATH = "./SALES_ANALYTICS_DASHBOARD/Data/sales_data_1000.csv"
NUM_ROWS = 1000

regions = ["Punjab", "KPK", "Balochistan", "Sindh"]
products = ["Shirts", "Pants", "T-Shirts", "Jeans"]

# price ranges per product (min, max)
price_ranges = {
    "Shirts": (700, 900),
    "Pants": (1000, 1300),
    "T-Shirts": (400, 600),
    "Jeans": (1800, 2200),
}

def random_date(start_year=2025):
    start = datetime(start_year, 1, 1)
    end = datetime(start_year, 12, 31)
    delta = end - start
    random_days = random.randint(0, delta.days)
    return (start + timedelta(days=random_days)).date().isoformat()

def gen_row():
    date = random_date()
    region = random.choice(regions)
    product = random.choice(products)
    qty = random.randint(1, 50)
    # choose a unit price inside the product range, rounded to nearest 10
    low, high = price_ranges[product]
    unit_price = random.randrange(low, high+1, 10)
    total = qty * unit_price
    return [date, region, product, qty, unit_price, total]

def main():
    with open(OUT_PATH, "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["Date", "Region", "Product", "Quantity", "Unit_Price", "Total"])
        for _ in range(NUM_ROWS):
            writer.writerow(gen_row())

    print(f"Generated {NUM_ROWS} rows -> {OUT_PATH}")

if __name__ == "__main__":
    main()
