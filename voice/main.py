import audio
import transcribe

def main():
    audio_file, date_str, duration = audio.record_audio()
    transcribe.transcribe_audio(audio_file, date_str, duration)

if __name__ == "__main__":
    main()