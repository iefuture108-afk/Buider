import streamlit as st
from PIL import Image
import io
import requests
import urllib.parse
import random
import google.generativeai as genai

# 1. Setup Gemini for the facial analysis
genai.configure(api_key=st.secrets["GEMINI_API_KEY"])

def generate_ai_look(uploaded_file, vibe, style):
    """Uses Gemini for perfect face analysis, and Pollinations for free image generation."""
    
    raw_image = Image.open(uploaded_file)
    
    with st.spinner("Gemini is analyzing your facial features..."):
        analysis_prompt = (
            "Analyze this person's facial structure, skin tone, and face shape. "
            "Describe them in a single short sentence using only plain text. "
            "Do not use quotes, colons, or bullet points. Ignore their current hair."
        )
        
        try:
            model_vision = genai.GenerativeModel('gemini-2.5-flash')
            vision_response = model_vision.generate_content([raw_image, analysis_prompt])
            face_description = vision_response.text.strip()
            
            # Clean up any potential punctuation remnants that break URLs
            face_description = face_description.replace('"', '').replace("'", "").replace(":", "")
            
        except Exception as e:
            st.error(f"Facial analysis failed: {e}")
            return None

    with st.spinner("Generating your new AI hairstyle (Free Tier)..."):
        # 2. Build a highly clean prompt for the public engine
        image_prompt = (
            f"Professional studio portrait photo lookbook of a person with these features {face_description}. "
            f"They have a brand new hairstyle looking {style} with a distinct {vibe} aesthetic. "
            f"Hyper-realistic textures, clean background, sharp focus, 8k resolution."
        )
        
        try:
            # 3. Clean and encode the prompt for the Pollinations engine
            encoded_prompt = urllib.parse.quote(image_prompt)
            seed = random.randint(1, 99999)
            
            # We add the enhanced prompt with structural rules directly to Pollinations
            pollinations_url = f"https://image.pollinations.ai/p/{encoded_prompt}?width=1024&height=1024&seed={seed}&nologo=true"
            
            # Fetch the generated image bytes with a fallback timeout
            response = requests.get(pollinations_url, timeout=30)
            if response.status_code == 200 and len(response.content) > 1000:
                return response.content
            else:
                st.error("The generation server took too long. Please try clicking generate again!")
                return None

        except Exception as e:
            st.error(f"Image generation failed: {e}")
            return None

# --- Streamlit UI ---
st.title("AI Hairstyle Transformer")

uploaded_file = st.file_uploader("Upload your photo", type=["jpg", "png", "jpeg"])
vibe = st.selectbox("Pick a vibe", ["Professional", "Casual", "Edgy"])
style = st.radio("Pick your final style:", ["Short & Clean", "Long & Wavy", "Textured Fade"])

if st.button("Generate Final AI Look"):
    if uploaded_file:
        result_bytes = generate_ai_look(uploaded_file, vibe, style)
        
        if result_bytes:
            st.success("Generation complete!")
            # Display image directly from bytes
            st.image(result_bytes, caption="Here is your new AI-generated style!", use_container_width=True)
            
            # Enable free downloads
            st.download_button(
                label="Download AI Result",
                data=result_bytes,
                file_name=f"{style.lower().replace(' ', '_')}_look.png",
                mime="image/png"
            )
    else:
        st.error("Please upload an image first!")
