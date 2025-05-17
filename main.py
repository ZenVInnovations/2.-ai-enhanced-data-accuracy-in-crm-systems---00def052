from data_cleaning import load_and_clean_data
from duplicate_detection import detect_duplicates
from incomplete_data_handling import analyze_incomplete_data
import pandas as pd

if __name__ == "__main__":
    file_paths = ['data/raw_crm_data_1.csv', 'data/raw_crm_data_2.csv']
    cleaned_data = load_and_clean_data(file_paths)

    print("\n--- Duplicate Detection ---")
    detect_duplicates(cleaned_data)

    print("\n--- Incomplete Data Handling ---")
    analyze_incomplete_data(cleaned_data)

    # Further steps could involve:
    # - Saving the cleaned and deduplicated data
    # - Implementing more sophisticated AI models for data validation
    # - Generating reports