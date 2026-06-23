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

# 🖌️ Custom CSS Branding & Premium UI Layout
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
st.subheader("Enterprise Agent Edition: Deep Multi-Engine Cinema Intelligence")
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
    st.info("🧠 **Autonomous Critic Agent Online:** This engine uses recursive query expansion to target Indian trade registries, box-office ledgers, and critical reviews across multiple nodes simultaneously.")
    
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

# 🧠 AGENT MODULE 1: Self-Correcting Subject Extractor
def extract_clean_subject(api_key, raw_query):
    try:
        client = Groq(api_key=api_key)
        prompt = f"""Analyze the user's input: "{raw_query}".
        Isolate the precise name of the Indian movie, web series, actor, or director.
        Respond with ONLY the clean title/name. No symbols, no punctuation, no sentences.
        Example: "can you give me the budget of pushpa 2 rule movie" -> Pushpa 2: The Rule
        Example: "tell me about prabhas remuneration" -> Prabhas"""
        
        completion = client.chat.completions.create(
            messages=[{"role": "user", "content": prompt}],
            model="llama-3.3-70b-versatile",
            temperature=0.0,
            max_tokens=25
        )
        return completion.choices[0].message.content.strip()
    except:
        return raw_query

# 🛠️ AGENT MODULE 2: Deep Context Harvesting Network
@st.cache_data(show_spinner=False)
def fetch_wikipedia_dossier(search_term):
    wiki_agent = wikipediaapi.Wikipedia(
        user_agent="FilmIntelIndiaGroq/2.0 (contact: admin@filmintel.com)", language="en"
    )
    page = wiki_agent.page(search_term)
    if page.exists():
        # Pulling a much deeper slice of data (12,000 chars) to capture full cast tables & box office text
        return page.title, page.text[:12000]
    return search_term, "No direct encyclopedic records found."

def execute_targeted_crawl(query):
    url = f"https://html.duckduckgo.com/html/?q={requests.utils.quote(query)}"
    try:
        headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"}
        res = requests.get(url, headers=headers, timeout=12)
        soup = BeautifulSoup(res.text, "html.parser")
        snippets = [s.text.strip() for s in soup.find_all('a', class_='result__snippet')[:5]]
        return "\n".join(snippets) if snippets else ""
    except:
        return ""

@st.cache_data(show_spinner=False)
def gather_deep_trade_intel(subject):
    # Search Loop 1: Core Financials & Rights
    q1 = f"{subject} movie box office collections budget profit loss OTT streaming rights partner news"
    trade_intel = execute_targeted_crawl(q1)
    
    # Search Loop 2: Indian Trade Outlets Critic Aggregation
    q2 = f"{subject} review rating critical response analysis site:123telugu.com OR site:pinkvilla.com OR site:bollywoodhungama.com"
    critic_intel = execute_targeted_crawl(q2)
    
    return trade_intel, critic_intel

# 🤖 AGENT MODULE 3: Elite Cinema Synthesis Core
@st.cache_data(show_spinner=False)
def run_agent_synthesis(api_key, user_query, subject, wiki_data, trade_data, critic_data):
    prompt = f"""
    You are the premier, industry-leading AI cinema business consultant and entertainment analyst for Indian Cinema.
    Your mission is to answer the user's query with complete data, absolute precision, and zero placeholder guessing.
    
    User Query: {user_query}
    Target Subject: {subject}
    
    You have been supplied with deep text packages directly scraped from the web:
    
    [DATAFEED 1: SYSTEM ENCYCLOPEDIA RECORDS]
    {wiki_data}
    
    [DATAFEED 2: FINANCIAL TRADE REGISTRY & OTT TRACKING]
    {trade_data}
    
    [DATAFEED 3: JOURNALISTIC MEDIA REVIEWS & CRITIC RATINGS]
    {critic_data}
    
    System Instructions:
    1. Cross-reference all datafeeds. Do not state that information is missing if it exists in ANY of the datafeeds. 
    2. Build a high-tier, professional analysis dossier using clear, bold headings and structured bullet points.
    3. Include dedicated deep-dive sections covering:
       - 🎬 Cast & Production Crew Lineup (with relevant performance reviews or remuneration tracking if present).
       - 💰 Financial Performance Balance Sheet (Budget metrics vs. Total Domestic/Global Box Office Gross collections).
       - 📺 Digital & OTT Distribution Assets (Explicitly list streaming partners like Netflix, Prime Video, Aha, Zee5, Hotstar and digital rights value details).
       - 📈 Critical Consensus & Media Ratings Summary.
    4. If details diverge across trade papers, present them comparatively like an enterprise auditor. Never summarize lazily.
    """
    
    try:
        client = Groq(api_key=api_key)
        chat_completion = client.chat.completions.create(
            messages=[{"role": "user", "content": prompt}],
            model="llama-3.3-70b-versatile",
            temperature=0.1
        )
        return chat_completion.choices[0].message.content, True
    except Exception as e:
        return str(e), False

# Unified Single Input Interface
user_query = st.text_input("🔍 Search for any Indian Movie, Web Series, Actor, or ask a custom question:")

if st.button("🚀 Run Comprehensive Intelligence Scan"):
    if not user_api_key:
        st.error("Please ensure your Groq API Key is actively connected in the configuration panel.")
    elif not user_query:
        st.warning("Please input a movie title, celebrity profile, or industry topic to begin.")
    else:
        with st.spinner("🧠 Autonomous agent crawling multi-node indices, compiling trade registers, and parsing reviews..."):
            
            # Step 1: Extract pure title context
            subject = extract_clean_subject(user_api_key, user_query)
            
            # Step 2: Parallel multi-engine collection
            wiki_title, wiki_text = fetch_wikipedia_dossier(subject)
            trade_text, critic_text = gather_deep_trade_intel(subject)
            
            # Step 3: Deep Synthesis
            report, success = run_agent_synthesis(
                user_api_key, user_query, wiki_title, trade_text, critic_text
            )
            
            if success:
                st.success(f"📊 Global Media & Financial Dossier Compiled Successfully!")
                st.markdown("### 🤖 FilmIntel Comprehensive Briefing:")
                st.info(report)
            else:
                st.error(f"Critical System Analysis Fault: {report}")

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
