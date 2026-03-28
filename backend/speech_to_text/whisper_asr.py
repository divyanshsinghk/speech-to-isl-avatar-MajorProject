import whisper


class WhisperASR:
    def __init__(self, model_size="small"):
        print(" Loading Whisper model...")
        self.model = whisper.load_model(model_size)
        print(" Whisper loaded")

    def transcribe(self, audio_path):
        print(" Transcribing...")
        result = self.model.transcribe(audio_path)
        text = result["text"].strip()
        print(" Text:", text)
        return text
