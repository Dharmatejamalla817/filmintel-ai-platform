import streamlit as st
import requests
from google import genai
import wikipediaapi
import time

st.set_page_config(page_title="Indian FilmIntel AI", page_icon="🎬", layout="wide")

st.title("🎬 Indian FilmIntel AI Platform")
st.subheader("Enterprise Edition: Token-Optimized Regional Cinema Engine")
st.markdown("---")

try:
    GOOGLE_API_KEY = st.secrets["GEMINI_API_KEY"]
except:
    GOOGLE_API_KEY = ""

with st.sidebar:
    st.header("🔑 System Access")
    user_api_key = GOOGLE_API_KEY if GOOGLE_API_KEY else st.text_input("Enter your Gemini API Key:", type="password")
    st.markdown("---")
    st.info("🎯 **Token Saver Engine Active:** Wikipedia content is dynamically trimmed to protect free-tier API quotas while preserving critical film metrics.")

movie_input = st.text_input("🎥 Enter Indian Movie Name (e.g., Baahubali, RRR, Devara, Pokiri):")
question_input = st.text_input("💬 Ask any question (Cast, Crew, Budget, Profit/Loss, OTT Streaming Rights):")

if st.button("🚀 Execute Deep Intelligence Retrieval"):
    if not user_api_key:
        st.error("Please provide a valid Gemini API Key!")
    elif not movie_input or not question_input:
        st.warning("Please fill out both entry boxes.")
    else:
        with st.spinner("🧠 Accessing optimized Indian cinema archives..."):
            
            wiki_agent = wikipediaapi.Wikipedia(
                user_agent="FilmIntelIndiaApp/1.0 (contact: admin@filmintelai.com)",
                language="en"
            )
            
            page = wiki_agent.page(movie_input)
            
            if page.exists():
                wiki_title = page.title
                # ✂️ TOKEN SAVER: We pull the top 6,000 characters which always contains the core box office data and crew metadata
                wiki_content = page.text[:6000]
                st.success(f"📈 Found Core Records for: {wiki_title}!")
            else:
                st.warning(f"Exact page for '{movie_input}' not found. Using generic fallback data...")
                wiki_title = movie_input
                wiki_content = "No direct text records found."

            prompt = f"""
            You are an expert film analyst specialized in Indian Cinema (Tollywood, Bollywood, and South Indian regional industries).
            Analyze the user's question using the verified records payload below.
            
            [COMPACT RECORDS FOR {wiki_title}]:
            {wiki_content}
            
            User Question: {question_input}
            
            Instructions:
            Provide a clean, analytical LLM report. Extract details regarding cast, crew, budgets, profits, losses, and OTT/streaming distribution rights.
            """
            
            # 🔄 Balanced Model Fallback Matrix
            models_to_try = ["gemini-2.5-flash", "gemini-2.0-flash"]
            response_text = None
            ai_success = False
            quota_error_msg = ""
            
            client = genai.Client(api_key=user_api_key)
            
            for current_model in models_to_try:
                try:
                    response = client.models.generate_content(
                        model=current_model,
                        contents=prompt
                    )
                    response_text = response.text
                    ai_success = True
                    break 
                except Exception as model_err:
                    err_str = str(model_err)
                    if "429" in err_str or "RESOURCE_EXHAUSTED" in err_str:
                        quota_error_msg = "429 Quota Limit Hit"
                        st.warning(f"⚠️ Free-tier limit momentarily filled on '{current_model}'. Switching routes...")
                        continue
                    elif "503" in err_str or "UNAVAILABLE" in err_str:
                        st.warning(f"⚠️ Server pool for '{current_model}' is congested. Rerouting...")
                        continue
                    else:
                        st.error(f"API Error: {model_err}")
                        break

            if ai_success and response_text:
                st.markdown("### 🤖 FilmIntel AI Strategic Report:")
                st.info(response_text)
            elif quota_error_msg:
                st.error("🚨 **Google Free-Tier Quota Exhausted!** You've requested a lot of data quickly.")
                st.info("⏱️ **Self-Healing Action:** Please wait **60 seconds** for Google to completely reset your free minute token count, then click search again!")
            else:
                st.error("Could not complete the request due to server congestion. Please retry in a few moments.")
