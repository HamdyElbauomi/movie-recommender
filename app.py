import streamlit as st
import pickle
import pandas as pd
import requests
import base64
import os

def download_file_from_drive(file_id, destination):
    url = f"https://drive.google.com/uc?id={file_id}"
    response = requests.get(url)
    if response.status_code == 200:
        with open(destination, "wb") as f:
            f.write(response.content)
    else:
        st.error("Failed to download the file. Please check the file ID or permissions.")

def is_valid_pickle_file(file_path):
    try:
        with open(file_path, "rb") as f:
            pickle.load(f)
        return True
    except Exception:
        return False

# Download the similarity.pkl file from Google Drive
file_id = "16qftb-hYK9qdnc2ZOPSP8awthhb_vyNS"  # Replace with your actual file ID
similarity_file = "similarity.pkl"

if not os.path.exists(similarity_file):
    download_file_from_drive(file_id, similarity_file)

if not is_valid_pickle_file(similarity_file):
    st.error("The downloaded file is not a valid pickle file. Please check the source.")
else:
    similarity = pickle.load(open(similarity_file, "rb"))


def set_background(image_url):
    st.markdown(
        f"""
        <style>
        .stApp {{
            background-image: url("{image_url}");
            background-size: cover;
            background-position: center;
            background-repeat: no-repeat;
        }}
        </style>
        """,
        unsafe_allow_html=True
    )

# Use the  image URL
set_background("https://4kwallpapers.com/images/walls/thumbs_3t/4845.jpg")

 


def fetch_poster(movie_id):
    response = requests.get(f'https://api.themoviedb.org/3/movie/{movie_id}?api_key=69f5cea05ad0d7ad5c34a00fa93b3462&language=en-US')
    response_json = response.json()
    return "https://image.tmdb.org/t/p/w500/" + response_json['poster_path']

def recommend(movie_name):
    movie_index = movies[movies['title'] == movie_name].index[0]
    distances = similarity[movie_index]
    movie_list = sorted(list(enumerate(distances)), reverse=True, key=lambda x: x[1])[1:6]

    recommended_movies = []
    recommended_movies_posters = []

    for i in movie_list:
        index = i[0]
        movie_id = index
        # fetch poster from API
        recommended_movies.append(movies.iloc[index]['title'])
        recommended_movies_posters.append(fetch_poster(movies.iloc[index]['movie_id']))

    return recommended_movies, recommended_movies_posters


moveies_dict = pickle.load(open('movies.pkl', 'rb'))
movies = pd.DataFrame(moveies_dict)

# similarity = pickle.load(open('https://drive.google.com/file/d/16qftb-hYK9qdnc2ZOPSP8awthhb_vyNS/view?usp=sharing', 'rb'))

st.title('Movie Recommender System')
selected_movie_name = st.selectbox(
    'Type or select a movie from the dropdown',
    movies['title'].values)

if st.button('Show Recommendation'):
    names, posters =  recommend(selected_movie_name)
    col1, col2, col3, col4, col5 = st.columns(5)
    with col1:
        st.text(names[0])
        st.image(posters[0])
    with col2:
        st.text(names[1])
        st.image(posters[1])

    with col3:
        st.text(names[2])
        st.image(posters[2])
    with col4:
        st.text(names[3])
        st.image(posters[3])
    with col5:
        st.text(names[4])
        st.image(posters[4])
    
