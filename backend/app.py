from fastapi import FastAPI, UploadFile, File
from fastapi.responses import JSONResponse
from transformers import pipeline
import torchaudio
import tempfile
import os

app = FastAPI()

# Root and Health Check
@app.get("/")
def root():
    return {"message": "Voia is LIVE!🚀"}

@app.get("/healthz")
async def health_check():
    return {"status": "ok"}


# Initialize Hugging Face pipeline
asr = pipeline("automatic-speech-recognition", model="openai/whisper-tiny.en")
# asr = pipeline("automatic-speech-recognition", model="openai/whisper-medium.en")


# Voice to Text (Listen)
@app.post("/listen")
async def listen(file: UploadFile = File(...)):
    try:
        # Save the uploaded audio to a temp file
        with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as tmp:
            tmp.write(await file.read())
            tmp_path = tmp.name

        # Load waveform with torchaudio (ffmpeg not needed)
        waveform, sample_rate = torchaudio.load(tmp_path)

        # Transcribe using Hugging Face pipeline
        result = asr({
            "array": waveform.squeeze().numpy(),
            "sampling_rate": sample_rate
        })

        # Clean up temp file
        os.remove(tmp_path)

        return {"text": result["text"]}

    except Exception as e:
        return JSONResponse(status_code=500, content={"error": str(e)})