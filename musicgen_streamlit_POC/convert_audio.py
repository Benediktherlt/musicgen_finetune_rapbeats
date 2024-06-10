
import subprocess
import os

def convert_audio_to_midi(input_file, output_folder):
    # Verwende audio-to-midi, um die WAV-Dateien in MIDI umzuwandeln
    midi_output_file = os.path.join(output_folder, os.path.basename(input_file).replace(".wav", ".mid"))
    subprocess.run(['audio-to-midi', input_file, '-o', midi_output_file])
    return midi_output_file


