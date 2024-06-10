from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import subprocess
import os
from musicgen_streamlit_POC.convert_audio import split_audio_with_umx, convert_audio_to_midi

app = FastAPI()

class GenerateRequest(BaseModel):
    text: str
    style: str

class ConvertToMidiRequest(BaseModel):
    audio_file: str

@app.post("/generate/")
async def generate(request: GenerateRequest):
    
    text = request.text
    style = request.style
    
    audio_file_path = f"generated_data/musicgen_output/{text}_{style}.wav"
    cover_file_path = f"generated_data/generated_albumcovers/{text}_{style}.png"

    with open(audio_file_path, 'w') as f:
        f.write('dummy audio content')
    with open(cover_file_path, 'w') as f:
        f.write('dummy cover content')
    
    return {
        "filename": audio_file_path,
        "cover_url": cover_file_path
    }

@app.post("/convert_to_midi/")
async def convert_to_midi(request: ConvertToMidiRequest):
    audio_file = request.audio_file
    output_folder = "generated_data/separate_audio_data"
    
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)
    
    midi_file = convert_audio_to_midi(audio_file, output_folder)
    
    return {"midi_files": [midi_file]}
