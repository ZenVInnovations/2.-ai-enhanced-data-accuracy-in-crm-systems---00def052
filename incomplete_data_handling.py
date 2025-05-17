import pandas as pd

def identify_missing_values(df):
    """Identify missing values in the DataFrame."""
    missing_counts = df.isnull().sum()
    total_cells = df.size
    missing_percentage = (missing_counts / total_cells) * 100
    missing_info = pd.DataFrame({'Missing Count': missing_counts, 'Missing Percentage': missing_percentage})
    return missing_info[missing_info['Missing Count'] > 0].sort_values(by='Missing Percentage', ascending=False)

def handle_missing_values(df, strategy='drop', columns=None, fill_value=None):
    """Handle missing values based on the specified strategy."""
    df_copy = df.copy()
    if strategy == 'drop':
        if columns:
            #  Check if all columns exist before dropping.
            valid_columns = [col for col in columns if col in df_copy.columns]
            if valid_columns:
                df_copy.dropna(subset=valid_columns, inplace=True)
            else:
                print("Warning: None of the specified columns exist in the DataFrame.")
        else:
            df_copy.dropna(inplace=True)
    elif strategy == 'fill':
        if columns and fill_value is not None:
             #  Check if all columns exist before filling.
            valid_columns = [col for col in columns if col in df_copy.columns]
            if valid_columns:
                df_copy[valid_columns] = df_copy[valid_columns].fillna(fill_value)
            else:
                print("Warning: None of the specified columns exist in the DataFrame.")
        elif fill_value is not None:
            df_copy.fillna(fill_value, inplace=True)
        else:
            print("Warning: Fill value not provided for 'fill' strategy.")
    elif strategy == 'impute_mean' and columns:
        for col in columns:
            if col in df_copy.columns: # Check if the column exists
                if pd.api.types.is_numeric_dtype(df_copy[col]):
                    df_copy[col].fillna(df_copy[col].mean(), inplace=True)
                else:
                    print(f"Warning: Cannot impute mean for non-numeric column '{col}'.")
            else:
                 print(f"Warning: Column '{col}' not found in DataFrame.")
    elif strategy == 'impute_median' and columns:
        for col in columns:
            if col in df_copy.columns: # Check if the column exists
                if pd.api.types.is_numeric_dtype(df_copy[col]):
                    df_copy[col].fillna(df_copy[col].median(), inplace=True)
                else:
                    print(f"Warning: Cannot impute median for non-numeric column '{col}'.")
            else:
                print(f"Warning: Column '{col}' not found in DataFrame.")
    else:
        print("Warning: Invalid missing value handling strategy.")
    return df_copy

def analyze_incomplete_data(cleaned_df):
    """Analyze and handle incomplete data."""
    print("Missing Value Analysis:")
    missing_info = identify_missing_values(cleaned_df)
    print(missing_info)

    # Example of handling missing phone numbers by dropping rows
    df_dropped_phone = handle_missing_values(cleaned_df, strategy='drop', columns=['Phone', 'Contact'])
    print("\nData after dropping rows with missing phone numbers:")
    print(df_dropped_phone.head())

    # Example of filling missing cities with a default value
    df_filled_city = handle_missing_values(cleaned_df, strategy='fill', columns=['City', 'Location'], fill_value='Unknown')
    print("\nData after filling missing cities/locations:")
    print(df_filled_city.head())

if __name__ == "__main__":
    # Create a sample DataFrame with missing values for demonstration
    data = {'Name': ['John Doe', 'Jane Smith', 'Peter Jones', None, 'Alice Brown'],
            'Email': ['john.doe@example.com', None, 'peter.j@example.com', 'test@example.com', 'alice.b@sample.com'],
            'Phone': ['123-456-7890', '987-654-3210', None, '111-222-3333', None],
            'City': ['New York', 'Los Angeles', 'London', None, 'Paris']}
    sample_df = pd.DataFrame(data)
    analyze_incomplete_data(sample_df)
