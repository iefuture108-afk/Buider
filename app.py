import streamlit as st
from PIL import Image
import io
from google import genai
from google.genai import types

# 1. Setup the Gemini Client using Streamlit Secrets
# It automatically picks up GEMINI_API_KEY from your environment/secrets
client = genai.Client(api_key=st.secrets["GEMINI_API_KEY"])

def generate_ai_look(uploaded_file, vibe, style):
    """Uses Gemini Vision to evaluate features and Gemini Image models to generate the final look."""
    
    # Open the file as a PIL Image so the Gemini SDK can process it directly
    raw_image = Image.open(uploaded_file)
    
    with st.spinner("Gemini is analyzing your facial features..."):
        analysis_prompt = (
            "Analyze this person's facial features, skin tone, and face shape. "
            "Write a concise, detailed description of their physical appearance. "
            "Ignore their current hairstyle entirely; focus strictly on their facial structure "
            "so we can replicate their likeness accurately."
        )
        
        try:
            # Step 1: Analyze the face using Gemini 2.5 Flash
            vision_response = client.models.generate_content(
                model='gemini-2.5-flash',
                contents=[raw_image, analysis_prompt]
            )
            face_description = vision_response.text
            
        except Exception as e:
            st.error(f"Facial analysis failed: {e}")
            return None

    with st.spinner("Generating your new AI hairstyle..."):
        # Step 2: Build the prompt combining face details + selected styles
        dalle_style_prompt = (
            f"A professional high-quality studio portrait photography of a person with these exact features: {face_description}. "
            f"They have a brand new hairstyle that is completely clean, looking '{style}' with a clear '{vibe}' vibe. "
            f"Studio lighting, cinematic lookbook aesthetic, crisp and highly realistic textures."
        )
        
        try:
            # Step 3: Generate the image using Gemini's native image generation capability
            image_response = client.models.generate_content(
                model='gemini-2.5-flash-image',
                contents=dalle_style_prompt,
                config=types.GenerateContentConfig(
                    response_modalities=["IMAGE"],
                    image_config=types.ImageConfig(
                        aspect_ratio="1:1"
                    )
                )
            )
            
            # Extract the raw generated image from response parts
            for part in image_response.parts:
                if part.inline_data:
                    generated_img = part.as_image()
                    
                    # Convert PIL Image into raw bytes for Streamlit's download button
                    img_byte_arr = io.BytesIO()
                    generated_img.save(img_byte_arr, format='PNG')
                    return img_byte_arr.getvalue()
                    
            st.error("No image data was returned by the model.")
            return None

        except Exception as e:
            st.error(f"Image generation failed: {e}")
            return None

# --- Streamlit UI ---
st.title("AI Hairstyle Transformer (Gemini Edition)")

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
