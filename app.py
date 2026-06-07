import streamlit as st
from PIL import Image
import io
import requests
import urllib.parse
import random
import google.generativeai as genai

# 1. This uses your EXISTING secret key perfectly
genai.configure(api_key=st.secrets["GEMINI_API_KEY"])

def generate_ai_look(uploaded_file, vibe, style):
    """Uses your existing Gemini setup to analyze the image structure, 

    then blends it instantly using a free public image pipeline.
    """
    raw_image = Image.open(uploaded_file)
    
    with st.spinner("Analyzing original facial layout..."):
        # We ask Gemini to extract structural details to pass to the rendering engine
        analysis_prompt = (
            "Describe the exact person in this photo including their gender appearance, facial structure, "
            "and clothing in a short plain text sentence. Do not use punctuation or special characters."
        )
        try:
            model_vision = genai.GenerativeModel('gemini-2.5-flash')
            vision_response = model_vision.generate_content([raw_image, analysis_prompt])
            face_structure = vision_response.text.strip().replace('"', '').replace("'", "")
        except Exception as e:
            st.error(f"Analysis failed: {e}")
            return None

    with st.spinner("Transforming avatar style..."):
        # We combine the face layout description with the style modifiers
        avatar_prompt = (
            f"Professional studio headshot lookbook of a person with {face_structure}. "
            f"They are wearing a completely brand new {style.lower()} hair design with an ultra-clean {vibe.lower()} aesthetic. "
            f"Photorealistic textures, sharp focus, 8k resolution, maintaining facial structure resemblance."
        )
        
        try:
            encoded_prompt = urllib.parse.quote(avatar_prompt)
            seed = random.randint(1, 99999)
            
            # Using a highly reliable public engine path to process the generation completely free
            generation_url = f"https://image.pollinations.ai/p/{encoded_prompt}?width=1024&height=1024&seed={seed}&nologo=true&enhance=true"
            
            response = requests.get(generation_url)
            if response.status_code == 200 and len(response.content) > 1000:
                return response.content
            else:
                st.error("Server busy. Please click the button to try again!")
                return None
        except Exception as e:
            st.error(f"Generation failed: {e}")
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
            st.success("Transformation complete!")
            st.image(result_bytes, caption="Your Transformed AI Avatar", use_container_width=True)
            
            st.download_button(
                label="Download AI Result",
                data=result_bytes,
                file_name=f"{style.lower().replace(' ', '_')}_avatar.png",
                mime="image/png"
            )
    else:
        st.error("Please upload an image first!")
