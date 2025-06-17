import pandas as pd
import argparse
from pathlib import Path

class UIAgent:
    def __init__(self):
        self.parser = argparse.ArgumentParser(description="Data Cleaning System")
        self._setup_arguments()

    def _setup_arguments(self):
        self.parser.add_argument('--input', type=str, required=True, help='Path to input CSV file')
        self.parser.add_argument('--output', type=str, default='data/output/cleaned_data.csv', 
                               help='Path to save cleaned CSV file')
        self.parser.add_argument('--show', action='store_true', help='Show cleaned data preview')

    def run(self):
        args = self.parser.parse_args()
        
        # Validate input file
        input_path = Path(args.input)
        if not input_path.exists():
            print(f"Error: Input file {args.input} not found!")
            return
        
        return {
            'input_path': input_path,
            'output_path': Path(args.output),
            'show_preview': args.show
        }

    def display_preview(self, df):
        """Display a preview of the cleaned data"""
        print("\nCleaned Data Preview:")
        print(df.head())
        print("\nData Summary:")
        print(df.info())

    def display_success(self, output_path):
        """Display success message"""
        print(f"\nData cleaning completed successfully!")
        print(f"Cleaned data saved to: {output_path}")