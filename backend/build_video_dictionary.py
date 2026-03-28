import json
from isl_drive_lookup import get_all_folders, get_files_recursive  # ✅ FIXED IMPORT

video_dict = {}

# words to ignore (noise)
IGNORE_WORDS = {
    "YOUR", "THE", "A", "AN", "OF", "TO", "AND",
    "WITH", "FROM", "THIS", "THAT", "BY", "ITS"
}


def normalize(filename):
    name = filename.upper().replace(".MP4", "")
    name = name.replace("_", " ")
    name = name.replace("'", "")  # remove apostrophe
    return name.strip()


def clean_words(name):
    words = name.split()

    clean = []
    for w in words:
        # ❌ remove junk like (, ), -, , etc.
        if not w.isalpha():
            continue

        # ❌ remove very small tokens
        if len(w) < 2:
            continue

        if w in IGNORE_WORDS:
            continue

        clean.append(w)

    return clean


def add_mapping(key, filename):
    if key not in video_dict:
        video_dict[key] = filename
    else:
        existing = video_dict[key]

        # ✅ prefer exact/simple file (single concept)
        if "_" not in filename:
            video_dict[key] = filename

        # ✅ otherwise prefer shorter filename
        elif filename.count("_") < existing.count("_"):
            video_dict[key] = filename


def build_dictionary():
    folders = get_all_folders()

    print(f"Found {len(folders)} folders")

    total_files = 0

    for folder in folders:
        print(f"Processing folder: {folder['name']}")

        # ✅ RECURSIVE SCRAPING (CRITICAL FIX)
        files = get_files_recursive(folder['id'])
        print(f"  → {len(files)} files")

        total_files += len(files)

        for file in files:
            filename = file['name']

            # ❌ skip non-video files
            if not filename.lower().endswith(".mp4"):
                continue

            name = normalize(filename)
            words = clean_words(name)

            if not words:
                continue

            # 🥇 FULL PHRASE
            add_mapping(name, filename)

            # 🥉 SINGLE WORDS
            for word in words:
                add_mapping(word, filename)

    print(f"\nTotal files processed: {total_files}")
    print(f"Total dictionary entries: {len(video_dict)}")

    # save dictionary
    with open("video_dictionary.json", "w") as f:
        json.dump(video_dict, f, indent=2)

    print("✅ Smart dictionary created!")


if __name__ == "__main__":
    build_dictionary()