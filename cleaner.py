import pandas as pd
from fuzzywuzzy import fuzz

def clean_data(df, mode="Basic Cleaning"):
    """Main data cleaning function that returns cleaned DataFrame"""
    # Create a copy to avoid modifying original
    cleaned_df = df.copy()
    
    # Basic cleaning (applied to all modes)
    cleaned_df = cleaned_df.drop_duplicates()
    cleaned_df = cleaned_df.dropna(how='all')
    
    # Standardize text columns
    text_cols = cleaned_df.select_dtypes(include='object').columns
    for col in text_cols:
        cleaned_df[col] = cleaned_df[col].str.strip()
    
    if mode == "Advanced Cleaning":
        # Advanced cleaning operations
        cleaned_df = fix_duplicates(cleaned_df)
        cleaned_df = standardize_addresses(cleaned_df)
        cleaned_df = impute_missing_values(cleaned_df)
    
    return cleaned_df

def fix_duplicates(df, threshold=85):
    """Fuzzy matching for near-duplicates"""
    to_drop = set()
    
    for i in range(len(df)):
        for j in range(i+1, len(df)):
            # Compare key fields
            similarity = fuzz.token_set_ratio(
                f"{df.iloc[i]['name']} {df.iloc[i]['email']} {df.iloc[i]['phone']}",
                f"{df.iloc[j]['name']} {df.iloc[j]['email']} {df.iloc[j]['phone']}"
            )
            if similarity >= threshold:
                to_drop.add(j)
    
    return df.drop(index=list(to_drop)).reset_index(drop=True)

def standardize_addresses(df):
    """Standardize address formats"""
    if 'address' in df.columns:
        replacements = {
            'Street': 'St',
            'Avenue': 'Ave',
            'Road': 'Rd'
        }
        for old, new in replacements.items():
            df['address'] = df['address'].str.replace(old, new)
    return df

def impute_missing_values(df):
    """Fill missing values intelligently"""
    if 'segment' in df.columns:
        df['segment'] = df['segment'].fillna('Unknown')
    return df