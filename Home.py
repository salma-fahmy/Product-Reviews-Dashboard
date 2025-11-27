import streamlit as st
import pandas as pd

# رابط مباشر للملف
url = "https://www.dropbox.com/scl/fi/wx0fsu580mfl0kjcaub2f/cleaned_reviews.csv?dl=1"

try:
    # قراءة الملف مع التجربة بفاصل تلقائي وحل مشاكل الترميز
    df = pd.read_csv(url, sep=None, engine='python', encoding='utf-8')
    st.write("أسماء الأعمدة في الملف:")
    st.write(df.columns.tolist())
except Exception as e:
    st.error(f"حدث خطأ أثناء قراءة الملف: {e}")
