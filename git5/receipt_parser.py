#receipt_parser.py

import json
import re

with open("raw.txt", "r", encoding="utf-8") as file:
    text = file.read()


# Extract prices
price_pattern = r'\b\d+\.\d{2}\b'
prices = re.findall(price_pattern, text)

# convert prices to float
prices = [float(p) for p in prices]


# Extract product names
# assumes format: ProductName PRICE
product_pattern = r'([A-Za-z ]+)\s+\d+\.\d{2}'
products = re.findall(product_pattern, text)

# clean product names
products = [p.strip() for p in products]


# Extract date and time
datetime_pattern = r'\d{4}-\d{2}-\d{2}\s+\d{2}:\d{2}'
datetime_match = re.search(datetime_pattern, text)

datetime_value = datetime_match.group() if datetime_match else None


# Extract payment method
payment_pattern = r'Payment Method:\s*(.+)'
payment_match = re.search(payment_pattern, text)

payment_method = payment_match.group(1) if payment_match else None

total = sum(prices)




data = {
    "products": products,
    "prices": prices,
    "total_calculated": total,
    "date_time": datetime_value,
    "payment_method": payment_method
}

print(json.dumps(data, indent=4))