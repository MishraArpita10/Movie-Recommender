import streamlit as st
import pickle
import pandas as pd
import requests

# Create a session (faster + stable)
session = requests.Session()


# Fetch poster from TMDB
@st.cache_data
def fetch_poster(movie_id):
    url = f'https://api.tmdb.org/3/movie/{movie_id}?api_key=ab76934188641ac3de20fd223fa4005a&language=en-US'

    try:
        response = session.get(url, timeout=5)
        data = response.json()
        print("Movie ID:", movie_id)
        print("Poster Path:", data.get('poster_path'))
        print("---------------------------------")
        if data.get('poster_path'):
            return "https://image.tmdb.org/t/p/w500/" + data['poster_path']
        else:
            return "https://via.placeholder.com/500x750?text=No+Poster"

    except:
        return "https://via.placeholder.com/500x750?text=Error"


# Recommendation function
def recommend(movie):
    recommended_movies = []
    recommended_movies_poster = []

    # Get index of selected movie
    movie_index = movies[movies['title'] == movie].index[0]
    distances = similarity[movie_index]

    # Get top 5 similar movies
    movie_list = sorted(
        list(enumerate(distances)),
        reverse=True,
        key=lambda x: x[1]
    )[1:6]

    for i in movie_list:
        index = i[0]

        # Correct movie_id (VERY IMPORTANT)
        movie_id = movies.iloc[index]['movie_id']
        #print(movie_id)

        # Append data
        recommended_movies.append(movies.iloc[index]['title'])
        recommended_movies_poster.append(fetch_poster(movie_id))

    return recommended_movies, recommended_movies_poster


# Load data
movies = pickle.load(open('movies.pkl', 'rb'))
similarity = pickle.load(open('similarity.pkl', 'rb'))

movies_list = movies['title'].values

# UI
st.title('🎬 Movie Recommendation System')

selected_movie_name = st.selectbox(
    "Select a movie",
    movies_list
)

# Button click
if st.button('Recommend'):
    names, posters = recommend(selected_movie_name)

    col1, col2, col3, col4, col5 = st.columns(5)

    with col1:
        st.image(posters[0])
        st.caption(names[0])

    with col2:
        st.image(posters[1])
        st.caption(names[1])

    with col3:
        st.image(posters[2])
        st.caption(names[2])

    with col4:
        st.image(posters[3])
        st.caption(names[3])

    with col5:
        st.image(posters[4])
        st.caption(names[4])