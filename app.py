import streamlit as st
import requests
from google import genai
import wikipediaapi
import json

st.set_page_config(page_title="Indian FilmIntel Pro", page_icon="🎬", layout="wide")

st.title("🎬 Indian FilmIntel AI Platform")
st.subheader("Pro Edition: Zero-Crash Autonomous Web & OTT Research Agent")
st.markdown("---")

try:
    GOOGLE_API_KEY = st.secrets["GEMINI_API_KEY"]
except:
    GOOGLE_API_KEY = ""

with st.sidebar:
    st.header("🔑 System Access")
    use_custom_key = st.checkbox("🔑 Use my own Gemini API Key (If system quota is full)")
    user_api_key = st.text_input("Enter personal API Key:", type="password") if use_custom_key else GOOGLE_API_KEY
    
    st.markdown("---")
    st.info("⚡ **Pro Optimizations Active:**\n* **Local Cache Engine:** Keeps server alive.\n* **Live OTT Web Scraping:** Pulls active news data outside of Wikipedia.")

# 🧠 SPEED CACHE 1: Cache Wikipedia downloads so we don't spam the server
@st.cache_data(show_spinner=False)
def fetch_wikipedia_data(movie_name):
    wiki_agent = wikipediaapi.Wikipedia(
        user_agent="FilmIntelIndiaAppPro/2.0 (contact: admin@filmintelai.com)", language="en"
    )
    page = wiki_agent.page(movie_name)
    if page.exists():
        return page.title, page.text[:7000] # Grab core structure and charts
    return movie_name, "No direct encyclopedic records found."

# 🌐 OTT LIVE SCRAPER: Background web agent to find streaming rights news
@st.cache_data(show_spinner=False)
def fetch_live_ott_news(movie_name):
    search_query = f"{movie_name} official digital streaming rights OTT platform"
    url = f"https://html.duckduckgo.com/html/?q={requests.utils.quote(search_query)}"
    try:
        headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"}
        res = requests.get(url, headers=headers, timeout=10)
        # Quick and robust extraction of snippet headers from search entries
        from bs4 import BeautifulSoup
        soup = BeautifulSoup(res.text, "html.parser")
        snippets = [s.text.strip() for s in soup.find_all('a', class_='result__snippet')[:4]]
        return "\n".join(snippets) if snippets else "No direct active OTT headlines found."
    except:
        return "Live web research stream temporarily unavailable."

# 🤖 MAIN LLM GENERATION CACHE: Prevents duplicate questions from consuming tokens
@st.cache_data(show_spinner=False)
def run_cached_ai_analysis(api_key, movie, question, wiki_data, ott_data):
    prompt = f"""
    You are the absolute premier business consultant for the Indian Film Industry (Tollywood, Bollywood, and South Indian cinema).
    Answer the user's question completely. You have been provided two real-time text sources pulled from the internet.
    
    [SOURCE 1: WIKIPEDIA ARCHIVES FOR HISTORICALS, CREW & BOX OFFICE]:
    {wiki_data}
    
    [SOURCE 2: LIVE WEB NEWS SNIPPETS FOR OTT/STREAMING RIGHTS]:
    {ott_data}
    
    User Question: {question}
    
    Instructions:
    1. Deliver a highly polished report using clean headings, sections, and clear bullet points.
    2. Focus heavily on specifying who directed, who produced, budget structures, final box office profit/loss, and explicitly state which digital platform (Netflix, Prime, Hotstar, Aha, Zee5, etc.) owns the OTT streaming rights based on Source 2 news or Source 1 tracking.
    3. If the data is missing from the text sources, use your internal industry weights to provide the best verified industry answer.
    """
    
    client = genai.Client(api_key=api_key)
    # Using the fast model with a fallback attempt matrix
    for model_node in ["gemini-2.5-flash", "gemini-2.0-flash"]:
        try:
            response = client.models.generate_content(model=model_node, contents=prompt)
            return response.text, True, False
        except Exception as e:
            if "429" in str(e) or "RESOURCE_EXHAUSTED" in str(e):
                continue
    return None, False, True

# App Layout Input Matrix
movie_input = st.text_input("🎥 Enter Indian Movie Name (e.g., Baahubali, RRR, Devara, Pokiri, Pushpa):")
question_input = st.text_input("💬 Ask anything (e.g., Give me a full profit breakdown and who bought OTT rights?):")

if st.button("🚀 Execute Hybrid Intelligence Analysis"):
    if not user_api_key:
        st.error("Please ensure a valid Gemini API Key is active!")
    elif not movie_input or not question_input:
        st.warning("Please fill out both entry parameters.")
    else:
        with st.spinner("🧠 Web Agent scanning Wikipedia records & live streaming news feeds..."):
            
            # Step 1 & 2: Pull text from both data pipelines efficiently
            wiki_title, wiki_text = fetch_wikipedia_data(movie_input)
            ott_news_text = fetch_live_ott_news(movie_input)
            
            # Step 3: Run the cached generation logic
            analysis_output, success, quota_blocked = run_cached_ai_analysis(
                user_api_key, movie_input, question_input, wiki_text, ott_news_text
            )
            
            if success:
                st.success(f"📈 Strategic Briefing Completed for {wiki_title}!")
                st.markdown("### 🤖 FilmIntel Executive Briefing:")
                st.info(analysis_output)
            elif quota_blocked:
                st.error("🚨 Google Free-Tier Daily Quota Exhausted! Please activate 'Use my own Gemini API Key' in the sidebar to keep analyzing completely unrestricted.")
            else:
                st.error("All server clusters are currently congested. Please wait a moment and try again.")
