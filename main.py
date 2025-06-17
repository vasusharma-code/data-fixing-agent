import pandas as pd
from agents.detection_agent import DetectionAgent
from agents.correction_agent import CorrectionAgent
from agents.enrichment_agent import EnrichmentAgent
from agents.ui_agent import UIAgent

def main():
    # Initialize agents
    ui_agent = UIAgent()
    config = ui_agent.run()
    
    # Load data
    try:
        df = pd.read_csv(config['input_path'])
    except Exception as e:
        print(f"Error loading CSV file: {e}")
        return
    
    # Initialize agents
    detection_agent = DetectionAgent()
    correction_agent = CorrectionAgent()
    enrichment_agent = EnrichmentAgent()
    
    # Run pipeline
    print("Starting data cleaning pipeline...")
    
    # Step 1: Detection
    print("\nRunning Detection Agent...")
    issues = detection_agent.detect_issues(df)
    
    # Step 2: Correction
    print("Running Correction Agent...")
    corrected_df = correction_agent.correct_issues(df, issues)
    
    # Step 3: Enrichment
    print("Running Enrichment Agent...")
    enriched_df = enrichment_agent.enrich_data(corrected_df)
    
    # Save results
    output_path = config['output_path']
    output_path.parent.mkdir(parents=True, exist_ok=True)
    enriched_df.to_csv(output_path, index=False)
    
    # Show preview if requested
    if config['show_preview']:
        ui_agent.display_preview(enriched_df)
    
    ui_agent.display_success(output_path)

if __name__ == "__main__":
    main()