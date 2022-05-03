# Import libraries
import mysql.connector
import pandas as pd
import streamlit as st
import getpass
import seaborn as sn
from matplotlib import pyplot as plt
import numpy as np


st.title('Recommandation movies')

# # Cleaning process regarding the variable that has the "time" variable, and rename it to something easier to write
#

# title_basic["runtimeMinutes"].dropna()  #drop all na from the desiered column
# title_basic["runtimeMinutes"].unique()  #one value is "nan", need to remove it
# title_basic.rename(columns={"runtimeMinutes":"minutes"}, inplace=True) #change variable namefor something easier to write
#
# title_basic = title_basic.loc[title_basic["minutes"].isna() != True, :]  #beyond the dropna(axis=1) this is the other method
# title_basic["minutes"]=title_basic["minutes"].astype(int, errors="ignore")
#
# title_basic = title_basic.loc[title_basic["startYear"].isna() != True, :]
# title_basic["titleType"]=title_basic["titleType"].str.lower()
#
# #filter only the titletypes we want, in total we get 2,343,750 rows
# filter_title=title_basic[title_basic["titleType"].str.contains("movie|short|video",na=True)]
# filter_title=filter_title.loc[(filter_title["titleType"]!="videogame") & (filter_title["titleType"]!="tvpilot") & (filter_title["titleType"]!="tvshort"),:]
#
#
# #variale "endYear is all the time filled with NA's values, so i remove it
# filter_title.drop(["endYear"], axis=1, inplace=True)
#
# total=pd.merge(filter_title,title_episode,how="left",on="tconst")
# total.drop(["parentTconst","seasonNumber","episodeNumber"], axis=1, inplace=True)
# total.info()
# #can see that there is any type of movie/short/tvmovie/video with a parentTconst. So it is all good, continue with the filter_title
#
#
# #transform minutes into a intenger varaible (instead of an object)
# total["minutes"]=total["minutes"].astype(int)
#
#
# # want to see what is the mean time (in minutes) each title type has througout the years
# title_basic_table= total.pivot_table(index="startYear", columns= "titleType", values = "minutes", aggfunc="mean" )
# title_basic_table.reset_index(inplace=True )
#
# #does not make sense to have rows from products that still do not exist, so filter out products from 2022 onwards
# title_basic_table = title_basic_table.loc[title_basic_table["startYear"] <= 2022,:]
#
#
#
# # In[ ]:
#
#
# #first visualization to display in the interface
#
# sn.set(rc = {'figure.figsize':(15,8)})
# sn.set_style("white")
#
# sn.lineplot(data=title_basic_table, x="startYear", y="movie", color="blue", label = "Movie")
# sn.lineplot(data=title_basic_table, x="startYear", y="short", color="purple", label = "Short")
# sn.lineplot(data=title_basic_table, x="startYear", y="tvmovie", color="black", label = "TV Movie")
# #sn.lineplot(data=title_basic_table, x="startYear", y="tvshort", color="orange", label = "TV Short")
# #sn.lineplot(data=title_basic_table, x="startYear", y="tvspecial", color="red", label = "TV Special")
# sn.lineplot(data=title_basic_table, x="startYear", y="video", color="orange", label = "Video")#.set(title="The length evolution of media products", ylabel="Minutes", xlabel="Year")
# plt.legend(title='Media Products:', fontsize=12)
# plt.xlabel('Year', fontsize=20);
# plt.ylabel('Minutes', fontsize=20);
# plt.title('The length evolution of media products', fontsize=25)
# plt.tick_params(axis='both', which='major', labelsize=15)
# #sn.lineplot(data=title_basic_table, x="startYear", y="videoGame", color="purple", label = "Video Game").set(title="The length evolution of media products", ylabel="Minutes", xlabel="Year")
#
#
# # In[ ]:
#
#
# #overall we plan to see if movies/videos/short/tvshort/tvmovie (..) all together how was the evolution
# title_basic= total.pivot_table(index="startYear", values = "minutes", aggfunc="mean" )
# title_basic.reset_index(inplace=True)
# title_basic=title_basic.loc[title_basic["startYear"]<= 2022,:]
#
#
# # In[ ]:
#
#
# #second visualization
#
# sn.set(rc = {'figure.figsize':(15,8)})
# sn.set_style("white")
# sn.lineplot(data=title_basic, x="startYear", y="minutes")
# plt.xlabel('Year', fontsize=20);
# plt.ylabel('Minutes', fontsize=20);
# plt.title("Average length of movies/videos/tvmovies/short from 1874-2021", fontsize=25)
# plt.tick_params(axis='both', which='major', labelsize=15)
#

st.markdown('# International')

df_top10_number = pd.read_csv('./data/6ko_top10_number.csv')
df_top10_minutes = pd.read_csv('./data/6ko_top10_minutes.csv')

col1, col2 = st.columns(2)
with col1:
    st.header("Top 10 in number of media translated")
    df_top10_number
with col2:
    st.header("Top 10 in number of minutes translated")
    df_top10_minutes


st.markdown('# Top 5 magasins sharing the audience opinion')

# Import files for the analyse
rating_movies_audience_publisher = pd.read_csv("./data/rating_movies_audience_publisher")
publishers_selection_differences = pd.read_csv("./data/publishers_selection_differences", skiprows=2)
publishers_selection_differences.columns = ["publiser_name","mean","std","count","max"]
publishers_list = list(publishers_selection_differences.sort_values(['mean','std'], ascending=[0,1]).head(10)["publiser_name"])

# Get correlation
publishers_corr = pd.pivot_table(rating_movies_audience_publisher[rating_movies_audience_publisher.publisher_name.isin(publishers_list)],
               values="review_score_float", index="rotten_tomatoes_link", columns=['publisher_name']).merge(rating_movies_audience_publisher[["rotten_tomatoes_link", "audience_rating"]], on="rotten_tomatoes_link").corr(min_periods=220)[["audience_rating"]]

fig_corr, ax_corr = plt.subplots()

ax_corr = sn.heatmap(publishers_corr.sort_values("audience_rating", ascending=False)[1:6])
ax_corr.set_yticklabels(list(publishers_corr.sort_values("audience_rating", ascending=False)[1:6].index))

publishers_corr.sort_values("audience_rating", ascending=False)[1:6]
st.pyplot(fig_corr)
