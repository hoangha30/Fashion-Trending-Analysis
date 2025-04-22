#!/usr/bin/env python3
"""
csv_merger.py

A script to merge multiple CSV files containing a specific column (e.g., image URLs) into one CSV.

Edit the constants below:
    INPUT_CSV_FILES - List of CSV file paths to merge
    OUTPUT_CSV      - Path to the merged output CSV file
    KEY_COLUMN      - Column name to include from each file

Requirements:
    - Python 3.x

This script:
 1. Reads each CSV in INPUT_CSV_FILES.
 2. Checks for KEY_COLUMN; skips files missing it.
 3. Aggregates all rows with UNIQUE values in KEY_COLUMN.
 4. Writes the merged unique rows to OUTPUT_CSV.
"""
import os
import csv

# ---------------------- USER CONFIGURATION ----------------------
INPUT_CSV_FILES = [
    '/Users/hanguyen/Downloads/pinterest.csv',
    '/Users/hanguyen/Downloads/pinterest (1).csv',
    '/Users/hanguyen/Downloads/pinterest (2).csv',
    '/Users/hanguyen/Downloads/pinterest (3).csv',
    '/Users/hanguyen/Downloads/pinterest (4).csv'
]
OUTPUT_CSV = '/Users/hanguyen/Documents/Trending-Fashion-Analysis/Metadata/pinterest_merged.csv'
KEY_COLUMN = 'hCL src'
# ---------------------------------------------------------------

def merge_csv_files(input_files, output_file, key_column):
    """Merge multiple CSVs based on a key column, retaining unique rows."""
    seen = set()
    merged = []

    for file_path in input_files:
        if not os.path.isfile(file_path):
            print(f"Warning: '{file_path}' not found — skipping.")
            continue
        with open(file_path, newline='', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            if key_column not in reader.fieldnames:
                print(f"Warning: column '{key_column}' missing in '{file_path}' — skipping.")
                continue
            for row in reader:
                key = row[key_column]
                if key and key not in seen:
                    seen.add(key)
                    merged.append({key_column: key})

    if not merged:
        print("No valid rows to merge. Exiting.")
        return

    os.makedirs(os.path.dirname(output_file) or '.', exist_ok=True)
    with open(output_file, 'w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=[key_column])
        writer.writeheader()
        writer.writerows(merged)
    print(f"Merged {len(merged)} unique rows into '{output_file}'.")


def main():
    merge_csv_files(INPUT_CSV_FILES, OUTPUT_CSV, KEY_COLUMN)

if __name__ == '__main__':
    main()
