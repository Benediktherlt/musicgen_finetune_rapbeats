import streamlit as st
import requests


if "description" not in st.session_state:
    st.session_state["description"] = None
if "selected_style" not in st.session_state:
    st.session_state["selected_style"] = None

st.title('Type Beat Generator')

st.write("Welcome to the Type Beat Generator! Enter something or select a style to create your own rap and album cover.")
st.write("""
Manual:
1. Choose one of the three rappers for your general type beat style.
2. Input a formal description of the desired vibe that the type beat should fulfill.
2.1. Press generate.

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


style_options = ['Don Toliver', 'Kid Cudi', 'Don Toliver']
selected_style = st.selectbox("Or select a predefined rapper style:", style_options)

if st.button('Submit Style'):
    if selected_style:
        st.session_state["selected_style"] = selected_style
        st.success("Style submitted successfully")
    else:
        st.error("Please select a style")

if st.session_state["selected_style"] is None:
    st.error("Style is required", icon="🚨")


all_fields_filled = st.session_state["description"] and st.session_state["selected_style"]

audio_placeholder = st.empty()

cover_placeholder = st.empty()

progress_bar = st.progress(0)

generate_button = st.button('Generate', disabled=not all_fields_filled)


if generate_button:
    progress_bar.progress(10)
    with st.spinner('Generating beat and album cover...'):
        #time.sleep(2)  
    
        payload = {
            "text": st.session_state["description"],
            "style": st.session_state["selected_style"]
        }
        response = requests.post('http://localhost:8000/generate/', json=payload)
        if response.status_code == 200:
            result = response.json()
            audio_file = result['filename']
            cover_url = result['cover_url']
          
            audio_placeholder.audio(audio_file, format='audio/wav')
            
            cover_placeholder.image(cover_url, caption='Generated Album Cover')
            progress_bar.progress(100)
        else:
            st.error("Failed to generate rap and cover")
            progress_bar.progress(0)

if st.button('Generate MIDI Files of the Beat'):
    test_audio_file = "generated_data/musicgen_output/[FREE FOR PROFIT] TRAVIS SCOTT X DON TOLIVER X BABY KEEM TYPE BEAT ÔÇ£INSOMNIAÔÇØ (152kbit_Opus).wav"
    response = requests.post('http://localhost:8000/convert_to_midi/', json={"audio_file": test_audio_file})
    if response.status_code == 200:
        midi_files = response.json()['midi_files']
        st.success("MIDI files generated successfully!")
        for midi_file in midi_files:
            with open(midi_file, 'rb') as f:
                st.download_button(
                    label=f"Download {midi_file}",
                    data=f,
                    file_name=midi_file,
                    mime='audio/midi'
                )
    else:
        st.error("Failed to generate MIDI files")
