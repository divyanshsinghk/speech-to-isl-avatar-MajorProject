import json
from isl_drive_lookup import service, get_all_folders

MAX_DURATION_MS = 20000  # 20 seconds


def get_files_with_metadata(folder_id):
    res = service.files().list(
        q=f"'{folder_id}' in parents",
        fields="files(id, name, videoMediaMetadata)"
    ).execute()

    return res.get('files', [])


def scrape_all_files():
    data = []

    folders = get_all_folders()

    print(f"Total folders: {len(folders)}")

    for folder in folders:
        print(f"Checking folder: {folder['name']}")

        files = get_files_with_metadata(folder['id'])

        for file in files:
            name = file['name']

            metadata = file.get("videoMediaMetadata", {})
            duration = metadata.get("durationMillis")

            # ❗ Skip if no duration info
            if not duration:
                continue

            duration = int(duration)

            # ❌ FILTER LONG VIDEOS
            if duration > MAX_DURATION_MS:
                print(f"Skipping long video: {name}")
                continue

            data.append({
                "filename": name,
                "duration": duration
            })

    with open("filtered_dataset.json", "w") as f:
        json.dump(data, f, indent=2)

    print("✅ Filtered dataset saved!")


if __name__ == "__main__":
    scrape_all_files()