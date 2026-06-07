import streamlit as st
import numpy as np
from PIL import Image
import mediapipe as mp

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

# FACE DETECTION (MEDIAPIPE ONLY)
mp_face = mp.solutions.face_detection
face_detection = mp_face.FaceDetection()

def detect_face(image):
    img = np.array(image)
    img_rgb = img  # already RGB from PIL
    results = face_detection.process(img_rgb)

    if results.detections:
        for detection in results.detections:
            bbox = detection.location_data.relative_bounding_box
            h, w, _ = img.shape

            x = int(bbox.xmin * w)
            y = int(bbox.ymin * h)
            width = int(bbox.width * w)
            height = int(bbox.height * h)

            return img[y:y+height, x:x+width]
    return img


# SIMPLE OVERLAY (NO CV2)
def add_overlay(face_img, color):
    overlay = face_img.copy()
    h, w, _ = overlay.shape

    # Create colored band (hair simulation)
    overlay[0:int(h*0.25), :] = color

    # Blend manually
    blended = (0.6 * face_img + 0.4 * overlay).astype(np.uint8)
    return blended


# MAIN
if uploaded_file:
    image = Image.open(uploaded_file).convert("RGB")
    st.image(image, caption="Your Photo", use_column_width=True)

    face = detect_face(image)

    st.markdown("---")
    st.header("✨ Your Top 3 Looks")

    col1, col2, col3 = st.columns(3)

    # MEN
    if "Men" in category:
        with col1:
            st.image(add_overlay(face, [0, 0, 0]))
            st.success("🔥 Textured Top + Fade")

        with col2:
            st.image(add_overlay(face, [40, 40, 40]))
            st.success("💼 Side Part")

        with col3:
            st.image(add_overlay(face, [80, 80, 80]))
            st.success("😎 Messy Style")

    # WOMEN
    elif "Women" in category:
        with col1:
            st.image(add_overlay(face, [120, 0, 120]))
            st.success("✨ Layered Hair")

        with col2:
            st.image(add_overlay(face, [200, 50, 50]))
            st.success("💃 Soft Curls")

        with col3:
            st.image(add_overlay(face, [150, 100, 50]))
            st.success("👑 Straight Sleek")

    # KIDS
    elif "Kids" in category:
        with col1:
            st.image(add_overlay(face, [0, 150, 200]))
            st.success("🧒 Cute Short")

        with col2:
            st.image(add_overlay(face, [100, 200, 0]))
            st.success("🎒 School Style")

        with col3:
            st.image(add_overlay(face, [200, 100, 0]))
            st.success("🎉 Fun Style")

    st.markdown("---")

    st.header("🧠 AI Suggestion")

    if "Men" in category:
        st.info("Best for you: Textured Top + Mid Fade + Sharp Beard")
    elif "Women" in category:
        st.info("Best for you: Soft Layers with Volume")
    else:
        st.info("Best for you: Clean, simple & comfortable cut")

else:
    st.warning("Upload your photo to generate looks")
