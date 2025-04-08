import whisper

def transcribe_audio(filepath):
    """Transcribes audio and logs the result."""
    # print("Transcribing...")
    model = whisper.load_model("medium")
    result = model.transcribe(filepath)

    # print("Transcription:")
    # print(result["text"])

    return result['text']