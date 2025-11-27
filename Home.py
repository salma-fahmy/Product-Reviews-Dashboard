import streamlit as st
import pandas as pd

# رابط CSV مباشر من Dropbox
url = "https://www.dropbox.com/scl/fi/wx0fsu580mfl0kjcaub2f/cleaned_reviews.csv?dl=1"

# قراءة CSV
df = pd.read_csv(url)

# عرض أسماء الأعمدة
st.write("أسماء الأعمدة في الملف:")
st.write(df.columns.tolist())
