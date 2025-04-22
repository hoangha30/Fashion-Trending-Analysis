#!/usr/bin/env python3
"""
pinterest_scrape.py

A script to download images from URLs stored in a CSV file.

Edit the constants below to point to your CSV file and adjust settings:
    CSV_FILE       - Path to the CSV containing image URLs
    URL_COLUMN     - Name of the column with image URLs
    OUTPUT_DIR     - Directory to save downloaded images
    DOWNLOAD_LIMIT - Maximum number of images to download (None for no limit)

Requirements:
    - Python 3.x
    - requests

"""
import os
import csv
import requests
from urllib.parse import urlparse

# ---------------------- USER CONFIGURATION ----------------------
CSV_FILE = './Metadata/pinterest_merged.csv'
URL_COLUMN = 'hCL src'
OUTPUT_DIR = './pinterest_img'
DOWNLOAD_LIMIT = None  # e.g., 50, or None for all
# ---------------------------------------------------------------

def download_image(url, folder):
    """Downloads a single image to the specified folder."""
    try:
        response = requests.get(url, stream=True)
        response.raise_for_status()
        filename = os.path.basename(urlparse(url).path)
        path = os.path.join(folder, filename)
        with open(path, 'wb') as f:
            for chunk in response.iter_content(1024):
                f.write(chunk)
        print(f"Downloaded: {filename}")
    except Exception as e:
        print(f"Failed to download {url}: {e}")


def main():
    # Prepare output directory
    os.makedirs(OUTPUT_DIR, exist_ok=True)

    # Read URLs from CSV
    print(f"Reading URLs from {CSV_FILE}...")
    urls = []
    with open(CSV_FILE, newline='', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        if URL_COLUMN not in reader.fieldnames:
            raise ValueError(f"Column '{URL_COLUMN}' not found in CSV file.")
        for row in reader:
            url = row.get(URL_COLUMN)
            if url:
                urls.append(url)

    total = len(urls)
    print(f"Found {total} URLs.")

    # Apply download limit
    if DOWNLOAD_LIMIT is not None:
        urls = urls[:DOWNLOAD_LIMIT]

    # Download images
    for idx, url in enumerate(urls, 1):
        print(f"[{idx}/{len(urls)}] Downloading {url}")
        download_image(url, OUTPUT_DIR)

    print("Done!")

if __name__ == '__main__':
    main()
