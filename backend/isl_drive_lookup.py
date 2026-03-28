from googleapiclient.discovery import build
from google.oauth2.service_account import Credentials
import json

SCOPES = ['https://www.googleapis.com/auth/drive.readonly']
CREDENTIALS_FILE = 'credentials.json'
ROOT_FOLDER_ID = '1U-Pr4r1-cupgNOOq9NH_uTsQnPSVEKco'

# Setup
creds = Credentials.from_service_account_file(
    CREDENTIALS_FILE, scopes=SCOPES
)
service = build('drive', 'v3', credentials=creds)


# 🔤 Normalize text
def normalize(text):
    text = text.upper().strip()
    text = text.replace("'", "")
    return text


# 📁 Get ALL folders
def get_all_folders():
    results = service.files().list(
        q=f"'{ROOT_FOLDER_ID}' in parents and mimeType='application/vnd.google-apps.folder'",
        fields="files(id, name)"
    ).execute()

    return results.get('files', [])


# 📂 Recursive file fetch
def get_files_recursive(folder_id):
    all_files = []
    page_token = None

    while True:
        response = service.files().list(
            q=f"'{folder_id}' in parents",
            fields="nextPageToken, files(id, name, mimeType)",
            pageToken=page_token
        ).execute()

        files = response.get('files', [])

        for file in files:
            if file['mimeType'] == 'application/vnd.google-apps.folder':
                all_files.extend(get_files_recursive(file['id']))
            else:
                all_files.append(file)

        page_token = response.get('nextPageToken')
        if not page_token:
            break

    return all_files


# 🔥 LOAD DICTIONARY
with open("video_dictionary.json") as f:
    VIDEO_DICT = json.load(f)


# 🔥 FILE INDEX
FILE_INDEX = {}


def build_file_index():
    print("Building file index (one-time)...")

    folders = get_all_folders()

    for folder in folders:
        files = get_files_recursive(folder['id'])

        for file in files:
            FILE_INDEX[file['name']] = file['id']

    print(f"Indexed {len(FILE_INDEX)} files")


# 🎯 GET VIDEO URL (FIXED)
def get_video_url(query):
    query_clean = normalize(query)

    if query_clean not in VIDEO_DICT:
        return None

    filename = VIDEO_DICT[query_clean]

    if filename not in FILE_INDEX:
        return None

    file_id = FILE_INDEX[filename]

    # ✅ FIXED URL
    return f"https://drive.google.com/file/d/{file_id}/preview"