# CRM Data Cleaning Tool �✨

A Streamlit application for cleaning and validating CRM data with colorful UI enhancements.

![App Screenshot](screenshot.png) *(Add a screenshot later if you'd like)*

## Features ✨

- **Dual Cleaning Modes**:
  - Basic Cleaning (standard cleanup)
  - Advanced Cleaning (aggressive transformations) ---> ("Use this mode for better acuracy")
- **Data Validation**:
  - Email format validation
  - Phone number validation
  - Required field checks
- **Visual Enhancements**:
  - Colorful gradient UI
  - Balloon animations on success
  - Styled data previews
- **File Handling**:
  - Drag & drop CSV upload
  - Automatic directory creation
  - Cleaned data download

## Project Structure 📂
CRM_PROJ/
├── data/
│ ├── raw/ # Original uploaded files
│ └── cleaned/ # Processed clean files
├── utils/
│ ├── cleaner.py # Data cleaning functions
│ └── validator.py # Data validation functions
├── app.py # Main Streamlit application
└── requirements.txt # Dependencies

## Installation ⚙️

1. Clone the repository:
   `
   git clone https://github.com/yourusername/crm-data-cleaner.git
   cd crm-data-cleaner

2. Create and activate a virtual environment (recommended):
    python -m venv venv
    source venv/bin/activate  # Linux/Mac
    venv\Scripts\activate     # Windows

3. Install dependencies:
    pip install -r requirements.txt

Usage 🚀
1.Run the application:
    streamlit run app.py

2 In the browser:
    Upload your CRM data (CSV format)
    Select processing mode
    Click "Clean Data"
    View results and download cleaned data

# Requirements 📋
Python 3.8+
Streamlit
Pandas
FuzzyWuzzy (for advanced cleaning)

Listed in requirements.txt:
    streamlit>=1.13.0
    pandas>=1.5.0
    fuzzywuzzy>=0.18.0
    python-Levenshtein>=0.12.0

# Customization 🎨

You can easily modify:
    Color scheme in the CSS section of app.py
    Cleaning logic in utils/cleaner.py
    Validation rules in utils/validator.py

# Troubleshooting ⚠️

Common Issues:
    set_page_config() error: Ensure it's the first Streamlit command
    Import errors: Verify all dependencies are installed    
    File permission issues: Check directory write permissions

