# -*- coding: utf-8 -*-
"""pythonproject.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1nxqXISqCt3_lnuiUmaKlarhT6US9ZVqC
"""

import pandas as pd
import numpy as np
from ast import literal_eval
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity

tmdb_5000_credits_dataframe = pd.read_csv("tmdb_5000_credits.csv")
tmdb_5000_movies_dataframe = pd.read_csv("tmdb_5000_movies.csv")

tmdb_5000_movies_dataframe.head(2)

tmdb_5000_credits_dataframe.head(2)

del tmdb_5000_movies_dataframe['original_title']

tmdb_5000_movies_dataframe.head(2)

tmdb_5000_credits_dataframe.columns = ['id','title','cast','crew']

tmdb_5000_movies_dataframe = tmdb_5000_movies_dataframe.merge(tmdb_5000_credits_dataframe, on="id")

tmdb_5000_movies_dataframe.head(2)

del tmdb_5000_movies_dataframe['title_y']

tmdb_5000_movies_dataframe.head(2)

eval_column_list = ["cast", "crew", "keywords", "genres"]

for i in eval_column_list:
    tmdb_5000_movies_dataframe[i] = tmdb_5000_movies_dataframe[i].apply(literal_eval)

tmdb_5000_movies_dataframe[eval_column_list].head(2)

def get_director(x):
    for i in x:
        if i["job"] == "Director":
            return i["name"]
    return np.nan

def get_list(x):
    if isinstance(x, list):
        names = [i["name"] for i in x]
        print(names)
        if len(names) > 3:
            names = names[:3]

        return names

    return []

tmdb_5000_movies_dataframe["director"] = tmdb_5000_movies_dataframe["crew"].apply(get_director)

tmdb_5000_movies_dataframe["director"].head(5)

eval_column_list = ["cast", "keywords", "genres"]
for i in eval_column_list:
    tmdb_5000_movies_dataframe[i] = tmdb_5000_movies_dataframe[i].apply(get_list)

tmdb_5000_movies_dataframe["cast"].head()

tmdb_5000_movies_dataframe["keywords"].head()

tmdb_5000_movies_dataframe["genres"].head()

tmdb_5000_movies_dataframe[['title_x',"cast", "keywords", "genres"]].head(5)

tmdb_5000_movies_dataframe[['title_x', 'cast', 'director', 'keywords', 'genres']].head(2)

def clean_data(row):
    if isinstance(row, list):
        return [str.lower(i.replace(" ", "")) for i in row]
    else:
        if isinstance(row, str):
            return str.lower(row.replace(" ", ""))
        else:
            return ""

features = ['cast', 'keywords', 'director', 'genres']
for feature in features:
    tmdb_5000_movies_dataframe[feature] = tmdb_5000_movies_dataframe[feature].apply(clean_data)

tmdb_5000_movies_dataframe[['title_x', 'cast', 'director', 'keywords', 'genres']].head(2)

def determinents(features):
    return ' '.join(features['keywords']) + ' ' + ' '.join(features['cast']) + ' ' + features['director'] + ' ' + ' '.join(features['genres'])

tmdb_5000_movies_dataframe["determinents"] = tmdb_5000_movies_dataframe.apply(determinents, axis=1)

print(tmdb_5000_movies_dataframe[["title_x","determinents"]].head(5))

count_vectorizer = CountVectorizer(stop_words="english")
count_matrix = count_vectorizer.fit_transform(tmdb_5000_movies_dataframe["determinents"])
print(count_matrix.shape)

cosine_sim2 = cosine_similarity(count_matrix, count_matrix) 
print(cosine_sim2.shape)
movies_df = tmdb_5000_movies_dataframe.reset_index(drop=True)
indices = pd.Series(movies_df.index, index=movies_df['title_x'])

indices = pd.Series(movies_df.index, index=movies_df["title_x"]).drop_duplicates()
print(indices.head())

def get_recommendations(title, cosine_sim=cosine_sim2):
    idx = indices[title]
    similarity_scores = list(enumerate(cosine_sim[idx]))
    similarity_scores= sorted(similarity_scores, key=lambda x: x[1], reverse=True)
    similarity_scores=  similarity_scores[1:11]
    movies_indices = [ind[0] for ind in similarity_scores]
    movies = movies_df["title_x"].iloc[movies_indices]
    return movies

x=input("Enter Movie: -")
print("Recommendations for ",x)
print(get_recommendations(x, cosine_sim2))
print()
y=input('Enter Movie: -')
print("Recommendations for ",y)
print(get_recommendations(y, cosine_sim2))