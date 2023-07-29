# streamlit_app.py
import pandas as pd
import streamlit as st
from google.oauth2 import service_account
from google.cloud import bigquery

# Create API client.
credentials = service_account.Credentials.from_service_account_info(
    st.secrets["gcp_service_account"]
)
client = bigquery.Client(credentials=credentials)

# Perform query.
# Uses st.cache_data to only rerun when the query changes or after 10 min.
@st.cache_data(ttl=600)
def run_query(query):
    query_job = client.query(query)
    rows_raw = query_job.result()
    # Convert to list of dicts. Required for st.cache_data to hash the return value.
    rows = [dict(row) for row in rows_raw]
    return rows


movie_source = "https://raw.githubusercontent.com/Shungu/unifi-data-engineer/main/movies.csv"
movies = pd.read_csv(movie_source).head(10)
#rows = "C:/Users/shung_on75qpk/OneDrive/Documents/Unifi Data Engineer/ml-25m/ratings.csv"
rows = run_query("SELECT * FROM `unifi-data-engineer.MovieRecommendation.Ratings`")
ratings = pd.DataFrame(rows).head(10)
# Print results.
st.table(movies)
st.table(ratings)
