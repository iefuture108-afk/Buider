import streamlit as st
import base64
import requests
from PIL import Image
from io import BytesIO
from openai import OpenAI

# 1. Setup Client using Streamlit Secrets
client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

def encode_image_to_base64(uploaded_file):
    """Convert the uploaded file directly to a base64 string for GPT-4o."""
    return base64.b64encode(uploaded_file.getvalue()).decode("utf-8")

def generate_ai_look(uploaded_file, vibe, style):
    """Uses GPT-4o to analyze the face and DALL-E 3 to generate the new hairstyle."""
    with st.spinner("Analyzing features and crafting your new look..."):
        # Convert image for vision API
        base64_image = encode_image_to_base64(uploaded_file)
        
        # Step 1: Analyze the face to maintain consistency
        analysis_prompt = (
            "Analyze this person's facial features, skin tone, and face shape. "
            "Write a concise, detailed description of their appearance. Do not focus on their current hair, "
            "just their core facial characteristics so we can recreate their likeness accurately."
        )
        
        try:
            vision_response = client.chat.completions.create(
                model="gpt-4o",
                messages=[
                    {
                        "role": "user",
                        "content": [
                            {"type": "text", "text": analysis_prompt},
                            {
                                "type": "image_url",
                                "image_url": {"url": f"data:image/jpeg;base64,{base64_image}"}
                            }
                        ]
                    }
                ],
                max_tokens=150
            )
            face_description = vision_response.choices[0].message.content
            
        except Exception as e:
            st.error(f"Analysis failed: {e}")
            return None

        # Step 2: Combine analysis with selected style for DALL-E 3
        dalle_prompt = (
            f"A high-quality, professional studio portrait of a person with the following features: {face_description}. "
            f"They are showcasing a new hairstyle that is '{style}' with a distinct '{vibe}' vibe. "
            f"The lighting should be clean and cinematic, mimicking an upscale lookbook or high-end product commercial photoshoot. "
            f"Maintain natural textures and realistic proportions."
        )

    with st.spinner("Generating your AI hairstyle..."):
        try:
            # Step 3: Generate the image
            generation_response = client.images.generate(
                model="dall-e-3",
                prompt=dalle_prompt,
                n=1,
                size="1024x1024",
                response_format="url"
            )
            
            image_url = generation_response.data[0].url
            
            # Fetch the generated image bytes for displaying and downloading
            img_data = requests.get(image_url).content
            return img_data

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
        # Pass the uploaded_file directly so we can grab raw bytes easily
        result_bytes = generate_ai_look(uploaded_file, vibe, style)
        
        if result_bytes:
            st.success("Generation complete!")
            # Display generated image
            st.image(result_bytes, caption="Here is your new AI-generated style!", use_container_width=True)
            
            # Allow downloading of the actual generated asset
            st.download_button(
                label="Download AI Result",
                data=result_bytes,
                file_name=f"{style.lower().replace(' ', '_')}_look.png",
                mime="image/png"
            )
    else:
        st.error("Please upload an image first!")
