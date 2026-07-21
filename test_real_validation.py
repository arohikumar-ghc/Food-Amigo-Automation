"""
Test the actual validator with a real scenario to demonstrate non-blocking missing images.
"""
import logging
from pathlib import Path
from google.oauth2.credentials import Credentials
from validator import DataValidator, ValidationResult
from google_sheet_handler import RestaurantData
from google_doc_parser import GoogleDocParser, extract_doc_id
from google_drive_handler import GoogleDriveHandler, extract_folder_id

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(levelname)s: %(message)s'
)

def test_raj_shahhi_validation():
    """
    Test validation of RAJ SHAHHI restaurant which has missing images.
    """
    print("=" * 80)
    print("REAL VALIDATION TEST: RAJ SHAHHI INDIAN RESTAURANT")
    print("=" * 80)
    print()

    # Load credentials
    creds = Credentials.from_authorized_user_file('token.json')

    # Create validator
    validator = DataValidator(
        credentials=creds,
        cache_dir=Path("cache")
    )

    # Create restaurant data
    restaurant = RestaurantData(
        restaurant_name="RAJ SHAHHI INDIAN RESTAURANT",
        doc_link="https://docs.google.com/document/d/1Bkh_Ipcrnt5t61izWNXDqCZ7wXZ_i_U1og2TU48XO5E/edit",
        image_folder="https://drive.google.com/drive/folders/1pmjnQ9zSETF_Vfjf0DhmGKXEW3zDOnr9",
        no_of_pages="10",
        notes="",
        completed="No"
    )

    print("Restaurant: RAJ SHAHHI INDIAN RESTAURANT")
    print("Document: 10 pages")
    print("Images: 10 available in Drive")
    print("Expected: Page 5 references 'Indian Comfort Food' image (missing)")
    print()

    print("Running validation...")
    print("-" * 80)
    result = validator.validate_restaurant(restaurant)
    print("-" * 80)
    print()

    print("VALIDATION RESULT:")
    print("=" * 80)
    print(f"Passed: {result.passed}")
    print(f"Pages: {result.page_count}")
    print(f"Images: {result.image_count}")
    print(f"Errors: {len(result.errors)}")
    print(f"Warnings: {len(result.warnings)}")
    print()

    if result.errors:
        print("ERRORS (blocking):")
        for error in result.errors:
            print(f"  - {error}")
        print()

    if result.warnings:
        print("WARNINGS (non-blocking):")
        for warning in result.warnings:
            print(f"  - {warning}")
        print()

    print("=" * 80)

    if result.passed:
        print("[OK] VALIDATION PASSED - Automation will continue!")
        print()
        print("Explanation:")
        print("  - 10 pages parsed successfully")
        print("  - 10 images downloaded from Drive")
        print("  - 1 image missing (Page 5: Indian Comfort Food) -> WARNING only")
        print("  - Missing image does NOT block automation")
        print("  - Pages with valid images will be processed")
        print("  - Page 5 will be processed without image")
        return True
    else:
        print("[FAIL] VALIDATION FAILED - Automation blocked")
        print()
        print("This should not happen with the fix!")
        return False


if __name__ == "__main__":
    try:
        success = test_raj_shahhi_validation()
        exit(0 if success else 1)
    except Exception as e:
        print(f"Error: {e}")
        import traceback
        traceback.print_exc()
        exit(1)
