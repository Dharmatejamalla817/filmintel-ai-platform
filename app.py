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

# 🖌️ Injection of Professional Custom CSS Branding
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
st.subheader("Llama-Core Edition: Deep Cast & Crew Intelligence Agent")
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
    st.info("⚡ **Cast Matrix Engine Active:** Now mining real-time salaries, remuneration, trade values, and career analysis trends for the lead cast and crew.")
    
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

# 🛠️ MULTI-ENGINE PIPELINES
@st.cache_data(show_spinner=False)
def fetch_wikipedia_data(movie_name):
    wiki_agent = wikipediaapi.Wikipedia(
        user_agent="FilmIntelIndiaGroq/1.0 (contact: admin@filmintel.com)", language="en"
    )
    page = wiki_agent.page(movie_name)
    if page.exists():
        return page.title, page.text[:7000]
    return movie_name, "No direct encyclopedic records found."

def crawl_web_headlines(query):
    url = f"https://html.duckduckgo.com/html/?q={requests.utils.quote(query)}"
    try:
        headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"}
        res = requests.get(url, headers=headers, timeout=10)
        soup = BeautifulSoup(res.text, "html.parser")
        snippets = [s.text.strip() for s in soup.find_all('a', class_='result__snippet')[:4]]
        return "\n".join(snippets) if snippets else "No direct media updates found."
    except:
        return "Network source pool timed out."

@st.cache_data(show_spinner=False)
def fetch_deep_research_data(movie_name, focus_keywords):
    # Search Stream A: OTT, Budget, Trade Distribution Logistics
    trade_query = f"{movie_name} movie official box office budget profit loss OTT platform rights news"
    trade_results = crawl_web_headlines(trade_query)
    
    # Search Stream B: Critical Reception, Reviews, and Ratings
    review_query = f"{movie_name} movie review rating critical reception site:pinkvilla.com OR site:123telugu.com OR site:bollywoodhungama.com"
    review_results = crawl_web_headlines(review_query)
    
    # Search Stream C: Specialized Cast & Crew Remuneration and Production Trade Intel
    cast_query = f"{movie_name} {focus_keywords} salary remuneration performance reviews career impact news headlines"
    cast_results = crawl_web_headlines(cast_query)
    
    return trade_results, review_results, cast_results

# Deep Execution Core
@st.cache_data(show_spinner=False)
def run_groq_ai_analysis(api_key, movie, question, wiki_data, trade_data, review_data, cast_data):
    prompt = f"""
    You are the absolute premier business consultant and senior research analyst for the Indian Film Industry.
    Answer the user's question completely using the highly detailed real-time intelligence feeds compiled below.
    
    [DATAFEED 1: ENCYCLOPEDIC ARCHIVES (CAST, CREW, CORE PLOT)]
    {wiki_data}
    
    [DATAFEED 2: LIVE MEDIA LOGISTICS (OTT PARTNERS, BUDGETS, LOSS/PROFIT METRICS)]
    {trade_data}
    
    [DATAFEED 3: CRITICAL RECEPTION & REVIEWS (CRITIC REVIEWS, PUBLIC RECEPTION, RATINGS)]
    {review_data}
    
    [DATAFEED 4: CAST INTEL & CAREER REMUNERATION METRICS]
    {cast_data}
    
    User Question: {question}
    
    Instructions:
    1. Deliver an elite, deeply analytical report with bold headers, logical sections, and clear bullet points.
    2. Incorporate explicit findings regarding the cast and crew's details, such as their salary metrics/remuneration rumors for this specific movie, the critical reception of their acting performance, and how this film impacts their theatrical market value.
    3. Synthesize all information uniformly. Present clear sections analyzing the financial standings (budget vs gross), critical reception/consensus ratings, and details regarding OTT rights.
    """
    
    try:
        client = Groq(api_key=api_key)
        chat_completion = client.chat.completions.create(
            messages=[{"role": "user", "content": prompt}],
            model="llama-3.3-70b-versatile",
            temperature=0.2
        )
        return chat_completion.choices[0].message.content, True
    except Exception as e:
        return str(e), False

# Input Layout
movie_input = st.text_input("🎥 Enter Indian Movie Name (e.g., Baahubali, RRR, Devara, Pushpa):")
cast_input = st.text_input("👥 Enter Specific Cast/Crew Names to target (e.g., Prabhas, Jr NTR, Allu Arjun, Sukumar, Anirudh):")
question_input = st.text_input("💬 Ask anything (e.g., How much did the lead cast get paid, how was their performance reviewed, and who bought OTT rights?):")

if st.button("🚀 Execute Comprehensive Intel Retrieval"):
    if not user_api_key:
        st.error("Please add a valid Groq API Key to proceed!")
    elif not movie_input or not question_input:
        st.warning("Please fill out the Movie Name and Question fields.")
    else:
        with st.spinner("🧠 Crawling deep-web indices for cast metrics, reviews, budgets, and streaming assets..."):
            # Execute all scrapers simultaneously
            wiki_title, wiki_text = fetch_wikipedia_data(movie_input)
            trade_text, review_text, cast_text = fetch_deep_research_data(movie_input, cast_input)
            
            output, success = run_groq_ai_analysis(
                user_api_key, movie_input, question_input, wiki_text, trade_text, review_text, cast_text
            )
            
            if success:
                st.success(f"📊 Completed In-Depth Master Dossier for {wiki_title}!")
                st.markdown("### 🤖 FilmIntel Executive Briefing:")
                st.info(output)
            else:
                st.error(f"Groq API Execution Error: {output}")

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
