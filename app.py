import streamlit as st
from recommender import load_data, get_recommendations

st.title("🎬 Movie Recommendation System")

# Load movie data
data = load_data()

# Movie selection
movie_list = data['title'].tolist()
selected_movie = st.selectbox("Select a movie you like:", movie_list)

# Genre filtering
genre_list = data['genre'].unique().tolist()
selected_genre = st.selectbox("Select a genre:", ["All"] + genre_list)

# Slider for number of recommendations
num_recommendations = st.slider('How many recommendations?', min_value=1, max_value=10, value=5)

# Optional: Add a search box
search_text = st.text_input("Or search for a movie:")
if search_text:
    filtered_movies = [title for title in movie_list if search_text.lower() in title.lower()]
    if filtered_movies:
        selected_movie = st.selectbox("Matching movies:", filtered_movies)
    else:
        st.warning("No movies found.")

# Recommend button
if st.button("Recommend"):
    # Call the recommendation function
    recommendations = get_recommendations(selected_movie, data, selected_genre, num_recommendations)

    # Display the recommended movies
    st.write("### Recommended Movies:")
    for movie in recommendations:
        movie_data = data[data['title'] == movie]
        if not movie_data.empty:
            poster_url = movie_data.iloc[0]['poster_url']
            st.image(poster_url, width=150)
            st.write(f"👉 {movie}")
        else:
            st.write(f"👉 {movie} (Poster not found)")
