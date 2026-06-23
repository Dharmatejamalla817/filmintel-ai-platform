import streamlit as st
import requests
import wikipediaapi
from bs4 import BeautifulSoup
from groq import Groq

# 🎨 Streamlit Page Layout Optimization
st.set_page_config(
    page_title="Indian FilmIntel Pro", 
    page_icon="🎬", 
    layout="wide",
    initial_sidebar_state="expanded"
)

# 🖌️ Custom CSS Branding & Layout Tweaks
st.markdown("""
    <style>
        #MainMenu {visibility: hidden;}
        footer {visibility: hidden;}
        header {visibility: hidden;}
        
        .custom-footer {
            position: fixed;
            left: 0;
            bottom: 0;
            width: 100%;
            background-color: #111111;
            color: #888888;
            text-align: center;
            padding: 12px;
            font-size: 14px;
            border-top: 1px solid #333333;
            z-index: 100;
            font-family: 'Helvetica Neue', Helvetica, Arial, sans-serif;
        }
        .custom-footer a {
            color: #ff4b4b;
            text-decoration: none;
            font-weight: bold;
        }
    </style>
""", unsafe_allow_html=True)

st.title("🎬 Indian FilmIntel AI Platform")
st.subheader("Llama-Core Edition: Unified Cinema Intelligence Engine")
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
    st.info("⚡ **Unified Query Parsing Active:** The single input box dynamically handles movies, web series, actor profiles, or general industry questions.")
    
    # Creator Attribution
    st.markdown("""
        <div style='background-color: #1e1e1e; padding: 10px; border-radius: 5px; border-left: 3px solid #ff4b4b;'>
            <small style='color: #fff; font-weight: bold;'>👨‍💻 Architect Info:</small><br>
            <small style='color: #ccc;'>Developed & Engineered by:<br><b style='color: #ff4b4b;'>Malla Dharma Teja</b></small>
        </div>
        <br>
        <small style='color: #777;'>
        © 2026 FilmIntel India AI.<br>
        All Rights Reserved.<br>
        Powered by Groq Cloud Systems.
        </small>
    """, unsafe_allow_html=True)

# 🛠️ MULTI-ENGINE BACKGROUND SCRAIPING MATRICES
@st.cache_data(show_spinner=False)
def fetch_wikipedia_data(search_term):
    wiki_agent = wikipediaapi.Wikipedia(
        user_agent="FilmIntelIndiaGroq/1.0 (contact: admin@filmintel.com)", language="en"
    )
    page = wiki_agent.page(search_term)
    if page.exists():
        return page.title, page.text[:8000]
    return search_term, "No direct encyclopedic matches found. Rely on web streams and core weights."

@st.cache_data(show_spinner=False)
def fetch_live_web_intelligence(search_term):
    # Dynamic search looking for general trade data, reviews, and streaming platform distributions
    query = f"{search_term} movie web series actor box office budget OTT streaming rights review news"
    url = f"https://html.duckduckgo.com/html/?q={requests.utils.quote(query)}"
    try:
        headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"}
        res = requests.get(url, headers=headers, timeout=10)
        soup = BeautifulSoup(res.text, "html.parser")
        snippets = [s.text.strip() for s in soup.find_all('a', class_='result__snippet')[:6]]
        return "\n".join(snippets) if snippets else "No secondary web headlines indexed."
    except:
        return "Live web research stream temporarily offline."

# Core Execution System
@st.cache_data(show_spinner=False)
def run_groq_ai_analysis(api_key, user_query, wiki_data, web_data):
    prompt = f"""
    You are an elite, world-class business intelligence analyst and critic specializing in Indian Cinema (Tollywood, Bollywood, Kollywood, and regional OTT platforms).
    
    The user has submitted this request: "{user_query}"
    
    To help you provide a flawless, comprehensive answer, your background scrapers have compiled the following real-time web documents:
    
    [DOCUMENT 1: ENCYCLOPEDIC ARCHIVES]
    {wiki_data}
    
    [DOCUMENT 2: LIVE WEB INTELLIGENCE & TRADE PORTALS]
    {web_data}
    
    Instructions:
    1. Determine the intent of the user's query. If they searched an actor, analyze their career status, upcoming projects, and trade value. If they searched a movie/web series, break down the cast, director, budget, profit/loss parameters, critical reviews, and OTT streaming rights.
    2. Format the final output layout beautifully using clean, bold headings, bullet points, and clear sections.
    3. Ensure all numbers (Crores, Millions) and platform mappings (Netflix, Prime Video, Hotstar, Aha, Zee5) are presented clearly based on the provided documents.
    """
    
    try:
        client = Groq(api_key=api_key)
        chat_completion = client.chat.create(
            messages=[{"role": "user", "content": prompt}],
            model="llama-3.3-70b-versatile",
            temperature=0.2
        )
        return chat_completion.choices[0].message.content, True
    except Exception as e:
        return str(e), False

# Single Simplified Search Interface
user_query = st.text_input("🔍 Search for any Indian Movie, Web Series, Actor, or ask a custom question:")

if st.button("🚀 Search Intelligence Network"):
    if not user_api_key:
        st.error("Please ensure a valid Groq API Key is active!")
    elif not user_query:
        st.warning("Please type something into the search bar to initiate analysis.")
    else:
        with st.spinner("🧠 Scanning intelligence network and synthesizing live reports..."):
            # Execute automated context harvesting
            wiki_title, wiki_text = fetch_wikipedia_data(user_query)
            web_text = fetch_live_web_intelligence(user_query)
            
            # Process via Llama Core
            output, success = run_groq_ai_analysis(user_api_key, user_query, wiki_text, web_text)
            
            if success:
                st.success(f"📊 Report Generated successfully!")
                st.markdown("### 🤖 FilmIntel Core Report:")
                st.info(output)
            else:
                st.error(f"Execution Error: {output}")

# ────────── PUBLIC DISCLAIMER & STICKY FOOTER SECTION ──────────
st.markdown("<br><br><br><br>", unsafe_allow_html=True)

st.caption("""
⚠️ **Enterprise Disclaimer:** This application acts as an autonomous AI compilation engine. All research reports, financial insights, 
budgets, and streaming right structures are synthesized in real-time utilizing public domain encyclopedia records and indexed web news aggregates. 
Box office metrics and OTT distribution statuses fluctuate and should be cross-verified for formal auditing purposes. 
""")

st.markdown("""
    <div class="custom-footer">
        © 2026 <b>FilmIntel India AI</b> | Developed by <b>Malla Dharma Teja</b> | 
        Designed for South Indian Cinema Archives | Powered by <a href="https://groq.com/" target="_blank">Groq LPU Systems</a>
    </div>
""", unsafe_allow_html=True)
