import streamlit as st
import requests
from google import genai

st.set_page_config(page_title="FilmIntel AI Enterprise", page_icon="🎬", layout="wide")

st.title("🎬 FilmIntel AI Enterprise Dashboard")
st.subheader("Hybrid Intelligence: Live Web Data + Custom Industry Documents")
st.markdown("---")

# 🔐 Production Security: Pulling keys from the cloud environment secrets instead of hardcoding
try:
    GOOGLE_API_KEY = st.secrets["GEMINI_API_KEY"]
    TMDB_API_KEY = st.secrets["TMDB_API_KEY"]
except:
    # Fallback for local testing if secrets aren't set yet
    GOOGLE_API_KEY = ""
    TMDB_API_KEY = ""

# Sidebar Configuration
with st.sidebar:
    st.header("🔑 Configuration")
    # If keys aren't in cloud secrets, let users type them manually
    if not GOOGLE_API_KEY:
        user_api_key = st.text_input("Enter your Gemini API Key:", type="password")
    else:
        user_api_key = GOOGLE_API_KEY
        st.success("🔒 System API Key Connected Securely")
        
    st.markdown("---")
    st.header("📂 Upload Knowledge Base")
    uploaded_file = st.file_uploader("Upload internal notes, scripts, or reviews (.txt format):", type=["txt"])
    
    document_contents = ""
    if uploaded_file is not None:
        document_contents = uploaded_file.read().decode("utf-8")
        st.success("📄 Custom Document Loaded!")

def fetch_live_web_data(movie_name):
    if not TMDB_API_KEY:
        st.error("Missing TMDB API Key configuration.")
        return None
    search_url = "https://api.themoviedb.org/3/search/movie"
    try:
        response = requests.get(search_url, params={"api_key": TMDB_API_KEY, "query": movie_name}, timeout=15)
        data = response.json()
        if not data.get('results'): return None
        movie_id = data['results'][0]['id']
        details_url = f"https://api.themoviedb.org/3/movie/{movie_id}"
        return requests.get(details_url, params={"api_key": TMDB_API_KEY}, timeout=15).json()
    except:
        return None

# Main Layout
col1, col2 = st.columns([1, 1])
with col1:
    movie_input = st.text_input("🎥 Target Movie Name:", placeholder="e.g., Baahubali")
with col2:
    question_input = st.text_input("💬 Ask your deep industry or script question:", placeholder="e.g., Why did the budget increase?")

if st.button("🚀 Run Deep Evaluation"):
    if not user_api_key:
        st.error("Please provide a valid Gemini API Key!")
    elif not movie_input or not question_input:
        st.warning("Please fill out all search and question fields.")
    else:
        with st.spinner("Processing deep hybrid intelligence queries..."):
            raw_web_data = fetch_live_web_data(movie_input)
            
            doc_context = f"\n[UPLOADED DOCUMENT RECORDS]:\n{document_contents}" if document_contents else "\n(No custom document uploaded)"
            web_context = f"\n[LIVE DATABASE RECORDS]:\n{raw_web_data}" if raw_web_data else "\n(No web data found)"
            
            prompt = f"""
            You are a premier executive film consultant. Analyze this query using two sources.
            {web_context}
            {doc_context}
            User Question: {question_input}
            Instructions: Answer exhaustively. Synthesize web records and custom documents seamlessly.
            """
            
            try:
                client = genai.Client(api_key=user_api_key)
                response = client.models.generate_content(model='gemini-2.5-flash', contents=prompt)
                st.success("📊 Strategic Analysis Complete!")
                st.info(response.text)
            except Exception as ai_err:
                st.error(f"AI System Error: {ai_err}")
