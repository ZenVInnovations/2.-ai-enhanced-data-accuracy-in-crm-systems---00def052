import pandas as pd
import re
import os

def standardize_text(text):
    """Lowercase and remove non-alphanumeric characters."""
    if isinstance(text, str):
        return re.sub(r'[^a-zA-Z0-9\s]', '', text).lower().strip()
    return text

def standardize_phone(phone):
    """Standardize phone number format (remove non-digits)."""
    if isinstance(phone, str):
        return re.sub(r'\D+', '', phone)
    return phone

def standardize_country(country):
    """Standardize country names (basic example)."""
    if isinstance(country, str):
        return country.lower().strip()
    return country

def clean_dataframe(df):
    """Apply cleaning functions to relevant columns."""
    df['Name_cleaned'] = df['Name'].apply(standardize_text) if 'Name' in df.columns else None
    df['FullName_cleaned'] = df['FullName'].apply(standardize_text) if 'FullName' in df.columns else None
    df['Email_cleaned'] = df['Email'].apply(lambda x: x.lower().strip() if isinstance(x, str) else x) if 'Email' in df.columns else None
    df['Email Address_cleaned'] = df['Email Address'].apply(lambda x: x.lower().strip() if isinstance(x, str) else x) if 'Email Address' in df.columns else None
    df['Phone_cleaned'] = df['Phone'].apply(standardize_phone) if 'Phone' in df.columns else None
    df['Contact_cleaned'] = df['Contact'].apply(standardize_phone) if 'Contact' in df.columns else None
    df['City_cleaned'] = df['City'].apply(standardize_text) if 'City' in df.columns else None
    df['Location_cleaned'] = df['Location'].apply(standardize_text) if 'Location' in df.columns else None
    df['Country_cleaned'] = df['Country'].apply(standardize_country) if 'Country' in df.columns else None
    df['Region_cleaned'] = df['Region'].apply(standardize_country) if 'Region' in df.columns else None
    return df

def load_and_clean_data(file_paths):
    """Loads data from multiple CSV files and cleans it."""
    all_data = []
    for file_path in file_paths:
        print(f"Attempting to load file: {file_path}")  # Debugging line
        try:
            df = pd.read_csv(file_path)
            cleaned_df = clean_dataframe(df)
            all_data.append(cleaned_df)
        except FileNotFoundError:
            print(f"Error: File not found at {file_path}")
    return pd.concat(all_data, ignore_index=True)

if __name__ == "__main__":
    # Construct file paths relative to the 'src' directory
    script_dir = os.path.dirname(__file__)
    parent_dir = os.path.dirname(script_dir)
    data_dir = os.path.join(parent_dir, 'data')
    file_paths = [
        os.path.join(data_dir, 'raw_crm_data_1.csv'),
        os.path.join(data_dir, 'raw_crm_data_2.csv')
    ]
    print(f"Current working directory: {os.getcwd()}")  # Debugging line
    print(f"Constructed data directory: {data_dir}")  # Debugging line
    print(f"Constructed file paths: {file_paths}")  # Debugging line
    cleaned_data = load_and_clean_data(file_paths)
    print("Cleaned Data:")
    print(cleaned_data)