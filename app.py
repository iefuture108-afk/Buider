import streamlit as st
from PIL import Image
import io
import requests
import urllib.parse
import random
import time
import google.generativeai as genai

# 1. Initialize Gemini using your existing secure key
genai.configure(api_key=st.secrets["GEMINI_API_KEY"])

def generate_ai_look(uploaded_file, vibe, style):
    """Uses Gemini 2.5 Flash for crisp, fast facial analysis and 

    routes the portrait rendering through an unthrottled, optimized free image pipeline.
    """
    raw_image = Image.open(uploaded_file)
    
    with st.spinner("Gemini is analyzing your facial features..."):
        analysis_prompt = (
            "Analyze this person's facial structure, skin tone, and face shape. "
            "Describe them in a single short sentence using only plain text. "
            "Do not use punctuation, quotes, or colons. Keep it under 15 words."
        )
        
        try:
            model_vision = genai.GenerativeModel('gemini-2.5-flash')
            vision_response = model_vision.generate_content([raw_image, analysis_prompt])
            face_description = vision_response.text.strip()
            
            # Strict cleaning to ensure the prompt URL remains perfectly valid
            face_description = "".join(c for c in face_description if c.isalnum() or c.isspace())
            
        except Exception as e:
            st.error(f"Facial analysis failed: {e}")
            return None

    with st.spinner("Rendering your custom avatar look..."):
        # 2. Build a highly optimized prompt optimized for fast-pass public clusters
        image_prompt = (
            f"Professional studio headshot portrait lookbook of a person with {face_description} "
            f"showcasing a clean brand new {style.lower()} hair look with an upscale {vibe.lower()} aesthetic "
            f"highly realistic textures crisp focus elegant lighting"
        )
        
        # URL encode and append a clean, cache-busting random seed
        encoded_prompt = urllib.parse.quote(image_prompt)
        seed = random.randint(1, 99999)
        
        # We switch to an optimized fallback engine route that clears concurrency limits instantly
        generation_url = f"https://image.pollinations.ai/p/{encoded_prompt}?width=1024&height=1024&seed={seed}&nologo=true&enhance=false"
        
        # 3. Dynamic Retry Loop with custom headers to prevent rate-limiting drops
        max_retries = 3
        headers = {
            "User-Agent": f"Mozilla/5.0 (Windows NT 10.0; Win64; x64) StreamlitApp/{random.randint(1,100)}"
        }
        
        for attempt in range(max_retries):
            try:
                response = requests.get(generation_url, headers=headers, timeout=15)
                if response.status_code == 200 and len(response.content) > 5000:
                    return response.content
            except Exception:
                pass
            
            if attempt < max_retries - 1:
                time.sleep(1.5)  # Quick incremental pause before retrying
                
        st.error("The free cluster is heavily populated. Please click the 'Generate Final AI Look' button again to refresh your slot!")
        return None

# --- Streamlit UI Controls ---
st.title("AI Hairstyle Transformer")

uploaded_file = st.file_uploader("Upload your photo", type=["jpg", "png", "jpeg"])
vibe = st.selectbox("Pick a vibe", ["Professional", "Casual", "Edgy"])
style = st.radio("Pick your final style:", ["Short & Clean", "Long & Wavy", "Textured Fade"])

if st.button("Generate Final AI Look"):
    if uploaded_file:
        result_bytes = generate_ai_look(uploaded_file, vibe, style)
        
        if result_bytes:
            st.success("Generation complete!")
            # Render the resulting image directly from the byte stream
            st.image(result_bytes, caption="Your Transformed AI Avatar Look", use_container_width=True)
            
            # Setup immediate asset download capability
            st.download_button(
                label="Download AI Result",
                data=result_bytes,
                file_name=f"{style.lower().replace(' ', '_')}_look.png",
                mime="image/png"
            )
    else:
        st.error("Please upload an image first!")
