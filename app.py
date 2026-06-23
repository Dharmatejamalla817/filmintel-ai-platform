import streamlit as st
import requests
from google import genai
import wikipediaapi

st.set_page_config(page_title="Indian FilmIntel AI", page_icon="🎬", layout="wide")

# Custom Indian Cinema Header
st.title("🎬 Indian FilmIntel AI Platform")
st.subheader("Enterprise Edition: High-Availability Regional Cinema Core")
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
    st.info("🎯 **Regional Indian Focus Active:** This LLM agent reads complete historical data logs directly from Wikipedia open archives to parse Tollywood, Bollywood, and South Indian box office and creative metrics.")

# Search Layout
movie_input = st.text_input("🎥 Enter Indian Movie Name (e.g., Baahubali, RRR, Devara, Pokiri):")
question_input = st.text_input("💬 Ask any question (Cast, Crew, Budget, Profit/Loss, OTT Streaming Rights):")

if st.button("🚀 Execute Deep Intelligence Retrieval"):
    if not user_api_key:
        st.error("Please provide a valid Gemini API Key!")
    elif not movie_input or not question_input:
        st.warning("Please fill out both entry boxes.")
    else:
        with st.spinner("🧠 Autonomous Web Agent accessing Indian cinema archives..."):
            
            # Setup Wikipedia Client
            wiki_agent = wikipediaapi.Wikipedia(
                user_agent="FilmIntelIndiaApp/1.0 (contact: admin@filmintelai.com)",
                language="en"
            )
            
            page = wiki_agent.page(movie_input)
            
            if page.exists():
                wiki_title = page.title
                wiki_content = page.text
                st.success(f"📈 Found Live Verified Records for: {wiki_title}!")
            else:
                st.warning(f"Exact page match for '{movie_input}' not found. Using generic fallback data...")
                wiki_title = movie_input
                wiki_content = "No direct encyclopedic text records found. Rely on base model knowledge base."

            # Prompts Engine Setup
            prompt = f"""
            You are an expert film analyst specialized in Indian Cinema (including Tollywood, Bollywood, and all South Indian regional industries).
            Analyze the user's question with absolute precision using the verified records payload below.
            
            [LIVE ENCYCLOPEDIA RECORDS FOR {wiki_title}]:
            {wiki_content[:15000]}
            
            User Question: {question_input}
            
            System Instructions:
            1. Deliver a highly polished, analytical LLM response.
            2. Meticulously extract details regarding cast, crew, budgets, profit/loss calculations, and digital/OTT/satellite rights distributions.
            3. Handle numbers clearly. Preserve Crore (INR) metrics or convert them transparently for clarity.
            """
            
            # 🔄 Self-Healing Model Traversal Strategy
            models_to_try = ["gemini-2.5-flash", "gemini-2.5-pro"]
            response_text = None
            ai_success = False
            
            client = genai.Client(api_key=user_api_key)
            
            for current_model in models_to_try:
                try:
                    # Attempt to get a response from the current model
                    response = client.models.generate_content(
                        model=current_model,
                        contents=prompt
                    )
                    response_text = response.text
                    ai_success = True
                    break  # Success! Break out of the loop
                except Exception as model_err:
                    # If it's a 503 error, log a warning and let the loop check the next model
                    if "503" in str(model_err) or "UNAVAILABLE" in str(model_err):
                        st.warning(f"⚠️ Server pool for '{current_model}' is currently congested. Route switching active...")
                        continue
                    else:
                        # If it's a different error (like an invalid API key), stop immediately
                        st.error(f"Critical API configuration issue: {model_err}")
                        break

            # Render final output state
            if ai_success and response_text:
                st.markdown("### 🤖 FilmIntel AI Strategic Report:")
                st.info(response_text)
            else:
                st.error("🚨 All global Google AI server nodes are heavily congested right now. Please wait 15 seconds and click the button again to retry your request!")
