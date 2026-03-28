from speech_to_text.whisper_asr import WhisperASR

from nlp_processing.preprocess import preprocess_text
from nlp_processing.isl_grammar import apply_isl_grammar
from nlp_processing.gloss_generator import generate_gloss

from isl_drive_lookup import get_video_url, build_file_index


# 🔥 Initialize ONCE
asr = WhisperASR()


def run_pipeline(audio_path):
    print("\nINPUT:", audio_path)

    # 🎤 Speech → Text
    text = asr.transcribe(audio_path)
    print("Recognized Text:", text)

    if not text:
        return {
            "text": "",
            "tokens": [],
            "videos": {},
            "metrics": {}
        }

    # 🧹 NLP
    tokens = preprocess_text(text)
    print("Tokens:", tokens)

    tokens = apply_isl_grammar(tokens)
    print("ISL Tokens:", tokens)

    gloss = generate_gloss(tokens)
    print("Gloss:", gloss)

    # 🎬 Build ordered video sequence
    videos = {}

    # 🥇 Try full phrase
    full_url = get_video_url(gloss)

    if full_url:
        print("✅ Full phrase match")
        videos[gloss] = full_url
    else:
        print("⚠️ Falling back to word-level")

        for token in tokens:
            url = get_video_url(token)
            videos[token] = url  # may be None (frontend handles fallback)

    # 📊 Metrics (dummy for now)
    metrics = {
        "wer": 0.1,
        "accuracy": 0.9,
        "precision": 0.85,
        "recall": 0.88,
        "f1": 0.86,
        "latency": 1200,
        "sequence_accuracy": 0.82
    }

    return {
        "text": text,
        "tokens": tokens,
        "videos": videos,
        "metrics": metrics
    }


# 🔥 Build index once when server starts
build_file_index()