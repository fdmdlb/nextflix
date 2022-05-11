# Import libraries
import pandas as pd
import streamlit as st
from streamlit_option_menu import option_menu
from sklearn.preprocessing import StandardScaler
from sklearn.neighbors import NearestNeighbors
from unidecode import unidecode
from sklearn.preprocessing import MultiLabelBinarizer

with st.sidebar:
    selected = option_menu('Main Menu', ['Recommendations', 'About Us'], 
        icons=['film', 'people'], menu_icon='house', default_index=0)



if selected == "Recommendations":
    st.markdown('<H1 style="color:red;text-align:center;" >NEXTFLIX</H1>', unsafe_allow_html=True)
    
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
    weights = [1, 10, 10, 5, 5, 1, 1, 1, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 5, 5, 5, 5, 5, 5]


    # defining X, and normalizing X, computing KNN
    X = pd.concat([df_movies[['runtime', 'audience_rating','audience_count', 'tomatometer_rating', 'tomatometer_count','year', 'month', 'day']],genres,content_ratings],axis=1)
    scaler = StandardScaler().fit(X)
    X_scaled = scaler.transform(X)
    distanceKNN = NearestNeighbors(n_neighbors=11, metric_params={'w': weights}).fit(X_scaled)

    # menu to type key words
    search = choice = ''
    search = st.text_input('Please enter a movie title you like: ')

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

            table_content = ''
            for row in range(len(df_display)):
                table_content += '<tr><td>' + df_display['movie_title'].iloc[row] + '</td><td align=center>' + str(int(df_display['audience_rating'].iloc[row])) + '</td><td align=center>' + str(int(df_display['tomatometer_rating'].iloc[row])) + '</td></tr>'

            st.markdown('<table><tr><th>Movie Title</th><th>Public Ratings</th><th>TomatoMeter</th></tr>' + table_content + '</table>', unsafe_allow_html=True)
            search = choice = ''

        else:
            st.write("Sorry, I couldn't find any match")
    ########################################################################


if selected == 'About Us':
    st.markdown('<H1 style="color:red;text-align:center;" >The Team</H1>', unsafe_allow_html=True)

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
    "img": "https://raw.githubusercontent.com/FMrtnz/project_movie_recommand/main/img/joao2.png",
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
            f'<div class="us-card"><img src="{one["img"]}"><p>{one["name"]}</p><a href="{one["linkedin"]}">LinkedIn</a>',
            unsafe_allow_html=True
            )
    st.markdown('<br><br>', unsafe_allow_html=True)
    st.markdown('<H1 style="color:red;text-align:center;" >The Original Project</H1>', unsafe_allow_html=True)
    st.markdown("The original project was to perform Exploratory Data Analysis of multiple data sets from IMDb and Rotten Tomatoes web sites, in order to provide a relevent movie recommendation system.<br>You may view the full project on <a href='https://github.com/FMrtnz/project_movie_recommand'>GitHub</a> and <a href='https://share.streamlit.io/fmrtnz/project_movie_recommand/main/interface.py'>Streamlit</a>.", unsafe_allow_html=True)
    