import streamlit as st
import requests
import wikipediaapi
from bs4 import BeautifulSoup
from groq import Groq

st.set_page_config(page_title="Indian FilmIntel Llama-Core", page_icon="🎬", layout="wide")

st.title("🎬 Indian FilmIntel AI Platform")
st.subheader("Llama-Core Edition: High-Speed Autonomous Cinema Agent")
st.markdown("---")

# Load secure system key for Groq
try:
    SYSTEM_GROQ_KEY = st.secrets["GROQ_API_KEY"]
except:
    SYSTEM_GROQ_KEY = ""

with st.sidebar:
    st.header("🔑 System Access")
    use_custom_key = st.checkbox("🔑 Use my own Groq API Key")
    user_api_key = st.text_input("Enter personal Groq Key:", type="password") if use_custom_key else SYSTEM_GROQ_KEY
    
    st.markdown("---")
    st.info("⚡ **Groq LPU Engine Active:** Powered by Meta Llama-3 architecture for ultra-high-speed South Indian cinema analysis with zero lag.")

# Local caching setups to protect performance limits
@st.cache_data(show_spinner=False)
def fetch_wikipedia_data(movie_name):
    wiki_agent = wikipediaapi.Wikipedia(
        user_agent="FilmIntelIndiaGroq/1.0 (contact: admin@filmintel.com)", language="en"
    )
    page = wiki_agent.page(movie_name)
    if page.exists():
        return page.title, page.text[:8000]
    return movie_name, "No direct encyclopedic records found."

@st.cache_data(show_spinner=False)
def fetch_live_ott_news(movie_name):
    search_query = f"{movie_name} official digital streaming rights OTT platform news"
    url = f"https://html.duckduckgo.com/html/?q={requests.utils.quote(search_query)}"
    try:
        headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"}
        res = requests.get(url, headers=headers, timeout=10)
        soup = BeautifulSoup(res.text, "html.parser")
        snippets = [s.text.strip() for s in soup.find_all('a', class_='result__snippet')[:4]]
        return "\n".join(snippets) if snippets else "No direct active OTT headlines found."
    except:
        return "Live web research stream temporarily unavailable."

# Execution Core using the official Groq client
@st.cache_data(show_spinner=False)
def run_groq_ai_analysis(api_key, movie, question, wiki_data, ott_data):
    prompt = f"""
    You are the absolute premier business consultant for the Indian Film Industry (Tollywood, Bollywood, and South Indian cinema).
    Answer the user's question completely using the two real-time text sources pulled from the internet.
    
    [SOURCE 1: WIKIPEDIA ARCHIVES]:
    {wiki_data}
    
    [SOURCE 2: LIVE WEB NEWS SNIPPETS FOR OTT RIGHTS]:
    {ott_data}
    
    User Question: {question}
    
    Instructions:
    Deliver a highly polished report using clear headings and bullet points. Focus heavily on specifying the director, producer, budget structures, final box office profit/loss, and explicitly state which digital platform (Netflix, Prime, Hotstar, Aha, Zee5, etc.) owns the OTT streaming rights based on the sources.
    """
    
    try:
        client = Groq(api_key=api_key)
        # Using Llama 3.3 70B for highly precise reasoning, or 8B for absolute blistering speeds
        chat_completion = client.chat.completions.create(
            messages=[
                {"role": "user", "content": prompt}
            ],
            model="llama-3.3-70b-versatile",
            temperature=0.2
        )
        return chat_completion.choices[0].message.content, True
    except Exception as e:
        return str(e), False

# Layout Elements
movie_input = st.text_input("🎥 Enter Indian Movie Name (e.g., Baahubali, RRR, Devara, Pushpa):")
question_input = st.text_input("💬 Ask anything (e.g., Give me a full profit breakdown and who bought OTT rights?):")

if st.button("🚀 Execute Llama Retrieval"):
    if not user_api_key:
        st.error("Please add a Groq API Key to proceed!")
    elif not movie_input or not question_input:
        st.warning("Please fill out both search entry slots.")
    else:
        with st.spinner("🧠 Llama parsing real-time regional data matrices..."):
            wiki_title, wiki_text = fetch_wikipedia_data(movie_input)
            ott_news_text = fetch_live_ott_news(movie_input)
            
            output, success = run_groq_ai_analysis(
                user_api_key, movie_input, question_input, wiki_text, ott_news_text
            )
            
            if success:
                st.success(f"📊 Completed Analysis for {wiki_title}!")
                st.markdown("### 🤖 FilmIntel Executive Briefing:")
                st.info(output)
            else:
                st.error(f"Groq API Execution Error: {output}")
