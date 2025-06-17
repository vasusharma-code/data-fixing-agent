import streamlit as st
import pandas as pd
from agents.detection_agent import DetectionAgent
from agents.correction_agent import CorrectionAgent
from agents.enrichment_agent import EnrichmentAgent
from utils.helpers import log_action
from pathlib import Path
import time
import os

# Set page config
st.set_page_config(page_title="Data Cleaning System", layout="wide")

# Initialize directories
Path("data/logs").mkdir(parents=True, exist_ok=True)
Path("data/output").mkdir(parents=True, exist_ok=True)

# Sidebar for file upload
st.sidebar.title("Data Cleaning System")
uploaded_file = st.sidebar.file_uploader("Upload CSV file", type=["csv"])

# Main app
st.title("Automated Data Cleaning Pipeline")

if uploaded_file:
    # Load data
    df = pd.read_csv(uploaded_file)
    
    # Show original data
    with st.expander("Original Data Preview"):
        st.dataframe(df)
        st.write(f"Shape: {df.shape}")

    # Initialize agents
    detection_agent = DetectionAgent()
    correction_agent = CorrectionAgent()
    enrichment_agent = EnrichmentAgent()

    # Create tabs
    tab1, tab2, tab3, tab4 = st.tabs([
        "Detection", 
        "Correction", 
        "Enrichment", 
        "Final Result"
    ])

    with tab1:
        st.subheader("Data Issues Detection")
        if st.button("Run Detection"):
            with st.spinner("Detecting issues..."):
                issues = detection_agent.detect_issues(df)
                st.session_state.issues = issues
                time.sleep(1)  # For better UX
            
            st.success("Detection completed!")
            
            # Display issues
            st.write("### Detected Issues")
            for issue_type, details in issues.items():
                if details:  # Only show if issues found
                    st.write(f"**{issue_type.replace('_', ' ').title()}**")
                    if isinstance(details, list):
                        st.write(f"Rows affected: {len(details)}")
                    elif isinstance(details, dict):
                        st.json(details)
                    st.write("---")

    with tab2:
        st.subheader("Data Correction")
        if 'issues' in st.session_state:
            if st.button("Run Correction"):
                with st.spinner("Correcting data..."):
                    corrected_df = correction_agent.correct_issues(df.copy(), st.session_state.issues)
                    st.session_state.corrected_df = corrected_df
                    time.sleep(1)
                
                st.success("Correction completed!")
                st.dataframe(corrected_df)
        else:
            st.warning("Please run detection first")

    with tab3:
        st.subheader("Data Enrichment")
        if 'corrected_df' in st.session_state:
            if st.button("Run Enrichment"):
                with st.spinner("Enriching data..."):
                    enriched_df = enrichment_agent.enrich_data(st.session_state.corrected_df.copy())
                    st.session_state.enriched_df = enriched_df
                    time.sleep(1)
                
                st.success("Enrichment completed!")
                st.dataframe(enriched_df)
        else:
            st.warning("Please run correction first")

    with tab4:
        st.subheader("Final Result")
        if 'enriched_df' in st.session_state:
            st.dataframe(st.session_state.enriched_df)
            
            # Download button
            csv = st.session_state.enriched_df.to_csv(index=False).encode('utf-8')
            st.download_button(
                label="Download cleaned data",
                data=csv,
                file_name="cleaned_data.csv",
                mime="text/csv"
            )
            
            # Show logs
            with st.expander("View Logs"):
                if os.path.exists("data/logs/detection_log.txt"):
                    st.write("**Detection Log**")
                    st.code(open("data/logs/detection_log.txt").read())
                
                if os.path.exists("data/logs/correction_log.txt"):
                    st.write("**Correction Log**")
                    st.code(open("data/logs/correction_log.txt").read())
                
                if os.path.exists("data/logs/enrichment_log.txt"):
                    st.write("**Enrichment Log**")
                    st.code(open("data/logs/enrichment_log.txt").read())
        else:
            st.warning("Please complete all previous steps")

else:
    st.info("Please upload a CSV file to begin")