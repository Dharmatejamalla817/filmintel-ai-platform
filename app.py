import streamlit as st
import requests
from google import genai
import wikipediaapi

st.set_page_config(page_title="Indian FilmIntel AI", page_icon="🎬", layout="wide")

st.title("🎬 Indian FilmIntel AI Platform")
st.subheader("Public Edition: Zero-Downtime Regional Cinema Engine")
st.markdown("---")

# 🔐 Load Master System Key from Cloud Secrets
try:
    SYSTEM_GOOGLE_API_KEY = st.secrets["GEMINI_API_KEY"]
except:
    SYSTEM_GOOGLE_API_KEY = ""

with st.sidebar:
    st.header("🔑 System Access")
    
    # If the system key is exhausted, users can input their own to keep playing!
    use_custom_key = st.checkbox("🔑 Use my own Gemini API Key (If system quota is full)")
    
    if use_custom_key:
        user_api_key = st.text_input("Enter your personal Gemini API Key:", type="password")
    else:
        user_api_key = SYSTEM_GOOGLE_API_KEY
        if SYSTEM_GOOGLE_API_KEY:
            st.success("🔒 Connected to FilmIntel Master Node")
        else:
            user_api_key = st.text_input("Enter a Gemini API Key to begin:", type="password")
            
    st.markdown("---")
    st.info("🎯 **Tollywood & Bollywood Optimized:** This public platform pulls live text architectures from open encyclopedias to analyze South Indian box office records, cast structures, and OTT distributions.")

movie_input = st.text_input("🎥 Enter Indian Movie Name (e.g., Baahubali, RRR, Devara, Pokiri, Sholay):")
question_input = st.text_input("💬 Ask any question (e.g., Who bought the OTT streaming rights and what was the profit/loss?):")

if st.button("🚀 Execute Deep Intelligence Retrieval"):
    if not user_api_key:
        st.error("Please provide or enter a valid Gemini API Key in the sidebar configuration!")
    elif not movie_input or not question_input:
        st.warning("Please fill out both entry boxes to activate the research agent.")
    else:
        with st.spinner("🧠 Gathering regional cinema data updates..."):
            
            # Setup Wikipedia agent with compliant headers
            wiki_agent = wikipediaapi.Wikipedia(
                user_agent="FilmIntelIndiaApp/1.0 (contact: admin@filmintelai.com)",
                language="en"
            )
            
            page = wiki_agent.page(movie_input)
            
            if page.exists():
                wiki_title = page.title
                # ✂️ Token Optimizer: Keeps request context clean and cheap
                wiki_content = page.text[:5000]
                st.success(f"📈 Analyzed Verified Records for: {wiki_title}")
            else:
                st.warning(f"Exact data match for '{movie_input}' not found. Searching base historical knowledge...")
                wiki_title = movie_input
                wiki_content = "No direct text database rows found. Analyze using internal training weights."

            prompt = f"""
            You are an elite cinematic business consultant specializing in Indian Cinema (including Tollywood, Bollywood, and all South Indian languages).
            Answer the user's query meticulously by extracting historical facts from the encyclopedia text below.
            
            [VERIFIED ARCHIVE FOR {wiki_title}]:
            {wiki_content}
            
            User Question: {question_input}
            
            Instructions:
            1. Provide an incredibly rich, well-formatted response with bold headings and bullet points.
            2. Break down crew, cast, producer tracking, profits, losses, and budget overruns.
            3. Clearly call out streaming/OTT rights partners (like Netflix, Amazon Prime, Aha, Zee5) if mentioned in the archives.
            """
            
            models_to_try = ["gemini-2.5-flash", "gemini-2.0-flash"]
            response_text = None
            ai_success = False
            is_quota_blocked = False
            
            # Executing query
            try:
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
                            is_quota_blocked = True
                            continue
                        elif "503" in err_str or "UNAVAILABLE" in err_str:
                            continue
                        else:
                            raise model_err
                            
            except Exception as global_err:
                st.error(f"System Connection Error: {global_err}")

            # Final View Rendering
            if ai_success and response_text:
                st.markdown("### 🤖 FilmIntel AI Strategic Report:")
                st.info(response_text)
            elif is_quota_blocked:
                st.error("🚨 **Google AI Free-Tier Daily Quota Exhausted!**")
                st.markdown("""
                The shared master API key has reached its maximum daily usage limits from Google. 
                
                **🛠️ How to keep using the app right now:**
                1. Check the **'Use my own Gemini API Key'** box in the sidebar.
                2. Paste a free key from [Google AI Studio](https://aistudio.google.com/).
                3. Click search again to get instant, unlimited answers!
                """)
            else:
                st.error("The network engine is currently experiencing heavy congestion. Please re-try your search request in a few moments.")
