"""
Google Drive integration for downloading restaurant images.
"""
import logging
import re
from typing import Dict, List, Optional
from pathlib import Path
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
import requests
import io


logger = logging.getLogger("foodamigo_automation.google_drive")


class GoogleDriveHandler:
    """Handler for Google Drive file operations."""

    def __init__(self, credentials: Credentials):
        """
        Initialize Drive handler.

        Args:
            credentials: Google OAuth2 credentials
        """
        self.credentials = credentials
        self.service = build('drive', 'v3', credentials=credentials)

    def list_folder_files(self, folder_id: str) -> List[Dict]:
        """
        List all files in a Google Drive folder.

        Args:
            folder_id: Google Drive folder ID

        Returns:
            List of file metadata dicts with keys: id, name, mimeType

        Raises:
            Exception: If listing fails
        """
        logger.info(f"Listing files in folder: {folder_id}")

        try:
            results = []
            page_token = None

            while True:
                # Query for files in folder
                query = f"'{folder_id}' in parents and trashed=false"

                response = self.service.files().list(
                    q=query,
                    spaces='drive',
                    fields='nextPageToken, files(id, name, mimeType)',
                    pageToken=page_token
                ).execute()

                files = response.get('files', [])
                results.extend(files)

                page_token = response.get('nextPageToken')
                if not page_token:
                    break

            logger.info(f"✓ Found {len(results)} files in folder")
            return results

        except HttpError as e:
            logger.error(f"Failed to list folder: {e}")
            raise Exception(f"Google Drive API error: {e}")

    def download_images_to_cache(
        self,
        folder_id: str,
        cache_dir: Path,
        restaurant_name: str
    ) -> Dict[str, Path]:
        """
        Download all images from folder to local cache.

        Args:
            folder_id: Google Drive folder ID
            cache_dir: Local cache directory
            restaurant_name: Restaurant name (for subfolder)

        Returns:
            Dictionary mapping filename -> local file path
            Example: {"001-butter-chicken.jpg": Path("cache/hwy-to-india/001-butter-chicken.jpg")}

        Raises:
            Exception: If download fails
        """
        logger.info(f"Downloading images for {restaurant_name}...")

        # Create restaurant cache subdirectory
        restaurant_cache = cache_dir / self._sanitize_filename(restaurant_name)
        restaurant_cache.mkdir(parents=True, exist_ok=True)

        # List all files
        files = self.list_folder_files(folder_id)

        # Filter image files
        image_extensions = ['.jpg', '.jpeg', '.png', '.gif', '.webp']
        image_files = [
            f for f in files
            if any(f['name'].lower().endswith(ext) for ext in image_extensions)
        ]

        if not image_files:
            logger.warning(f"No image files found in folder")
            return {}

        logger.info(f"Downloading {len(image_files)} images...")

        # Download each image
        downloaded = {}
        failed = []

        for file_info in image_files:
            try:
                file_id = file_info['id']
                filename = file_info['name']

                # Download file
                local_path = restaurant_cache / filename
                self._download_file(file_id, local_path)

                # Store in lookup (case-insensitive key)
                key = filename.lower()
                downloaded[key] = local_path

                logger.debug(f"✓ Downloaded: {filename}")

            except Exception as e:
                logger.error(f"✗ Failed to download {file_info['name']}: {e}")
                failed.append(file_info['name'])

        logger.info(f"✓ Downloaded {len(downloaded)}/{len(image_files)} images")

        if failed:
            logger.warning(f"Failed downloads: {', '.join(failed)}")

        return downloaded

    def _download_file(self, file_id: str, local_path: Path):
        """
        Download a single file from Drive.

        Args:
            file_id: Google Drive file ID
            local_path: Local path to save file

        Raises:
            Exception: If download fails
        """
        try:
            # Get file content
            request = self.service.files().get_media(fileId=file_id)

            # Download in chunks
            fh = io.BytesIO()
            downloader = request.execute()

            # Save to file
            with open(local_path, 'wb') as f:
                f.write(downloader)

        except HttpError as e:
            raise Exception(f"Drive API error: {e}")

    def _sanitize_filename(self, name: str) -> str:
        """
        Sanitize filename for safe file system usage.

        Args:
            name: Original name

        Returns:
            Sanitized name (lowercase, hyphens)
        """
        # Replace spaces and special chars with hyphens
        name = re.sub(r'[^\w\s-]', '', name)
        name = re.sub(r'[\s]+', '-', name)
        return name.lower()


def extract_folder_id(folder_url: str) -> str:
    """
    Extract folder ID from Google Drive URL.

    Args:
        folder_url: Full Google Drive folder URL

    Returns:
        Folder ID

    Example:
        URL: https://drive.google.com/drive/folders/1ABC123...
        Returns: 1ABC123...
    """
    match = re.search(r'/folders/([a-zA-Z0-9-_]+)', folder_url)
    if match:
        return match.group(1)
    raise ValueError(f"Could not extract folder ID from URL: {folder_url}")


def find_image_case_insensitive(filename: str, image_lookup: Dict[str, Path]) -> Optional[Path]:
    """
    Find image in lookup dictionary with case-insensitive matching.
    Also handles extension mismatches (e.g., .jpg vs .png).

    Args:
        filename: Image filename from document (e.g., "001-Butter-Chicken.jpg")
        image_lookup: Dictionary mapping lowercase filename -> Path

    Returns:
        Local file path if found, None otherwise
    """
    key = filename.lower()

    # Try exact match first
    if key in image_lookup:
        return image_lookup[key]

    # Try matching without extension (handles .jpg vs .png mismatches)
    name_without_ext = key.rsplit('.', 1)[0] if '.' in key else key

    for lookup_filename, path in image_lookup.items():
        lookup_name_without_ext = lookup_filename.rsplit('.', 1)[0] if '.' in lookup_filename else lookup_filename
        if name_without_ext == lookup_name_without_ext:
            return path

    return None


# Example usage
if __name__ == "__main__":
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )

    from google.oauth2.credentials import Credentials

    # Load credentials
    creds = Credentials.from_authorized_user_file('token.json')

    handler = GoogleDriveHandler(creds)

    # Extract folder ID from URL
    folder_url = "YOUR_GOOGLE_DRIVE_FOLDER_URL"
    folder_id = extract_folder_id(folder_url)

    # Download images
    cache_dir = Path("cache")
    image_lookup = handler.download_images_to_cache(
        folder_id=folder_id,
        cache_dir=cache_dir,
        restaurant_name="HWY TO INDIA"
    )

    print(f"Downloaded {len(image_lookup)} images")
    for filename, path in image_lookup.items():
        print(f"  {filename} -> {path}")

    # Example: Find image case-insensitively
    filename = "001-Butter-Chicken.JPG"
    found = find_image_case_insensitive(filename, image_lookup)
    print(f"\nLooking for: {filename}")
    print(f"Found: {found}")
