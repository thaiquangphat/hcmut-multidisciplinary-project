import whisper
import torch

def transcribe_audio(filepath):
    """Transcribes audio and logs the result."""
    # print("Transcribing...")

    device = "cuda" if torch.cuda.is_available() else "cpu"

    model = whisper.load_model("medium", device=device)
    result = model.transcribe(filepath, fp16=(device=='gpu'))

    # print("Transcription:")
    # print(result["text"])

    return result['text']