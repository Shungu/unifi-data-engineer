import streamlit as st
import pandas as pd
import numpy as np
##movies = ["Jumanji","Ghost Busters","Rambo","Shark Attack"]

movie_source = "C:/Users/shung_on75qpk/OneDrive/Documents/Unifi Data Engineer/ml-25m/movies.csv"
movies = pd.read_csv(movie_source)
movie_title = movies["title"]

ratings_source = "C:/Users/shung_on75qpk/OneDrive/Documents/Unifi Data Engineer/ml-25m/ratings.csv"
ratings = pd.read_csv(ratings_source)

import re
def clean_movie_title(title):
    title = re.sub("[^a-zA-Z0-9 ]", "", title)
    return title

from sklearn.metrics.pairwise import cosine_similarity
def search(title):
    title = clean_movie_title(title)
    vector = vectorizer.transform([title])
    similarity = cosine_similarity(vector, tfidf).flatten()

    indices = np.argpartition(similarity, -10)[-10:]

    results = movies.iloc[indices].iloc[::-1]
    return results

def find_movie_id(movie_name):
    join_movie_users = pd.merge(movies , ratings, on="movieId")
    join_movie_users = join_movie_users[join_movie_users["title"] == movie_name]
    movie_id = join_movie_users["movieId"].unique()
    movie_id = movie_id[0]
    return movie_id

def find_similar_movies(movie_id):
    similar_users = ratings[(ratings["movieId"] == movie_id) & (ratings["rating"] >= 4)]["userId"].unique()
    similar_user_movies = ratings[(ratings["userId"].isin(similar_users)) & (ratings["rating"] >= 4)]["movieId"]
    similar_user_ratings = similar_user_movies.value_counts() / len(similar_users)
    high_similar_user_ratings = similar_user_ratings[similar_user_ratings > .10]

    all_users = ratings[(ratings["movieId"].isin(high_similar_user_ratings.index)) & (ratings["rating"] >= 4)]
    all_user_ratings = all_users["movieId"].value_counts() / len(all_users["userId"].unique())
    rec_percentages = pd.concat([high_similar_user_ratings, all_user_ratings], axis=1)
    rec_percentages.columns = ["similar users", "all users"]
    rec_percentages["score"] = rec_percentages["similar users"] / rec_percentages["all users"]
    rec_percentages = rec_percentages.sort_values("score", ascending=False)
    rec_percentages = rec_percentages.head(11).merge(movies, left_index=True, right_on="movieId")[["title"]]
    return rec_percentages


st.header("Movie and TV Show Recommendation Engine")
st.markdown(
    """
    <style>
    .reportview-container {
        background: url("https://wallpapercave.com/wp/p4iaEa4.jpg");
    }
   </style>
    """,
    unsafe_allow_html=True
)
st.markdown("<h4 style='text-align: center; color: red;'>Created by Shungu Dhlamini</h4>", unsafe_allow_html=True)
selected_value = st.selectbox("Select a movie you have watched from the drop down", movie_title)

if st.button("Recommend My Movies"):
    movie_id = find_movie_id(selected_value)
    movie_recommendation = find_similar_movies(movie_id)
    top_rated_header = f'Top Rated by people who also watched: { selected_value }'
    st.markdown(top_rated_header, unsafe_allow_html=True)
    movie_recommendation = movie_recommendation.tail(10)
    recommendations = st.table(movie_recommendation)
