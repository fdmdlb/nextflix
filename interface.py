#!/usr/bin/env python
# coding: utf-8

# In[ ]:


# Import libraries
import mysql.connector
import pandas as pd
import streamlit as st
import getpass
import seaborn as sn
from matplotlib import pyplot as plt
import numpy as np


st.title('Recommandation movies')

# #Cleaning process regarding the variable that has the "time" variable, and rename it to something easier to write
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
