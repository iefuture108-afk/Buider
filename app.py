import streamlit as st
from PIL import Image
import numpy as np

st.set_page_config(page_title="How I Look - India", layout="centered")

st.title("🇮🇳 How I Look App")
st.subheader("Find your best hairstyle & beard look instantly")

# Upload Image
uploaded_file = st.file_uploader("Upload your photo", type=["jpg", "jpeg", "png"])

# Style Selection
style = st.selectbox(
    "Choose your vibe",
    ["Controlled Rugged (Recommended)", "Clean Professional", "Trendy Stylish", "Low Maintenance"]
)

# Budget Selection
budget = st.selectbox(
    "Select your budget",
    ["₹200", "₹500", "₹1000"]
)

if uploaded_file is not None:
    image = Image.open(uploaded_file)
    st.image(image, caption="Your Photo", use_column_width=True)

    st.markdown("---")

    st.header("✨ Your Recommended Look")

    if style == "Controlled Rugged (Recommended)":
        st.success("Textured Top + Mid Fade + Sharp Beard")
        st.write("Natural, confident, not over-styled. Perfect for your personality.")

    elif style == "Clean Professional":
        st.success("Side Part + Low Fade + Trimmed Beard")
        st.write("Sharp, formal, ideal for office & interviews.")

    elif style == "Trendy Stylish":
        st.success("Textured Quiff + Fade + Defined Beard")
        st.write("Modern, eye-catching, great for social events.")

    elif style == "Low Maintenance":
        st.success("Short Crop + Low Fade + Light Beard")
        st.write("Easy to manage, always clean look.")

    st.markdown("---")

    st.header("🧔 Beard Recommendation")
    st.write("""
    - Keep full beard but shape it
    - Clean neckline (above Adam's apple)
    - Slight cheek line definition
    - Use beard oil daily
    """)

    st.markdown("---")

    st.header("⏱ 2-Minute Daily Routine")
    st.write("""
    1. Damp hair slightly
    2. Apply small amount of matte wax
    3. Style with fingers (not comb)
    4. Apply 2–3 drops beard oil
    """)

    st.markdown("---")

    st.header("💸 Product Recommendation")

    if budget == "₹200":
        st.write("""
        - Set Wet Hair Wax (Matte)
        - Patanjali Aloe Vera Gel
        """)

    elif budget == "₹500":
        st.write("""
        - Beardo Hair Wax
        - Beardo Beard Oil
        - Simple Face Wash (Soap-free)
        """)

    elif budget == "₹1000":
        st.write("""
        - Ustraa Hair Clay
        - Bombay Shaving Company Beard Oil
        - Cetaphil Gentle Cleanser
        """)

    st.markdown("---")

    st.info("Tip: Show this to your barber for best results 💈")

else:
    st.warning("Please upload an image to get started.")
