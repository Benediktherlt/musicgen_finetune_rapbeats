import streamlit as st
from connect_with_runpod import run_inference_on_runpod
import os
import logging

logging.basicConfig(level=logging.INFO)

if "description" not in st.session_state:
    st.session_state["description"] = None
if "progress" not in st.session_state:
    st.session_state["progress"] = 0

st.title('Type Beat Generator')

st.write("Welcome to the Type Beat Generator! Enter something to create your own rap and album cover.")
st.write("""
Manual:
1. Input a formal description of the desired vibe that the type beat should fulfill.
2. Press generate.

The created type beat and album cover are both downloadable. For the type beat, you can either directly download it as a .wav or trigger a MIDI conversion to download separate MIDI files.
""")

user_input = st.text_input("Enter something here:")

if st.button('Submit Description'):
    if user_input:
        st.session_state["description"] = user_input
        st.success("Description submitted successfully")
    else:
        st.error("Please enter a description")

if st.session_state["description"] is None:
    st.error("Description is required", icon="🚨")

all_fields_filled = st.session_state["description"]

audio_placeholder = st.empty()

progress_bar = st.progress(0)


def update_progress(step):
    st.session_state["progress"] = min(st.session_state["progress"] + step, 100)
    progress_bar.progress(st.session_state["progress"])

generate_button = st.button('Generate', disabled=not all_fields_filled)

if generate_button:
    st.session_state["progress"] = 0
    update_progress(10)  
    with st.spinner('Generating beat and album cover...'):
        logging.info(f"Generating with description: {st.session_state['description']}")
        result, error, progress = run_inference_on_runpod(st.session_state["description"])
        update_progress(progress - st.session_state["progress"])  
        if result:
            logging.info(f"Generated file: {result}")
            audio_placeholder.audio(result, format='audio/wav')
            update_progress(10)  
        else:
            logging.error(f"Failed to generate rap and cover: {error}")
            st.error(f"Failed to generate rap and cover: {error}")
            update_progress(0)