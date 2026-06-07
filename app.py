import streamlit as st
from PIL import Image
import base64
from openai import OpenAI
import io

# -------------------------
# CONFIG
# -------------------------
st.set_page_config(page_title="How I Look AI 🇮🇳", layout="centered")

st.title("🇮🇳 How I Look AI")
st.subheader("Real AI Hairstyle Generator 🔥")

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
# CONVERT IMAGE
# -------------------------
def image_to_bytes(image):
    buf = io.BytesIO()
    image.save(buf, format="PNG")
    return buf.getvalue()

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

        image_base64 = response.data[0].b64_json
        return base64.b64decode(image_base64)

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

    # ---------------- MEN ----------------
    if "Men" in category:
        prompts = [
            "portrait of a man with textured top haircut and fade sides, stylish beard, realistic",
            "portrait of a man with side part hairstyle, clean professional look, realistic",
            "portrait of a man with messy modern hairstyle, trendy beard, realistic"
        ]

    # ---------------- WOMEN ----------------
    elif "Women" in category:
        prompts = [
            "portrait of a woman with layered haircut, volume hairstyle, realistic",
            "portrait of a woman with soft curls hairstyle, elegant look, realistic",
            "portrait of a woman with straight sleek hair, modern style, realistic"
        ]

    # ---------------- KIDS ----------------
    else:
        prompts = [
            "portrait of a kid with cute short hairstyle, realistic",
            "portrait of a kid with neat school haircut, realistic",
            "portrait of a kid with fun playful hairstyle, realistic"
        ]

    # ---------------- GENERATE ----------------
    for col, prompt in zip([col1, col2, col3], prompts):
        with col:
            with st.spinner("Generating..."):
                result = generate_look(prompt)

                if result:
                    st.image(result)
                    st.success(prompt.split(",")[0])
                else:
                    st.error("AI failed, try again")

else:
    st.warning("Upload your photo to generate AI looks")
