import streamlit as st
import requests
from google import genai
import wikipediaapi

st.set_page_config(page_title="Indian FilmIntel AI", page_icon="🎬", layout="wide")

# Custom Indian Cinema Styling & Header
st.title("🎬 Indian FilmIntel AI Platform")
st.subheader("The Ultimate Intelligence Hub for Tollywood, Bollywood & South Indian Cinema")
st.markdown("---")

# Secure Keys Processing
try:
    GOOGLE_API_KEY = st.secrets["GEMINI_API_KEY"]
except:
    GOOGLE_API_KEY = ""

with st.sidebar:
    st.header("🔑 System Access")
    user_api_key = GOOGLE_API_KEY if GOOGLE_API_KEY else st.text_input("Enter your Gemini API Key:", type="password")
    
    st.markdown("---")
    st.info("🎯 **Regional Indian Focus Active:** This LLM agent is heavily optimized to parse Tollywood, Kollywood, Mollywood, Sandalwood, and Bollywood historical records using live Wikipedia open encyclopedias.")

# Beautiful LLM Search and Query Interface
movie_input = st.text_input("🎥 Enter Indian Movie Name (e.g., Baahubali, RRR, Devara, Pokiri):")
question_input = st.text_input("💬 Ask any tiny or massive question (Cast, Budget, Profit/Loss, Director, OTT Streaming Rights):")

if st.button("🚀 Execute Deep Intelligence Retrieval"):
    if not user_api_key:
        st.error("Please ensure your Gemini API Key is provided or configured in secrets!")
    elif not movie_input or not question_input:
        st.warning("Please fill out both fields to trigger the automated web research agent.")
    else:
        with st.spinner("🧠 Autonomous Web Agent accessing Indian cinema archives..."):
            
            # 🌐 Initialize Wikipedia Open Engine with standard compliance User-Agent
            wiki_agent = wikipediaapi.Wikipedia(
                user_agent="FilmIntelIndiaApp/1.0 (contact: admin@filmintelai.com)",
                language="en"
            )
            
            # Attempt to pull deep unstructured text context directly from Wikipedia
            page = wiki_agent.page(movie_input)
            
            if page.exists():
                wiki_title = page.title
                # Grabbing the massive, complete text content (Introduction, Production, Cast, Reception, Box Office, OTT)
                wiki_content = page.text
                st.success(f"📈 Found Live Verified Encyclopedia Records for: {wiki_title}!")
            else:
                # Fallback search if exact match fails
                st.warning(f"Exact page match for '{movie_input}' not found. Attempting generic context fallback...")
                wiki_title = movie_input
                wiki_content = "No direct encyclopedic text records found. Rely on fallback base model data."

            # 🤖 Structuring the Ultimate Prompt for South Indian & Bollywood Logistics
            prompt = f"""
            You are an elite, specialized film analyst who is an expert in Indian Cinema (including Tollywood, Bollywood, and all South Indian industries). 
            You are tasked with analyzing the user's question with absolute precision.
            
            To help you answer with 100% accuracy, here is the complete, live, raw text payload retrieved directly from the open web/encyclopedia records for '{wiki_title}':
            
            [LIVE ENCYCLOPEDIA RECORDS]:
            {wiki_content[:15000]}  # Pulls up to 15,000 characters of dense historical text records
            
            User Question: {question_input}
            
            System Instructions:
            1. Deliver a clean, highly professional executive response that reads like a premium cinematic LLM report.
            2. Scan the provided records meticulously for every detail regarding cast, crew, production overruns, directors, producers, profit/loss margins, and digital/OTT/satellite rights distributions.
            3. If the user asks about an outdated or vintage film, locate its historical release and economic context within the text.
            4. Present numbers (budget, collection) clearly. If the text lists budgets in Crores (INR) or Millions, preserve and explain the conversions clearly.
            """
            
            try:
                # Booting up the world-class Gemini Brain to synthesize the text
                client = genai.Client(api_key=user_api_key)
                response = client.models.generate_content(
                    model='gemini-2.5-flash',
                    contents=prompt
                )
                
                st.markdown("### 🤖 FilmIntel AI Strategic Report:")
                st.info(response.text)
                
            except Exception as e:
                st.error(f"AI Synthesis Module Error: {e}")
