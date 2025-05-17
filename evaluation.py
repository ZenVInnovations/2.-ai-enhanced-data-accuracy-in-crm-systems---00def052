import pandas as pd

def calculate_duplicate_detection_metrics(ground_truth_duplicates, predicted_duplicates):
    """Calculates precision, recall, and F1-score for duplicate detection."""
    tp = len(set(ground_truth_duplicates) & set(predicted_duplicates))
    fp = len(set(predicted_duplicates) - set(ground_truth_duplicates))
    fn = len(set(ground_truth_duplicates) - set(predicted_duplicates))

    if tp + fp == 0:
        precision = 0
    else:
        precision = tp / (tp + fp)

    if tp + fn == 0:
        recall = 0
    else:
        recall = tp / (tp + fn)

    if precision + recall == 0:
        f1 = 0
    else:
        f1 = 2 * (precision * recall) / (precision + recall)

    return {"precision": precision, "recall": recall, "f1": f1}

def calculate_completeness(df_before, df_after, columns_to_check):
    """Calculates the improvement in completeness for specified columns."""
    missing_before = df_before[columns_to_check].isnull().sum().sum()
    total_before = df_before.size
    completeness_before = 1 - (missing_before / total_before)

    missing_after = df_after[columns_to_check].isnull().sum().sum()
    total_after = df_after.size # Assuming no rows were dropped for this metric
    completeness_after = 1 - (missing_after / total_after)

    improvement = completeness_after - completeness_before
    return {"completeness_before": completeness_before, "completeness_after": completeness_after, "improvement": improvement}

# You'll need functions to load your ground truth data and the results of your pipeline

if __name__ == "__main__":
    # Example usage (you'll need your actual ground truth and pipeline results)
    ground_truth = [('John Doe', 'john.doe@example.com'), ('Jane Smith', 'jane.smith@example.com')]
    predicted = [('John Doe', 'john.doe@example.com'), ('John D.', 'johndoe@example.com')]

    duplicate_metrics = calculate_duplicate_detection_metrics(ground_truth, predicted)
    print("Duplicate Detection Metrics:", duplicate_metrics)

    # Assume you have df_raw and df_cleaned from your pipeline
    data_raw = {'Name': ['John Doe', None, 'Jane Smith'], 'Email': ['jd@ex.com', 'a@b.com', None]}
    df_raw = pd.DataFrame(data_raw)
    data_cleaned = {'Name': ['John Doe', 'Unknown', 'Jane Smith'], 'Email': ['jd@ex.com', 'a@b.com', 'unknown@example.com']}
    df_cleaned = pd.DataFrame(data_cleaned)

    completeness_metrics = calculate_completeness(df_raw, df_cleaned, ['Name', 'Email'])
    print("\nCompleteness Metrics:", completeness_metrics)
    
#Integration: Call the functions in evaluation.py from your main.py after running your data cleaning and deduplication steps.