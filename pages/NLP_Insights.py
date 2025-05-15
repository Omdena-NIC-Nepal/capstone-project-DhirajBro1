import os
import streamlit as st
import pandas as pd
import nltk
import spacy
nltk.download('punkt')
nltk.download('punkt_tab')
nlp = spacy.load("en_core_web_sm")
from gensim import corpora, models
from utils.data_loader import NLP_analysis
from utils.processor import clean_topics, summarize_text, preprocess_for_lda
from textblob import TextBlob  # Assuming you're using TextBlob for sentiment

st.set_page_config(page_title="Climate Articles Analyzer", layout="wide")
st.title("🌎 Climate Articles Analyzer")

# Add input type selector
input_mode = st.sidebar.radio("📥 Select Input Mode", ["Preloaded Article", "Live Text Input"])

# Summary settings
st.sidebar.subheader("⚙️ Summary Settings")
num_sentences = st.sidebar.slider("Summary sentences", min_value=3, max_value=15, value=5, step=1)

if input_mode == "Preloaded Article":
    df = NLP_analysis()
    selected_article = st.sidebar.selectbox("📄 Select an article", df['filename'])
    article_row = df[df['filename'] == selected_article].iloc[0]
    article_text = article_row['article']
    st.subheader(f"📰 {selected_article}")
else:
    st.subheader("✍️ Enter Your Own Text")
    article_text = st.text_area("Type or paste your article below:", height=300)
    if not article_text.strip():
        st.warning("Please enter some text above to analyze.")
        st.stop()

# Show summarized text
st.subheader("📄 Article Summary")
with st.spinner("Generating summary..."):
    summary = summarize_text(article_text, num_sentences=num_sentences)
st.write(summary)

# Option to read full article
with st.expander("🔍 Read full article"):
    st.write(article_text)

# Sentiment analysis
st.subheader("💬 Sentiment Analysis")
blob = TextBlob(article_text)
sentiment = "Positive" if blob.sentiment.polarity > 0 else "Negative" if blob.sentiment.polarity < 0 else "Neutral"
sentiment_emoji = "😊" if blob.sentiment.polarity > 0.1 else "😠" if blob.sentiment.polarity < -0.1 else "😐"

col1, col2, col3 = st.columns(3)
col1.metric("Sentiment", f"{sentiment} {sentiment_emoji}")
col2.metric("Polarity", f"{blob.sentiment.polarity:.2f}")
col3.metric("Subjectivity", f"{blob.sentiment.subjectivity:.2f}")



# -------- Named Entities --------
st.subheader("🏷️ Named Entities")
if input_mode == "Preloaded Article":
    if article_row['named_entities']:
        with st.expander("Show named entities"):
            entities = article_row['named_entities'].split(', ')
            for entity in entities:
                st.write(f"- {entity}")
    else:
        st.write("No named entities detected.")
else:
    with st.spinner("Extracting named entities..."):
        doc = nlp(article_text)
        entities = list(set(ent.text for ent in doc.ents if ent.label_ in ["PERSON", "ORG", "GPE", "LOC", "EVENT"]))
        if entities:
            with st.expander("Show named entities"):
                for entity in entities:
                    st.write(f"- {entity}")
        else:
            st.write("No named entities detected.")

# -------- Topics --------
st.subheader("📌 Topics")
if input_mode == "Preloaded Article":
    with st.expander("Show topics summary"):
        cleaned_topics = clean_topics(article_row['topics'])
        for topic_name, keywords in cleaned_topics:
            st.markdown(f"**{topic_name}** → {', '.join([f'`{kw}`' for kw in keywords])}")
else:
    with st.spinner("Extracting topics..."):
        try:
            tokens = preprocess_for_lda(article_text)
            if tokens:
                dictionary = corpora.Dictionary([tokens])
                corpus = [dictionary.doc2bow(tokens)]
                lda_model = models.LdaModel(corpus, num_topics=3, id2word=dictionary, passes=5)
                with st.expander("Show topics summary"):
                    for idx, topic in lda_model.print_topics():
                        st.markdown(f"**Topic {idx+1}** → {topic}")
            else:
                st.write("Not enough valid words to generate topics.")
        except Exception as e:
            st.error(f"Error in topic modeling: {e}")

