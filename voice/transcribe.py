import whisper
import log_audio

def transcribe_audio(filepath, date_str, duration):
    """Transcribes audio and logs the result."""
    print("Transcribing...")
    model = whisper.load_model("medium")
    result = model.transcribe(filepath)

    print("Transcription:")
    print(result["text"])

    log_audio.log_command(result["text"], filepath, date_str, duration)