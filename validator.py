"""
Pre-validation module for batch automation.

Validates all data sources before starting automation to catch errors early.
"""
import logging
from typing import List, Dict, Tuple
from pathlib import Path
from google.oauth2.credentials import Credentials
from googleapiclient.errors import HttpError
from google_sheet_handler import RestaurantData
from google_doc_parser import GoogleDocParser, extract_doc_id, ParseError
from google_drive_handler import GoogleDriveHandler, extract_folder_id, find_image_case_insensitive


logger = logging.getLogger("foodamigo_automation.validator")


class ValidationResult:
    """Result of validation for a single restaurant."""

    def __init__(self, restaurant_name: str):
        self.restaurant_name = restaurant_name
        self.passed = True
        self.errors = []
        self.warnings = []
        self.page_count = 0
        self.image_count = 0

    def add_error(self, message: str):
        """Add a validation error."""
        self.errors.append(message)
        self.passed = False

    def add_warning(self, message: str):
        """Add a validation warning."""
        self.warnings.append(message)

    def __repr__(self):
        status = "✓ PASS" if self.passed else "✗ FAIL"
        return f"ValidationResult({self.restaurant_name}: {status}, {len(self.errors)} errors, {len(self.warnings)} warnings)"


class DataValidator:
    """Validator for restaurant data before automation."""

    def __init__(self, credentials: Credentials, cache_dir: Path):
        """
        Initialize validator.

        Args:
            credentials: Google OAuth2 credentials
            cache_dir: Directory for image cache
        """
        self.credentials = credentials
        self.cache_dir = cache_dir
        self.doc_parser = GoogleDocParser(credentials)
        self.drive_handler = GoogleDriveHandler(credentials)

    def validate_restaurant(self, restaurant: RestaurantData) -> ValidationResult:
        """
        Validate all data for a single restaurant.

        Args:
            restaurant: RestaurantData from Google Sheet

        Returns:
            ValidationResult with pass/fail status and errors
        """
        logger.info(f"{'='*60}")
        logger.info(f"Validating: {restaurant.restaurant_name}")
        logger.info(f"{'='*60}")

        result = ValidationResult(restaurant.restaurant_name)

        # Step 1: Validate basic data
        if not restaurant.restaurant_name.strip():
            result.add_error("Restaurant name is empty")
            return result  # Can't continue without name

        if not restaurant.doc_link.strip():
            result.add_error("Google Doc link is missing")

        if not restaurant.image_folder.strip():
            result.add_error("Image folder link is missing")

        # Can't continue if links missing
        if not result.passed:
            return result

        # Step 2: Validate Google Doc
        doc_pages = None
        try:
            doc_id = extract_doc_id(restaurant.doc_link)
            logger.info(f"→ Parsing Google Doc: {doc_id}")

            doc_pages = self.doc_parser.parse_document(doc_id)
            result.page_count = len(doc_pages)

            logger.info(f"  ✓ Document parsed: {len(doc_pages)} pages found")

            # Validate expected page count (if provided)
            if restaurant.no_of_pages.strip():
                try:
                    expected_count = int(restaurant.no_of_pages)
                    if len(doc_pages) != expected_count:
                        result.add_warning(
                            f"Page count mismatch: Expected {expected_count}, found {len(doc_pages)}"
                        )
                except ValueError:
                    result.add_warning(f"Invalid 'No. of Pages' value: {restaurant.no_of_pages}")

        except ParseError as e:
            result.add_error(f"Document parsing failed: {e}")
        except ValueError as e:
            result.add_error(f"Invalid Doc URL: {e}")
        except Exception as e:
            result.add_error(f"Unexpected error accessing document: {e}")

        # Can't continue if doc parsing failed
        if not doc_pages:
            return result

        # Step 3: Validate Google Drive folder and download images
        image_lookup = None
        try:
            folder_id = extract_folder_id(restaurant.image_folder)
            logger.info(f"→ Downloading images from Drive folder: {folder_id}")

            image_lookup = self.drive_handler.download_images_to_cache(
                folder_id=folder_id,
                cache_dir=self.cache_dir,
                restaurant_name=restaurant.restaurant_name
            )

            result.image_count = len(image_lookup)
            logger.info(f"  ✓ Downloaded {len(image_lookup)} images")

            if not image_lookup:
                result.add_error("No images found in Drive folder")

        except ValueError as e:
            result.add_error(f"Invalid Drive folder URL: {e}")
        except HttpError as e:
            result.add_error(f"Drive API error: {e}")
        except Exception as e:
            result.add_error(f"Unexpected error accessing Drive folder: {e}")

        # Can't continue if image download failed
        if not image_lookup:
            return result

        # Step 4: Validate image references in document
        logger.info(f"→ Validating image references...")

        missing_images = []
        for i, page in enumerate(doc_pages, 1):
            if not hasattr(page, 'image_filename') or not page.image_filename:
                result.add_warning(f"Page {i} ({page.page_name}): No image filename specified")
                continue

            # Check if image exists in cache
            found = find_image_case_insensitive(page.image_filename, image_lookup)
            if not found:
                missing_images.append(f"Page {i} ({page.page_name}): {page.image_filename}")

        if missing_images:
            result.add_error(f"Missing {len(missing_images)} images referenced in document:")
            for missing in missing_images[:5]:  # Show first 5
                result.add_error(f"  - {missing}")
            if len(missing_images) > 5:
                result.add_error(f"  ... and {len(missing_images) - 5} more")

        # Step 5: Validate page structure
        logger.info(f"→ Validating page structure...")

        invalid_pages = []
        for i, page in enumerate(doc_pages, 1):
            validation_errors = page.validate()
            if validation_errors:
                invalid_pages.append(f"Page {i} ({page.page_name}): {', '.join(validation_errors)}")

        if invalid_pages:
            result.add_error(f"{len(invalid_pages)} pages have validation errors:")
            for invalid in invalid_pages[:3]:  # Show first 3
                result.add_error(f"  - {invalid}")
            if len(invalid_pages) > 3:
                result.add_error(f"  ... and {len(invalid_pages) - 3} more")

        # Final status
        if result.passed:
            logger.info(f"✓ VALIDATION PASSED")
            logger.info(f"  Pages: {result.page_count}")
            logger.info(f"  Images: {result.image_count}")
            if result.warnings:
                logger.warning(f"  Warnings: {len(result.warnings)}")
        else:
            logger.error(f"✗ VALIDATION FAILED")
            logger.error(f"  Errors: {len(result.errors)}")

        return result

    def validate_all(self, restaurants: List[RestaurantData]) -> Dict[str, ValidationResult]:
        """
        Validate all restaurants.

        Args:
            restaurants: List of RestaurantData from sheet

        Returns:
            Dictionary mapping restaurant name -> ValidationResult
        """
        logger.info(f"\n{'='*60}")
        logger.info(f"VALIDATION PHASE: {len(restaurants)} restaurants")
        logger.info(f"{'='*60}\n")

        results = {}

        for i, restaurant in enumerate(restaurants, 1):
            logger.info(f"\n[{i}/{len(restaurants)}] Validating {restaurant.restaurant_name}...")

            result = self.validate_restaurant(restaurant)
            results[restaurant.restaurant_name] = result

        # Summary
        logger.info(f"\n{'='*60}")
        logger.info(f"VALIDATION SUMMARY")
        logger.info(f"{'='*60}")

        passed = [r for r in results.values() if r.passed]
        failed = [r for r in results.values() if not r.passed]

        logger.info(f"Total: {len(results)}")
        logger.info(f"✓ Passed: {len(passed)}")
        logger.info(f"✗ Failed: {len(failed)}")

        if failed:
            logger.warning(f"\nFailed restaurants:")
            for result in failed:
                logger.warning(f"  - {result.restaurant_name}: {len(result.errors)} errors")

        return results


# Example usage
if __name__ == "__main__":
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(message)s'
    )

    from google.oauth2.credentials import Credentials
    from google_sheet_handler import GoogleSheetHandler, extract_spreadsheet_id

    # Load credentials
    creds = Credentials.from_authorized_user_file('token.json')

    # Setup sheet handler
    sheet_handler = GoogleSheetHandler()
    sheet_handler.authenticate()

    sheet_url = "YOUR_GOOGLE_SHEET_URL"
    sheet_id = extract_spreadsheet_id(sheet_url)
    sheet_handler.set_spreadsheet(sheet_id)

    # Get pending restaurants
    pending = sheet_handler.get_pending_restaurants()

    # Validate all
    validator = DataValidator(
        credentials=creds,
        cache_dir=Path("cache")
    )

    results = validator.validate_all(pending)

    # Print detailed results
    print("\n" + "="*60)
    print("DETAILED RESULTS")
    print("="*60)

    for name, result in results.items():
        print(f"\n{name}:")
        print(f"  Status: {'✓ PASS' if result.passed else '✗ FAIL'}")
        print(f"  Pages: {result.page_count}")
        print(f"  Images: {result.image_count}")

        if result.errors:
            print(f"  Errors:")
            for error in result.errors:
                print(f"    - {error}")

        if result.warnings:
            print(f"  Warnings:")
            for warning in result.warnings:
                print(f"    - {warning}")
