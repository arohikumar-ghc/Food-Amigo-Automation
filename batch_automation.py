"""
Batch automation orchestrator for processing multiple restaurants from Google Sheet.

Main workflow:
1. Read Google Sheet for pending restaurants
2. Validate all data (docs, images, structure)
3. Process each restaurant sequentially
4. Update sheet with completion status
"""
import logging
import sys
import io
from pathlib import Path
from typing import List, Dict
from datetime import datetime
from google.oauth2.credentials import Credentials
from google_sheet_handler import GoogleSheetHandler, RestaurantData, extract_spreadsheet_id
from google_doc_parser import GoogleDocParser, extract_doc_id
from google_drive_handler import GoogleDriveHandler, extract_folder_id, find_image_case_insensitive
from validator import DataValidator, ValidationResult
from automation import FoodAmigoAutomation
from config import AutomationConfig
from models import SEOPageData


# Setup logging
# Force UTF-8 encoding for console output to handle Unicode characters
import io
console_handler = logging.StreamHandler(
    io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', line_buffering=True)
)
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('logs/batch_automation.log', encoding='utf-8'),
        console_handler
    ]
)

logger = logging.getLogger("foodamigo_automation.batch")


class BatchAutomation:
    """
    Orchestrator for batch SEO page creation across multiple restaurants.
    """

    def __init__(
        self,
        spreadsheet_url: str,
        credentials_file: str = "credentials.json",
        token_file: str = "token.json",
        cache_dir: str = "cache"
    ):
        """
        Initialize batch automation.

        Args:
            spreadsheet_url: Full Google Sheets URL
            credentials_file: Path to OAuth2 credentials
            token_file: Path to token cache
            cache_dir: Directory for image cache
        """
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
        self.validator = None
        self.doc_parser = None
        self.drive_handler = None

        # Statistics
        self.stats = {
            "total_restaurants": 0,
            "validated": 0,
            "processed": 0,
            "completed": 0,
            "partial": 0,
            "failed": 0,
            "skipped": 0
        }

    def setup(self):
        """Setup Google API authentication and handlers."""
        logger.info("="*70)
        logger.info("BATCH AUTOMATION SETUP")
        logger.info("="*70)

        # Authenticate with Google
        logger.info("→ Authenticating with Google APIs...")
        self.sheet_handler = GoogleSheetHandler(self.credentials_file, self.token_file)
        self.sheet_handler.authenticate()

        # Load credentials for other services
        self.credentials = Credentials.from_authorized_user_file(self.token_file)

        # Set spreadsheet
        sheet_id = extract_spreadsheet_id(self.spreadsheet_url)
        self.sheet_handler.set_spreadsheet(sheet_id)

        # Initialize other handlers
        self.validator = DataValidator(self.credentials, self.cache_dir)
        self.doc_parser = GoogleDocParser(self.credentials)
        self.drive_handler = GoogleDriveHandler(self.credentials)

        logger.info("✓ Setup complete\n")

    def run(self, config: AutomationConfig, validate_only: bool = False):
        """
        Run batch automation workflow.

        Args:
            config: AutomationConfig with Food Amigo credentials
            validate_only: If True, only validate data without running automation

        Returns:
            Dictionary with statistics
        """
        logger.info("="*70)
        logger.info("BATCH AUTOMATION STARTED")
        logger.info("="*70)
        logger.info(f"Timestamp: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        logger.info(f"Mode: {'VALIDATE ONLY' if validate_only else 'FULL AUTOMATION'}")
        logger.info("="*70 + "\n")

        # Phase 1: Load restaurants from sheet
        logger.info("PHASE 1: LOADING RESTAURANTS FROM SHEET")
        logger.info("-"*70)

        pending_restaurants = self.sheet_handler.get_pending_restaurants()
        self.stats["total_restaurants"] = len(pending_restaurants)

        if not pending_restaurants:
            logger.warning("No pending restaurants found in sheet")
            return self.stats

        logger.info(f"✓ Found {len(pending_restaurants)} pending restaurants\n")

        # Phase 2: Validate all data
        logger.info("PHASE 2: VALIDATION")
        logger.info("-"*70)

        validation_results = self.validator.validate_all(pending_restaurants)

        # Filter to only passed restaurants
        validated_restaurants = [
            r for r in pending_restaurants
            if validation_results[r.restaurant_name].passed
        ]

        self.stats["validated"] = len(validated_restaurants)

        if not validated_restaurants:
            logger.error("✗ No restaurants passed validation. Aborting.")
            return self.stats

        logger.info(f"\n✓ {len(validated_restaurants)} restaurants passed validation")

        if validate_only:
            logger.info("\nValidation-only mode. Stopping here.")
            return self.stats

        # Phase 3: Process each restaurant
        logger.info("\n" + "="*70)
        logger.info("PHASE 3: AUTOMATION")
        logger.info("="*70 + "\n")

        for i, restaurant in enumerate(validated_restaurants, 1):
            logger.info(f"\n{'='*70}")
            logger.info(f"RESTAURANT [{i}/{len(validated_restaurants)}]: {restaurant.restaurant_name}")
            logger.info(f"{'='*70}")

            try:
                result = self._process_restaurant(restaurant, config, validation_results[restaurant.restaurant_name])

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
                        notes=f"Partial: {result['pages_created']}/{result['total_pages']} pages created. Errors: {result['errors']}"
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

                # Wait between restaurants (avoid overwhelming server)
                if i < len(validated_restaurants):
                    logger.info(f"\nWaiting 30 seconds before next restaurant...")
                    import time
                    time.sleep(30)

            except Exception as e:
                logger.error(f"✗ Critical error processing restaurant: {e}", exc_info=True)

                # Update sheet with error
                self.sheet_handler.update_completion_status(
                    restaurant=restaurant,
                    completed=False,
                    notes=f"Critical error: {str(e)[:200]}"
                )

                self.stats["failed"] += 1

        # Phase 4: Summary
        self._print_summary()

        return self.stats

    def _process_restaurant(
        self,
        restaurant: RestaurantData,
        config: AutomationConfig,
        validation_result: ValidationResult
    ) -> Dict:
        """
        Process a single restaurant (create all SEO pages).

        Args:
            restaurant: RestaurantData from sheet
            config: AutomationConfig
            validation_result: ValidationResult from validation phase

        Returns:
            Dictionary with status and statistics
        """
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
            # Load document (already validated, should succeed)
            doc_id = extract_doc_id(restaurant.doc_link)
            pages = self.doc_parser.parse_document(doc_id)
            result["total_pages"] = len(pages)

            logger.info(f"→ Processing {len(pages)} pages...")

            # Load image cache (already downloaded during validation)
            folder_id = extract_folder_id(restaurant.image_folder)
            image_lookup = self.drive_handler.download_images_to_cache(
                folder_id=folder_id,
                cache_dir=self.cache_dir,
                restaurant_name=restaurant.restaurant_name
            )

            logger.info(f"→ Image cache loaded: {len(image_lookup)} images")

            # Start automation
            # Override restaurant name in config
            config.restaurant_name = restaurant.restaurant_name

            with FoodAmigoAutomation(config) as automation:
                # Login and navigate
                automation.start_browser()
                automation.login()
                automation.select_restaurant()
                automation.open_storefront_editor()

                # Process each page
                for page_num, page_data in enumerate(pages, 1):
                    logger.info(f"\n[Page {page_num}/{len(pages)}] {page_data.page_name}")

                    try:
                        # Attach image path to page data
                        if hasattr(page_data, 'image_filename') and page_data.image_filename:
                            image_path = find_image_case_insensitive(page_data.image_filename, image_lookup)
                            if image_path:
                                page_data.image_local_path = str(image_path)
                                logger.debug(f"  Image: {page_data.image_filename} -> {image_path}")
                            else:
                                logger.warning(f"  Image not found: {page_data.image_filename}")

                        # Create page (with idempotency check)
                        page_status = automation.create_seo_page(page_data, page_num)

                        if page_status == "success":
                            result["pages_created"] += 1
                            logger.info(f"  ✓ Page created successfully")

                        elif page_status == "skipped":
                            result["pages_skipped"] += 1
                            logger.info(f"  ⊙ Page already exists, skipped")

                        elif page_status == "partial":
                            result["pages_created"] += 1
                            logger.warning(f"  ⚠ Page created with partial content")

                        else:  # failed
                            result["pages_failed"] += 1
                            result["errors"].append(f"Page {page_num} ({page_data.page_name})")
                            logger.error(f"  ✗ Page creation failed")

                        # Navigate back to dashboard for next page
                        if page_num < len(pages):
                            automation.navigate_to_dashboard()

                    except Exception as e:
                        result["pages_failed"] += 1
                        result["errors"].append(f"Page {page_num} ({page_data.page_name}): {str(e)[:100]}")
                        logger.error(f"  ✗ Error creating page: {e}")

                        # Try to recover for next page
                        try:
                            automation.navigate_to_dashboard()
                        except:
                            logger.error("  Could not recover to dashboard, stopping restaurant")
                            break

            # Determine final status
            if result["pages_failed"] == 0 and result["pages_created"] > 0:
                result["status"] = "completed"
            elif result["pages_created"] > 0:
                result["status"] = "partial"
            else:
                result["status"] = "failed"
                result["error"] = "No pages created successfully"

            logger.info(f"\n✓ Restaurant processing complete:")
            logger.info(f"  Created: {result['pages_created']}")
            logger.info(f"  Skipped: {result['pages_skipped']}")
            logger.info(f"  Failed: {result['pages_failed']}")

        except Exception as e:
            result["status"] = "failed"
            result["error"] = str(e)
            logger.error(f"✗ Restaurant processing failed: {e}")

        return result

    def _print_summary(self):
        """Print final summary statistics."""
        logger.info("\n" + "="*70)
        logger.info("BATCH AUTOMATION SUMMARY")
        logger.info("="*70)
        logger.info(f"Total Restaurants: {self.stats['total_restaurants']}")
        logger.info(f"Validated: {self.stats['validated']}")
        logger.info(f"Processed: {self.stats['processed']}")
        logger.info(f"")
        logger.info(f"✓ Completed: {self.stats['completed']}")
        logger.info(f"⚠ Partial: {self.stats['partial']}")
        logger.info(f"✗ Failed: {self.stats['failed']}")
        logger.info(f"⊙ Skipped (validation failed): {self.stats['total_restaurants'] - self.stats['validated']}")
        logger.info("="*70)
        logger.info(f"Finished: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        logger.info("="*70 + "\n")


# Main entry point
if __name__ == "__main__":
    import argparse
    import os
    from dotenv import load_dotenv

    # Load .env file
    load_dotenv()

    parser = argparse.ArgumentParser(description="Food Amigo Batch SEO Automation")
    parser.add_argument("--sheet-url", help="Google Sheet URL (or set GOOGLE_SHEET_URL in .env)")
    parser.add_argument("--validate-only", action="store_true", help="Only validate data, don't run automation")
    parser.add_argument("--credentials", default="credentials.json", help="Path to Google credentials JSON")
    parser.add_argument("--token", default="token.json", help="Path to token cache")

    args = parser.parse_args()

    # Get sheet URL from command line OR .env file
    sheet_url = args.sheet_url or os.getenv("GOOGLE_SHEET_URL")

    if not sheet_url:
        logger.error("No Google Sheet URL provided!")
        logger.error("Either:")
        logger.error("  1. Use: python batch_automation.py --sheet-url \"YOUR_SHEET_URL\"")
        logger.error("  2. Or add GOOGLE_SHEET_URL=... to your .env file")
        sys.exit(1)

    # Load Food Amigo config from .env
    try:
        config = AutomationConfig.from_env()
    except Exception as e:
        logger.error(f"Failed to load config: {e}")
        logger.error("Make sure .env file has FOODAMIGO_EMAIL and FOODAMIGO_PASSWORD")
        sys.exit(1)

    # Run batch automation
    batch = BatchAutomation(
        spreadsheet_url=sheet_url,
        credentials_file=args.credentials,
        token_file=args.token
    )

    batch.setup()
    stats = batch.run(config, validate_only=args.validate_only)

    # Exit with error code if any restaurants failed
    if stats["failed"] > 0:
        sys.exit(1)
