import streamlit as st
import pickle
import pandas as pd
import requests

# Set page config
st.set_page_config(page_title="Movie Recommender", layout="wide")

# Apply custom CSS for background, font, and styling
st.markdown(
    """
    <style>
    /* Background and font settings */
    .stApp {
        background-color: #f4f4f9; /* Light background color */
        font-family: 'Arial', sans-serif;
    }

    /* Header styling */
    h1 {
        color: #2c3e50; /* Darker color for header text */
        text-align: left;
        font-weight: bold;
        font-size: 3em;
        margin-top: 20px;
        margin-left: 20px;
    }

    /* Movie title styling */
    .movie-title {
        color: #3498db; /* Vibrant blue color for movie titles */
        font-size: 1.2em;
        font-weight: bold;
        text-align: left;
        margin-top: 10px;
        text-shadow: 1px 1px 2px #dddddd;
    }

    /* Movie poster shadow */
    .movie-poster {
        box-shadow: 0px 4px 12px rgba(0, 0, 0, 0.3);
        border-radius: 8px;
        margin: 10px auto;
        max-width: 40%; /* Adjusted width */
        
    }

    /* Button styling */
    .stButton > button {
        background-color: #e74c3c; /* Red button color */
        color: #ffffff; /* White color for button text */
        border-radius: 12px;
        font-size: 1.2em;
        padding: 12px 20px;
        margin: 20px 0;
        display: block;
        border: none;
    }

    .stButton > button:hover {
        background-color: #c0392b; /* Darker red on hover */
    }

    /* Dropdown styling */
    .stSelectbox {
        color: #2c3e50; /* Dark color for dropdown text */
        background-color: #ffffff; /* White background for dropdown */
        border-radius: 8px;
        font-size: 1em;
        padding: 10px;
        margin-left: 20px;
        border: 1px solid #bdc3c7; /* Light border color */
    }

    /* Dropdown label styling */
    .stSelectbox > div > label {
        color: #2c3e50; /* Dark color for dropdown label text */
        font-size: 1.2em;
        margin-left: 20px;
    }

    /* Overall container styling */
    .stContainer {
        background-color: #ffffff; /* White background for container */
        padding: 30px;
        border-radius: 15px;
        margin-top: 30px;
        box-shadow: 0px 4px 12px rgba(0, 0, 0, 0.1); /* Light shadow for container */
        text-align: left; /* Align everything to the left */
    }

    </style>
    """,
    unsafe_allow_html=True
)

def fetch_poster(movie_id):
    url = f"https://api.themoviedb.org/3/movie/{movie_id}?api_key=ef97600648bb5286653718f43a22dd04&language=en-US"
    data = requests.get(url).json()
    poster_path = data['poster_path']
    full_path = "https://image.tmdb.org/t/p/w500/" + poster_path
    return full_path

def recommend(movie):
    index = movies[movies['title'] == movie].index[0]
    distances = sorted(list(enumerate(similarity[index])), reverse=True, key=lambda x: x[1])
    recommended_movie_names = []
    recommended_movie_posters = []
    for i in distances[1:6]:
        # fetch the movie poster
        movie_id = movies.iloc[i[0]].movie_id
        recommended_movie_posters.append(fetch_poster(movie_id))
        recommended_movie_names.append(movies.iloc[i[0]].title)

    return recommended_movie_names, recommended_movie_posters

# Header
st.markdown("<h1>Movie Recommender System</h1>", unsafe_allow_html=True)

movies = pickle.load(open('movies.pkl', 'rb'))
similarity = pickle.load(open('similarity.pkl', 'rb'))

movie_list = movies['title'].values
selected_movie = st.selectbox(
    "Type or select a movie from the dropdown",
    movie_list,
)

if st.button('Show Recommendation'):
    recommended_movie_names, recommended_movie_posters = recommend(selected_movie)
    col1, col2, col3, col4, col5 = st.columns(5)

    with col1:
        st.markdown(f"<p class='movie-title'>{recommended_movie_names[0]}</p>", unsafe_allow_html=True)
        st.markdown(f"<img src='{recommended_movie_posters[0]}' class='movie-poster'>", unsafe_allow_html=True)
    with col2:
        st.markdown(f"<p class='movie-title'>{recommended_movie_names[1]}</p>", unsafe_allow_html=True)
        st.markdown(f"<img src='{recommended_movie_posters[1]}' class='movie-poster'>", unsafe_allow_html=True)
    with col3:
        st.markdown(f"<p class='movie-title'>{recommended_movie_names[2]}</p>", unsafe_allow_html=True)
        st.markdown(f"<img src='{recommended_movie_posters[2]}' class='movie-poster'>", unsafe_allow_html=True)
    with col4:
        st.markdown(f"<p class='movie-title'>{recommended_movie_names[3]}</p>", unsafe_allow_html=True)
        st.markdown(f"<img src='{recommended_movie_posters[3]}' class='movie-poster'>", unsafe_allow_html=True)
    with col5:
        st.markdown(f"<p class='movie-title'>{recommended_movie_names[4]}</p>", unsafe_allow_html=True)
        st.markdown(f"<img src='{recommended_movie_posters[4]}' class='movie-poster'>", unsafe_allow_html=True)
