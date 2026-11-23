"""
ISM2411 Lab 12 — Read a Sales CSV, Write a Cleaned Report

REFLECTION QUESTIONS
Q1: You've now completed a full ETL pipeline: read a CSV, transform the data, write a new CSV. 
How does this help in a business context?
A1: ETL processes allow automated processing of data. Data can be read from files, manipulated 
(cleansed, filtered, calculated) and then written to new files. This makes efficient, scalable 
processes. It saves time and removes human error. It means that analysts and managers can make 
decisions using clean data without spending hours manually cleaning data.

Q2: Exercise 8 showed you append mode. Think of a real business process that would benefit from an append-only log.
A2: An example of ETL processes in practice would be an ordering system in an online shop. Every 
time an order is made in this system, a new row of data is added to a transaction log file. The 
information added includes the time the order was made, the order ID, the customer and the amount. 
This provides a permanent record of when orders have been made. This data can be useful for 
compliance, debugging and knowing the status of orders at a certain point in time. As we only 
ever add to this file and never edit previous data in the file, append mode is ideal.
"""

import csv
from datetime import datetime

# EXERCISE 1: Setup
print("=" * 60)
print("EXERCISE 1: Setup")
print("=" * 60)
try:
    with open("data/sales.csv", "r") as f:
        print("✓ sales.csv found and opened successfully")
except FileNotFoundError:
    print("✗ Error: sales.csv not found in data/ folder")
print()

# EXERCISE 2: Read and print raw rows
print("=" * 60)
print("EXERCISE 2: Read and print raw rows")
print("=" * 60)
with open("data/sales.csv", "r") as f:
    reader = csv.reader(f)
    for row in reader:
        print(row)
print()

# EXERCISE 3: Skip the header
print("=" * 60)
print("EXERCISE 3: Skip the header")
print("=" * 60)
with open("data/sales.csv", "r") as f:
    reader = csv.reader(f)
    header = next(reader)
    print(f"Header: {header}")
    print("Data rows:")
    for row in reader:
        print(row)
print()

# EXERCISE 4: Compute totals
print("=" * 60)
print("EXERCISE 4: Compute totals")
print("=" * 60)
total_revenue = 0
with open("data/sales.csv", "r") as f:
    reader = csv.reader(f)
    next(reader)  # skip header
    for row in reader:
        product = row[0]
        price = float(row[1])
        quantity = int(row[2])
        revenue = price * quantity
        total_revenue += revenue
        print(f"{product}: {quantity} units × ${price:.2f} = ${revenue:.2f}")
print(f"Total revenue: ${total_revenue:.2f}")
print()

# EXERCISE 5: Filter and write
print("=" * 60)
print("EXERCISE 5: Filter and write to cleaned.csv")
print("=" * 60)
count = 0
with open("data/sales.csv", "r") as f_in:
    reader = csv.reader(f_in)
    header = next(reader)
    
    with open("data/cleaned.csv", "w", newline="") as f_out:
        writer = csv.writer(f_out)
        writer.writerow(header)
        
        for row in reader:
            product = row[0]
            price = float(row[1])
            quantity = int(row[2])
            total = price * quantity
            
            if total > 100:
                writer.writerow([product, price, quantity])
                count += 1

print(f"✓ cleaned.csv created with {count} orders > $100")
print()

# EXERCISE 6: csv.DictReader
print("=" * 60)
print("EXERCISE 6: Use csv.DictReader")
print("=" * 60)
# DictReader returns each row as a dictionary, allowing access by column name instead of index.
# csv.reader returns lists (need row[0], row[1], row[2])
# csv.DictReader returns dicts (use row["product"], row["price"], row["quantity"])
total_revenue_dict = 0
with open("data/sales.csv", "r") as f:
    reader = csv.DictReader(f)
    for row in reader:
        product = row["product"]
        price = float(row["price"])
        quantity = int(row["quantity"])
        revenue = price * quantity
        total_revenue_dict += revenue
        print(f"{product}: {quantity} units × ${price:.2f} = ${revenue:.2f}")
print(f"Total revenue (DictReader): ${total_revenue_dict:.2f}")
print()

# EXERCISE 7: Sales summary by product
print("=" * 60)
print("EXERCISE 7: Sales summary by product")
print("=" * 60)
summary = {}
with open("data/sales.csv", "r") as f:
    reader = csv.DictReader(f)
    for row in reader:
        product = row["product"]
        price = float(row["price"])
        quantity = int(row["quantity"])
        revenue = price * quantity
        
        if product in summary:
            summary[product] += revenue
        else:
            summary[product] = revenue

for product, total in summary.items():
    print(f"{product}: ${total:.2f}")
print()

# EXERCISE 8: Append mode log
print("=" * 60)
print("EXERCISE 8: Append mode log")
print("=" * 60)
timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
with open("data/run_log.txt", "a") as f:
    f.write(f"Script run at {timestamp}\n")

print(f"✓ Logged script execution to data/run_log.txt")
with open("data/run_log.txt", "r") as f:
    print("Current log contents:")
    print(f.read())