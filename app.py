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
st.subheader("Enterprise Ecosystem Edition: Multi-Hat Cinema Intelligence Workspace")
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
    
    # 🎩 NEW FEATURE: ECOSYSTEM TARGET SELECTOR
    st.header("🎯 Workspace Mode")
    user_role = st.selectbox(
        "Select your industry role:",
        ["🍿 Audience & Super-Fan", "💼 Producer & Director (B2B)", "🎭 Actor & Crew Marketplace", "📰 News Reporter & Critic"]
    )
    
    st.markdown("---")
    
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

# --- INJECTED MOCK DATA BASES FOR MARKETPLACE MATCHING ---
# In a full release, this connects to a database. For this upgrade, it simulates the capability instantly.
MOCK_CREW_DB = """
[PORTFOLIO ID 101] Name: Sai Kumar; Role: Cinematographer; Location: Hyderabad; Experience: Low-light tracking, rustic action, dark themes; Availability: Free August 2026; Budget: 5 Lakhs/project.
[PORTFOLIO ID 102] Name: Anjali Rao; Role: VFX Coordinator; Location: Hyderabad; Experience: CGI integration, mythological assets, green screen; Availability: Free July 2026; Budget: 8 Lakhs/project.
[PORTFOLIO ID 103] Name: R. Narayanan; Role: Line Producer; Location: Chennai; Experience: Mid-budget schedules, location scouting, European permissions; Availability: Immediate; Budget: 10 Lakhs/project.
"""

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
    q1 = f"{subject} movie box office collections budget profit loss OTT streaming rights partner news"
    trade_intel = execute_targeted_crawl(q1)
    
    q2 = f"{subject} review rating critical response analysis site:123telugu.com OR site:pinkvilla.com OR site:bollywoodhungama.com"
    critic_intel = execute_targeted_crawl(q2)
    
    return trade_intel, critic_intel

# 🤖 AGENT MODULE 3: Multi-Hat Ecosystem Synthesis Core
def run_ecosystem_synthesis(api_key, user_query, role, subject, wiki_data, trade_data, critic_data):
    # Adjust instructions dynamically based on the selected target persona
    if role == "💼 Producer & Director (B2B)":
        system_focus = f"""
        You are an elite, B2B Hollywood/Tollywood financial and logistical analyst. 
        Focus heavily on providing complete logistical analytics, instant market research reports, budget structures, and profit-and-loss assessments.
        If the user uploads script lines or concept fragments, provide an automated breakdown of required locations, cast tracking, and estimated production requirements.
        """
    elif role == "🎭 Actor & Crew Marketplace":
        system_focus = f"""
        You are the ultimate Talent Matching AI for cinema networks. 
        Cross-reference the query against our internal talent pool database context to vet and match candidates for casting calls, lighting crews, or VFX directors based on location, availability, and style.
        
        INTERNAL TALENT POOL DATABASE CONTEXT:
        {MOCK_CREW_DB}
        """
    elif role == "📰 News Reporter & Critic":
        system_focus = """
        You are a high-speed facts desk agent for journalists and cinematic critics.
        Focus on extreme mathematical precision, trend spotting, record tracking, and fact-checking. 
        Always attempt to construct structured comparison data tables summarizing box-office jumps or records that a reporter can immediately copy-paste into an article.
        """
    else: # Default Audience & Super-Fan
        system_focus = """
        You are a hyper-personalized, conversational cinema discovery guide for fans.
        Aggregate the web sentiment from social mentions and reviews to answer why audiences love or dislike elements of this subject, offering clear, digestible summaries.
        """

    prompt = f"""
    {system_focus}
    
    User Query: {user_query}
    Target Subject: {subject}
    
    [DATAFEED 1: ENCYCLOPEDIA RECORDS]
    {wiki_data}
    
    [DATAFEED 2: FINANCIAL TRADE REGISTRY & OTT TRACKING]
    {trade_data}
    
    [DATAFEED 3: JOURNALISTIC MEDIA REVIEWS & CRITIC RATINGS]
    {critic_data}
    
    Deliver a comprehensive, professional output formatted beautifully with bold Markdown headers.
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

# Unified Single Input Interface
if user_role == "💼 Producer & Director (B2B)":
    user_query = st.text_area("🔍 Paste your Script Concept / Treatment Outline, or ask a logistical/financial question:")
else:
    user_query = st.text_input(f"🔍 [{user_role}] Search anything or ask a question:")

if st.button("🚀 Execute High-Speed Intelligence Scan"):
    if not user_api_key:
        st.error("Please ensure your Groq API Key is actively connected in the configuration panel.")
    elif not user_query:
        st.warning("Please enter a query or script outline to trigger the processing nodes.")
    else:
        with st.spinner(f"🧠 FilmIntel Ecosystem routing query via specialized [{user_role}] parameters..."):
            
            # Step 1: Extract pure title context
            subject = extract_clean_subject(user_api_key, user_query)
            
            # Step 2: Parallel multi-engine collection
            wiki_title, wiki_text = fetch_wikipedia_dossier(subject)
            trade_text, critic_text = gather_deep_trade_intel(subject)
            
            # Step 3: Multi-Hat Dynamic Synthesis
            report, success = run_ecosystem_synthesis(
                user_api_key, user_query, user_role, wiki_title, wiki_text, trade_text, critic_text
            )
            
            if success:
                st.success(f"📊 {user_role} Intelligence Briefing Compiled Successfully!")
                st.markdown(f"### 🤖 FilmIntel Core Report ({user_role}):")
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
