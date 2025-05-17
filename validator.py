import re
import pandas as pd

def validate_data(df):
    """Validate cleaned data and return only valid rows"""
    errors = []
    valid_df = df.copy()
    
    # Email validation
    if 'email' in valid_df.columns:
        email_regex = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        invalid_emails = valid_df[~valid_df['email'].astype(str).str.match(email_regex, na=False)]
        if not invalid_emails.empty:
            errors.append(f"❌ {len(invalid_emails)} invalid email(s) removed")
            valid_df = valid_df[valid_df['email'].astype(str).str.match(email_regex, na=False)]
    
    # Phone validation
    if 'phone' in valid_df.columns:
        phone_regex = r'^[0-9]{3}-[0-9]{4}$'
        invalid_phones = valid_df[~valid_df['phone'].astype(str).str.match(phone_regex, na=False)]
        if not invalid_phones.empty:
            errors.append(f"❌ {len(invalid_phones)} invalid phone(s) removed")
            valid_df = valid_df[valid_df['phone'].astype(str).str.match(phone_regex, na=False)]
    
    # Required fields check
    required_fields = ['name', 'email']
    for field in required_fields:
        if field in valid_df.columns and valid_df[field].isnull().any():
            missing_count = valid_df[field].isnull().sum()
            errors.append(f"❌ {missing_count} missing value(s) in {field} removed")
            valid_df = valid_df.dropna(subset=[field])
    
    return {
        "is_valid": len(errors) == 0,
        "errors": errors,
        "valid_rows": len(valid_df),
        "valid_df": valid_df  # Return the filtered DataFrame
    }