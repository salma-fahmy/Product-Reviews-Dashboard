import streamlit as st
import pandas as pd

url = "https://www.dropbox.com/scl/fi/wx0fsu580mfl0kjcaub2f/cleaned_reviews.csv?dl=1"

try:
    df = pd.read_csv(
        url,
        engine='python',      # محرك أكثر مرونة
        quotechar='"',        # للتعامل مع علامات الاقتباس
        error_bad_lines=False, # تجاهل الصفوف المشكلة
        warn_bad_lines=True    # طباعة تحذير للصفوف اللي تم تجاهلها
    )
    st.write("أسماء الأعمدة في الملف:")
    st.write(df.columns.tolist())
except Exception as e:
    st.error(f"حدث خطأ أثناء قراءة الملف: {e}")
