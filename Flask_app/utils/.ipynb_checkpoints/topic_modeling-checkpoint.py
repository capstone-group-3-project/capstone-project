# topic_modeling.py

import pandas as pd
import nltk
import gensim
from nltk.corpus import stopwords
from gensim import corpora, models
import re
from wordcloud import WordCloud
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import seaborn as sns
from gensim.models import CoherenceModel
import os
from sklearn.feature_extraction.text import TfidfVectorizer
import numpy as np
from textblob import TextBlob
from flask import current_app, session

nltk.download('stopwords')
nltk.download('wordnet')

def preprocess_text(text):
    text = re.sub(r'[^a-zA-Z]', ' ', text)
    text = text.lower()
    stop_words = set(stopwords.words('english')) | {'br'}
    words = text.split()
    words = [word for word in words if word not in stop_words]
    lemmatizer = nltk.WordNetLemmatizer()
    words = [lemmatizer.lemmatize(word) for word in words]
    return " ".join(words)

def run_topic_modeling(file_path):
    df = pd.read_csv(file_path, sep='\t', on_bad_lines='skip', usecols=['review_body'], nrows=1000)
    df = df.dropna()
    df['cleaned_review'] = df['review_body'].apply(preprocess_text)

    text_data = [text.split() for text in df['cleaned_review']]
    dictionary = corpora.Dictionary(text_data)
    corpus = [dictionary.doc2bow(text) for text in text_data]

    # Get settings from session or use default values
    num_topics = session.get('num_topics', 5)
    num_passes = session.get('num_passes', 10)
    num_words = session.get('num_words', 4)

    ldamodel = models.LdaModel(corpus, num_topics=num_topics, id2word=dictionary, passes=num_passes)
    topics = ldamodel.print_topics(num_words=num_words)
    
    visualizations = generate_visualizations(ldamodel, corpus, dictionary, text_data, num_topics)
    
    return topics, visualizations

def generate_visualizations(ldamodel, corpus, dictionary, text_data, num_topics):
    visualizations = []
    
    img_dir = 'static/images'
    os.makedirs(img_dir, exist_ok=True)
    
    for i in range(num_topics):
        topic_words = dict(ldamodel.show_topic(i, 200))
        wordcloud = WordCloud(width=400, height=400,
                              background_color='white',
                              stopwords=stopwords.words('english'),
                              min_font_size=10).generate_from_frequencies(topic_words)
        
        plt.figure(figsize=(5, 5))
        plt.imshow(wordcloud, interpolation='bilinear')
        plt.axis("off")
        plt.title(f"Topic {i}")
        img_path = f'{img_dir}/wordcloud_topic_{i}.png'
        plt.savefig(img_path)
        visualizations.append(img_path)
        plt.close()
    
    return visualizations

def analyze_statistics(file_path):
    df = pd.read_csv(file_path, sep='\t', on_bad_lines='skip', usecols=['review_body', 'star_rating'], nrows=1000)
    df = df.dropna()

    statistics = {
        'total_reviews': len(df),
        'average_rating': df['star_rating'].mean(),
        'rating_distribution': df['star_rating'].value_counts().to_dict()
    }

    return statistics

def analyze_sentiments(file_path):
    df = pd.read_csv(file_path, sep='\t', on_bad_lines='skip', usecols=['review_body'], nrows=1000)
    df = df.dropna()

    def get_sentiment(text):
        analysis = TextBlob(text)
        return analysis.sentiment.polarity

    df['sentiment'] = df['review_body'].apply(get_sentiment)
    sentiments = {
        'positive': len(df[df['sentiment'] > 0]),
        'neutral': len(df[df['sentiment'] == 0]),
        'negative': len(df[df['sentiment'] < 0])
    }

    return sentiments
