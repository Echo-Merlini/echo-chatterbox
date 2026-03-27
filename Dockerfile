FROM python:3.11-slim

RUN apt-get update && apt-get install -y ffmpeg libsndfile1 && rm -rf /var/lib/apt/lists/*

WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY server.py .

# /voices — voice reference WAVs
# /root/.cache/huggingface — model cache so HF models survive restarts
VOLUME ["/voices", "/root/.cache/huggingface"]
EXPOSE 5050

CMD ["uvicorn", "server:app", "--host", "0.0.0.0", "--port", "5050"]
