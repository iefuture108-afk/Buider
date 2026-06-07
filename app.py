import streamlit as st
from PIL import Image
import base64
from openai import OpenAI

# -------------------------
# CONFIG
# -------------------------
st.set_page_config(page_title="How I Look AI 🇮🇳", layout="centered")

st.title("🇮🇳 How I Look AI")
st.subheader("AI Hairstyle Generator 🔥")

st.info("Upload your photo → AI generates your best looks")

# -------------------------
# API KEY
# -------------------------
client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

# -------------------------
# CATEGORY
# -------------------------
category = st.radio(
    "Select Category",
    ["Men 👨", "Women 👩", "Kids 🧒"],
    horizontal=True
)

uploaded_file = st.file_uploader("Upload your photo", type=["jpg", "jpeg", "png"])

# -------------------------
# AI GENERATION
# -------------------------
def generate_look(prompt):
    try:
        response = client.images.generate(
            model="gpt-image-1",
            prompt=prompt,
            size="512x512"
        )

        img_base64 = response.data[0].b64_json
        return base64.b64decode(img_base64)

    except Exception as e:
        st.error(f"Error: {e}")
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

    if "Men" in category:
        prompts = [
            "man with textured haircut fade sides stylish beard realistic",
            "man with side part professional hairstyle realistic",
            "man with messy modern hairstyle trendy beard realistic"
        ]

    elif "Women" in category:
        prompts = [
            "woman layered haircut volume realistic",
            "woman soft curls hairstyle elegant realistic",
            "woman sleek straight hair modern realistic"
        ]

    else:
        prompts = [
            "kid cute short hairstyle realistic",
            "kid neat school haircut realistic",
            "kid fun playful hairstyle realistic"
        ]

    for col, prompt in zip([col1, col2, col3], prompts):
        with col:
            with st.spinner("Generating..."):
                result = generate_look(prompt)

                if result:
                    st.image(result)
                    st.success("AI Look")
                else:
                    st.error("AI failed, try again")

else:
    st.warning("Upload your photo to generate AI looks")
