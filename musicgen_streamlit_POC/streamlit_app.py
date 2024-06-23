import streamlit as st
from connect_with_runpod import run_inference_on_runpod
import os
import logging
from convert_audio import convert_audio_to_midi, get_latest_file
import time

logging.basicConfig(level=logging.INFO)

if "description" not in st.session_state:
    st.session_state["description"] = None
if "progress" not in st.session_state:
    st.session_state["progress"] = 0
if "generated_file" not in st.session_state:
    st.session_state["generated_file"] = None
if "latest_file" not in st.session_state:
    st.session_state["latest_file"] = None
if "midi_file" not in st.session_state:
    st.session_state["midi_file"] = None

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
            st.session_state["generated_file"] = result
            audio_placeholder.audio(result, format='audio/wav')
            st.session_state["latest_file"] = get_latest_file(os.path.join(os.path.dirname(result), "..", "musicgen_output"))
            update_progress(10)
        else:
            logging.error(f"Failed to generate rap and cover: {error}")
            st.error(f"Failed to generate rap and cover: {error}")
            update_progress(0)

if st.session_state["generated_file"]:
    st.write("Generated file available for download:")
    st.download_button(
        label="Download WAV",
        data=open(st.session_state["generated_file"], "rb").read(),
        file_name=os.path.basename(st.session_state["generated_file"])
    )

if st.session_state["latest_file"]:
    convert_to_midi_button = st.button('Generate MIDI Files')

    if convert_to_midi_button:
        with st.spinner('Converting to MIDI...'):
            input_file = st.session_state["latest_file"]
            output_folder = os.path.join(os.path.dirname(input_file), "..", "seperated_audio_data")
            output_folder = os.path.abspath(output_folder)
            midi_file = convert_audio_to_midi(input_file, output_folder)
            if midi_file:
                st.success("MIDI conversion successful!")
                st.session_state["midi_file_path"] = midi_file  # Pfad der Datei speichern

if "midi_file_path" in st.session_state:
    midi_file_path = st.session_state["midi_file_path"]
    if os.path.exists(midi_file_path):
        st.write("MIDI file available for download:")
        st.download_button(
            label="Download MIDI",
            data=open(midi_file_path, "rb").read(),
            file_name=os.path.basename(midi_file_path)
        )
    else:
        st.error(f"MIDI file not found: {midi_file_path}")