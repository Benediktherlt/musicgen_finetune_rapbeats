from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

class RequestData(BaseModel):
    text: str  # Input text from the frontend.

@app.post("/generate/")
async def generate_rap(request: RequestData):

    return {"message": "Audio generated successfully", "filename": "path_to_generated_audio.wav"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
