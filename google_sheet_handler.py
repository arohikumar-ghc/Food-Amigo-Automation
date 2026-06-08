"""
Google Sheets integration for batch automation control panel.
"""
import logging
from typing import List, Dict, Optional
from pathlib import Path
from google.oauth2.credentials import Credentials
from google.auth.transport.requests import Request
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError


logger = logging.getLogger("foodamigo_automation.google_sheet")

# Google Sheets API scopes
SCOPES = ['https://www.googleapis.com/auth/spreadsheets']


class RestaurantData:
    """Data structure for restaurant from Google Sheet."""

    def __init__(self, row_index: int, row_data: List[str]):
        """
        Initialize restaurant data from sheet row.

        Args:
            row_index: Row number in sheet (for updates)
            row_data: List of cell values from row
        """
        self.row_index = row_index

        # Parse columns (handle missing columns gracefully)
        self.restaurant_name = row_data[0] if len(row_data) > 0 else ""
        self.doc_link = row_data[1] if len(row_data) > 1 else ""
        self.image_folder = row_data[2] if len(row_data) > 2 else ""
        self.no_of_pages = row_data[3] if len(row_data) > 3 else ""
        self.completed = row_data[4] if len(row_data) > 4 else ""
        self.last_run = row_data[5] if len(row_data) > 5 else ""
        self.notes = row_data[6] if len(row_data) > 6 else ""

    def is_pending(self) -> bool:
        """Check if restaurant is pending processing."""
        return self.completed.lower() not in ["yes", "y", "completed"]

    def __repr__(self):
        return f"RestaurantData(name={self.restaurant_name}, pending={self.is_pending()})"


class GoogleSheetHandler:
    """Handler for Google Sheets API operations."""

    def __init__(self, credentials_file: str = "credentials.json", token_file: str = "token.json"):
        """
        Initialize Google Sheets handler.

        Args:
            credentials_file: Path to OAuth2 credentials JSON
            token_file: Path to store access token
        """
        self.credentials_file = credentials_file
        self.token_file = token_file
        self.service = None
        self.spreadsheet_id = None

    def authenticate(self):
        """
        Authenticate with Google Sheets API.

        Creates token.json on first run (requires browser auth).
        Subsequent runs reuse token.json.
        """
        logger.info("Authenticating with Google Sheets API...")

        creds = None
        token_path = Path(self.token_file)

        # Load existing token if available
        if token_path.exists():
            logger.debug("Loading existing token...")
            creds = Credentials.from_authorized_user_file(self.token_file, SCOPES)

        # If no valid credentials, authenticate
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                logger.debug("Refreshing expired token...")
                creds.refresh(Request())
            else:
                logger.info("Starting OAuth2 flow (browser will open)...")
                flow = InstalledAppFlow.from_client_secrets_file(
                    self.credentials_file, SCOPES)
                creds = flow.run_local_server(port=0)

            # Save credentials for next run
            with open(self.token_file, 'w') as token:
                token.write(creds.to_json())
            logger.debug("Token saved for future use")

        self.service = build('sheets', 'v4', credentials=creds)
        logger.info("✓ Google Sheets authentication successful")

    def set_spreadsheet(self, spreadsheet_id: str):
        """
        Set the spreadsheet ID to work with.

        Args:
            spreadsheet_id: Google Sheet ID (from URL)
        """
        self.spreadsheet_id = spreadsheet_id
        logger.info(f"Working with spreadsheet: {spreadsheet_id}")

    def read_restaurants(self, sheet_name: str = "Sheet1", header_row: int = 1) -> List[RestaurantData]:
        """
        Read all restaurants from the sheet.

        Args:
            sheet_name: Name of the sheet tab
            header_row: Row number where headers are (1-indexed)

        Returns:
            List of RestaurantData objects

        Raises:
            Exception: If sheet read fails
        """
        if not self.service:
            raise Exception("Not authenticated. Call authenticate() first.")

        if not self.spreadsheet_id:
            raise Exception("No spreadsheet set. Call set_spreadsheet() first.")

        logger.info(f"Reading restaurants from sheet '{sheet_name}'...")

        try:
            # Read all data from sheet (skip header row)
            range_name = f"{sheet_name}!A{header_row + 1}:G"
            result = self.service.spreadsheets().values().get(
                spreadsheetId=self.spreadsheet_id,
                range=range_name
            ).execute()

            rows = result.get('values', [])

            if not rows:
                logger.warning("No data found in sheet")
                return []

            # Parse rows into RestaurantData objects
            restaurants = []
            for i, row in enumerate(rows, start=header_row + 1):
                # Skip empty rows
                if not row or not row[0].strip():
                    continue

                restaurant = RestaurantData(row_index=i, row_data=row)
                restaurants.append(restaurant)

            logger.info(f"✓ Found {len(restaurants)} restaurants in sheet")
            return restaurants

        except HttpError as e:
            logger.error(f"Failed to read sheet: {e}")
            raise Exception(f"Google Sheets API error: {e}")

    def get_pending_restaurants(self, sheet_name: str = "Sheet1") -> List[RestaurantData]:
        """
        Get only pending restaurants (Completed != Yes).

        Args:
            sheet_name: Name of the sheet tab

        Returns:
            List of pending RestaurantData objects
        """
        all_restaurants = self.read_restaurants(sheet_name)
        pending = [r for r in all_restaurants if r.is_pending()]

        logger.info(f"✓ Found {len(pending)} pending restaurants (out of {len(all_restaurants)} total)")
        return pending

    def update_completion_status(
        self,
        restaurant: RestaurantData,
        completed: bool,
        notes: str = "",
        sheet_name: str = "Sheet1"
    ):
        """
        Update completion status for a restaurant.

        Args:
            restaurant: RestaurantData object with row_index
            completed: True if completed successfully
            notes: Optional notes/error message
            sheet_name: Name of the sheet tab
        """
        if not self.service or not self.spreadsheet_id:
            raise Exception("Not authenticated or no spreadsheet set")

        logger.info(f"Updating status for {restaurant.restaurant_name}...")

        # Prepare values
        completed_value = "Yes" if completed else "No"
        timestamp = self._get_current_timestamp()

        # Update columns E (Completed), F (Last Run), G (Notes)
        range_name = f"{sheet_name}!E{restaurant.row_index}:G{restaurant.row_index}"
        values = [[completed_value, timestamp, notes]]

        body = {'values': values}

        try:
            self.service.spreadsheets().values().update(
                spreadsheetId=self.spreadsheet_id,
                range=range_name,
                valueInputOption='RAW',
                body=body
            ).execute()

            logger.info(f"✓ Status updated: Completed={completed_value}, Notes={notes}")

        except HttpError as e:
            logger.error(f"Failed to update status: {e}")
            raise Exception(f"Google Sheets API error: {e}")

    def _get_current_timestamp(self) -> str:
        """Get current timestamp in readable format."""
        from datetime import datetime
        return datetime.now().strftime("%Y-%m-%d %H:%M:%S")


def extract_spreadsheet_id(sheet_url: str) -> str:
    """
    Extract spreadsheet ID from Google Sheets URL.

    Args:
        sheet_url: Full Google Sheets URL

    Returns:
        Spreadsheet ID

    Example:
        URL: https://docs.google.com/spreadsheets/d/1ABC123.../edit
        Returns: 1ABC123...
    """
    import re
    match = re.search(r'/spreadsheets/d/([a-zA-Z0-9-_]+)', sheet_url)
    if match:
        return match.group(1)
    raise ValueError(f"Could not extract spreadsheet ID from URL: {sheet_url}")


# Example usage
if __name__ == "__main__":
    # Setup logging
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )

    # Example: Read restaurants from sheet
    handler = GoogleSheetHandler()
    handler.authenticate()

    # Set your spreadsheet ID (extract from URL)
    sheet_url = "YOUR_GOOGLE_SHEET_URL"
    sheet_id = extract_spreadsheet_id(sheet_url)
    handler.set_spreadsheet(sheet_id)

    # Get pending restaurants
    pending = handler.get_pending_restaurants()

    for restaurant in pending:
        print(f"Restaurant: {restaurant.restaurant_name}")
        print(f"  Doc Link: {restaurant.doc_link}")
        print(f"  Image Folder: {restaurant.image_folder}")
        print(f"  Pages: {restaurant.no_of_pages}")
        print()
