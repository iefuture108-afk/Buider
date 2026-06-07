import streamlit as st
from PIL import Image
import io
from google import genai
from google.genai import types

# 1. Initialize the official client securely using your existing secret
client = genai.Client(api_key=st.secrets["GEMINI_API_KEY"])

def generate_ai_look(uploaded_file, vibe, style):
    """Uses Gemini 2.5 Flash for crisp face analysis and Gemini 2.5 Flash Image 
    for instant, native, and free image generation.
    """
    raw_image = Image.open(uploaded_file)
    
    with st.spinner("Gemini is analyzing your facial features..."):
        analysis_prompt = (
            "Analyze this person's facial structure, skin tone, and face shape. "
            "Write a concise description of their core facial characteristics. "
            "Ignore their current hair completely."
        )
        
        try:
            # Step 1: Analyze the face structure
            vision_response = client.models.generate_content(
                model='gemini-2.5-flash',
                contents=[raw_image, analysis_prompt]
            )
            face_description = vision_response.text.strip()
            
        except Exception as e:
            st.error(f"Facial analysis failed: {e}")
            return None

    with st.spinner("Generating your new AI lookbook portrait natively..."):
        # Step 2: Combine the visual blueprint with user style choices
        image_prompt = (
            f"A professional crisp studio lookbook portrait photography of a person with these features: {face_description}. "
            f"They are showcasing a brand new hairstyle looking '{style}' with a clear '{vibe}' aesthetic. "
            f"Studio lighting, natural textures, sharp focus, high resolution."
        )
        
        try:
            # Step 3: Call Google's native image generation model
            image_response = client.models.generate_content(
                model='gemini-2.5-flash-image',
                contents=image_prompt,
                config=types.GenerateContentConfig(
                    response_modalities=["IMAGE"],
                    image_config=types.ImageConfig(
                        aspect_ratio="1:1"
                    )
                )
            )
            
            # Extract raw image data directly from response parts
            for part in image_response.parts:
                if part.inline_data:
                    generated_img = part.as_image()
                    
                    # Convert PIL Image into raw bytes for Streamlit
                    img_byte_arr = io.BytesIO()
                    generated_img.save(img_byte_arr, format='PNG')
                    return img_byte_arr.getvalue()
                    
            st.error("Google's engine completed the request but returned an empty canvas. Try again!")
            return None

        except Exception as e:
            st.error(f"Native image generation failed: {e}")
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
            # Display image directly from bytes
            st.image(result_bytes, caption="Your New AI Style Portrait", use_container_width=True)
            
            # Enable free downloads
            st.download_button(
                label="Download AI Result",
                data=result_bytes,
                file_name=f"{style.lower().replace(' ', '_')}_look.png",
                mime="image/png"
            )
    else:
        st.error("Please upload an image first!")
