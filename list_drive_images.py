"""
List all images in the Google Drive folder to see what's actually there.
"""
import sys
import io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', line_buffering=True)
sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8', line_buffering=True)

from google.oauth2.credentials import Credentials
from google_drive_handler import GoogleDriveHandler, extract_folder_id

def main():
    # Folder from your sheet
    folder_url = "https://drive.google.com/drive/folders/1wuA-90cxcn8bV9Avj2-pBbk9Chjf1dnq"
    folder_id = extract_folder_id(folder_url)

    print("="*70)
    print("LISTING IMAGES IN GOOGLE DRIVE FOLDER")
    print("="*70)
    print(f"Folder ID: {folder_id}")
    print(f"Folder URL: {folder_url}")
    print()

    # Load credentials
    creds = Credentials.from_authorized_user_file('token.json')

    # Initialize handler
    drive_handler = GoogleDriveHandler(creds)

    # List files
    print("Fetching file list from Drive...")
    files = drive_handler.list_folder_files(folder_id)

    print(f"\n✓ Found {len(files)} files in folder:\n")
    print("-"*70)

    if files:
        for i, file in enumerate(files, 1):
            print(f"{i}. {file['name']}")
            print(f"   ID: {file['id']}")
            print(f"   MIME: {file.get('mimeType', 'unknown')}")
            print()
    else:
        print("No files found in folder!")

    print("="*70)
    print("\nIMAGES REFERENCED IN GOOGLE DOC:")
    print("-"*70)
    print("Page 1 (Lamb Vindaloo): lamb-vindaloo-lancaster-pa.jpg")
    print("Page 2 (Chicken Tikka Masala): chicken-tikka-masala-lancaster-pa.jpg")
    print()
    print("="*70)
    print("\nFIX OPTIONS:")
    print("-"*70)
    print("1. Rename files in Google Drive to match the doc")
    print("2. Update the Google Doc with the correct filenames")
    print("3. Upload new images with the correct names")

if __name__ == "__main__":
    main()
