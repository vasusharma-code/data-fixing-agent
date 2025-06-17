import pandas as pd
from utils.helpers import log_action, validate_email

class DetectionAgent:
    def __init__(self, log_file="data/logs/detection_log.txt"):
        self.log_file = log_file
        self.issues = {
            'missing_data': [],
            'invalid_emails': [],
            'duplicates': [],
            'invalid_countries': []
        }

    def detect_issues(self, df):
        """Detect various data issues in the dataframe"""
        self._detect_missing_data(df)
        self._detect_invalid_emails(df)
        self._detect_duplicates(df)
        return self.issues

    def _detect_missing_data(self, df):
        """Detect missing values in required columns"""
        required_cols = ['name', 'email', 'country', 'age']
        for col in required_cols:
            missing = df[col].isna()
            if missing.any():
                indices = df[missing].index.tolist()
                self.issues['missing_data'].append((col, indices))
                log_action(self.log_file, f"Missing data detected in column '{col}' at rows: {indices}")

    def _detect_invalid_emails(self, df):
        """Detect invalid email formats"""
        if 'email' in df.columns:
            invalid_emails = df[~df['email'].apply(lambda x: validate_email(str(x)) if pd.notna(x) else False)]
            if not invalid_emails.empty:
                self.issues['invalid_emails'] = invalid_emails.index.tolist()
                log_action(self.log_file, f"Invalid emails detected at rows: {invalid_emails.index.tolist()}")

    def _detect_duplicates(self, df):
        """Detect duplicate rows based on email"""
        if 'email' in df.columns:
            duplicates = df[df.duplicated(subset=['email'], keep=False)]
            if not duplicates.empty:
                self.issues['duplicates'] = duplicates.index.tolist()
                log_action(self.log_file, f"Duplicate rows detected: {duplicates.index.tolist()}")