import csv
import re

files = [
    'data/daily_sales_data_0.csv',
    'data/daily_sales_data_1.csv',
    'data/daily_sales_data_2.csv',
]

output_rows = []

for f in files:
    with open(f, newline='', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            if row['product'].strip().lower() == 'pink morsel':
                price = float(re.sub(r'[^\d.]', '', row['price']))
                quantity = int(row['quantity'])
                sales = price * quantity
                output_rows.append({
                    'sales': f"${sales:.2f}",
                    'date': row['date'].strip(),
                    'region': row['region'].strip()
                })

with open('output.csv', 'w', newline='') as out:
    writer = csv.DictWriter(out, fieldnames=['sales', 'date', 'region'])
    writer.writeheader()
    writer.writerows(output_rows)

print(f"Done! {len(output_rows)} rows written to output.csv")