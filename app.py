import streamlit as st
import pickle
import pandas as pd
import requests
import os
import gdown

def download_file_from_drive(file_id, destination):
    url = f'https://drive.google.com/uc?id={file_id}'
    gdown.download(url, output=destination, quiet=False)

def is_valid_pickle_file(file_path):
    try:
        with open(file_path, "rb") as f:
            pickle.load(f)
        return True
    except Exception:
        return False

# Download the similarity.pkl file from Google Drive using gdown
def ensure_similarity_file(file_id, local_path):
    if not os.path.exists(local_path) or not is_valid_pickle_file(local_path):
        download_file_from_drive(file_id, local_path)
        if not is_valid_pickle_file(local_path):
            st.error("The downloaded file is not a valid pickle. Please check the file ID or permissions.")
            st.stop()

file_id = "16qftb-hYK9qdnc2ZOPSP8awthhb_vyNS"
similarity_file = "similarity.pkl"
ensure_similarity_file(file_id, similarity_file)
similarity = pickle.load(open(similarity_file, "rb"))

# Set app background

def set_background(image_url):
    st.markdown(
        f"""
        <style>
        .stApp {{
            background-image: url(\"{image_url}\");
            background-size: cover;
            background-position: center;
            background-repeat: no-repeat;
        }}
        </style>
        """,
        unsafe_allow_html=True
    )

set_background("https://4kwallpapers.com/images/walls/thumbs_3t/4845.jpg")

# Fetch poster helper
def fetch_poster(movie_id):
    response = requests.get(
        f'https://api.themoviedb.org/3/movie/{movie_id}?api_key=69f5cea05ad0d7ad5c34a00fa93b3462&language=en-US'
    )
    data = response.json()
    return f"https://image.tmdb.org/t/p/w500/{data.get('poster_path', '')}"

# Recommendation logic
def recommend(movie_name):
    idx = movies[movies['title'] == movie_name].index[0]
    distances = similarity[idx]
    pairs = sorted(list(enumerate(distances)), key=lambda x: x[1], reverse=True)[1:6]

    names, posters = [], []
    for i, _ in pairs:
        movie_id = movies.iloc[i]['movie_id']
        names.append(movies.iloc[i]['title'])
        posters.append(fetch_poster(movie_id))
    return names, posters

# Load movies list
movies_dict = pickle.load(open('movies.pkl', 'rb'))
movies = pd.DataFrame(movies_dict)

# Streamlit UI
st.title('Movie Recommender System')
selected = st.selectbox('Type or select a movie:', movies['title'].values)
if st.button('Show Recommendation'):
    names, posters = recommend(selected)
    cols = st.columns(5)
    for col, name, poster in zip(cols, names, posters):
        with col:
            st.text(name)
            st.image(poster)  
