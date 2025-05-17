import streamlit as st

# MUST be the first Streamlit command
st.set_page_config(
    page_title="AI Enhanced Data Accuracy in CRM System",
    page_icon="🧹",
    layout="wide"
)

# Now import other modules
import pandas as pd
import os
from utils.cleaner import clean_data
from utils.validator import validate_data

# Custom CSS for colorful UI
st.markdown("""
<style>
    /* Main background */
    .stApp {
        background: linear-gradient(135deg, #f5f7fa 0%, #e4e8f0 100%);
    }
    
    /* Sidebar styling */
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #4b6cb7 0%, #182848 100%) !important;
    }
    .sidebar .sidebar-content {
        color: white;
    }
    
    /* Title styling */
    h1 {
        color: #4b6cb7;
        text-shadow: 1px 1px 3px rgba(0,0,0,0.1);
    }
    
    /* Button styling */
    .stButton>button {
        background: linear-gradient(45deg, #4b6cb7, #3a56a8) !important;
        color: white !important;
        border: none;
        border-radius: 8px;
        padding: 0.5rem 1rem;
        box-shadow: 0 4px 8px rgba(0,0,0,0.1);
        transition: all 0.3s ease;
    }
    .stButton>button:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 12px rgba(0,0,0,0.15);
    }
    
    /* File uploader styling */
    [data-testid="stFileUploader"] {
        border: 2px dashed #4b6cb7 !important;
        border-radius: 12px;
        padding: 2rem;
        background: rgba(255,255,255,0.9);
    }
    
    /* Expander header */
    .streamlit-expanderHeader {
        background: linear-gradient(90deg, #4b6cb7 0%, #3a56a8 100%) !important;
        color: white !important;
        border-radius: 8px 8px 0 0 !important;
    }
    
    /* Success message */
    .stAlert.stAlert-success {
        background: rgba(75, 192, 192, 0.1) !important;
        border-left: 4px solid #4bc0c0 !important;
    }
    
    /* Error message */
    .stAlert.stAlert-error {
        background: rgba(255, 99, 132, 0.1) !important;
        border-left: 4px solid #ff6384 !important;
    }
</style>
""", unsafe_allow_html=True)

# Create data directories if they don't exist
os.makedirs("data/raw", exist_ok=True)
os.makedirs("data/cleaned", exist_ok=True)

# Colorful sidebar
with st.sidebar:
    st.markdown("""
    <h2 style='color: white;'>⚙️ Settings</h2>
    <hr style='background-color: white; height: 2px; border: none;'>
    """, unsafe_allow_html=True)
    
    processing_mode = st.radio(
        "Processing Mode",
        ["Basic Cleaning", "Advanced Cleaning"],
        help="Choose the cleaning intensity level"
    )
    
    st.markdown("""
    <hr style='background-color: white; height: 2px; border: none;'>
    <p style='color: white;'>🌈 <b>AI Enhanced Cleaning</b></p>
    <p style='color: white; font-size: small;'>Transform your messy data into clean insights!</p>
    """, unsafe_allow_html=True)

# Main Interface with colorful elements
st.markdown("""
<h1 style='border-bottom: 2px solid #4b6cb7; padding-bottom: 10px;'>
    🤖 <span style='color: #4b6cb7;'>AI Enhanced Data Accuracy in CRM System</span> ✨
</h1>
""", unsafe_allow_html=True)

st.markdown("""
<p style='font-size: large; color: #555;'>
    Upload your raw CRM data for AI-powered cleaning and validation
</p>
""", unsafe_allow_html=True)

# File Upload with colorful styling
uploaded_file = st.file_uploader(
    "📁 Drag & Drop your CRM data (CSV)",
    type=["csv"],
    accept_multiple_files=False,
    help="Upload your customer data in CSV format"
)

if uploaded_file:
    # Save uploaded file
    raw_path = os.path.join("data", "raw", uploaded_file.name)
    with open(raw_path, "wb") as f:
        f.write(uploaded_file.getbuffer())
    
    # Read data
    df = pd.read_csv(raw_path)
    
    with st.expander("🔍 View Raw Data", expanded=True):
        st.dataframe(df.style.highlight_null(color='#FFEE58'))
        st.markdown(f"""
        <p style='color: #555;'>
            📊 <b>Shape:</b> {df.shape} | 📋 <b>Columns:</b> {', '.join(df.columns)}
        </p>
        """, unsafe_allow_html=True)
    
    if st.button("✨ Clean Data", key="clean_button"):
        with st.spinner("🧼 AI is cleaning your data..."):
            # Original cleaning logic remains unchanged
            cleaned_df = clean_data(df.copy(), mode=processing_mode)
            validation_report = validate_data(cleaned_df)
            
            if 'email' in cleaned_df.columns:
                email_regex = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
                cleaned_df = cleaned_df[cleaned_df['email'].astype(str).str.match(email_regex, na=False)]
            
            if 'phone' in cleaned_df.columns:
                phone_regex = r'^[0-9]{3}-[0-9]{4}$'
                cleaned_df = cleaned_df[cleaned_df['phone'].astype(str).str.match(phone_regex, na=False)]
            
            clean_path = os.path.join("data", "cleaned", f"cleaned_{uploaded_file.name}")
            cleaned_df.to_csv(clean_path, index=False)
        
        # Show results with colorful styling
        st.balloons()
        st.success(f"✅ AI cleaning complete! Valid records: {len(cleaned_df)}/{len(df)}")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("<h3 style='color: #4b6cb7;'>🧽 Cleaned Data Preview</h3>", unsafe_allow_html=True)
            st.dataframe(cleaned_df.head().style.background_gradient(cmap='Blues'))
            
        with col2:
            st.markdown("<h3 style='color: #4b6cb7;'>📝 Validation Report</h3>", unsafe_allow_html=True)
            if validation_report["errors"]:
                for error in validation_report["errors"]:
                    st.error(f"❌ {error}")
            else:
                st.success("✔️ Perfect! No validation errors found")
        
        # Download button with styling
        st.download_button(
            label="⬇️ Download Cleaned Data",
            data=cleaned_df.to_csv(index=False),
            file_name=f"cleaned_{uploaded_file.name}",
            mime="text/csv",
            key="download_button"
        )