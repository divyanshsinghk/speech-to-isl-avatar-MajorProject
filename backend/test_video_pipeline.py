from nlp_processing.preprocess import preprocess_text
from nlp_processing.gloss_generator import generate_gloss
from nlp_processing.isl_grammar import apply_isl_grammar

from isl_drive_lookup import get_video_url, build_file_index
from video_player import play_videos
from display_fingerspelling import display_fingerspelling


def run_test(sentence):
    print("\nINPUT:", sentence)

    # 🧹 Preprocess
    tokens = preprocess_text(sentence)
    print("Tokens:", tokens)

    # 📐 Grammar
    tokens = apply_isl_grammar(tokens)
    print("ISL Tokens:", tokens)

    # 🧠 Gloss
    gloss = generate_gloss(tokens)
    print("Gloss:", gloss)

    # 🔥 ORDER-PRESERVING SEQUENCE
    sequence = []

    # 🥇 Try full phrase
    print("Trying full phrase:", gloss)
    url = get_video_url(gloss)

    if url:
        print("✅ Full phrase match found")
        sequence.append(("video", url))

    else:
        print("⚠️ Falling back to word-level")

        for token in tokens:
            print("Searching for:", token)

            url = get_video_url(token)

            if url:
                print("Found:", token)
                sequence.append(("video", url))
            else:
                sequence.append(("fallback", token))

    # 🎬 PLAY IN ORDER
    for item_type, value in sequence:

        if item_type == "video":
            play_videos([value])

        elif item_type == "fallback":
            if value != "I":  # 🔥 ignore weak tokens
                display_fingerspelling([value])


if __name__ == "__main__":
    # 🔥 build index once
    build_file_index()

    run_test("I pray to hanuman")
    run_test("I don't know")
    run_test("I am happy")