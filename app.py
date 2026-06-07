import streamlit as st
import requests
import time

def generate_ai_look(uploaded_file, vibe, style):
    # ... (Keep your existing Gemini analysis code here) ...
    
    # 1. Use a tuple (connect_timeout, read_timeout)
    # The first value is for connecting, the second is for waiting for data
    timeout_config = (5, 45) 
    
    with st.spinner("Generating your new style..."):
        # 2. Implement a retry loop to handle transient server issues
        for attempt in range(3): 
            try:
                response = requests.get(pollinations_url, timeout=timeout_config)
                
                # Check if the request was successful and content is valid
                if response.status_code == 200 and len(response.content) > 1000:
                    return response.content
                
                # If status is not 200, wait and try again
                time.sleep(2) 
            
            except requests.exceptions.Timeout:
                st.warning(f"Attempt {attempt+1}: Server took too long. Retrying...")
            except requests.exceptions.RequestException as e:
                st.error(f"Error: {e}")
                break
        
        return None
