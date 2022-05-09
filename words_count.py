import pandas as pd
import streamlit as st
from ast import literal_eval
from sklearn.feature_extraction.text import CountVectorizer
from wordcloud import WordCloud
import numpy as np
import plotly.express as px
from PIL import Image


def blue_color_func(word, font_size, position, orientation, random_state=None, **kwargs):
    return "hsl(225, 54.55%%, %d%%)" % np.random.uniform(49,59)
    #return "hsl(200, 100, 50)" % np.random.uniform(60,100)

def display_wordcloud():
    word_freq = pd.read_csv('./data/freq_words_rotten_vs_fresh.csv')
    word_freq.rename(columns={'Unnamed: 0':'word'}, inplace=True )

    lemmentize_words_genres = pd.read_csv('./data/genres_X_lem.csv', converters={"genres": literal_eval, "X_lem": literal_eval})

    st.markdown('## Most frequents words in Rotten vs Fresh movies')
    list_fresh = word_freq[(word_freq.freq_total > 0.4)].sort_values(["rel_fresh"], ascending=[0]).head(10)["word"].values
    list_rotten = word_freq[(word_freq.freq_total > 0.4)].sort_values(["rel_rot"], ascending=[0]).head(10)["word"].values
    list_words = np.append(list_rotten, list_fresh)
    #word_freq
    fig = px.bar(word_freq[word_freq["word"].isin(list_words)].sort_values("General"), x='word', y=["Fresh", "Rotten"], title="Rotten vs Fresh movies", barmode="group")
    st.plotly_chart(fig)

    col1, col2 = st.columns(2)
    with col1:
        # Set an input to choose region
        genres_explodes = lemmentize_words_genres.explode(["genres"])
        mask = np.array(Image.open("./img/circle.png"))
        genre_selected = st.selectbox(
             'Select a genre',
             options=list(genres_explodes["genres"].value_counts().index))
        X = genres_explodes[genres_explodes["genres"] == genre_selected]['X_lem'].apply(lambda wlist: " ".join(wlist))
        vectorizer = CountVectorizer(max_features=10)
        text_matrix = vectorizer.fit_transform(X)
        df_matrix = pd.DataFrame(text_matrix.toarray(), columns = vectorizer.get_feature_names_out())
        wordcloud = WordCloud(mask=mask, background_color=None, mode="RGBA" ,width=700,height=500, min_font_size=10).generate_from_frequencies(df_matrix.sum())
        st.image(wordcloud.recolor(color_func=blue_color_func, random_state=3).to_array())
