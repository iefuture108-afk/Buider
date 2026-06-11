import streamlit as st
import requests
import numpy as np
from PIL import Image
import io
import random
from google import genai
import base64

# =============================================================================
# CONFIGURATION & PAGE SETUP
# =============================================================================

st.set_page_config(
    page_title="AI Hairstyle Transformer",
    page_icon="✂️",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# =============================================================================
# HELPER FUNCTIONS
# =============================================================================

@st.cache_data(ttl=3600)
def extract_face_description(image_file, api_key: str) -> str:
    """
    Phase 1: Facial Structure Extraction
    Uses Google GenAI SDK to extract physical summary from uploaded portrait.
    Returns a single sentence plain-text description without punctuation that
    could corrupt URL strings.
    """
    try:
        # Initialize Google GenAI client
        client = genai.Client(api_key=api_key)
        
        # Read image bytes
        image_bytes = image_file.read()
        
        # Prepare the image for GenAI
        image_input = {
            "mime_type": "image/jpeg",
            "data": image_bytes
        }
        
        # Strict prompt ignoring current hair, extracting only face shape, gender, skin tone
        prompt = """Analyze this portrait and extract ONLY the physical characteristics. 
        Ignore any current hair features completely. 
        Describe face shape (oval, round, square, heart, diamond), gender presentation (male/female), 
        and skin tone (light, medium, dark). 
        Output must be exactly ONE sentence with NO quotation marks, NO colons, NO punctuation 
        except spaces. Example format: oval face female with medium skin tone"""
        
        # Call gemini-2.5-flash model
        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=[prompt, image_input]
        )
        
        # Clean the response: remove quotes, colons, extra punctuation
        clean_text = response.text.strip()
        clean_text = clean_text.replace('"', '').replace("'", '')
        clean_text = clean_text.replace(':', '').replace(';', '')
        clean_text = clean_text.replace('.', '').replace(',', '')
        clean_text = clean_text.replace('!', '').replace('?', '')
        
        # Normalize whitespace
        clean_text = ' '.join(clean_text.split())
        
        return clean_text
        
    except Exception as e:
        st.error(f"Face extraction failed: {str(e)}")
        raise


@st.cache_data(ttl=0)
def generate_hairstyle_image(
    face_description: str,
    vibe: str,
    style: str,
    seed: int
) -> bytes:
    """
    Phase 2: Asynchronous Image Generation
    Routes through Pollinations API with Flux engine to bypass Gemini quota walls.
    Implements 3-attempt loop with randomized User-Agent to circumvent queue drops.
    """
    
    # Build the polished visual blueprint
    visual_blueprint = f"""
    A realistic professional portrait of a person with {face_description},
    wearing {vibe} {style} hairstyle, high quality, photorealistic,
    detailed facial features, natural lighting, studio photography
    """
    
    # Pollinations API URL with Flux engine
    base_url = "https://image.pollinations.ai/prompt/"
    encoded_prompt = visual_blueprint.replace("
", " ").strip()
    
    pollinations_url = f"{base_url}{encoded_prompt}&model=flux&seed={seed}&width=1024&height=1024&nologo=true"
    
    # Randomized User-Agent headers to circumvent container queue drops
    user_agents = [
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36",
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:122.0) Gecko/20100101 Firefox/122.0",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.2 Safari/605.1.15",
        "Mozilla/5.0 (Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
    ]
    
    # 3-attempt request loop
    for attempt in range(3):
        try:
            # Randomize User-Agent for each attempt
            random_agent = user_agents[attempt % len(user_agents)]
            
            headers = {
                "User-Agent": random_agent,
                "Accept": "image/png,image/jpeg,*/*",
                "Accept-Language": "en-US,en;q=0.9",
                "Connection": "keep-alive"
            }
            
            # Make request with timeout
            response = requests.get(
                pollinations_url,
                headers=headers,
                timeout=45
            )
            
            # Check for successful response
            if response.status_code == 200:
                return response.content
            elif response.status_code == 429:
                # Resource exhausted - retry with different agent
                st.warning(f"Rate limit hit, retrying... ({attempt + 1}/3)")
                continue
            else:
                st.warning(f"Attempt {attempt + 1} failed with status {response.status_code}")
                continue
                
        except requests.exceptions.Timeout:
            st.warning(f"Timeout on attempt {attempt + 1}, retrying...")
            continue
        except requests.exceptions.ConnectionError:
            st.warning(f"Connection error on attempt {attempt + 1}, retrying...")
            continue
        except Exception as e:
            st.warning(f"Error on attempt {attempt + 1}: {str(e)}")
            continue
    
    # All attempts failed
    raise Exception("Image generation failed after 3 attempts. Please try again.")


def create_download_button(image_bytes: bytes) -> None:
    """
    Creates an instant PNG download button using in-memory binary cache.
    """
    # Create download button
    st.download_button(
        label="⬇️ Download PNG",
        data=image_bytes,
        file_name="hairstyle_transform.png",
        mime="image/png",
        use_container_width=True,
        type="primary"
    )


# =============================================================================
# MAIN APPLICATION INTERFACE
# =============================================================================

def main():
    """
    Main application entry point.
    Implements clean single-column scannable web dashboard.
    """
    
    # Title
    st.title("AI Hairstyle Transformer")
    st.markdown("---")
    
    # File Input - restrict to PNG, JPG, JPEG only
    st.subheader("Upload Your Portrait")
    uploaded_file = st.file_uploader(
        "Choose an image (PNG, JPG, JPEG only)",
        type=["png", "jpg", "jpeg"],
        accept_multiple_files=False
    )
    
    if uploaded_file is not None:
        # Display uploaded image
        st.image(
            uploaded_file,
            caption="Your uploaded portrait",
            use_container_width=True
        )
        st.markdown("---")
    
    # Aesthetic Modifiers
    st.subheader("Customize Your Style")
    
    # Pick a vibe - selectbox
    vibe = st.selectbox(
        "Pick a vibe",
        options=["Professional", "Casual", "Edgy"],
        index=0
    )
    
    # Pick your final style - radio group
    style = st.radio(
        "Pick your final style",
        options=["Short & Clean", "Long & Wavy", "Textured Fade"],
        index=0
    )
    
    st.markdown("---")
    
    # Execution Trigger
    st.subheader("Generate Your New Look")
    
    generate_button = st.button(
        "✨ Transform My Hairstyle",
        type="primary",
        use_container_width=True
    )
    
    # Handle button click
    if generate_button:
        if uploaded_file is None:
            st.error("⚠️ Please upload a portrait image first!")
            st.stop()
        
        # Get API key from secrets
        api_key = st.secrets.get("GEMINI_API_KEY")
        
        if not api_key:
            st.error("⚠️ GEMINI_API_KEY not found in secrets! Please add it to your .streamlit/secrets.toml")
            st.stop()
        
        # Background spinners and progress
        with st.spinner("🔍 Analyzing your facial structure..."):
            try:
                # Phase 1: Extract face description
                face_description = extract_face_description(uploaded_file, api_key)
                st.success(f"✓ Face analysis complete: {face_description}")
                
            except Exception as e:
                st.error(f"❌ Face extraction failed: {str(e)}")
                st.stop()
        
        with st.spinner("🎨 Generating your new hairstyle..."):
            try:
                # Generate cache-busting dynamic seed
                seed = random.randint(100000, 999999)
                
                # Phase 2: Generate hairstyle image
                image_bytes = generate_hairstyle_image(
                    face_description=face_description,
                    vibe=vibe,
                    style=style,
                    seed=seed
                )
                
                # Validate image bytes
                if len(image_bytes) < 1000:
                    st.error("❌ Generated image is invalid or too small")
                    st.stop()
                
                st.success("✓ Hairstyle generated successfully!")
                
                # Display result
                st.subheader("Your New Look")
                st.image(
                    image_bytes,
                    caption=f"{vibe} {style} hairstyle",
                    use_container_width=True
                )
                
                # Unlock download button
                st.markdown("---")
                create_download_button(image_bytes)
                
            except Exception as e:
                st.error(f"❌ Image generation failed: {str(e)}")
                st.stop()


# =============================================================================
# APPLICATION ENTRY POINT
# =============================================================================

if __name__ == "__main__":
    main()
