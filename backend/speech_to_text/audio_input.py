import sounddevice as sd
import scipy.io.wavfile as wav
import numpy as np

def record_audio(filename="input.wav", duration=10, fs=16000):
    print("Recording... speak loudly and continuously")

    device_id = 1  # Microphone Array (AMD Audio Device)

    audio = sd.rec(
        int(duration * fs),
        samplerate=fs,
        channels=1,
        device=device_id,
        dtype="int16"
    )
    sd.wait()

    # Convert to float for amplification
    audio = audio.astype(np.float32)

    # Amplify signal
    max_val = np.max(np.abs(audio))
    if max_val < 500:
        print(" Audio level too low, amplifying")
        audio *= 20

    audio = np.clip(audio, -32768, 32767)
    audio = audio.astype(np.int16)

    wav.write(filename, fs, audio)
    print(" Recording saved as", filename)
    print(" Max amplitude:", int(np.max(np.abs(audio))))

    return filename
