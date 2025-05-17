import os
import streamlit as st
import pandas as pd
import nltk
import spacy
nltk.download('punkt')
nltk.download('punkt_tab')
nltk.download('stopwords')
from nltk.corpus import stopwords
nlp = spacy.load("en_core_web_sm")
from gensim import corpora, models
from nltk.tokenize import word_tokenize
import re
from utils.data_loader import NLP_analysis
from utils.processor import clean_topics, summarize_text, preprocess_for_lda
from textblob import TextBlob
from langdetect import detect, DetectorFactory
DetectorFactory.seed = 0  

st.set_page_config(page_title="Climate Articles Analyzer", layout="wide")
st.title("🌎 Climate Articles Analyzer")

# Add input type selector
input_mode = st.sidebar.radio("📥 Select Input Mode", ["Preloaded Article", "Live Text Input","Language Prediction"])


if input_mode == "Preloaded Article":
    df = NLP_analysis()
    selected_article = st.sidebar.selectbox("📄 Select an article", df['filename'])
    article_row = df[df['filename'] == selected_article].iloc[0]
    article_text = article_row['article']
    st.subheader(f"📰 {selected_article}")
    # Summary settings
    st.sidebar.subheader("⚙️ Summary Settings")
    num_sentences = st.sidebar.slider("Summary sentences", min_value=3, max_value=15, value=5, step=1)
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
elif input_mode == "Live Text Input":
    article_text = st.text_area("✍️ Paste your article text here", height=300)
    st.button("Analyse")
    if not article_text.strip():
        st.warning("Please paste your text above to see analysis.")
        st.stop()
    # Summary settings
    st.sidebar.subheader("⚙️ Summary Settings")
    num_sentences = st.sidebar.slider("Summary sentences", min_value=3, max_value=15, value=5, step=1)
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
else:
    st.subheader("🌐 Language Predicton")
    article_text = st.text_area("✍️ Enter text in any language", height=300)
    st.button("Predict Language")
    if article_text.strip():
        try:
            lang_code = detect(article_text)
            language_names = {
                'en': 'English', 'ne': 'Nepali', 'fr': 'French',
                'es': 'Spanish', 'de': 'German', 'zh-cn': 'Chinese', 'ja': 'Japanese'
            }
            lang_display = language_names.get(lang_code, f"Unknown ({lang_code})")
            st.success(f"✅ Detected Language: **{lang_display}**")
        except Exception as e:
            st.error(f"Language Predicton failed: {e}")
    else:
        st.info("Please enter some text above to detect its language.")



# -------- Named Entities --------

if input_mode == "Preloaded Article":
    st.subheader("🏷️ Named Entities")
    if article_row['named_entities']:
        with st.expander("Show named entities"):
            entities = article_row['named_entities'].split(', ')
            for entity in entities:
                st.write(f"- {entity}")
    else:
        st.write("No named entities detected.")
elif input_mode == "Live Text Input":
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

if input_mode == "Preloaded Article":
    st.subheader("📌 Topics")
    with st.expander("Show topics summary"):
        cleaned_topics = clean_topics(article_row['topics'])
        for topic_name, keywords in cleaned_topics:
            st.markdown(f"**{topic_name}** → {', '.join([f'`{kw}`' for kw in keywords])}")
elif input_mode == "Live Text Input":
    if article_text.strip():
        with st.spinner("Extracting topics..."):
            try:
                # Preprocessing
                text_cleaned = re.sub(r'\W+', ' ', article_text.lower())
                tokens = word_tokenize(text_cleaned)
                tokens = [t for t in tokens if t not in stopwords.words('english') and len(t) > 2]

                if tokens:
                    dictionary = corpora.Dictionary([tokens])
                    corpus = [dictionary.doc2bow(tokens)]
                    lda_model = models.LdaModel(corpus, num_topics=3, id2word=dictionary, passes=5)

                    # Convert to your topic string format
                    topic_string = ""
                    for idx, topic in lda_model.print_topics():
                        topic_words = re.findall(r'"(.*?)"', topic)
                        topic_string += f"Topic {idx+1}: " + ", ".join([f'"{w}"' for w in topic_words]) + "; "

                    # Use your clean_topics function
                    cleaned = clean_topics(topic_string)
                    with st.expander("Show topics summary"):
                        for topic_name, keywords in cleaned:
                            st.markdown(f"**{topic_name}** → {', '.join([f'`{kw}`' for kw in keywords])}")
                else:
                    st.write("Not enough valid words to generate topics.")
            except Exception as e:
                st.error(f"Topic modeling error: {e}")
    else:
        st.warning("Please enter article text for analysis.")
