import whisper
import torch

def transcribe_audio(filepath, device):
    """Transcribes audio and logs the result."""
    # print("Transcribing...")

    model = whisper.load_model("medium", device=device)
    result = model.transcribe(filepath, fp16=(device=='gpu'))

    # print("Transcription:")
    # print(result["text"])

    return result['text']