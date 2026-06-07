import streamlit as st
from PIL import Image
import io
import requests
import urllib.parse
import random
import time
from google import genai

# 1. Initialize Gemini for face analysis using your working Free Tier key
client = genai.Client(api_key=st.secrets["GEMINI_API_KEY"])

def generate_ai_look(uploaded_file, vibe, style):
    """Uses Gemini Free Tier for facial feature analysis,

    then renders the image using a fast, high-concurrency stable diffusion public node.
    """
    raw_image = Image.open(uploaded_file)
    
    with st.spinner("Gemini is analyzing your facial features..."):
        analysis_prompt = (
            "Analyze this person's facial structure, skin tone, and face shape. "
            "Describe them in a single sentence using plain text under 15 words. "
            "Do not use punctuation, quotes, or colons. Ignore their current hair."
        )
        
        try:
            # Step 1: Face analysis via Gemini 2.5 Flash (Completely Free & Allowed)
            vision_response = client.models.generate_content(
                model='gemini-2.5-flash',
                contents=[raw_image, analysis_prompt]
            )
            face_description = vision_response.text.strip()
            # Clean non-alphanumeric text to ensure URL stability
            face_description = "".join(c for c in face_description if c.isalnum() or c.isspace())
            
        except Exception as e:
            st.error(f"Facial analysis failed: {e}")
            return None

    with st.spinner("Rendering your new style avatar..."):
        # Step 2: Build a hyper-optimized layout prompt for the core engine
        image_prompt = (
            f"Professional symmetric studio Lookbook headshot portrait of a person with {face_description} "
            f"showcasing a clean brand new {style.lower()} hair look with an upscale {vibe.lower()} design aesthetic "
            f"photorealistic textures crisp highly focused sharp details elegant lighting"
        )
        
        encoded_prompt = urllib.parse.quote(image_prompt)
        seed = random.randint(1, 99999)
        
        # Step 3: Use an unthrottled fast-rendering pipeline route
        generation_url = f"https://image.pollinations.ai/p/{encoded_prompt}?width=1024&height=1024&seed={seed}&nologo=true&model=flux"
        
        # Retry logic with unique User-Agent to avoid server line congestion
        max_retries = 3
        headers = {
            "User-Agent": f"Mozilla/5.0 (Windows NT 10.0; Win64; x64) HairstyleApp/{random.randint(10,99)}"
        }
        
        for attempt in range(max_retries):
            try:
                response = requests.get(generation_url, headers=headers, timeout=20)
                if response.status_code == 200 and len(response.content) > 5000:
                    return response.content
            except Exception:
                pass
            
            if attempt < max_retries - 1:
                time.sleep(2)
                
        st.error("The public server is heavily congested right now. Please click the button again to try another processing slot!")
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
            st.image(result_bytes, caption="Your New AI Style Portrait", use_container_width=True)
            
            st.download_button(
                label="Download AI Result",
                data=result_bytes,
                file_name=f"{style.lower().replace(' ', '_')}_look.png",
                mime="image/png"
            )
    else:
        st.error("Please upload an image first!")
