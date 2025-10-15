import streamlit as st
import pickle
import pandas as pd
import requests
import gdown
import os
# =============================
# Fetch Poster Function

# =============================
similarity_file = "similarity.pkl"
similarity_drive_id = "1LOOfclrKgEXD10kJ9duHHH0Dui5MOk9d"  # Replace with your file ID

if not os.path.exists(similarity_file):
    gdown.download(f"https://drive.google.com/uc?id={similarity_drive_id}", similarity_file, quiet=False)

# =============================
# Load Data
# =============================


def fetch_poster(movie_id):
    response = requests.get(
        f'https://api.themoviedb.org/3/movie/{movie_id}?api_key=3e69dcf8d612f456577678b3eb902b32&language=en-US'
    )
    data = response.json()
    return "https://image.tmdb.org/t/p/w500/" + data['poster_path']

# =============================
# Recommend Function
# =============================
def recommend(movie):
    movie_index = movies[movies['title'] == movie].index[0]
    distances = similarity[movie_index]
    movies_list = sorted(list(enumerate(distances)), reverse=True, key=lambda x: x[1])[1:6]

    recommended_movies = []
    recommended_movies_poster = []
    for i in movies_list:
        movie_id = movies.iloc[i[0]].movie_id
        recommended_movies.append(movies.iloc[i[0]].title)
        recommended_movies_poster.append(fetch_poster(movie_id))
    return recommended_movies, recommended_movies_poster

# =============================
# Load Data
# =============================
movie_dict = pickle.load(open('movie_dict.pkl', 'rb'))
movies = pd.DataFrame(movie_dict)
similarity = pickle.load(open('similarity.pkl', 'rb'))

# =============================
# Netflix-style UI
# =============================
st.set_page_config(page_title="Movie Recommender", layout="wide")

# Custom CSS for Netflix-like UI
st.markdown("""
    <style>
    body {
        background-color: #141414;
        color: #ffffff;
    }
    .block-container {
        padding-top: 2rem;
        padding-bottom: 2rem;
        max-width: 90%;
    }
    h1 {
        color: #E50914;
        font-family: 'Arial Black', sans-serif;
    }
    .movie-title {
        text-align: center;
        font-size: 14px;
        margin-top: 8px;
        color: #ddd;
    }
    img {
        border-radius: 10px;
        transition: transform 0.3s;
    }
    img:hover {
        transform: scale(1.05);
    }
    </style>
""", unsafe_allow_html=True)

# =============================
# Header
# =============================
st.title("🎬 Movie Recommender System")
st.write("Find movies similar to your favorites")

# =============================
# Movie Selection
# =============================
selected_movie_name = st.selectbox(
    "Search for a movie:",
    movies['title'].values
)

# =============================
# Show Recommendations
# =============================
if st.button("Recommend"):
    names, posters = recommend(selected_movie_name)

    st.subheader("Recommended for you:")

    cols = st.columns(5)
    for i in range(5):
        with cols[i]:
            st.image(posters[i], use_container_width=True)
            st.markdown(f"<div class='movie-title'>{names[i]}</div>", unsafe_allow_html=True)
