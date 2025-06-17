# Mini Agent-Based Data Fixing System

A lightweight agentic system for cleaning and enriching customer data with both CLI and web interfaces.

## Features

- **Detection Agent**: Identifies data issues (missing values, invalid emails, duplicates)
- **Correction Agent**: Fixes issues using rules and fuzzy matching
- **Enrichment Agent**: Adds new attributes using LLMs (optional)
- **Dual Interfaces**:
  - Command Line (CLI) for automated workflows
  - Web Interface (Streamlit) for interactive use

## Installation

### 1. Clone the repository
```bash
git clone https://github.com/vasusharma-code/data-fixing-agent
cd data-fixing-system
2. Install requirements
For CLI version only:
bash
pip install pandas fuzzywuzzy python-Levenshtein
For Web version:
bash
pip install pandas fuzzywuzzy python-Levenshtein streamlit
Optional (for LLM enrichment):
bash
pip install openai
Usage
Command Line Interface (CLI)
bash
python main.py --input data/input/messy_customers.csv --output data/output/cleaned_data.csv --show
Arguments:

--input: Path to input CSV file (required)

--output: Output path for cleaned data (default: data/output/cleaned_data.csv)

--show: Display preview of cleaned data

Web Interface
bash
streamlit run web_app.py
Then open http://localhost:8501 in your browser.


File Structure
text
data-fixing-system/
├── agents/          # Agent modules
├── data/            # Input/output data
├── utils/           # Helper functions
├── main.py          # CLI entry point
├── web_app.py       # Web interface
└── README.md
Troubleshooting
Common Issues:

FileNotFoundError:

Create required folders: mkdir -p data/{input,output,logs}

ModuleNotFoundError:

Verify installation: pip show pandas fuzzywuzzy

Reinstall requirements: pip install -r requirements.txt

Streamlit connection issues:

Check firewall settings

Try alternative port: streamlit run web_app.py --server.port 8502

For additional help, please open an issue in our GitHub repository.

text

### Key Improvements:
1. **Clearer Installation** - Separated requirements for CLI vs web
2. **Better Organization** - Added system requirements and file structure
3. **Troubleshooting** - Common issues with solutions
4. **Dual Interface Docs** - Both CLI and web instructions
5. **Modern Formatting** - Better readability with code blocks

## Demo Videos

### CLI Agent Working
[![CLI Agent Demo](https://img.youtube.com/vi/Evta7gejn8g/0.jpg)](https://www.youtube.com/watch?v=Evta7gejn8g)

### Web-Based Agent
[![Web Agent Demo](https://img.youtube.com/vi/RdJo8ayw-j4/0.jpg)](https://www.youtube.com/watch?v=RdJo8ayw-j4)
