import streamlit as st
import numpy as np
from PIL import Image

# MUST BE FIRST
st.set_page_config(page_title="How I Look AI 🇮🇳", layout="centered")

st.title("🇮🇳 How I Look AI")
st.subheader("Find your best hairstyle instantly")

st.info("Step 1: Select category → Step 2: Upload photo → Step 3: Get your best look")

# CATEGORY
category = st.radio(
    "Select Category",
    ["Men 👨", "Women 👩", "Kids 🧒"],
    horizontal=True
)

uploaded_file = st.file_uploader("Upload your photo", type=["jpg", "jpeg", "png"])

# SIMPLE OVERLAY (NO AI LIBS)
def add_overlay(image, color):
    img = np.array(image)
    h, w, _ = img.shape

    overlay = img.copy()
    overlay[0:int(h*0.25), :] = color  # top "hair" zone

    blended = (0.6 * img + 0.4 * overlay).astype(np.uint8)
    return blended

# MAIN
if uploaded_file:
    image = Image.open(uploaded_file).convert("RGB")
    st.image(image, caption="Your Photo", use_column_width=True)

    st.markdown("---")
    st.header("✨ Your Top 3 Looks")

    col1, col2, col3 = st.columns(3)

    # MEN
    if "Men" in category:
        with col1:
            st.image(add_overlay(image, [0, 0, 0]))
            st.success("🔥 Textured Top + Fade")

        with col2:
            st.image(add_overlay(image, [50, 50, 50]))
            st.success("💼 Side Part")

        with col3:
            st.image(add_overlay(image, [90, 90, 90]))
            st.success("😎 Messy Style")

    # WOMEN
    elif "Women" in category:
        with col1:
            st.image(add_overlay(image, [120, 0, 120]))
            st.success("✨ Layered Hair")

        with col2:
            st.image(add_overlay(image, [200, 50, 50]))
            st.success("💃 Soft Curls")

        with col3:
            st.image(add_overlay(image, [150, 100, 50]))
            st.success("👑 Straight Sleek")

    # KIDS
    elif "Kids" in category:
        with col1:
            st.image(add_overlay(image, [0, 150, 200]))
            st.success("🧒 Cute Short")

        with col2:
            st.image(add_overlay(image, [100, 200, 0]))
            st.success("🎒 School Style")

        with col3:
            st.image(add_overlay(image, [200, 100, 0]))
            st.success("🎉 Fun Style")

    st.markdown("---")

    st.header("🧠 AI Suggestion")

    if "Men" in category:
        st.info("Best for you: Textured Top + Mid Fade + Sharp Beard")
    elif "Women" in category:
        st.info("Best for you: Soft Layers with Volume")
    else:
        st.info("Best for you: Clean & comfortable style")

else:
    st.warning("Upload your photo to generate looks")
