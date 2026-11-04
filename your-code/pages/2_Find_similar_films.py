import numpy as np
import streamlit as st
from sentence_transformers import SentenceTransformer

from sakila import query

st.set_page_config(page_title="Find similar films", page_icon="🔎")
st.title("🔎 Find similar films")


@st.cache_resource
def load_model():
    """TODO 7: load and return the sentence embedding model all-MiniLM-L6-v2 (Week 7, Day 2)."""
    return SentenceTransformer("all-MiniLM-L6-v2")


@st.cache_resource
def film_vectors():
    """TODO 8: read the title, description and rating of every film, embed the descriptions
    (normalised), and return the DataFrame and the vectors."""
    films = query("SELECT title, description, rating FROM film ORDER BY film_id")
    vectors = load_model().encode(films["description"].tolist(), normalize_embeddings=True)
    return films, vectors


# TODO 9: a st.text_area for the customer's description and a st.button("Get your recommendations").
#         When it is clicked: warn if the text is empty; otherwise embed it, compute the cosine similarity
#         with every film (a dot product, since the vectors are normalised), and show the top 3 films
#         with their title, rating and similarity.
request = st.text_area(
    "Describe the kind of film you want",
    placeholder="A thoughtful drama about a monk who discovers a shark in Australia",
)

if st.button("Get your recommendations"):
    if not request.strip():
        st.warning("Please describe the kind of film you are looking for first.")
    else:
        with st.spinner("Reading the 1,000 film descriptions (only slow the first time)..."):
            films, vectors = film_vectors()
        request_vector = load_model().encode([request], normalize_embeddings=True)[0]

        similarities = vectors @ request_vector          # dot product = cosine similarity (unit-length vectors)
        top_three = np.argsort(similarities)[::-1][:3]   # positions of the 3 highest scores, best first

        st.subheader("Your top three films")
        for position in top_three:
            film = films.iloc[position]
            st.markdown(
                f"**{film['title'].title()}** · rated {film['rating']} · similarity {similarities[position]:.2f}"
            )