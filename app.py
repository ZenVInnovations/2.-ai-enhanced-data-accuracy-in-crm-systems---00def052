import pandas as pd
import numpy as np
from sklearn.impute import KNNImputer
from sklearn.ensemble import IsolationForest
import re

# Load CRM data
def load_crm_data(filepath):
    try:
        df = pd.read_csv(filepath)
        print("Data loaded successfully.")
        return df
    except Exception as e:
        print(f"Error loading file: {e}")
        return pd.DataFrame()

# Basic data validation
def validate_email(email):
    pattern = r"^[\w\.-]+@[\w\.-]+\.\w+$"
    return bool(re.match(pattern, str(email)))

def validate_phone(phone):
    return str(phone).isdigit() and (7 <= len(str(phone)) <= 15)

def clean_and_validate_data(df):
    df['valid_email'] = df['email'].apply(validate_email)
    df['valid_phone'] = df['phone'].apply(validate_phone)
    return df

# Handle missing values
def impute_missing_data(df):
    numeric_cols = df.select_dtypes(include=[np.number]).columns
    imputer = KNNImputer(n_neighbors=3)
    df[numeric_cols] = imputer.fit_transform(df[numeric_cols])
    return df

# Detect anomalies using Isolation Forest
def detect_anomalies(df, contamination=0.01):
    model = IsolationForest(contamination=contamination, random_state=42)
    numeric_cols = df.select_dtypes(include=[np.number]).columns
    df['anomaly'] = model.fit_predict(df[numeric_cols])
    return df

# Save clean data
def save_clean_data(df, output_path):
    df.to_csv(output_path.replace('.xlsx', '.csv'), index=False)
    print(f"Clean data saved to {output_path}")

# Full pipeline
def run_pipeline(input_path, output_path):
    df = load_crm_data(input_path)
    if df.empty:
        return
    df = clean_and_validate_data(df)
    df = impute_missing_data(df)
    df = detect_anomalies(df)
    save_clean_data(df, output_path)

if __name__ == "__main__":
    input_file = "crm_customers.csv"      #input data 
    output_file = "crm_cleaned.csv"       #output data 
    run_pipeline(input_file, output_file)

