import streamlit as st
import cv2
import numpy as np
from PIL import Image
import mediapipe as mp
st.info("Step 1: Select category → Step 2: Upload photo → Step 3: Get your best look")
st.set_page_config(page_title="How I Look AI 🇮🇳", layout="centered")

st.title("🇮🇳 How I Look AI")
st.subheader("Find your best hairstyle instantly")

# -----------------------------
# CATEGORY SELECTION
# -----------------------------
category = st.radio(
    "Select Category",
    ["Men 👨", "Women 👩", "Kids 🧒"],
    horizontal=True
)

uploaded_file = st.file_uploader("Upload your photo", type=["jpg", "jpeg", "png"])

# -----------------------------
# FACE DETECTION
# -----------------------------
mp_face = mp.solutions.face_detection
face_detection = mp_face.FaceDetection()

def detect_face(image):
    img = np.array(image)
    img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
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


# -----------------------------
# FAKE STYLE OVERLAY
# -----------------------------
def add_overlay(face_img, color):
    overlay = face_img.copy()
    h, w, _ = overlay.shape

    cv2.rectangle(overlay, (0, 0), (w, int(h*0.25)), color, -1)
    blended = cv2.addWeighted(overlay, 0.4, face_img, 0.6, 0)

    return blended


# -----------------------------
# MAIN LOGIC
# -----------------------------
if uploaded_file:
    image = Image.open(uploaded_file)
    st.image(image, caption="Your Photo", use_column_width=True)

    face = detect_face(image)

    st.markdown("---")
    st.header("✨ Your Top 3 Looks")

    col1, col2, col3 = st.columns(3)

    # ---------------- MEN ----------------
    if "Men" in category:
        with col1:
            st.image(add_overlay(face, (0, 0, 0)))
            st.success("🔥 Textured Top + Fade")
