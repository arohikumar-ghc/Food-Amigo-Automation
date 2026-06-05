"""
Batch automation using Excel files (alternative to Google Docs approach).

This is a hybrid approach:
- Google Sheet for restaurant list
- Excel files (.xlsx) for page content (instead of Google Docs)
- Google Drive for images (same as before)

Use this if you prefer to keep using Excel files instead of Google Docs.
"""
import logging
import sys
from pathlib import Path
from typing import List, Dict
from datetime import datetime
from google.oauth2.credentials import Credentials
from google_sheet_handler import GoogleSheetHandler, RestaurantData, extract_spreadsheet_id
from google_drive_handler import GoogleDriveHandler, extract_folder_id, find_image_case_insensitive
from automation import FoodAmigoAutomation
from config import AutomationConfig
from parser import parse_seo_document_all  # Use your existing Excel parser


# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('logs/batch_automation_excel.log'),
        logging.StreamHandler(sys.stdout)
    ]
)

logger = logging.getLogger("foodamigo_automation.batch_excel")


class BatchAutomationExcel:
    """
    Batch automation using Excel files for content.

    Google Sheet columns:
    | Restaurant Name | Excel File Path | Image Folder | No. of Pages | Completed | Last Run | Notes |
    """

    def __init__(
        self,
        spreadsheet_url: str,
        credentials_file: str = "credentials.json",
        token_file: str = "token.json",
        cache_dir: str = "cache"
    ):
        self.spreadsheet_url = spreadsheet_url
        self.credentials_file = credentials_file
        self.token_file = token_file
        self.cache_dir = Path(cache_dir)

        # Create directories
        self.cache_dir.mkdir(exist_ok=True)
        Path("logs").mkdir(exist_ok=True)

        # Initialize handlers
        self.sheet_handler = None
        self.credentials = None
        self.drive_handler = None

        # Statistics
        self.stats = {
            "total_restaurants": 0,
            "processed": 0,
            "completed": 0,
            "partial": 0,
            "failed": 0
        }

    def setup(self):
        """Setup Google API authentication."""
        logger.info("="*70)
        logger.info("BATCH AUTOMATION SETUP (Excel Mode)")
        logger.info("="*70)

        # Authenticate with Google
        logger.info("→ Authenticating with Google APIs...")
        self.sheet_handler = GoogleSheetHandler(self.credentials_file, self.token_file)
        self.sheet_handler.authenticate()

        # Load credentials for Drive
        self.credentials = Credentials.from_authorized_user_file(self.token_file)

        # Set spreadsheet
        sheet_id = extract_spreadsheet_id(self.spreadsheet_url)
        self.sheet_handler.set_spreadsheet(sheet_id)

        # Initialize Drive handler
        self.drive_handler = GoogleDriveHandler(self.credentials)

        logger.info("✓ Setup complete\n")

    def run(self, config: AutomationConfig):
        """
        Run batch automation.

        Args:
            config: AutomationConfig with Food Amigo credentials
        """
        logger.info("="*70)
        logger.info("BATCH AUTOMATION STARTED (Excel Mode)")
        logger.info("="*70)

        # Load restaurants from sheet
        logger.info("PHASE 1: LOADING RESTAURANTS FROM SHEET")
        logger.info("-"*70)

        pending_restaurants = self.sheet_handler.get_pending_restaurants()
        self.stats["total_restaurants"] = len(pending_restaurants)

        if not pending_restaurants:
            logger.warning("No pending restaurants found in sheet")
            return self.stats

        logger.info(f"✓ Found {len(pending_restaurants)} pending restaurants\n")

        # Process each restaurant
        logger.info("PHASE 2: PROCESSING RESTAURANTS")
        logger.info("-"*70)

        for i, restaurant in enumerate(pending_restaurants, 1):
            logger.info(f"\n{'='*70}")
            logger.info(f"RESTAURANT [{i}/{len(pending_restaurants)}]: {restaurant.restaurant_name}")
            logger.info(f"{'='*70}")

            try:
                result = self._process_restaurant(restaurant, config)

                # Update sheet based on result
                if result["status"] == "completed":
                    self.sheet_handler.update_completion_status(
                        restaurant=restaurant,
                        completed=True,
                        notes=f"Completed: {result['pages_created']} pages created"
                    )
                    self.stats["completed"] += 1

                elif result["status"] == "partial":
                    self.sheet_handler.update_completion_status(
                        restaurant=restaurant,
                        completed=False,
                        notes=f"Partial: {result['pages_created']}/{result['total_pages']} pages. Errors: {result['errors']}"
                    )
                    self.stats["partial"] += 1

                else:  # failed
                    self.sheet_handler.update_completion_status(
                        restaurant=restaurant,
                        completed=False,
                        notes=f"Failed: {result['error']}"
                    )
                    self.stats["failed"] += 1

                self.stats["processed"] += 1

                # Wait between restaurants
                if i < len(pending_restaurants):
                    logger.info(f"\nWaiting 30 seconds before next restaurant...")
                    import time
                    time.sleep(30)

            except Exception as e:
                logger.error(f"✗ Critical error: {e}", exc_info=True)
                self.sheet_handler.update_completion_status(
                    restaurant=restaurant,
                    completed=False,
                    notes=f"Critical error: {str(e)[:200]}"
                )
                self.stats["failed"] += 1

        # Summary
        self._print_summary()
        return self.stats

    def _process_restaurant(self, restaurant: RestaurantData, config: AutomationConfig) -> Dict:
        """Process a single restaurant."""
        result = {
            "status": "failed",
            "total_pages": 0,
            "pages_created": 0,
            "pages_skipped": 0,
            "pages_failed": 0,
            "error": None,
            "errors": []
        }

        try:
            # Excel file path is in doc_link column
            excel_path = Path(restaurant.doc_link)

            if not excel_path.exists():
                raise Exception(f"Excel file not found: {excel_path}")

            logger.info(f"→ Parsing Excel file: {excel_path}")

            # Parse Excel file using existing parser
            pages = parse_seo_document_all(excel_path)  # Your existing parser
            result["total_pages"] = len(pages)

            logger.info(f"  ✓ Parsed {len(pages)} pages")

            # Download images if folder provided
            image_lookup = {}
            if restaurant.image_folder.strip():
                folder_id = extract_folder_id(restaurant.image_folder)
                logger.info(f"→ Downloading images from Drive...")

                image_lookup = self.drive_handler.download_images_to_cache(
                    folder_id=folder_id,
                    cache_dir=self.cache_dir,
                    restaurant_name=restaurant.restaurant_name
                )
                logger.info(f"  ✓ Downloaded {len(image_lookup)} images")

            # Start automation
            config.restaurant_name = restaurant.restaurant_name

            with FoodAmigoAutomation(config) as automation:
                automation.start_browser()
                automation.login()
                automation.select_restaurant()
                automation.open_storefront_editor()

                # Process each page
                for page_num, page_data in enumerate(pages, 1):
                    logger.info(f"\n[Page {page_num}/{len(pages)}] {page_data.page_name}")

                    try:
                        # Attach image path if available
                        if hasattr(page_data, 'image_filename') and page_data.image_filename:
                            image_path = find_image_case_insensitive(page_data.image_filename, image_lookup)
                            if image_path:
                                page_data.image_local_path = str(image_path)

                        # Create page
                        page_status = automation.create_seo_page(page_data, page_num)

                        if page_status == "success":
                            result["pages_created"] += 1
                        elif page_status == "skipped":
                            result["pages_skipped"] += 1
                        else:
                            result["pages_failed"] += 1
                            result["errors"].append(f"Page {page_num}")

                        # Navigate to dashboard for next page
                        if page_num < len(pages):
                            automation.navigate_to_dashboard()

                    except Exception as e:
                        result["pages_failed"] += 1
                        result["errors"].append(f"Page {page_num}: {str(e)[:100]}")
                        logger.error(f"  ✗ Error: {e}")

            # Determine status
            if result["pages_failed"] == 0 and result["pages_created"] > 0:
                result["status"] = "completed"
            elif result["pages_created"] > 0:
                result["status"] = "partial"
            else:
                result["status"] = "failed"
                result["error"] = "No pages created"

            logger.info(f"\n✓ Restaurant complete: Created={result['pages_created']}, Skipped={result['pages_skipped']}, Failed={result['pages_failed']}")

        except Exception as e:
            result["status"] = "failed"
            result["error"] = str(e)
            logger.error(f"✗ Failed: {e}")

        return result

    def _print_summary(self):
        """Print summary statistics."""
        logger.info("\n" + "="*70)
        logger.info("BATCH AUTOMATION SUMMARY")
        logger.info("="*70)
        logger.info(f"Total: {self.stats['total_restaurants']}")
        logger.info(f"Processed: {self.stats['processed']}")
        logger.info(f"✓ Completed: {self.stats['completed']}")
        logger.info(f"⚠ Partial: {self.stats['partial']}")
        logger.info(f"✗ Failed: {self.stats['failed']}")
        logger.info("="*70)


# Main entry point
if __name__ == "__main__":
    import argparse
    import os
    from dotenv import load_dotenv

    # Load .env file
    load_dotenv()

    parser = argparse.ArgumentParser(description="Food Amigo Batch Automation (Excel Mode)")
    parser.add_argument("--sheet-url", help="Google Sheet URL (or set GOOGLE_SHEET_URL in .env)")
    parser.add_argument("--credentials", default="credentials.json", help="Google credentials")
    parser.add_argument("--token", default="token.json", help="Token cache")

    args = parser.parse_args()

    # Get sheet URL from command line OR .env file
    sheet_url = args.sheet_url or os.getenv("GOOGLE_SHEET_URL")

    if not sheet_url:
        logger.error("No Google Sheet URL provided!")
        logger.error("Either:")
        logger.error("  1. Use: python batch_automation_excel.py --sheet-url \"YOUR_SHEET_URL\"")
        logger.error("  2. Or add GOOGLE_SHEET_URL=... to your .env file")
        sys.exit(1)

    # Load config
    try:
        config = AutomationConfig.from_env()
    except Exception as e:
        logger.error(f"Failed to load config: {e}")
        sys.exit(1)

    # Run batch automation
    batch = BatchAutomationExcel(
        spreadsheet_url=sheet_url,
        credentials_file=args.credentials,
        token_file=args.token
    )

    batch.setup()
    stats = batch.run(config)

    if stats["failed"] > 0:
        sys.exit(1)
