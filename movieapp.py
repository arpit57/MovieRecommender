import streamlit as st
import pickle
import numpy as np
st.title("Movie Recommender")

movies = pickle.load(open("movie_list.pkl", "rb"))

s0 = pickle.load(open("similarity.pkl_0.pkl", 'rb'))
s1 = pickle.load(open("similarity.pkl_1.pkl", 'rb'))
similarity = np.concatenate((s0, s1))
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
