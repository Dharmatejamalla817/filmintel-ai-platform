import streamlit as st
import requests
from google import genai
import chromadb

st.set_page_config(page_title="FilmIntel AI Enterprise", page_icon="🎬", layout="wide")
st.title("🎬 FilmIntel AI Enterprise Dashboard")
st.subheader("Enterprise Edition: Powered by Local Vector Intelligence")
st.markdown("---")

# Production Security
try:
    GOOGLE_API_KEY = st.secrets["GEMINI_API_KEY"]
    TMDB_API_KEY = st.secrets["TMDB_API_KEY"]
except:
    GOOGLE_API_KEY = ""
    TMDB_API_KEY = ""

# Initialize Database Client inside the server memory
@st.cache_resource
def get_vector_db():
    # Creates a persistent database folder on the cloud server
    chroma_client = chromadb.PersistentClient(path="./filminte_vector_db")
    return chroma_client.get_or_create_collection(name="movie_knowledge")

collection = get_vector_db()

with st.sidebar:
    st.header("🔑 Configuration")
    user_api_key = GOOGLE_API_KEY if GOOGLE_API_KEY else st.text_input("Enter your Gemini API Key:", type="password")
    
    st.markdown("---")
    st.header("🧠 Train Your Custom Database")
    st.write("Paste reviews, articles, or scripts here to permanently expand the AI's knowledge base:")
    
    doc_title = st.text_input("Document Label (e.g., Baahubali Trivia):")
    custom_text = st.text_area("Paste massive text data here:")
    
    if st.button("📥 Inject to Vector Database"):
        if doc_title and custom_text:
            with st.spinner("Embedding text into vectors..."):
                # Slicing text into paragraphs and saving it into the vector engine
                paragraphs = [p.strip() for p in custom_text.split("\n\n") if p.strip()]
                for i, para in enumerate(paragraphs):
                    collection.add(
                        documents=[para],
                        ids=[f"{doc_title}_{i}"]
                    )
                st.success(f"Successfully trained database with {len(paragraphs)} records!")
        else:
            st.warning("Please provide both a label and text.")

# Main Interface
movie_input = st.text_input("🎥 Target Movie Name:")
question_input = st.text_input("💬 Ask anything (The AI will search the web AND your custom vector database):")

if st.button("🚀 Execute Hybrid Search"):
    if not user_api_key:
        st.error("Missing Gemini API Key!")
    elif not movie_input or not question_input:
        st.warning("Please fill out all fields.")
    else:
        with st.spinner("Searching semantic database fields..."):
            # 1. Query the local Vector Database for matching text blocks based on meaning
            db_results = collection.query(query_texts=[question_input], n_results=3)
            vector_context = "\n".join(db_results['documents'][0]) if db_results['documents'] else "No relevant custom records found."
            
            # 2. Fetch basic structural numbers from TMDB
            search_url = f"https://api.themoviedb.org/3/search/movie"
            web_context = "No structural data found."
            if TMDB_API_KEY:
                try:
                    res = requests.get(search_url, params={"api_key": TMDB_API_KEY, "query": movie_input}).json()
                    if res.get('results'):
                        web_context = str(res['results'][0])
                except:
                    pass

            # 3. Compile everything for Gemini
            prompt = f"""
            You are an expert film industry analyst. Answer the user's question by combining live web metadata and our custom vector database records.
            
            [LIVE WEB DATABASE ROWS]:
            {web_context}
            
            [SEMANTIC VECTOR DATABASE PARAGRAPHS]:
            {vector_context}
            
            User Question: {question_input}
            """
            
            try:
                client = genai.Client(api_key=user_api_key)
                response = client.models.generate_content(model='gemini-2.5-flash', contents=prompt)
                st.success("Analysis Complete!")
                st.info(response.text)
            except Exception as e:
                st.error(f"AI Execution Error: {e}")
