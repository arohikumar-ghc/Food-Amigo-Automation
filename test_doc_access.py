"""
Test if we can access the Google Doc with current credentials.
"""
import sys
import io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', line_buffering=True)
sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8', line_buffering=True)

from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from google.auth.transport.requests import Request
from google_auth_oauthlib.flow import InstalledAppFlow

SCOPES = ['https://www.googleapis.com/auth/documents.readonly']

def test_doc_access(doc_id: str):
    """Test if we can access a Google Doc."""

    print(f"Testing access to Google Doc: {doc_id}")
    print("="*70)

    # Load credentials
    creds = None
    try:
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)
    except Exception as e:
        print(f"Warning: Could not load token.json: {e}")

    # Refresh if needed
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            print("Refreshing expired credentials...")
            creds.refresh(Request())
        else:
            print("Need to authenticate...")
            flow = InstalledAppFlow.from_client_secrets_file('credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)

        # Save credentials
        with open('token.json', 'w') as token:
            token.write(creds.to_json())

    # Build service
    service = build('docs', 'v1', credentials=creds)

    # Try to access the document
    try:
        print("\nAttempting to fetch document...")
        document = service.documents().get(documentId=doc_id).execute()

        print("✓ SUCCESS! Document is accessible.")
        print(f"\nDocument Title: {document.get('title', 'N/A')}")
        print(f"Document ID: {document.get('documentId', 'N/A')}")
        print(f"Revision ID: {document.get('revisionId', 'N/A')}")

        # Check content
        content = document.get('body', {}).get('content', [])
        print(f"\nDocument has {len(content)} content elements")

        return True

    except Exception as e:
        print(f"✗ FAILED to access document")
        print(f"\nError: {e}")
        print("\nPossible causes:")
        print("  1. Document doesn't exist (HTTP 404)")
        print("  2. You don't have permission to access it")
        print("  3. Document was deleted")
        print("  4. Document ID is incorrect")
        print("\nTo fix:")
        print("  1. Verify the document exists by opening it in your browser:")
        print(f"     https://docs.google.com/document/d/{doc_id}/edit")
        print("  2. Make sure you're logged in with the same Google account")
        print("  3. Check that the document is shared with you or you own it")

        return False

if __name__ == "__main__":
    # Test the document from your sheet
    doc_id = "1G4JqWbPXmYrhfyWj6QEGZEvQELnpyS1hU5CNdU5kkPc"

    print("Google Doc Access Test")
    print("="*70)
    print()

    success = test_doc_access(doc_id)

    print("\n" + "="*70)
    if success:
        print("✓ Test PASSED - You can proceed with batch automation")
    else:
        print("✗ Test FAILED - Fix the issues above before running batch automation")

    sys.exit(0 if success else 1)
