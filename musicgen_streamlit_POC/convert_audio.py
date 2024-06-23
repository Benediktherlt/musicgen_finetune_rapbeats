import re
import os
import logging
from basic_pitch.inference import predict_and_save, ICASSP_2022_MODEL_PATH

logging.basicConfig(level=logging.INFO)

def convert_audio_to_midi(input_file, output_folder):
    try:
        if not os.path.exists(output_folder):
            os.makedirs(output_folder)
        
        predict_and_save(
            audio_path_list=[input_file],
            output_directory=output_folder,
            save_midi=True,
            sonify_midi=False,
            save_model_outputs=False,
            save_notes=False,
            model_or_model_path=ICASSP_2022_MODEL_PATH  
        )
        midi_output_file = os.path.join(output_folder, os.path.basename(input_file).replace(".wav.wav", ".wav_basic_pitch.mid"))
        logging.info(f"Converted {input_file} to {midi_output_file}")
        return midi_output_file
    except Exception as e:
        logging.error(f"Error converting {input_file} to MIDI: {e}")
        return None
    
def get_latest_file(directory):
    pattern = re.compile(r'output_(\d+)_(\d+)\.wav\.wav')

    files = []
    for filename in os.listdir(directory):
        match = pattern.match(filename)
        if match:
            date, time = match.groups()
            files.append((filename, date, time))
    
    files.sort(key=lambda x: (x[1], x[2]), reverse=True)
    
    if files:
        return os.path.join(directory, files[0][0])
    return None


