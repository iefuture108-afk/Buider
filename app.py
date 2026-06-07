import streamlit as st
from PIL import Image
import io
import requests
import random

def generate_ai_look(uploaded_file, vibe, style):
    """Sends the actual original image data directly to a free Hugging Face Image-to-Image model."""
    
    # 1. Open and resize image slightly so it uploads quickly over the API connection
    img = Image.open(uploaded_file)
    img = img.convert("RGB")
    img.thumbnail((768, 768)) # Optimal processing size for standard diffusion pipelines
    
    # Convert PIL Image back to raw JPEG bytes to send in the API body
    buffer = io.BytesIO()
    img.save(buffer, format="JPEG")
    image_bytes = buffer.getvalue()

    # 2. Construct the guiding prompt
    prompt = (
        f"A professional crisp studio lookbook portrait of this person showcasing a brand new hairstyle "
        f"that is looking {style.lower()} with a clear {vibe.lower()} aesthetic. "
        f"Maintain facial geometry likeness, natural hair texture, highly realistic details."
    )
    
    # We use an optimized, fast Image-to-Image pipeline hosted on Hugging Face's server
    API_URL = "https://api-inference.huggingface.co/models/stabilityai/stable-diffusion-xl-refiner-1.0"
    headers = {"Authorization": f"Bearer {st.secrets['HF_TOKEN']}"}

    payload = {
        "inputs": prompt,
        "image": image_bytes,
        "parameters": {
            "strength": 0.55,           # Controls how much changes (0.0 = identical face, 1.0 = completely new image)
            "guidance_scale": 7.5,
            "seed": random.randint(1, 99999)
        }
    }

    with st.spinner("Processing face data and rendering your new style..."):
        try:
            response = requests.post(API_URL, headers=headers, json=payload, timeout=45)
            
            # If the model is temporarily loading in the background on Hugging Face's server
            if response.status_code == 503:
                st.warning("The free AI model is waking up on the cloud server. Please wait 10 seconds and click generate again!")
                return None
                
            if response.status_code == 200:
                return response.content
            else:
                st.error(f"Engine response error ({response.status_code}): Please try clicking again.")
                return None
                
        except Exception as e:
            st.error(f"Connection failed: {e}")
            return None

# --- Streamlit UI Controls ---
st.title("AI Avatar Hairstyle Transformer")
st.write("Upload a clear selfie or portrait to instantly alter your hairstyle aesthetics using true image-to-image translation.")

uploaded_file = st.file_uploader("Upload your original photo", type=["jpg", "png", "jpeg"])

col1, col2 = st.columns(2)
with col1:
    vibe = st.selectbox("Pick an aesthetic vibe", ["Professional", "Casual", "Edgy"])
with col2:
    style = st.radio("Pick your new target style:", ["Short & Clean", "Long & Wavy", "Textured Fade"])

if st.button("Generate Final AI Look", type="primary"):
    if uploaded_file:
        # Display original image feedback
        st.image(uploaded_file, caption="Original Photo Reference", width=250)
        
        result_bytes = generate_ai_look(uploaded_file, vibe, style)
        
        if result_bytes:
            st.success("Transformation complete!")
            st.image(result_bytes, caption="Your New AI Avatar Look", use_container_width=True)
            
            st.download_button(
                label="Download AI Result",
                data=result_bytes,
                file_name=f"{style.lower().replace(' ', '_')}_avatar.png",
                mime="image/png"
            )
    else:
        st.error("Please upload an image first!")
