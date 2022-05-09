# Import libraries
import pandas as pd
import streamlit as st
import seaborn as sn
from matplotlib import pyplot as plt
import cultural_interest
import words_count
from PIL import Image
import plotly.express as px
from sklearn.preprocessing import StandardScaler
from sklearn.neighbors import NearestNeighbors
from unidecode import unidecode
from sklearn.preprocessing import MultiLabelBinarizer


df_top10_number = pd.read_csv('./data/6ko_top10_number.csv')
df_top10_minutes = pd.read_csv('./data/6ko_top10_minutes.csv')

top5_movies = pd.read_csv('./data/joaoTop5MOVIES.csv')
top5_genres=pd.read_csv('./data/top5_genres.csv')

rating_movies_audience_publisher = pd.read_csv("./data/rating_movies_audience_publisher")
publishers_selection_differences = pd.read_csv("./data/publishers_selection_differences", skiprows=2)
publishers_selection_differences.columns = ["publiser_name","mean","std","count","max"]

title_basic_table = pd.read_csv('./data/joana_visualization1.csv')
title_basic = pd.read_csv('./data/joana_visualization2.csv')

st.markdown('<H1 style="color:red;text-align:center;" >NEXTFLIX</H1>', unsafe_allow_html=True)

nav_list = [
            "Top 5 Genres",
             "Top 5 Movies",
            "Individual Media Length Evolution ",
            "Average Media Length Evolution",
            "Top 10 Translating Countries",
    "Top 5 Reviews sharing Audience Opinion",
            "Words Analyse",
            "Recommendation System",
            "About us"
            ]

with st.sidebar:
    selected = st.selectbox(
         'Select a genre',
         options=nav_list)


if selected==nav_list[7]:
    st.markdown(f'# {nav_list[7]}')
    ########################################################################
    # Recommendation system

    df_movies = pd.read_csv('./data/6ko_recommendation.csv')

    # all-titles-no-accents-lower-case
    df_movies['simple_title'] = df_movies['movie_title'].apply(lambda title: unidecode(title).lower())

    #splitting dates into y m d as int
    df_movies['year'] = df_movies['original_release_date'].apply(lambda date: int(date[:4]))
    df_movies['month'] = df_movies['original_release_date'].apply(lambda date: int(date[5:7]))
    df_movies['day'] = df_movies['original_release_date'].apply(lambda date: int(date[8:10]))

    # dummifying "content rating"
    content_ratings = pd.get_dummies(df_movies['content_rating'])

    # dummifying "genres"
    df_movies['genres'] = df_movies['genres'].apply(lambda s: s.split(', '))
    s = df_movies['genres']
    mlb = MultiLabelBinarizer()
    genres = pd.DataFrame(mlb.fit_transform(s),columns=mlb.classes_, index=df_movies.index)

    # weight parameters for minkowski's distance
    # 'runtime', 'audience_rating','audience_count', 'tomatometer_rating', 'tomatometer_count','year', 'month', 'day', 'genres'x21, 'content_ratings'x6
    weights = [1, 10, 10, 5, 5, 1, 1, 1, 10, 10,10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10 , 5, 5, 5, 5, 5, 5]


    # defining X, and normalizing X, computing KNN
    X = pd.concat([df_movies[['runtime', 'audience_rating','audience_count', 'tomatometer_rating', 'tomatometer_count','year', 'month', 'day']],genres,content_ratings],axis=1)
    scaler = StandardScaler().fit(X)
    X_scaled = scaler.transform(X)
    distanceKNN = NearestNeighbors(n_neighbors=11, metric_params={'w': weights}).fit(X_scaled)

    # menu to type key words
    search = choice = ''
    search = st.text_input('Please enter a movie title you liked: ')

    if search !='':
        search = unidecode(search).lower()
        options = df_movies[df_movies['simple_title'].str.contains(search)]
        df_choice = pd.DataFrame(range(1,len(options)+1), dtype='str', index=options.index, columns =['choice'])
        options = pd.concat([options,df_choice],axis=1)

        if len(options) > 1:
            option = st.selectbox('Please confirm your choice', options['choice']+' - '+options['movie_title'])
            key_id = options[options['choice'] == option[0:2].rstrip()].index[0]

        elif len(options) == 1:
            key_id = options.index[0]

        if len(options) >= 1:
            result = distanceKNN.kneighbors([X_scaled[key_id]])
            result_list = list(result[1][0])
            closests = result_list[1:]

            st.write('Here are our suggestions matching ',df_movies['movie_title'].loc[key_id])
            df_display = df_movies[['movie_title','audience_rating','tomatometer_rating']].loc[closests].copy()
            st.write('Suggestion title (Audience Rating | TomatoMeter)')
            df_display.apply(lambda row: st.write('* ', row[0], '(', str(int(row[1])), '|', str(int(row[2])), ')'),axis=1)
            search = choice = ''

        else:
            st.write('Sorry, I cannot find any match')
    ########################################################################

if selected==nav_list[4]:
    st.markdown(f'# {nav_list[4]}')
    cultural_interest.display_international()

if selected==nav_list[6]:
    st.markdown(f'# {nav_list[6]}')
    words_count.display_wordcloud()

if selected==nav_list[5]:
    st.markdown(f'# {nav_list[5]}')

    # Import files for the analyse
    publishers_list = list(publishers_selection_differences.sort_values(['mean','std'], ascending=[0,1]).head(10)["publiser_name"])

    # Get correlation
    publishers_corr = pd.pivot_table(rating_movies_audience_publisher[rating_movies_audience_publisher.publisher_name.isin(publishers_list)],
                   values="review_score_float", index="rotten_tomatoes_link", columns=['publisher_name']).merge(rating_movies_audience_publisher[["rotten_tomatoes_link", "audience_rating"]], on="rotten_tomatoes_link").corr(min_periods=220)[["audience_rating"]]

    top_5_reviews = publishers_corr.sort_values("audience_rating", ascending=False)[1:6]

    # critics = np.array(["https://twitter.com/KristianHarloff",
    # "https://www.facebook.com/dvdtown",
    # "https://americanprofile.com/",
    # "https://eu.seacoastonline.com/",
    # "https://thedivareview.com/"])

    img = ["./img/kristian.png",
    "./img/metropolis.png",
    "./img/american.png",
    "./img/seacoast.png",
    "./img/diva.png"]

    for i in range(0, 5):
        col1, col2 = st.columns(2)
        with col2:
            image = Image.open(img[i])
            st.image(image, width=300)
        with col1:
            st.write(f"#{i+1} {top_5_reviews.index[i]} ({str(round(top_5_reviews['audience_rating'].values[i], 2))})")

if selected==nav_list[2]:
    #####JOANA PART########################
    #first visualization

    st.markdown(f'# {nav_list[2]}')

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

    list_movies = [
    "Please choose an answer",
    "Canadian Army Newsreel",
    "Flighing Mushrooms",
    "Frogs on the plane",
    "Happy Dutch on Vacation",
    "Married with a codfish"]

    answer = st.radio(
     "What's the longest movie ?",
     list_movies)

    if answer == list_movies[0]:
     st.write('......')
    elif answer == list_movies[1]:
     st.write('Congrats, you win a full version of Canadian Army Newsreel ! :rocket:')
    else:
     st.write("Wrong answer ! :no_entry_sign:")

if selected==nav_list[3]:
    #second visualization

    st.markdown(f'# {nav_list[3]}')
    #st.title('coming soon')
    sn.set(rc = {'figure.figsize':(15,8)})
    sn.set_style("white")
    fig1_j,ax_j1=plt.subplots()

    ax_j1= sn.lineplot(data=title_basic, x="startYear", y="minutes").set(xlabel="Year", ylabel="Minutes")
    plt.xlabel('Year', fontsize=20)
    plt.ylabel('Minutes', fontsize=20);
    #plt.title("Average length of movies/videos/tvmovies/short from 1874-2021", fontsize=25)
    plt.tick_params(axis='both', which='major', labelsize=15)

    st.pyplot(fig1_j)

if selected==nav_list[1]:
    # ##joao part####
    st.markdown(f'# {nav_list[1]}')
    sn.set(rc = {'figure.figsize':(15,8)})
    sn.set_style("white")

    #st.dataframe(top5_movies)

    img2 = ["./data/redemption.jpg","./data/The_Dark_Knight.jpg","./data/inception_32.jpg","./data/fightCLUB.jpg","./data/PULPfiction.jpg"]


    for i in range(0,5):
        col1, col2 = st.columns(2)
        with col1:
            image_movie = Image.open(img2[i])
            st.image(image_movie, width=200)
        with col2:
            title=top5_movies['Title'].values[i]
            genre = top5_movies["Genres"].values[i]
            rating=top5_movies["Avg. Rating"].values[i]
            votes=top5_movies["Num.Votes"].values[i]
            popularity=round((top5_movies["Popularity"].values[i])/1000000,3)
            #st.write(title)
            #st.write(genre)
            #st.write(rating)
            with st.expander("Want to know more? Click!"):
                st.write("Title:",title)
                st.write("Genre: ", genre)
                st.write("Rating: ",rating)
                st.write("Number of Votes: ",votes)
                st.write("Popularity Score: ", popularity)

if selected==nav_list[0]:

    st.markdown(f'# {nav_list[0]}')
    sn.set_style("white")
    fig_genre = px.bar(top5_genres, x="Genres", y="Pop.Score").update_xaxes(showgrid=False)
    st.plotly_chart(fig_genre)

if selected==nav_list[8]:
    st.markdown(f'# {nav_list[8]}')
    us = [
    {"name":"Fabien Martinez",
     "img": "https://media-exp1.licdn.com/dms/image/C5603AQHJnh0UtSOiog/profile-displayphoto-shrink_200_200/0/1517442681233?e=1657756800&v=beta&t=LyfuwkU19EGf5Hyp5akMGx_rzIqGzo8bH1VreVcKq0k",
    "linkedin":"https://www.linkedin.com/in/fabien-martinez-a30561109/"},
    {"name":"François de la Bretèche",
    "img": "https://media-exp1.licdn.com/dms/image/C4D03AQG9QwJ6igbmKA/profile-displayphoto-shrink_800_800/0/1584797342559?e=1657756800&v=beta&t=hiwVl_fchl2uEhZph6uheK_59vq5QRJixzqiGkKTvoo",
    "linkedin":"https://www.linkedin.com/in/f-delabreteche/"},
    {"name":"Joana Alves",
    "img": "https://media-exp1.licdn.com/dms/image/C4D03AQFhUPgrR5wVUg/profile-displayphoto-shrink_800_800/0/1558610964713?e=1657756800&v=beta&t=zYzStxavELhinCITmuVNygzu3nH00jP3LLFKmv6hVkM",
    "linkedin":"https://www.linkedin.com/in/joana-pires-coelho/"
    },
    {"name":"João Almeida",
    "img": "",
    "linkedin":"https://github.com/The-Ineffable-Alias"}
    ]

    st.markdown(
    "<style>.us-card{text-align:center; margin:.8rem 0}.us-card p{margin:.3rem 0}.us-card img{-webkit-filter: grayscale(100%);filter: grayscale(100%);border-radius:50%;width:150px;height:150px;padding:1rem;}</style>",
    unsafe_allow_html=True
    )
    col1, col2, col3, col4 = st.columns(4)
    cols = [col1, col2, col3, col4]
    for index in range(0,4):
        with cols[index]:
            one = us[index]
            st.markdown(
            f'<div class="us-card"><img src="{one["img"]}"><p>{one["name"]}</p><a href="{one["linkedin"]}">linkedin</a>',
            unsafe_allow_html=True
            )
