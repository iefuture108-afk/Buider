import streamlit as st
from PIL import Image
import requests
import base64
import os

st.set_page_config(page_title="How I Look AI 🇮🇳", layout="centered")

st.title("🇮🇳 How I Look AI")
st.subheader("Real AI Hairstyle Generator 🔥")

st.info("Upload your photo → AI generates your best looks")

# API KEY
OPENAI_API_KEY = st.secrets["OPENAI_API_KEY"]

# CATEGORY
category = st.radio(
    "Select Category",
    ["Men 👨", "Women 👩", "Kids 🧒"],
    horizontal=True
)

uploaded_file = st.file_uploader("Upload your photo", type=["jpg", "jpeg", "png"])

# -------------------------
# IMAGE TO BASE64
# -------------------------
def encode_image(image):
    buffered = image.tobytes()
    return base64.b64encode(buffered).decode("utf-8")

# -------------------------
# AI GENERATION
# -------------------------
def generate_look(image, prompt):
    buffered = base64.b64encode(image.tobytes()).decode()

    headers = {
        "Authorization": f"Bearer {OPENAI_API_KEY}",
        "Content-Type": "application/json"
    }

    payload = {
        "model": "gpt-image-1",
        "prompt": prompt,
        "size": "512x512"
    }

    response = requests.post(
        "https://api.openai.com/v1/images/edits",
        headers=headers,
        json=payload
    )

    if response.status_code == 200:
        data = response.json()
        img_base64 = data["data"][0]["b64_json"]
        return base64.b64decode(img_base64)
    else:
        return None

# -------------------------
# MAIN
# -------------------------
if uploaded_file:
    image = Image.open(uploaded_file).convert("RGB")
    st.image(image, caption="Your Photo", use_column_width=True)

    st.markdown("---")
    st.header("✨ AI Generated Looks")

    col1, col2, col3 = st.columns(3)

    # PROMPTS
    if "Men" in category:
        prompts = [
            "man with textured top haircut, fade sides, stylish beard",
            "man with side part hairstyle, clean professional look",
            "man with messy modern hairstyle, trendy beard"
        ]

    elif "Women" in category:
        prompts = [
            "woman with layered haircut, volume, stylish look",
            "woman with soft curls hairstyle, elegant look",
            "woman with straight sleek hair, modern style"
        ]

    else:
        prompts = [
            "kid with cute short hairstyle",
            "kid with school neat haircut",
            "kid with fun playful hairstyle"
        ]

    # GENERATE
    for col, prompt in zip([col1, col2, col3], prompts):
        with col:
            with st.spinner("Generating..."):
                result = generate_look(image, prompt)

                if result:
                    st.image(result)
                    st.success(prompt.split(",")[0])
                else:
                    st.error("AI failed, try again")

else:
    st.warning("Upload your photo to generate AI looks")
