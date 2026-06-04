"""
Script to download latest version from Google Docs.
Run this before automation to get fresh content.
"""
import os
import time
from pathlib import Path

print("=" * 80)
print("GOOGLE DOC SYNC HELPER")
print("=" * 80)

# Instructions
print("""
MANUAL STEPS (Until you set up Google Drive app):

1. Open your Google Doc in browser
2. File → Download → Microsoft Word (.docx)
3. Save to: C:\\Users\\Arohi\\Downloads\\
4. File will be: Untitled document.docx

Press Enter when download is complete...
""")

input()

# Check if file exists in Downloads
downloads_path = Path("C:/Users/Arohi/Downloads/Untitled document.docx")
project_path = Path("seo_files/Untitled document.docx")

if downloads_path.exists():
    print("✓ Found downloaded file")

    # Get file modification time
    mod_time = os.path.getmtime(downloads_path)
    time_str = time.ctime(mod_time)

    print(f"  Last modified: {time_str}")
    print(f"  Moving to project...")

    # Copy to project folder
    import shutil
    shutil.copy2(downloads_path, project_path)

    print(f"✓ Updated: {project_path}")
    print("\nNow run: python main.py \"seo_files/Untitled document.docx\"")

else:
    print("✗ File not found in Downloads folder")
    print("  Please download manually and try again")

print("\n" + "=" * 80)
