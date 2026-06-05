"""
Regenerate token.json with all required scopes for batch automation.

This script will:
1. Delete the existing token.json (if it exists)
2. Re-authenticate with all required scopes
3. Create a new token.json with full permissions

Required scopes:
- spreadsheets: Read restaurant list from Google Sheets
- documents.readonly: Read page content from Google Docs
- drive.readonly: Download images from Google Drive
"""
import sys
import io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', line_buffering=True)
sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8', line_buffering=True)

from pathlib import Path
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow

# All scopes needed for batch automation
SCOPES = [
    'https://www.googleapis.com/auth/spreadsheets',          # Read Google Sheets
    'https://www.googleapis.com/auth/documents.readonly',    # Read Google Docs
    'https://www.googleapis.com/auth/drive.readonly',        # Download from Google Drive
]

def main():
    print("="*70)
    print("REGENERATE AUTHENTICATION TOKEN")
    print("="*70)
    print()

    token_path = Path("token.json")

    # Check if token exists
    if token_path.exists():
        print("⚠ Found existing token.json")
        print("  This token will be replaced with a new one that has all required scopes.")
        print()
        response = input("  Continue? [y/N]: ").strip().lower()
        if response != 'y':
            print("\nAborted.")
            return 1

        # Backup old token
        backup_path = Path("token.json.bak")
        token_path.rename(backup_path)
        print(f"✓ Backed up old token to {backup_path}")
        print()

    # Check credentials file
    creds_path = Path("credentials.json")
    if not creds_path.exists():
        print("✗ ERROR: credentials.json not found")
        print()
        print("Please ensure credentials.json is in the current directory.")
        print("This should be the OAuth2 client credentials from Google Cloud Console.")
        return 1

    print("Required scopes:")
    for scope in SCOPES:
        print(f"  • {scope}")
    print()

    print("Starting OAuth2 authentication flow...")
    print("Your browser will open to authenticate with Google.")
    print()

    try:
        # Run OAuth2 flow
        flow = InstalledAppFlow.from_client_secrets_file('credentials.json', SCOPES)
        creds = flow.run_local_server(port=0)

        # Save credentials
        with open('token.json', 'w') as token:
            token.write(creds.to_json())

        print()
        print("="*70)
        print("✓ SUCCESS! Token regenerated successfully")
        print("="*70)
        print()
        print("The new token.json has been created with all required scopes:")
        for scope in SCOPES:
            print(f"  ✓ {scope}")
        print()
        print("You can now run batch automation:")
        print("  python batch_automation.py --validate-only")
        print()

        return 0

    except Exception as e:
        print()
        print("="*70)
        print("✗ FAILED to regenerate token")
        print("="*70)
        print(f"\nError: {e}")
        print()
        print("Troubleshooting:")
        print("  1. Check that credentials.json is valid")
        print("  2. Ensure you have internet connection")
        print("  3. Try again and complete the browser authentication")
        return 1

if __name__ == "__main__":
    sys.exit(main())
