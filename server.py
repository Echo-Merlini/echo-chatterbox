#!/usr/bin/env python3
"""
Echo Chatterbox TTS Server — keeps model hot in memory for fast inference.
POST /speak  { "text": "...", "exaggeration": 0.5, "cfg_weight": 0.5 }
Returns: audio/wav
"""
import io, os, logging, threading
import soundfile as sf
from fastapi import FastAPI, HTTPException
from fastapi.responses import Response
from pydantic import BaseModel
from chatterbox.tts import ChatterboxTTS

logging.basicConfig(level=logging.INFO, format="%(asctime)s %(message)s")
log = logging.getLogger("chatterbox-server")

DEVICE = os.environ.get("DEVICE", "cpu")
VOICE_REF = os.environ.get("VOICE_REF", "/voices/active_ref.wav")

app = FastAPI(title="Chatterbox TTS Server")

log.info(f"Loading Chatterbox model on {DEVICE}...")
model = ChatterboxTTS.from_pretrained(device=DEVICE)
log.info("Model ready.")

_lock = threading.Lock()

class SpeakRequest(BaseModel):
    text: str
    exaggeration: float = 0.5
    cfg_weight: float = 0.5
    temperature: float = 0.8

@app.post("/speak")
def speak(req: SpeakRequest):
    if not req.text.strip():
        raise HTTPException(status_code=400, detail="text is required")
    ref = VOICE_REF if os.path.exists(VOICE_REF) else None
    log.info(f"Generating: {req.text[:60]}...")
    with _lock:
        wav = model.generate(req.text, audio_prompt_path=ref,
                             exaggeration=req.exaggeration,
                             cfg_weight=req.cfg_weight,
                             temperature=req.temperature)
    buf = io.BytesIO()
    sf.write(buf, wav.squeeze().numpy(), model.sr, format="WAV")
    buf.seek(0)
    log.info("Done.")
    return Response(content=buf.read(), media_type="audio/wav")

@app.get("/health")
def health():
    return {"status": "ok", "device": DEVICE, "voice_ref": VOICE_REF, "ref_exists": os.path.exists(VOICE_REF)}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=5050, log_level="info")
