import os
import streamlit as st
import pandas as pd
import nltk
nltk.download('punkt')
nltk.download('punkt\_tab')
from utils.data\_loader import NLP\_analysis
from utils.processor import clean\_topics, summarize\_text

st.set\_page\_config(page\_title="Climate Articles Analyzer", layout="wide")
st.title("🌎 Climate Articles Analyzer (From Precomputed Results)")

df = NLP\_analysis()
selected\_article = st.sidebar.selectbox("📄 Select an article", df\['filename'])
article\_row = df\[df\['filename'] == selected\_article].iloc\[0]

# Summary settings

st.sidebar.subheader("⚙️ Summary Settings")
num\_sentences = st.sidebar.slider("Summary sentences", min\_value=3, max\_value=15, value=5, step=1)

st.subheader(f"📰 {selected\_article}")

# Show summarized text

st.subheader("📄 Article Summary")
summary = summarize\_text(article\_row\['article'], num\_sentences=num\_sentences)
st.write(summary)

# Option to read full article

with st.expander("🔍 Read full article"):
st.write(article\_row\['article'])

# Sentiment analysis

st.subheader("💬 Sentiment Analysis")
col1, col2, col3 = st.columns(3)
col1.metric("Sentiment", article\_row\['sentiment'])
col2.metric("Polarity", f"{article\_row\['polarity']:.2f}")
col3.metric("Subjectivity", f"{article\_row\['subjectivity']:.2f}")

# Named entities

st.subheader("🏷️ Named Entities")
if article\_row\['named\_entities']:
with st.expander("Show named entities"):
entities = article\_row\['named\_entities'].split(', ')
for entity in entities:
st.write(f"- {entity}")
else:
st.write("No named entities detected.")

# Topics

st.subheader("📌 Topics (Global Across All Articles)")
with st.expander("Show topics summary"):
cleaned\_topics = clean\_topics(article\_row\['topics'])
for topic\_name, keywords in cleaned\_topics:
st.markdown(f"**{topic\_name}** → {', '.join(\[f'`{kw}`' for kw in keywords])}")


