"""
Automated setup script for image upload feature.
Backs up existing files and applies updates automatically.
"""
import os
import shutil
from pathlib import Path

# ANSI color codes for pretty output
GREEN = '\033[92m'
YELLOW = '\033[93m'
BLUE = '\033[94m'
RED = '\033[91m'
RESET = '\033[0m'

def print_header(text):
    """Print a formatted header."""
    print(f"\n{BLUE}{'=' * 80}{RESET}")
    print(f"{BLUE}{text.center(80)}{RESET}")
    print(f"{BLUE}{'=' * 80}{RESET}\n")

def print_success(text):
    """Print success message."""
    print(f"{GREEN}✓ {text}{RESET}")

def print_warning(text):
    """Print warning message."""
    print(f"{YELLOW}⚠ {text}{RESET}")

def print_error(text):
    """Print error message."""
    print(f"{RED}✗ {text}{RESET}")

def print_info(text):
    """Print info message."""
    print(f"{BLUE}→ {text}{RESET}")

def backup_file(file_path):
    """
    Backup a file by renaming it with _backup suffix.

    Args:
        file_path: Path to file to backup

    Returns:
        True if successful, False otherwise
    """
    backup_path = file_path.replace('.py', '_backup.py')

    if os.path.exists(file_path):
        try:
            # If backup already exists, remove it first
            if os.path.exists(backup_path):
                os.remove(backup_path)
                print_info(f"Removed old backup: {backup_path}")

            # Rename current file to backup
            os.rename(file_path, backup_path)
            print_success(f"Backed up: {file_path} → {backup_path}")
            return True
        except Exception as e:
            print_error(f"Failed to backup {file_path}: {e}")
            return False
    else:
        print_warning(f"File not found (will create new): {file_path}")
        return True

def create_images_folder():
    """Create images directory if it doesn't exist."""
    images_dir = Path("images")
    if not images_dir.exists():
        images_dir.mkdir()
        print_success(f"Created images directory: {images_dir.absolute()}")
    else:
        print_info(f"Images directory already exists: {images_dir.absolute()}")

def main():
    """Main setup function."""
    print_header("Food Amigo Image Upload Feature Setup")

    print("This script will:")
    print("  1. Backup your existing automation.py and main.py files")
    print("  2. Apply the updated code with image upload features")
    print("  3. Create the images/ folder")
    print()

    response = input("Proceed with setup? (y/n): ").strip().lower()
    if response != 'y':
        print("\nSetup cancelled.")
        return

    print()
    print_info("Starting setup...")
    print()

    # Step 1: Backup files
    print_header("Step 1: Backing up existing files")

    automation_backup = backup_file("automation.py")
    main_backup = backup_file("main.py")

    if not (automation_backup and main_backup):
        print_error("\nBackup failed! Aborting setup.")
        return

    # Step 2: Apply updated files
    print_header("Step 2: Applying updated code")

    # Check if updated files exist
    if os.path.exists("automation_updated.py"):
        try:
            shutil.copy("automation_updated.py", "automation.py")
            print_success("Applied: automation.py")
        except Exception as e:
            print_error(f"Failed to apply automation.py: {e}")
            return
    else:
        print_error("automation_updated.py not found! Please make sure all files are in the same directory.")
        return

    if os.path.exists("main_updated.py"):
        try:
            shutil.copy("main_updated.py", "main.py")
            print_success("Applied: main.py")
        except Exception as e:
            print_error(f"Failed to apply main.py: {e}")
            return
    else:
        print_error("main_updated.py not found! Please make sure all files are in the same directory.")
        return

    # Step 3: Create images folder
    print_header("Step 3: Setting up images directory")
    create_images_folder()

    # Final summary
    print_header("Setup Complete!")

    print(f"{GREEN}✓ Files updated successfully!{RESET}")
    print()
    print("Next steps:")
    print("  1. Add your images to the images/ folder:")
    print(f"     {YELLOW}images/blog page 1 image.jpg{RESET}")
    print(f"     {YELLOW}images/blog page 2 image.png{RESET}")
    print(f"     {YELLOW}images/blog page 3 image.jpg{RESET}")
    print("     ... etc.")
    print()
    print("  2. Run your automation script:")
    print(f"     {YELLOW}python main.py \"seo_files/your_document.docx\"{RESET}")
    print()
    print("Backup files created:")
    print(f"  - {YELLOW}automation_backup.py{RESET}")
    print(f"  - {YELLOW}main_backup.py{RESET}")
    print()
    print(f"{BLUE}To restore backups if needed:{RESET}")
    print(f"  {YELLOW}python restore_backup.py{RESET}")
    print()

    # Create restore script
    create_restore_script()
    print_success("Created restore_backup.py for easy rollback")
    print()

def create_restore_script():
    """Create a script to restore backups."""
    restore_script = '''"""
Quick script to restore backup files.
"""
import os
import shutil

def restore():
    """Restore backup files."""
    print("Restoring backup files...")

    if os.path.exists("automation_backup.py"):
        shutil.copy("automation_backup.py", "automation.py")
        print("✓ Restored automation.py")
    else:
        print("✗ automation_backup.py not found")

    if os.path.exists("main_backup.py"):
        shutil.copy("main_backup.py", "main.py")
        print("✓ Restored main.py")
    else:
        print("✗ main_backup.py not found")

    print("\\nRestore complete!")

if __name__ == "__main__":
    restore()
'''

    with open("restore_backup.py", "w", encoding="utf-8") as f:
        f.write(restore_script)

if __name__ == "__main__":
    main()
