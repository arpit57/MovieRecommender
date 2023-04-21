import streamlit as st
import pickle
import numpy as np
import pandas as pd
import sqlite3

st.title("Movie Recommender")

movies = pickle.load(open("movie_list.pkl", "rb"))

num_chunks = 5
retrieved_similarity = []

for chunk_idx in range(num_chunks):
    # Connect to the SQLite database for the current chunk
    conn = sqlite3.connect(f'similarity_chunk_{chunk_idx}.db')
    c = conn.cursor()

    # Read the data from the table
    c.execute("SELECT * FROM similarity")
    rows = c.fetchall()

    for row in rows:
        row_id, data = row
        numpy_row = np.frombuffer(data, dtype=float)
        retrieved_similarity.append(numpy_row)

    # Close the connection
    conn.close()

similarity = np.array(retrieved_similarity)



# s0 = pickle.load(open("similarity.pkl_0.pkl", 'rb'))
# s1 = pickle.load(open("similarity.pkl_1.pkl", 'rb'))
# s2 = pickle.load(open("similarity.pkl_2.pkl", 'rb'))
# s3 = pickle.load(open("similarity.pkl_3.pkl", 'rb'))
# s4 = pickle.load(open("similarity.pkl_4.pkl", 'rb'))

# similarity = np.concatenate((s0, s1, s2, s3, s4))

# similarity = pickle.load(open("similarity.pkl", 'rb'))
# print(movies)
selectedMovie = st.selectbox("", movies.title)



def recommend(movie):
    index = movies[movies['title'].apply(lambda x:x.lower()) == movie.lower()].index[0]
    distances = sorted(list(enumerate(similarity[index])),reverse=True,key = lambda x: x[1])
    l = []
    for i in distances[1:11]:
    	l.append(f"{movies.iloc[i[0]].title:<60} {movies.iloc[i[0]].year:<10} {movies.iloc[i[0]].rating}")
        # print(f"{movies.iloc[i[0]].title} ({movies.iloc[i[0]].year}, {movies.iloc[i[0]].rating}*)")
    return l

if st.button("Recommend"):
	st.text(f"{'Title' : <60} {'Year' : <10} {'Rating'}")
	for i in recommend(selectedMovie):
			st.text(i)
