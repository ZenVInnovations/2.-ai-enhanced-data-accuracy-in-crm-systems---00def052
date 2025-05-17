import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from fuzzywuzzy import fuzz
from fuzzywuzzy import process
# Import the necessary function(s) from data_cleaning.py
from data_cleaning import load_and_clean_data, clean_dataframe
def find_exact_duplicates(df, columns):
    """Find exact duplicates based on specified columns."""
    return df[df.duplicated(subset=columns, keep=False)].sort_values(by=columns)
def find_fuzzy_duplicates(df, column, threshold=85, n_matches=5):
    """Find fuzzy duplicates in a single text column using fuzzywuzzy."""
    unique_values = df[column].dropna().unique()
    duplicates = []
    for val in unique_values:
        matches = process.extract(val, unique_values, scorer=fuzz.ratio, limit=n_matches)
        for match_info in matches:
            if len(match_info) >= 2:  # Ensure we have at least match and score
                match, score = match_info[:2]  # Safely get the first two
                if score >= threshold and val != match and tuple(sorted((val, match))) not in [
                    (d['value1'], d['value2']) for d in duplicates
                ]:
                    duplicates.append({'value1': val, 'value2': match, 'similarity': score})
            else:
                print(f"Warning: Unexpected match_info format: {match_info} for value: {val}")

    if not duplicates:  # Check if the list is empty
        return pd.DataFrame(columns=['value1', 'value2', 'similarity'])  # Return an empty DataFrame with the correct columns
    return pd.DataFrame(duplicates).sort_values(by='similarity', ascending=False)


def find_semantic_duplicates(df, column, threshold=0.9):
    """Find semantic duplicates in a text column using TF-IDF and cosine similarity."""
    tfidf_vectorizer = TfidfVectorizer(stop_words='english')
    tfidf_matrix = tfidf_vectorizer.fit_transform(df[column].dropna())
    cosine_similarities = cosine_similarity(tfidf_matrix)

    duplicates = []
    index_to_value = {i: v for i, v in enumerate(df[column].dropna().unique())}
    values = list(index_to_value.values())

    for i in range(cosine_similarities.shape[0]):
        for j in range(i + 1, cosine_similarities.shape[1]):
            if cosine_similarities[i, j] >= threshold:
                value1 = index_to_value[i]
                value2 = index_to_value[j]
                if tuple(sorted((value1, value2))) not in [
                    (d['value1'], d['value2']) for d in duplicates
                ]:
                    duplicates.append(
                        {'value1': value1, 'value2': value2, 'similarity': cosine_similarities[i, j]}
                    )

    return pd.DataFrame(duplicates).sort_values(by='similarity', ascending=False)


def detect_duplicates(cleaned_df):
    """Detect various types of duplicates."""
    print("Exact Duplicates (based on cleaned Name and Email):")
    exact_name_email = find_exact_duplicates(cleaned_df, ['Name_cleaned', 'Email_cleaned'])
    print(exact_name_email)

    print("\nFuzzy Duplicates in Names:")
    fuzzy_names = find_fuzzy_duplicates(cleaned_df, 'Name_cleaned', threshold=80)
    print(fuzzy_names)

    print("\nFuzzy Duplicates in Emails:")
    fuzzy_emails = find_fuzzy_duplicates(cleaned_df, 'Email_cleaned', threshold=90)
    print(fuzzy_emails)

    # Note: Semantic duplicate detection can be computationally intensive for large datasets.
    # Consider applying it to specific subsets or using more efficient techniques.
    # if 'Name_cleaned' in cleaned_df.columns:
    #     print("\nSemantic Duplicates in Names:")
    #     semantic_names = find_semantic_duplicates(cleaned_df.dropna(subset=['Name_cleaned']), 'Name_cleaned', threshold=0.8)
    #     print(semantic_names)


if __name__ == "__main__":
    file_paths = ['data/raw_crm_data_1.csv', 'data/raw_crm_data_2.csv']
    cleaned_data = load_and_clean_data(file_paths)
    detect_duplicates(cleaned_data)
