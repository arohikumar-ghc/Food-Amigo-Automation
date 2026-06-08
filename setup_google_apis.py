"""
Helper script to guide users through Google API setup.
"""
import sys
from pathlib import Path


def print_header(text):
    """Print formatted header."""
    print("\n" + "="*70)
    print(text)
    print("="*70 + "\n")


def print_step(number, text):
    """Print formatted step."""
    print(f"\n[STEP {number}] {text}")
    print("-"*70)


def check_file_exists(filename):
    """Check if file exists."""
    path = Path(filename)
    if path.exists():
        print(f"✓ Found: {filename}")
        return True
    else:
        print(f"✗ Missing: {filename}")
        return False


def main():
    """Run setup wizard."""
    print_header("FOOD AMIGO BATCH AUTOMATION - SETUP WIZARD")

    print("This script will guide you through the setup process.")
    print("Follow the steps below to get started.")

    # Step 1: Check Python dependencies
    print_step(1, "Checking Python Dependencies")

    try:
        import google.auth
        import googleapiclient
        import playwright
        print("✓ All Python packages installed")
    except ImportError as e:
        print(f"✗ Missing package: {e}")
        print("\nPlease run:")
        print("  pip install -r requirements.txt")
        print("  playwright install chromium")
        sys.exit(1)

    # Step 2: Check credentials.json
    print_step(2, "Checking Google API Credentials")

    if not check_file_exists("credentials.json"):
        print("\n❌ credentials.json not found!")
        print("\nTo get credentials.json:")
        print("1. Go to: https://console.cloud.google.com/")
        print("2. Create a new project (or select existing)")
        print("3. Enable these APIs:")
        print("   - Google Sheets API")
        print("   - Google Docs API")
        print("   - Google Drive API")
        print("4. Go to: APIs & Services > Credentials")
        print("5. Click: Create Credentials > OAuth client ID")
        print("6. Application type: Desktop app")
        print("7. Download JSON file")
        print("8. Save as 'credentials.json' in this folder")
        print("\nAfter creating credentials.json, run this script again.")
        sys.exit(1)

    # Step 3: Check token.json (authentication)
    print_step(3, "Checking Google Authentication Token")

    if not check_file_exists("token.json"):
        print("\n⚠ token.json not found (first-time setup)")
        print("\nYou need to authenticate with Google.")
        print("This will open your browser to grant permissions.")

        input("\nPress ENTER to start authentication...")

        try:
            from google_sheet_handler import GoogleSheetHandler

            print("\nStarting authentication...")
            handler = GoogleSheetHandler()
            handler.authenticate()

            print("\n✓ Authentication successful!")
            print("✓ token.json created for future use")

        except Exception as e:
            print(f"\n✗ Authentication failed: {e}")
            sys.exit(1)
    else:
        print("✓ Already authenticated (token.json exists)")

    # Step 4: Check .env file
    print_step(4, "Checking Food Amigo Credentials")

    if not check_file_exists(".env"):
        print("\n⚠ .env file not found")
        print("\nCreating .env template...")

        with open(".env", "w") as f:
            f.write("# Food Amigo Login Credentials\n")
            f.write("FOODAMIGO_EMAIL=your-email@example.com\n")
            f.write("FOODAMIGO_PASSWORD=your-password\n")
            f.write("FOODAMIGO_RESTAURANT=dummy-value\n")
            f.write("\n# Note: Restaurant name will come from Google Sheet\n")

        print("✓ Created .env template")
        print("\n⚠ Please edit .env and add your Food Amigo credentials:")
        print("   - FOODAMIGO_EMAIL")
        print("   - FOODAMIGO_PASSWORD")
        print("\nAfter editing .env, run this script again.")
        sys.exit(1)
    else:
        # Verify .env has required fields
        from dotenv import load_dotenv
        import os

        load_dotenv()

        email = os.getenv("FOODAMIGO_EMAIL")
        password = os.getenv("FOODAMIGO_PASSWORD")

        if not email or "example.com" in email:
            print("\n⚠ Please edit .env and add your real Food Amigo email")
            sys.exit(1)

        if not password or len(password) < 5:
            print("\n⚠ Please edit .env and add your real Food Amigo password")
            sys.exit(1)

        print("✓ Food Amigo credentials configured")

    # Step 5: Check directories
    print_step(5, "Checking Directories")

    Path("logs").mkdir(exist_ok=True)
    print("✓ Created logs/ directory")

    Path("cache").mkdir(exist_ok=True)
    print("✓ Created cache/ directory")

    # Step 6: Summary
    print_header("SETUP COMPLETE! ✓")

    print("All prerequisites are ready. You can now:")
    print("\n1. Create your Google Sheet with restaurant data")
    print("   - See BATCH_AUTOMATION_GUIDE.md for sheet structure")
    print("\n2. Create Google Docs with page content")
    print("   - Use GOOGLE_DOC_TEMPLATE.txt as template")
    print("\n3. Upload images to Google Drive folders")
    print("   - Follow naming convention: 001-item-name.jpg")
    print("\n4. Run validation to test your data:")
    print("   python batch_automation.py --sheet-url \"YOUR_SHEET_URL\" --validate-only")
    print("\n5. Run full automation:")
    print("   python batch_automation.py --sheet-url \"YOUR_SHEET_URL\"")
    print("\nFor detailed instructions, see: BATCH_AUTOMATION_GUIDE.md")
    print("\n" + "="*70 + "\n")


if __name__ == "__main__":
    main()
