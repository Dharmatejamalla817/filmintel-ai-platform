import streamlit as st
import requests
from google import genai
import json
import os

st.set_page_config(page_title="FilmIntel AI Enterprise", page_icon="🎬", layout="wide")
st.title("🎬 FilmIntel AI Enterprise Dashboard")
st.subheader("Enterprise Edition: Powered by Stable Native Document Intelligence")
st.markdown("---")

# Production Security
try:
    GOOGLE_API_KEY = st.secrets["GEMINI_API_KEY"]
    TMDB_API_KEY = st.secrets["TMDB_API_KEY"]
except:
    GOOGLE_API_KEY = ""
    TMDB_API_KEY = ""

# 📁 Native Storage Setup: Free, lightweight, and won't crash Python 3.14!
DB_FILE = "native_movie_db.json"

def load_native_db():
    if os.path.exists(DB_FILE):
        with open(DB_FILE, "r") as f:
            return json.load(f)
    return {}

def save_native_db(data):
    with open(DB_FILE, "w") as f:
        json.dump(data, f)

# Load existing memory records
movie_memory = load_native_db()

with st.sidebar:
    st.header("🔑 Configuration")
    user_api_key = GOOGLE_API_KEY if GOOGLE_API_KEY else st.text_input("Enter your Gemini API Key:", type="password")
    
    st.markdown("---")
    st.header("🧠 Train Your Custom Database")
    st.write("Paste reviews, articles, or scripts here to expand the AI's knowledge base permanently:")
    
    target_movie = st.text_input("Movie Name to Link Text To (e.g., Baahubali):").strip().lower()
    custom_text = st.text_area("Paste massive text data, background trivia, or script pages here:")
    
    if st.button("📥 Inject to Native Database"):
        if target_movie and custom_text:
            with st.spinner("Saving data to native brain..."):
                if target_movie not in movie_memory:
                    movie_memory[target_movie] = []
                
                # Store the custom text chunk neatly linked to that movie name
                movie_memory[target_movie].append(custom_text)
                save_native_db(movie_memory)
                st.success(f"Successfully added custom records to the '{target_movie}' database!")
        else:
            st.warning("Please provide both a movie name and text data.")

# Main Layout
movie_input = st.text_input("🎥 Target Movie Name (e.g., Baahubali):")
question_input = st.text_input("💬 Ask anything (The AI will search the web API AND your custom database memory):")

if st.button("🚀 Execute Hybrid Search"):
    if not user_api_key:
        st.error("Missing Gemini API Key!")
    elif not movie_input or not question_input:
        st.warning("Please fill out all fields.")
    else:
        with st.spinner("Synthesizing hybrid data streams..."):
            lookup_key = movie_input.strip().lower()
            
            # 1. Fetch from our Custom Native Document Database if it exists
            custom_context = "No custom internal documents or reviews found for this movie in the database."
            if lookup_key in movie_memory:
                custom_context = "\n---\n".join(movie_memory[lookup_key])
            
            # 2. Fetch basic structural numbers from TMDB API
            search_url = f"https://api.themoviedb.org/3/search/movie"
            web_context = "No structural data found on the live web API."
            if TMDB_API_KEY:
                try:
                    res = requests.get(search_url, params={"api_key": TMDB_API_KEY, "query": movie_input}).json()
                    if res.get('results'):
                        web_context = str(res['results'][0])
                except:
                    pass

            # 3. Compile everything together for the LLM
            prompt = f"""
            You are an elite, expert film industry analyst. Answer the user's question with deep insights by combining two distinct knowledge records.
            
            [SOURCE 1: LIVE WEB API METADATA]:
            {web_context}
            
            [SOURCE 2: PROPRIETARY CUSTOM DOCUMENTS & REVIEWS]:
            {custom_context}
            
            User Question: {question_input}
            
            Instructions: Provide a comprehensive, data-driven answer. If the information isn't in the web API but is inside the proprietary documents, draw directly from the documents to give a flawless answer.
            """
            
            try:
                client = genai.Client(api_key=user_api_key)
                response = client.models.generate_content(model='gemini-2.5-flash', contents=prompt)
                st.success("Analysis Complete!")
                st.markdown("### 🤖 Strategic Executive Briefing:")
                st.info(response.text)
            except Exception as e:
                st.error(f"AI Execution Error: {e}")
