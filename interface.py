# Import libraries
import pandas as pd
import streamlit as st
from streamlit_option_menu import option_menu
from sklearn.preprocessing import StandardScaler
from sklearn.neighbors import NearestNeighbors
from unidecode import unidecode
from sklearn.preprocessing import MultiLabelBinarizer

st.set_page_config(page_title="Nextflix", page_icon='👁',menu_items={"About":'*bandev2022*'})

with st.sidebar:
    selected = option_menu('Main Menu', ['Recommendations', 'About', 'Greatest Actor'], 
               icons=['film', 'info-circle', 'gem'], menu_icon='house', default_index=0)

df_movies = pd.read_csv('./data/recommendation.csv')


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

if selected == "Recommendations":
    st.markdown('<H1 style="color:#ff4b4b;text-align:center;" >NEXTFLIX</H1>', unsafe_allow_html=True)
    
    # menu to type key words
    search = choice = ''
    search = st.text_input('Please enter a movie title you like: ')

    if search !='':
        # simplify input key words
        search = unidecode(search).lower()
        # create dataframe with all result matching key words
        options = df_movies[df_movies['simple_title'].str.contains(search)]
        # transform year into string to be displayed in menu
        options['year'] = options['year'].apply(str)
        # create a one-column datafram with orders of options
        df_choice = pd.DataFrame(range(1,len(options)+1), dtype='str', index=options.index, columns =['choice'])
        # concat order+movie dataframes
        options = pd.concat([options,df_choice],axis=1)
        
        if len(options) > 1:
            option = st.selectbox('Please confirm your choice', options['choice'] + ' - ' + options['movie_title'] + ' (' + options['year'] + ')')
            key_id = options[options['choice'] == option[0:2].rstrip()].index[0]

        elif len(options) == 1:
            key_id = options.index[0]

        if len(options) >= 1:
            result = distanceKNN.kneighbors([X_scaled[key_id]])
            result_list = list(result[1][0])
            closests = result_list[1:]

            st.markdown('Here are our suggestions matching <b style="color:#ff4b4b">'+(df_movies['movie_title'].loc[key_id])+'</b>', unsafe_allow_html=True)
            
            df_display = df_movies[['movie_title','audience_rating','tomatometer_rating','rotten_tomatoes_link']].loc[closests].copy()

            table_content = ''
            for row in range(len(df_display)):
                table_content += '<tr><td align="left">' + df_display['movie_title'].iloc[row] \
                + '</td><td>' + str(int(df_display['audience_rating'].iloc[row])) \
                + '</td><td>' + str(int(df_display['tomatometer_rating'].iloc[row])) \
                + '</td><td><a href="https://www.rottentomatoes.com/' + df_display['rotten_tomatoes_link'].iloc[row] + '">Rotten Tomatoes</a></td></tr>'
            
            st.markdown('<table style="text-align: center;"><tr bgcolor= "#262730"><th align="left">Movie Title</th><th width="1%">🍿</th><th width="1%">🍅</th><th width="20%">🔗</th></tr>'\
            + table_content + \
            '<tr bgcolor= "#262730"><td colspan=4 align="center" borderwidth=0>🍿Public Rating&nbsp;&nbsp;&nbsp;&nbsp;|&nbsp;&nbsp;&nbsp;🍅Tomato Meter&nbsp;&nbsp;&nbsp;|&nbsp;&nbsp;&nbsp;🔗More Info</td></tr></table>', unsafe_allow_html=True)

            search = choice = ''

        else:
            st.write("Sorry, I couldn't find any match")
        

if selected == 'About':
    
    st.markdown('<H1 style="color:#ff4b4b;text-align:center;" >The Data</H1>', unsafe_allow_html=True)
    sources = ['Rotten Tomatoes','Kaggle']
    st.markdown(f'<ul>\
                      <li>Number of movies in the database: {str(df_movies.shape[0])}</li>\
                      <li>Most recent release date: {str(df_movies.year.max())}</li>\
                      <li>Sources: {", ".join(sources)}</li>\
                  </ul>',
                  unsafe_allow_html=True)
        
    
    
    st.markdown('<br><H1 style="color:#ff4b4b;text-align:center;" >The Team</H1>', unsafe_allow_html=True)

    linkedin_icon = '<svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor" class="bi bi-linkedin" viewBox="0 0 16 16">\
                     <path d="M0 1.146C0 .513.526 0 1.175 0h13.65C15.474 0 16 .513 16 1.146v13.708c0 .633-.526 1.146-1.175 1.146H1.175C.526 16 0 15.487 0 14.854V1.146zm4.943 12.248V6.169H2.542v7.225h2.401zm-1.2-8.212c.837 0 1.358-.554 1.358-1.248-.015-.709-.52-1.248-1.342-1.248-.822 0-1.359.54-1.359 1.248 0 .694.521 1.248 1.327 1.248h.016zm4.908 8.212V9.359c0-.216.016-.432.08-.586.173-.431.568-.878 1.232-.878.869 0 1.216.662 1.216 1.634v3.865h2.401V9.25c0-2.22-1.184-3.252-2.764-3.252-1.274 0-1.845.7-2.165 1.193v.025h-.016a5.54 5.54 0 0 1 .016-.025V6.169h-2.4c.03.678 0 7.225 0 7.225h2.4z"/>\
                     </svg>'
    github_icon = '<svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor" class="bi bi-github" viewBox="0 0 16 16">\
                   <path d="M8 0C3.58 0 0 3.58 0 8c0 3.54 2.29 6.53 5.47 7.59.4.07.55-.17.55-.38 0-.19-.01-.82-.01-1.49-2.01.37-2.53-.49-2.69-.94-.09-.23-.48-.94-.82-1.13-.28-.15-.68-.52-.01-.53.63-.01 1.08.58 1.23.82.72 1.21 1.87.87 2.33.66.07-.52.28-.87.51-1.07-1.78-.2-3.64-.89-3.64-3.95 0-.87.31-1.59.82-2.15-.08-.2-.36-1.02.08-2.12 0 0 .67-.21 2.2.82.64-.18 1.32-.27 2-.27.68 0 1.36.09 2 .27 1.53-1.04 2.2-.82 2.2-.82.44 1.1.16 1.92.08 2.12.51.56.82 1.27.82 2.15 0 3.07-1.87 3.75-3.65 3.95.29.25.54.73.54 1.48 0 1.07-.01 1.93-.01 2.2 0 .21.15.46.55.38A8.012 8.012 0 0 0 16 8c0-4.42-3.58-8-8-8z"/>\
                   </svg>'

    us = [
    {"name":"François",
    "img": "https://raw.githubusercontent.com/fdmdlb/nextflix/main/img/francois.png",
    "link":'<a href="https://www.linkedin.com/in/f-delabreteche/">'+linkedin_icon+'</a>'},
    {"name":"João",
    "img": "https://raw.githubusercontent.com/fdmdlb/nextflix/main/img/joao.png",
    "link": '<a href="https://github.com/The-Ineffable-Alias">'+github_icon+'</a>'},
    {"name":"Joana",
    "img": "https://raw.githubusercontent.com/fdmdlb/nextflix/main/img/joana.png",
    "link": '<a href="https://www.linkedin.com/in/joana-pires-coelho/">'+linkedin_icon+'</a>'},
    {"name":"Fabien",
     "img": "https://raw.githubusercontent.com/fdmdlb/nextflix/main/img/fabien.png",
    "link":'<a href="https://linkedin.com/in/fabien-martinez-data-analyst/">'+linkedin_icon+'</a>'}
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
            f'<div class="us-card"><img src="{one["img"]}"><p>{one["name"]} {one["link"]}</p>',
            unsafe_allow_html=True
            )
    st.markdown('<br><H1 style="color:#ff4b4b;text-align:center;" >The Original Project</H1>', unsafe_allow_html=True)
    st.markdown("The original project was to perform Exploratory Data Analysis of multiple data sets from IMDb and Rotten Tomatoes web sites, in order to provide a relevent movie recommendation system.<br>You may view the full project on <a href='https://github.com/FMrtnz/project_movie_recommand'>GitHub</a> and <a href='https://share.streamlit.io/fmrtnz/project_movie_recommand/main/interface.py'>Streamlit</a>.", unsafe_allow_html=True)
    
    
    
if selected == 'Greatest Actor':
    st.markdown('<H1 style="color:#ff4b4b;text-align:center;" >The Greatest Actor</H1>', unsafe_allow_html=True)    
    
    st.markdown(f'<iframe width="700" height="394" src="https://www.youtube-nocookie.com/embed/hp1nTmMdYpE" title="YouTube video player" frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture" allowfullscreen></iframe>', unsafe_allow_html=True)
    
    linkedin_icon = '<svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor" class="bi bi-linkedin" viewBox="0 0 16 16">\
                     <path d="M0 1.146C0 .513.526 0 1.175 0h13.65C15.474 0 16 .513 16 1.146v13.708c0 .633-.526 1.146-1.175 1.146H1.175C.526 16 0 15.487 0 14.854V1.146zm4.943 12.248V6.169H2.542v7.225h2.401zm-1.2-8.212c.837 0 1.358-.554 1.358-1.248-.015-.709-.52-1.248-1.342-1.248-.822 0-1.359.54-1.359 1.248 0 .694.521 1.248 1.327 1.248h.016zm4.908 8.212V9.359c0-.216.016-.432.08-.586.173-.431.568-.878 1.232-.878.869 0 1.216.662 1.216 1.634v3.865h2.401V9.25c0-2.22-1.184-3.252-2.764-3.252-1.274 0-1.845.7-2.165 1.193v.025h-.016a5.54 5.54 0 0 1 .016-.025V6.169h-2.4c.03.678 0 7.225 0 7.225h2.4z"/>\
                     </svg>'
    