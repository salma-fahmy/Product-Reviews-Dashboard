# ------------------------- Product Reviews Dashboard -------------------------
import streamlit as st
import pandas as pd
import plotly.express as px
import warnings
import requests
from io import StringIO

warnings.filterwarnings('ignore')

# ------------------------- Page Config & CSS -------------------------
st.set_page_config(page_title="Product Reviews Dashboard", layout="wide", page_icon=":bar_chart:")

st.markdown("""
    <style>
        div.block-container { padding-top: 1rem; }
        .stat-card {
            border: 2px solid rgba(160, 160, 160, 0.3);
            border-radius: 15px;
            padding: 20px;
            text-align: center;
            background-color: rgba(200, 200, 200, 0.2);
            box-shadow: 2px 2px 10px rgba(0,0,0,0.05);
        }
        .stat-value {
            font-size: 36px;
            font-weight: bold;
            color: #674FEE;
        }
        .custom-hr {
            border: none;
            height: 2px;
            background: linear-gradient(to right, #F7418F, #FFCBCB, #3AA6B9);
            margin: 40px 0;
            border-radius: 5px;
        }
    </style>
""", unsafe_allow_html=True)

st.markdown("""
    <div style="display: flex; align-items: center; justify-content: center;">
        <h1 style="font-family: 'Courier New', Courier, monospace; font-weight: bold; font-size: 60px;">Product Reviews Dashboard</h1>
    </div>
""", unsafe_allow_html=True)

# ------------------------- Load Data -------------------------
# Dropbox direct download link (تأكد من dl=1)
url = "https://www.dropbox.com/s/wx0fsu580mfl0kjcaub2f/cleaned_reviews.csv?dl=1"

try:
    response = requests.get(url)
    response.raise_for_status()
    # التأكد إن الملف CSV صالح
    if "Time" in response.text.splitlines()[0]:
        data = StringIO(response.text)
        df = pd.read_csv(data)
    else:
        st.error("⚠️ The file content is not a valid CSV.")
        st.stop()
except Exception as e:
    st.error(f"⚠️ Failed to load CSV file: {e}")
    st.stop()

# Convert Time to datetime & extract Year, Month, Day
df['Time'] = pd.to_datetime(df['Time'])
df['Year'] = df['Time'].dt.year
df['Month'] = df['Time'].dt.month
df['Day'] = df['Time'].dt.day

# ------------------------- Sidebar -------------------------
st.sidebar.image("shopping.png", width=200)
st.sidebar.header("Choose your filters:")

years = sorted(df['Year'].unique())
start_years = years[:-1]
end_years = years

col1, col2 = st.sidebar.columns(2)
with col1:
    start_year = st.selectbox("Start Year", start_years, index=0)
with col2:
    end_year = st.selectbox("End Year", end_years, index=len(end_years)-1)

if start_year > end_year:
    st.sidebar.warning("⚠️ Start year must be less than or equal to end year.")
    st.stop()

filtered_df = df[(df['Year'] >= start_year) & (df['Year'] <= end_year)]

scores = sorted(df['Score'].unique())
selected_scores = st.sidebar.multiselect("Select Score(s)", scores)
if selected_scores:
    filtered_df = filtered_df[filtered_df['Score'].isin(selected_scores)]

# ------------------------- KPI Cards -------------------------
total_products = filtered_df['ProductId'].nunique()
total_users = filtered_df['UserId'].nunique()
total_reviews = filtered_df.shape[0]

col1, col2, col3 = st.columns(3)
with col1:
    st.markdown("<h3 style='text-align:center;font-size:20px;font-family:\"Courier New\";'>Total Products</h3>", unsafe_allow_html=True)
    st.markdown(f"<div class='stat-card'><div class='stat-value'>{total_products}</div></div>", unsafe_allow_html=True)
with col2:
    st.markdown("<h3 style='text-align:center;font-size:20px;font-family:\"Courier New\";'>Total Users</h3>", unsafe_allow_html=True)
    st.markdown(f"<div class='stat-card'><div class='stat-value'>{total_users}</div></div>", unsafe_allow_html=True)
with col3:
    st.markdown("<h3 style='text-align:center;font-size:20px;font-family:\"Courier New\";'>Total Reviews</h3>", unsafe_allow_html=True)
    st.markdown(f"<div class='stat-card'><div class='stat-value'>{total_reviews}</div></div>", unsafe_allow_html=True)

st.markdown('<hr class="custom-hr">', unsafe_allow_html=True)

# ------------------------- Sentiment Trend & Donuts for Diverse Users -------------------------
col1, col2 = st.columns([2, 1])  

with col1:
    diverse_filtered = filtered_df[filtered_df['Behavior'] == 'Diverse']
    if diverse_filtered.empty:
        st.info("No Diverse users found for the selected filters.")
    else:
        yearly_sentiment = (
            diverse_filtered
            .groupby('Year')['Sentiment']
            .value_counts(normalize=True)
            .unstack()
            .fillna(0)
            .reset_index()
        )
        yearly_sentiment['Year'] = yearly_sentiment['Year'].astype(int)

        y_columns = [col for col in ['positive','negative','neutral'] if col in yearly_sentiment.columns and yearly_sentiment[col].sum() > 0]

        st.markdown("<h3 style='text-align:center;font-size:20px;font-family:\"Courier New\";'>Sentiment Trend of Diverse Users Over Years</h3>", unsafe_allow_html=True)

        sentiment_colors = {'positive': '#674FEE', 'negative': 'red', 'neutral': 'gray'}
        fig_diverse = px.line(yearly_sentiment, x='Year', y=y_columns, markers=True, labels={'value':'Fraction of Reviews','variable':'Sentiment'}, color_discrete_map=sentiment_colors)
        fig_diverse.update_traces(line=dict(width=2), marker=dict(size=6))
        fig_diverse.update_yaxes(range=[0, 1])
        fig_diverse.update_xaxes(dtick=1)
        fig_diverse.update_layout(height=350, margin=dict(l=10,r=10,t=10,b=10))
        st.plotly_chart(fig_diverse, use_container_width=True)

with col2:
    st.markdown("<h3 style='text-align: center; font-size: 20px; font-family: \"Courier New\", Times, serif;'>Customer Sentiment</h3>", unsafe_allow_html=True)
    sentiment_counts = filtered_df['Sentiment'].value_counts()
    sentiment_colors = {'positive': '#674FEE', 'negative': "#C50101", 'neutral': "#A5A8A8"}
    fig_sentiment = px.pie(values=sentiment_counts.values, names=sentiment_counts.index, hole=0.6, color=sentiment_counts.index, color_discrete_map=sentiment_colors)
    fig_sentiment.update_traces(textinfo='percent', textfont_size=12)
    fig_sentiment.update_layout(height=130, margin=dict(l=5,r=5,t=6,b=5))
    st.plotly_chart(fig_sentiment, use_container_width=True, key="sentiment_donut")

    st.markdown("<h3 style='text-align: center; font-size: 20px; font-family: \"Courier New\", Times, serif;'>Customer Behavior</h3>", unsafe_allow_html=True)
    behavior_counts = filtered_df['Behavior'].value_counts()
    behavior_colors_list = ['#674FEE', "#3223FA", "#C50101", "#A5A8A8"]
    behavior_colors = {behavior_counts.index[i]: behavior_colors_list[i] for i in range(len(behavior_counts))}
    fig_behavior = px.pie(values=behavior_counts.values, names=behavior_counts.index, hole=0.6, color=behavior_counts.index, color_discrete_map=behavior_colors)
    fig_behavior.update_traces(textinfo='percent', textfont_size=12)
    fig_behavior.update_layout(height=130, margin=dict(l=5,r=5,t=6,b=5))
    st.plotly_chart(fig_behavior, use_container_width=True, key="behavior_donut")

st.markdown('<hr class="custom-hr">', unsafe_allow_html=True)

# ------------------------- باقي الكود يظل كما هو -------------------------
# يمكن إضافة باقي الكود كما في نسختك السابقة دون أي تعديل
