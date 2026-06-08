"""
Diagnostic script to check Google Sheet data and identify issues.
"""
import os
import sys
from dotenv import load_dotenv
from google_sheet_handler import GoogleSheetHandler, extract_spreadsheet_id
from google_doc_parser import extract_doc_id
from google_drive_handler import extract_folder_id

def main():
    load_dotenv()

    sheet_url = os.getenv('GOOGLE_SHEET_URL')
    if not sheet_url:
        print("ERROR: GOOGLE_SHEET_URL not found in .env file")
        return 1

    print(f"Google Sheet URL: {sheet_url}")
    print(f"Sheet ID: {extract_spreadsheet_id(sheet_url)}")
    print("\n" + "="*70)

    # Initialize handler
    handler = GoogleSheetHandler(
        credentials_file='credentials.json',
        token_file='token.json'
    )

    try:
        handler.authenticate()
        handler.set_spreadsheet(extract_spreadsheet_id(sheet_url))

        # Read restaurants
        print("\nReading restaurants from Sheet1...\n")
        restaurants = handler.read_restaurants('Sheet1')

        print(f"Total restaurants found: {len(restaurants)}\n")
        print("="*70)

        for idx, r in enumerate(restaurants, 1):
            print(f"\n[{idx}] {r.restaurant_name}")
            print("-"*70)
            print(f"  Doc Link:       {r.doc_link}")
            print(f"  Doc ID:         {extract_doc_id(r.doc_link) if r.doc_link else 'N/A'}")
            print(f"  Image Folder:   {r.image_folder}")
            print(f"  Folder ID:      {extract_folder_id(r.image_folder) if r.image_folder else 'N/A'}")
            print(f"  No. of Pages:   {r.no_of_pages}")
            print(f"  Completed:      {r.completed}")
            print(f"  Last Run:       {r.last_run if r.last_run else '(never)'}")
            print(f"  Is Pending:     {r.is_pending()}")
            print(f"  Notes:          {r.notes if r.notes else '(none)'}")

            # Validation checks
            issues = []
            if not r.doc_link or r.doc_link.strip() == "":
                issues.append("⚠ Doc Link is empty")
            if not r.image_folder or r.image_folder.strip() == "":
                issues.append("⚠ Image Folder is empty")

            if issues:
                print(f"\n  Issues:")
                for issue in issues:
                    print(f"    {issue}")

        print("\n" + "="*70)
        print("\nDiagnostic complete!")

        # Summary
        pending = [r for r in restaurants if r.is_pending()]
        print(f"\nSummary:")
        print(f"  Total:   {len(restaurants)}")
        print(f"  Pending: {len(pending)}")
        print(f"  Done:    {len(restaurants) - len(pending)}")

        if pending:
            print(f"\nPending restaurants:")
            for r in pending:
                print(f"  - {r.restaurant_name}")

    except Exception as e:
        print(f"\nERROR: {e}")
        import traceback
        traceback.print_exc()
        return 1

    return 0

if __name__ == "__main__":
    sys.exit(main())
