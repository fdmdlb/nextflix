# Import libraries
import pandas as pd
import streamlit as st
import seaborn as sn
from matplotlib import pyplot as plt

top5_movies = pd.read_csv('./data/joaoTop5MOVIES.csv')
top5_genres=pd.read_csv('./data/joaoGGroupedtop5GENRES.csv')

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
            "Top 5 Movies",
            "Top 5 Genres",
            "Recommandation system"
            ]

with st.sidebar:
    selected = st.selectbox(
         'Select a genre',
         options=nav_list)

if selected==nav_list[7]:
    st.markdown('# Recommandation System')
    # add the Recommandation code | Integrate the partial file from recommandation system
    import cultural_interest

if selected==nav_list[0]:
    st.markdown('# International')
    import cultural_interest

if selected==nav_list[1]:
    st.markdown('# words analyse')
    st.markdown('## Words by genre')
    import words_count

if selected==nav_list[2]:
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
    #st.download_button(label="download chart",data=title_basic_table)

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
    st.markdown('# Top 5 popular movies and respective characteristics')
    sn.set(rc = {'figure.figsize':(15,8)})
    sn.set_style("white")
    st.dataframe(top5_movies)


if selected==nav_list[6]:
    st.markdown('# Top 5 Genres')
    st.dataframe(top5_genres)
