import pandas as pd
from utils.helpers import log_action, fuzzy_match_country, load_valid_countries

class CorrectionAgent:
    def __init__(self, log_file="data/logs/correction_log.txt"):
        self.log_file = log_file
        self.valid_countries = load_valid_countries("utils/valid_countries.txt")

    def correct_issues(self, df, issues):
        """Correct detected issues in the dataframe"""
        df = self._handle_missing_data(df, issues.get('missing_data', []))
        df = self._handle_invalid_emails(df, issues.get('invalid_emails', []))
        df = self._handle_duplicates(df, issues.get('duplicates', []))
        df = self._standardize_countries(df)
        return df

    def _handle_missing_data(self, df, missing_data):
        """Handle missing data by filling with placeholder values"""
        for col, indices in missing_data:
            if col in ['age']:
                df.loc[indices, col] = df[col].median()
            else:
                df.loc[indices, col] = f"UNKNOWN_{col.upper()}"
            log_action(self.log_file, f"Filled missing {col} at rows {indices}")
        return df

    def _handle_invalid_emails(self, df, invalid_indices):
        """Mark invalid emails for later enrichment"""
        df.loc[invalid_indices, 'email_status'] = 'invalid'
        log_action(self.log_file, f"Marked {len(invalid_indices)} invalid emails for enrichment")
        return df

    def _handle_duplicates(self, df, duplicate_indices):
        """Remove duplicate rows keeping the first occurrence"""
        if duplicate_indices:
            df = df.drop_duplicates(subset=['email'], keep='first')
            log_action(self.log_file, f"Removed {len(duplicate_indices)} duplicate rows")
        return df

    def _standardize_countries(self, df):
        """Standardize country names using fuzzy matching"""
        if 'country' in df.columns:
            df['country'] = df['country'].apply(
                lambda x: fuzzy_match_country(x, self.valid_countries) if pd.notna(x) else 'UNKNOWN_COUNTRY'
            )
            log_action(self.log_file, "Standardized country names")
        return df