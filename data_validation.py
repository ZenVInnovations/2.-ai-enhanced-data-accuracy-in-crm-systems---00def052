import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import classification_report, accuracy_score
from sklearn.preprocessing import LabelEncoder

def create_label(row, valid_cities):
    """Example function to label 'City' as valid or invalid."""
    return 1 if row['City_cleaned'] in valid_cities else 0

def train_validation_model(df, column_to_validate, label_column, text_based=True):
    """Trains a supervised learning model for data validation."""
    df_cleaned = df.dropna(subset=[column_to_validate, label_column])
    X = df_cleaned[column_to_validate]
    y = df_cleaned[label_column]
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    if text_based:
        vectorizer = TfidfVectorizer(stop_words='english')
        X_train_vec = vectorizer.fit_transform(X_train)
        X_test_vec = vectorizer.transform(X_test)
        model = LogisticRegression()
        model.fit(X_train_vec, y_train)
        y_pred = model.predict(X_test_vec)
        print(f"Validation Model Performance for {column_to_validate}:")
        print(classification_report(y_test, y_pred))
        print(f"Accuracy: {accuracy_score(y_test, y_pred):.2f}")
        return model, vectorizer
    else:
        # For numerical or categorical features (requires different preprocessing)
        # Example for categorical using Label Encoding:
        encoder = LabelEncoder()
        X_train_encoded = encoder.fit_transform(X_train).reshape(-1, 1)
        X_test_encoded = encoder.transform(X_test).reshape(-1, 1)
        model = LogisticRegression()
        model.fit(X_train_encoded, y_train)
        y_pred = model.predict(X_test_encoded)
        print(f"Validation Model Performance for {column_to_validate}:")
        print(classification_report(y_test, y_pred))
        print(f"Accuracy: {accuracy_score(y_test, y_pred):.2f}")
        return model, encoder

def predict_validity(df, model, vectorizer=None, encoder=None, column_to_validate='Name_cleaned', prediction_column='is_valid'):
    """Predicts the validity of entries in a DataFrame column."""
    if vectorizer:
        X_vec = vectorizer.transform(df[column_to_validate].fillna(''))
        df[prediction_column] = model.predict(X_vec)
    elif encoder:
        X_encoded = encoder.transform(df[column_to_validate].fillna('')).reshape(-1, 1)
        df[prediction_column] = model.predict(X_encoded)
    else:
        print("Error: Vectorizer or Encoder not provided.")
    return df

if __name__ == "__main__":
    # Sample usage: You'd need a DataFrame with a pre-labeled column
    data = {'City_cleaned': ['new york', 'london', 'paris', 'new yorkk', 'berlinn'],
            'is_valid_city': [1, 1, 1, 0, 0]}  # 1 for valid, 0 for invalid
    labeled_df = pd.DataFrame(data)

    # Example of training a model to validate 'City'
    valid_cities_list = ['new york', 'london', 'paris', 'berlin']
    labeled_df['is_valid_city_manual'] = labeled_df.apply(lambda row: 1 if row['City_cleaned'] in valid_cities_list else 0, axis=1)
    city_model, city_vectorizer = train_validation_model(labeled_df, 'City_cleaned', 'is_valid_city_manual')

    # Assume you have a new DataFrame with cities to validate
    new_data = {'City_cleaned': ['tokyo', 'new york city', 'londn']}
    new_df = pd.DataFrame(new_data)
    validated_df = predict_validity(new_df, city_model, city_vectorizer, column_to_validate='City_cleaned', prediction_column='city_valid_predicted')
    print("\nValidation Predictions:")
    print(validated_df)