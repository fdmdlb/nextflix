# Import libraries
import pandas as pd
import streamlit as st
import seaborn as sn
from matplotlib import pyplot as plt
import numpy as np
import plotly.express as px
from ast import literal_eval
from sklearn.feature_extraction.text import CountVectorizer
from wordcloud import WordCloud

df_top10_number = pd.read_csv('./data/6ko_top10_number.csv')
df_top10_minutes = pd.read_csv('./data/6ko_top10_minutes.csv')

word_freq = pd.read_csv('./data/freq_words_rotten_vs_fresh.csv')
word_freq.rename(columns={'Unnamed: 0':'word'}, inplace=True )

lemmentize_words_genres = pd.read_csv('./data/genres_X_lem.csv', converters={"genres": literal_eval, "X_lem": literal_eval})

rating_movies_audience_publisher = pd.read_csv("./data/rating_movies_audience_publisher")
publishers_selection_differences = pd.read_csv("./data/publishers_selection_differences", skiprows=2)
publishers_selection_differences.columns = ["publiser_name","mean","std","count","max"]

title_basic_table = pd.read_csv('./data/joana_visualization1.csv')
title_basic = pd.read_csv('./data/joana_visualization2.csv')

st.title('Recommandation movies')

nav_list = ["International",
            "Words analyse",
            "Most representative reviews",
            "Individual length",
            "Average movie length",
            "?"
            ]

with st.sidebar:
    selected = st.selectbox(
         'Select a genre',
         options=nav_list)

if selected==nav_list[0]:
    st.markdown('# International')
    col1, col2 = st.columns(2)
    with col1:
        st.header("Top 10 in number of media translated")
        df_top10_number
    with col2:
        st.header("Top 10 in number of minutes translated")
        df_top10_minutes

if selected==nav_list[1]:
    st.markdown('# Most frequents words by genres')
    # Set an input to choose region
    genres_explodes = lemmentize_words_genres.explode(["genres"])
    genre_selected = st.selectbox(
         'Select a genre',
         options=list(genres_explodes["genres"].value_counts().index))
    X = genres_explodes[genres_explodes["genres"] == genre_selected]['X_lem'].apply(lambda wlist: " ".join(wlist))
    vectorizer = CountVectorizer(max_features=10)
    text_matrix = vectorizer.fit_transform(X)
    df_matrix = pd.DataFrame(text_matrix.toarray(), columns = vectorizer.get_feature_names_out())
    wordcloud = WordCloud(background_color="rgba(0,0,0,0)",width=700,height=500, min_font_size=10).generate_from_frequencies(df_matrix.sum())
    st.image(wordcloud.to_array())

if selected==nav_list[2]:
    st.markdown('# Most frequents words in Rotten vs Fresh movies')
    list_fresh = word_freq[(word_freq.freq_total > 0.4)].sort_values(["rel_fresh"], ascending=[0]).head(10)["word"].values
    list_rotten = word_freq[(word_freq.freq_total > 0.4)].sort_values(["rel_rot"], ascending=[0]).head(10)["word"].values
    list_words = np.append(list_rotten, list_fresh)
    #word_freq
    fig = px.bar(word_freq[word_freq["word"].isin(list_words)].sort_values("General"), x='word', y=["Fresh", "Rotten"], title="Rotten vs Fresh movies", barmode="group")
    st.plotly_chart(fig)

    st.markdown('# Top 5 reviews sharing the audience opinion')

    # Import files for the analyse
    publishers_list = list(publishers_selection_differences.sort_values(['mean','std'], ascending=[0,1]).head(10)["publiser_name"])

    # Get correlation
    publishers_corr = pd.pivot_table(rating_movies_audience_publisher[rating_movies_audience_publisher.publisher_name.isin(publishers_list)],
                   values="review_score_float", index="rotten_tomatoes_link", columns=['publisher_name']).merge(rating_movies_audience_publisher[["rotten_tomatoes_link", "audience_rating"]], on="rotten_tomatoes_link").corr(min_periods=220)[["audience_rating"]]

    fig_corr, ax_corr = plt.subplots()

    ax_corr = sn.heatmap(publishers_corr.sort_values("audience_rating", ascending=False)[1:6], annot=True)
    ax_corr.set_yticklabels(list(publishers_corr.sort_values("audience_rating", ascending=False)[1:6].index))

    #publishers_corr.sort_values("audience_rating", ascending=False)[1:6]
    st.pyplot(fig_corr)

if selected==nav_list[3]:
    #####JOANA PART########################
    #first visualization

    st.markdown('# Individual length evolution in minutes from 1874-2021')

    sn.set(rc = {'figure.figsize':(15,8)})
    sn.set_style("white")
    fig2_j,ax_j2=plt.subplots()

    ax_j2=sn.lineplot(data=title_basic_table, x="startYear", y="movie", color="blue", label = "Movie")
    sn.lineplot(data=title_basic_table, x="startYear", y="short", color="grey", label = "Short")
    sn.lineplot(data=title_basic_table, x="startYear", y="tvmovie", color="black", label = "TV Movie")
    sn.lineplot(data=title_basic_table, x="startYear", y="video", color="orange", label = "Video")
    plt.legend(title='Media Products:', fontsize=12)
    plt.xlabel('Year', fontsize=20);
    plt.ylabel('Minutes', fontsize=20);
    #plt.title('The length evolution of media products', fontsize=25)
    plt.tick_params(axis='both', which='major', labelsize=15)

    st.pyplot(fig2_j)

if selected==nav_list[4]:
    #second visualization

    st.markdown('# Average movie* length evolution from 1874-2021')

    sn.set(rc = {'figure.figsize':(15,8)})
    sn.set_style("white")
    fig1_j,ax_j1=plt.subplots()

    ax_j1= sn.lineplot(data=title_basic, x="startYear", y="minutes").set(xlabel="Year", ylabel="Minutes")
    plt.xlabel('Year', fontsize=20)
    plt.ylabel('Minutes', fontsize=20);
    #plt.title("Average length of movies/videos/tvmovies/short from 1874-2021", fontsize=25)
    plt.tick_params(axis='both', which='major', labelsize=15)

    st.pyplot(fig1_j)

if selected==nav_list[5]:
    ##joao part####
    top5_movies = pd.read_csv('./data/joaoTop5MOVIES.csv')

    st.title('Top 5 popular movies and respective characteristics')
    sn.set(rc = {'figure.figsize':(15,8)})
    sn.set_style("white")
    st.dataframe(top5_movies)
