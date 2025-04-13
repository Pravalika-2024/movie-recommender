import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

def load_data():
    return pd.read_csv("movies.csv")

def get_recommendations(title, data, selected_genre="All", top_n=5):
    # Optionally filter data by genre
    if selected_genre != "All":
        data = data[data['genre'] == selected_genre]

    # Fill NA in 'description' column to avoid errors
    data['description'] = data['description'].fillna("")

    # Vectorize the descriptions
    tfidf = TfidfVectorizer(stop_words='english')
    tfidf_matrix = tfidf.fit_transform(data['description'])

    # Compute cosine similarity
    cosine_sim = cosine_similarity(tfidf_matrix, tfidf_matrix)

    # Get the index of the selected movie
    try:
        idx = data[data['title'] == title].index[0]
    except IndexError:
        return []

    # Get similarity scores
    sim_scores = list(enumerate(cosine_sim[idx]))
    sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)

    # Get indices of top_n similar movies (excluding the selected one)
    sim_scores = sim_scores[1:top_n+1]
    movie_indices = [i[0] for i in sim_scores]

    return data.iloc[movie_indices]['title'].tolist()
