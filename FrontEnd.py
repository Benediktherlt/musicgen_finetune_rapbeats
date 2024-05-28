import streamlit as st
import requests

st.title('Rap Generator')

st.write("Welcome to the Rap Generator! Enter lyrics or select a style to create your own rap.")

user_input = st.text_input("Enter here:")

# Option to select a rapper style
style_options = ['Rapper1', 'Rapper2', 'Rapper3', 'Rapper4']
selected_style = st.selectbox("Or select a predefined rapper style:", style_options)

# Placeholder for audio
audio_placeholder = st.empty()

# Button to generate the rap
if st.button('Generate Rap'):
    if selected_style != 'Choose a style' or user_input:
        # Sending request to backend
        payload = {"text": user_input or selected_style}
        response = requests.post('http://localhost:8000/generate/', json=payload)
        if response.status_code == 200:
            audio_file = response.json()['filename']
            # Displaying the audio file
            audio_placeholder.audio(audio_file, format='audio/wav')
        else:
            st.error("Failed to generate rap")
    else:
        st.warning("Please enter lyrics or select a style.")

