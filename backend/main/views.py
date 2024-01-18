from django.shortcuts import render
import pandas as pd
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
import os
import re
# Create your views here.

movies = pd.read_csv(os.path.join(os.path.dirname(__file__), 'data', 'movies_new.csv'))
ratings = pd.read_csv(os.path.join(os.path.dirname(__file__), 'data', 'ratings_new.csv'))

vectorizer_title = TfidfVectorizer(ngram_range=(1,2))
title_vect = vectorizer_title.fit_transform(movies["title"].astype(str))

def clean_title(title):
  return re.sub(r"[^a-zA-Z0-9 ]", "", title)
def clean_genres(genres):
  return re.sub(r"[^a-zA-Z0-9 ]", " ", genres)

def show_movies(movie_title):
  movie_title = clean_title(movie_title.title())
  movie_title_vect = vectorizer_title.transform([movie_title])
  similarity = cosine_similarity(movie_title_vect, title_vect).flatten()
  max_value_title = np.argpartition(similarity, -4)[-1]
  locate_title = movies.iloc[max_value_title]
  return locate_title


class PredictAPIView(APIView):
    def post(self, request, *args, **kwargs):
        try:
            movie_title = request.data.get("title")
            
            movieId = show_movies(movie_title)["movieId"]
            user_like_movie = ratings[(ratings['movieId'] == movieId) & (ratings["rating"] > 4.5)]['userId']
            movies_users_like_prev = ratings[(ratings["userId"].isin(user_like_movie)) & (ratings["rating"] > 4.5)]["movieId"]
            similar_movies = movies_users_like_prev.value_counts() / len(user_like_movie)
            similar_movies = similar_movies[similar_movies > 0.1]
            users_like = ratings[(ratings["movieId"].isin(similar_movies.index)) & (ratings['rating'] > 4.5)]
            users_fav = users_like["movieId"].value_counts() / len(users_like["userId"].unique())
            recs = pd.concat([similar_movies, users_fav], axis=1)
            recs.columns = ["Similar", "All"]
            recs['score'] = recs["Similar"] / recs["All"]
            recommend = recs.sort_values("score", ascending=False)
            head = recommend.head(15).merge(movies, left_index=True, right_on="movieId")[["score", 'title', "genres"]]
            return Response({"data": head}, status=status.HTTP_200_OK)      
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
            