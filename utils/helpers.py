import re
import pandas as pd
from fuzzywuzzy import process, fuzz
from datetime import datetime

def log_action(log_file, message):
    """Log actions to a file with timestamp"""
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with open(log_file, "a") as f:
        f.write(f"[{timestamp}] {message}\n")

def validate_email(email):
    """Check if email is valid"""
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(pattern, email) is not None

def load_valid_countries(file_path):
    """Load list of valid countries from file"""
    with open(file_path, 'r') as f:
        return [line.strip() for line in f.readlines()]

def fuzzy_match_country(input_country, valid_countries, threshold=80):
    """Fuzzy match country names"""
    if pd.isna(input_country):
        return None
    match, score = process.extractOne(input_country, valid_countries, scorer=fuzz.token_set_ratio)
    return match if score >= threshold else None