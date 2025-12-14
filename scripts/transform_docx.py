from rich import print as rprint
from rich import inspect
import json
import re
from datetime import datetime
from pathlib import Path
from docx import Document
from datetime import datetime
import os
import unicodedata


folder_prepped = Path("data/raw/prepped")
originals_dir = Path("data/raw/original")
processing_log = Path("data/logs/processing_log.json")

def get_filenames():
    filenames = []
    for file in originals_dir.iterdir():
        file = file.name
        filenames.append(file)
    # print(filenames)
    return filenames

get_filenames()

# def read_entries(filename):


# Step 1: Read the Word file

# Open the docx file
# Loop through tables and rows (same as before)
# Extract the text from each cell

# Step 2: Clean the text during extraction

# Remove the "!" marker if it exists at the start
# Replace all typographic quotation marks („ " " ") with single quotes (')
# Normalize whitespace (newlines → spaces, multiple spaces → single)

# Step 3: Extract metadata from the text

# Find and extract price (using your existing regex patterns)
# Remove the price from the text after extracting it
# Determine topic from filename (your existing normalization logic)

# Step 4: Store each entry temporarily

# Create a dictionary for each entry with: text, price, topic, topic_normalised
# Add all entries to a list

# Step 5: Cleanup pass - filter out unwanted entries

# Loop through your list of entries
# Identify entries that start with "Siehe" or other reference patterns
# Either remove them or flag them (you need to decide which)
