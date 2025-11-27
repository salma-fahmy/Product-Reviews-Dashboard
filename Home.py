import streamlit as st
import pandas as pd

# رابط CSV مباشر
url = "https://www.dropbox.com/scl/fi/wx0fsu580mfl0kjcaub2f/cleaned_reviews.csv?dl=1"

# قراءة CSV
try:
    df = pd.read_csv(url)
    st.write("أسماء الأعمدة في الملف:")
    st.write(df.columns.tolist())
except Exception as e:
    st.error(f"حدث خطأ أثناء قراءة الملف: {e}")
