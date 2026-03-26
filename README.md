# echo-chatterbox

Chatterbox TTS server — keeps model hot in memory for fast inference.

## Endpoints

- `POST /speak` — Generate speech, returns `audio/wav`
- `GET /health` — Health check

### POST /speak

```json
{
  "text": "Hello world",
  "exaggeration": 0.5,
  "cfg_weight": 0.5,
  "temperature": 0.8
}
```

## Environment Variables

| Variable | Default | Description |
|----------|---------|-------------|
| `DEVICE` | `cpu` | Inference device: `cpu`, `mps`, or `cuda` |
| `VOICE_REF` | `/voices/active_ref.wav` | Path to voice clone reference WAV |

## Usage

```bash
docker compose up --build
```

Mount your voice reference WAV file into `/voices/` and set `VOICE_REF` accordingly.

## Port

`5050`
