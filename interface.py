# Import libraries
import pandas as pd
import streamlit as st
import seaborn as sn
from matplotlib import pyplot as plt

import cultural_interest
import words_count

df_top10_number = pd.read_csv('./data/6ko_top10_number.csv')
df_top10_minutes = pd.read_csv('./data/6ko_top10_minutes.csv')

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
            "Top 5 reviews sharing the audience opinion",
            "Individual length evolution in minutes from 1874-2021",
            "Average movie* length evolution from 1874-2021",
            "Top 5 popular movies and respective characteristics",
            "Top 5 Genres",
            "Recommandation system"
            ]

with st.sidebar:
    selected = st.selectbox(
         'Select a genre',
         options=nav_list)

if selected==nav_list[7]:
    st.markdown(f'# {nav_list[7]}')
    # add the Recommandation code | Integrate the partial file from recommandation system
    cultural_interest.display_international()

if selected==nav_list[0]:
    st.markdown(f'# {nav_list[0]}')
    cultural_interest.display_international()

if selected==nav_list[1]:
    st.markdown(f'# {nav_list[1]}')
    words_count.display_wordcloud()

if selected==nav_list[2]:
    st.markdown(f'# {nav_list[2]}')

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

    st.markdown(f'# {nav_list[3]}')

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

    st.markdown(f'# {nav_list[4]}')

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
    st.markdown(f'# {nav_list[5]}')
    sn.set(rc = {'figure.figsize':(15,8)})
    sn.set_style("white")
    st.dataframe(top5_movies)


if selected==nav_list[6]:
    st.markdown(f'# {nav_list[6]}')
    st.dataframe(top5_genres)
    
    def display_international():
        col1, col2 = st.columns(2)
        with col1:
            st.header("Top 10 in number of media translated")
            st.dataframe(df_top10_number)
        with col2:
            st.header("Top 10 in number of minutes translated")
            st.dataframe(df_top10_minutes)
