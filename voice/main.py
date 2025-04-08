import audio
import transcribe

def transcript_text():
    audio_file, date_str, duration = audio.record_audio()
    text = transcribe.transcribe_audio(audio_file)

    return text

if __name__ == "__main__":
    text = transcript_text()
    print(f'You said: {text}')