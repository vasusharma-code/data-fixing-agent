import pandas as pd
import openai  # or any other LLM provider
from utils.helpers import log_action

class EnrichmentAgent:
    def __init__(self, log_file="data/logs/enrichment_log.txt"):
        self.log_file = log_file
        # Initialize LLM API (you'll need to set up your API key)
        openai.api_key = 'your-api-key'  # Replace with actual API key

    def enrich_data(self, df):
        """Enrich the data with additional information"""
        df = self._enrich_missing_emails(df)
        df = self._add_customer_segment(df)
        log_action(self.log_file, "Data enrichment completed")
        return df

    def _enrich_missing_emails(self, df):
        """Generate plausible emails for invalid/missing emails"""
        invalid_mask = (df['email_status'] == 'invalid') | (df['email'].str.startswith('UNKNOWN_EMAIL'))
        
        for idx in df[invalid_mask].index:
            name = df.at[idx, 'name']
            if pd.notna(name):
                # Simple email generation (in a real scenario, you might use an LLM)
                first, *last = name.lower().split()
                domain = "example.com"  # Default domain
                email = f"{first}.{''.join(last)}@{domain}" if last else f"{first}@{domain}"
                df.at[idx, 'email'] = email
                df.at[idx, 'email_status'] = 'generated'
                log_action(self.log_file, f"Generated email for row {idx}: {email}")
        
        return df

    def _add_customer_segment(self, df):
        """Add customer segmentation based on age"""
        def get_segment(age):
            if pd.isna(age):
                return 'unknown'
            age = int(age)
            if age < 18: return 'teen'
            if age < 30: return 'young_adult'
            if age < 50: return 'adult'
            return 'senior'
        
        df['segment'] = df['age'].apply(get_segment)
        log_action(self.log_file, "Added customer segmentation")
        return df

    def _call_llm(self, prompt):
        """Helper method to call LLM for complex enrichment"""
        try:
            response = openai.Completion.create(
                engine="text-davinci-003",
                prompt=prompt,
                max_tokens=50,
                temperature=0.7
            )
            return response.choices[0].text.strip()
        except Exception as e:
            log_action(self.log_file, f"LLM call failed: {str(e)}")
            return None