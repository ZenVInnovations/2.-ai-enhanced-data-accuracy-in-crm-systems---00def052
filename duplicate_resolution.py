import pandas as pd

def merge_duplicate_records(group, merge_strategy='first_valid'):
    """Merges duplicate records based on a defined strategy.

    Args:
        group (pd.DataFrame): A DataFrame containing duplicate records.
        merge_strategy (str): The strategy to use for merging. Options:
            - 'first_valid': Prioritize the first non-missing value in each column.
            - 'most_frequent': Use the most frequent value in each column (for categorical data).
            - 'concatenate': Concatenate string values (separated by '; ').
            - 'average': Calculate the average for numeric columns.
            - 'min': Use the minimum value for numeric columns.
            - 'max': Use the maximum value for numeric columns.
            You can extend this with more sophisticated strategies.

    Returns:
        pd.Series: A Series representing the merged record.
    """
    merged_record = {}
    for col in group.columns:
        if merge_strategy == 'first_valid':
            first_valid = group[col].dropna().iloc[0] if not group[col].isnull().all() else None
            merged_record[col] = first_valid
        elif merge_strategy == 'most_frequent':
            if group[col].dtype == 'object':
                mode = group[col].mode()
                merged_record[col] = mode.iloc[0] if not mode.empty else None
            else:
                merged_record[col] = group[col].dropna().iloc[0] if not group[col].isnull().all() else None
        elif merge_strategy == 'concatenate':
            string_values = group[col].astype(str).str.strip().replace('nan', '').tolist()
            unique_non_empty = list(set([val for val in string_values if val]))
            merged_record[col] = '; '.join(unique_non_empty) if unique_non_empty else None
        elif merge_strategy == 'average':
            numeric_values = group[col].dropna()
            merged_record[col] = numeric_values.mean() if not numeric_values.empty else None
        elif merge_strategy == 'min':
            numeric_values = group[col].dropna()
            merged_record[col] = numeric_values.min() if not numeric_values.empty else None
        elif merge_strategy == 'max':
            numeric_values = group[col].dropna()
            merged_record[col] = numeric_values.max() if not numeric_values.empty else None
        else:
            # Default to first valid if strategy is not recognized
            first_valid = group[col].dropna().iloc[0] if not group[col].isnull().all() else None
            merged_record[col] = first_valid
    return pd.Series(merged_record)

def resolve_duplicates(df, duplicate_groups, merge_strategy='first_valid', index_column=None):
    """Resolves identified duplicates in the DataFrame.

    Args:
        df (pd.DataFrame): The original DataFrame.
        duplicate_groups (pd.DataFrameGroupBy): A DataFrameGroupBy object where each group
            represents a set of duplicate records (e.g., output of identify_duplicate_groups).
        merge_strategy (str): The strategy to use for merging duplicates (passed to merge_duplicate_records).
        index_column (str, optional): The name of a unique identifier column in your DataFrame.
            If provided, this column will be preserved for the merged record (using the first value).
            Defaults to None.

    Returns:
        pd.DataFrame: A new DataFrame with duplicate records resolved (merged).
    """
    merged_records = []
    original_indices_to_drop = set()

    for _, group in duplicate_groups:
        if len(group) > 1:
            merged = merge_duplicate_records(group.drop(columns=[index_column] if index_column in group.columns else [], errors='ignore'), merge_strategy=merge_strategy)
            if index_column in group.columns:
                merged[index_column] = group[index_column].iloc[0] # Preserve the index of the first record
            merged_records.append(merged)
            original_indices_to_drop.update(group.index[1:]) # Keep the first occurrence's index
        else:
            # If only one record in the group, keep it as is
            merged_records.append(group.iloc[0])

    resolved_df = pd.DataFrame(merged_records)
    return resolved_df.reset_index(drop=True)

def identify_duplicate_groups(df, keys, keep=False):
    """Identifies groups of potential duplicates based on specified keys.

    Args:
        df (pd.DataFrame): The DataFrame to check for duplicates.
        keys (list): A list of column names to consider for identifying duplicates.
        keep (bool or str, default False): Determines which duplicate(s) to mark.
            - False: Mark all duplicates as True.
            - 'first': Mark duplicates as True except for the first occurrence.
            - 'last': Mark duplicates as True except for the last occurrence.

    Returns:
        pd.DataFrameGroupBy: A DataFrameGroupBy object where each group represents
        a set of duplicate records.
    """
    duplicate_df = df[df.duplicated(subset=keys, keep=keep)].sort_values(by=keys)
    return df.groupby(keys)

if __name__ == "__main__":
    # Sample data with identified duplicates
    data = {'CustomerID': [1, 2, 3, 4, 5, 6, 7, 8, 4],
            'Name': ['John Doe', 'Jane Smith', 'Peter Jones', 'John D.', 'Alice Brown', 'Jane S.', 'Peter J.', 'Charlie Green', 'John Doe'],
            'Email': ['john.doe@example.com', 'jane.smith@example.com', 'peter.j@example.com', 'john.doe@example.com', 'alice.b@sample.com', 'jane.smith@example.com', 'peter.jones@example.com', 'charlie.g@test.org', 'john.doe@example.com'],
            'Phone': ['123-456-7890', '987-654-3210', '555-123-4567', '111-222-3333', '444-555-6666', '777-888-9999', '666-777-8888', '222-333-4444', '123-456-7890'],
            'City': ['New York', 'Los Angeles', 'London', 'New York', 'Paris', 'LA', 'London', 'Tokyo', 'NY'],
            'Country': ['USA', 'USA', 'UK', 'USA', 'France', 'USA', 'UK', 'Japan', 'USA'],
            'OrderCount': [5, 10, 3, 7, 2, 12, 4, 9, 6]}
    df = pd.DataFrame(data)

    # Clean the data (as done in data_cleaning.py)
    def standardize_text(text):
        if isinstance(text, str):
            return text.lower().strip()
        return text
    df['Name_cleaned'] = df['Name'].apply(standardize_text)
    df['Email_cleaned'] = df['Email'].apply(standardize_text)
    df['City_cleaned'] = df['City'].apply(standardize_text)

    # Identify duplicate groups based on cleaned Name and Email
    duplicate_groups = identify_duplicate_groups(df, keys=['Name_cleaned', 'Email_cleaned'])

    print("Original DataFrame:")
    print(df)
    print("\nDuplicate Groups (based on cleaned Name and Email):")
    for name, group in duplicate_groups:
        if len(group) > 1:
            print(f"\nGroup: {name}")
            print(group)

    # Resolve duplicates using 'first_valid' strategy
    resolved_df_first_valid = resolve_duplicates(df.copy(), duplicate_groups, merge_strategy='first_valid', index_column='CustomerID')
    print("\nDataFrame after resolving duplicates (first_valid):")
    print(resolved_df_first_valid)

    # Resolve duplicates using 'concatenate' strategy for City and Country
    def merge_concatenate(group):
        merged = pd.Series()
        for col in group.columns:
            if group[col].dtype == 'object':
                string_values = group[col].astype(str).str.strip().replace('nan', '').tolist()
                unique_non_empty = list(set([val for val in string_values if val]))
                merged[col] = '; '.join(unique_non_empty) if unique_non_empty else None
            elif pd.api.types.is_numeric_dtype(group[col]):
                merged[col] = group[col].dropna().iloc[0] if not group[col].isnull().all() else None
            else:
                merged[col] = group[col].dropna().iloc[0] if not group[col].isnull().all() else None
        return merged

    def resolve_duplicates_custom(df, duplicate_groups, index_column=None):
        merged_records = []
        for _, group in duplicate_groups:
            if len(group) > 1:
                merged = merge_concatenate(group.drop(columns=[index_column] if index_column in group.columns else [], errors='ignore'))
                if index_column in group.columns:
                    merged[index_column] = group[index_column].iloc[0]
                merged_records.append(merged)
            else:
                merged_records.append(group.iloc[0])
        return pd.DataFrame(merged_records).reset_index(drop=True)

    duplicate_groups_all = identify_duplicate_groups(df.copy(), keys=['Name_cleaned', 'Email_cleaned'])
    resolved_df_custom = resolve_duplicates_custom(df.copy(), duplicate_groups_all, index_column='CustomerID')
    print("\nDataFrame after resolving duplicates (custom concatenate for City/Country):")
    print(resolved_df_custom)