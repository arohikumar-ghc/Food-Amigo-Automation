"""
Demonstrate the validation behavior change for missing images.
"""
from validator import ValidationResult


def demo_old_behavior():
    """
    Demonstrate what would happen with the OLD behavior.
    """
    print("=" * 80)
    print("SCENARIO: Restaurant has 10 pages, but 1 image is missing")
    print("=" * 80)
    print()

    print("OLD BEHAVIOR (Before Fix):")
    print("-" * 80)
    print("Step 1: Parse document -> SUCCESS (10 pages)")
    print("Step 2: Download images -> SUCCESS (10 images from Drive)")
    print("Step 3: Validate images -> FOUND MISSING IMAGE")
    print("        Page 5: 'Indian Comfort Food in Hilliard, OH.jpg' NOT FOUND")
    print()
    print("Action: add_error('Missing 1 images...')")
    print("Result: validation.passed = False")
    print()
    print("OUTCOME: Automation STOPS")
    print("  [X] No pages created")
    print("  [X] 9 valid pages NOT processed")
    print("  [X] User must fix missing image before ANY page can be created")
    print()
    print()


def demo_new_behavior():
    """
    Demonstrate what happens with the NEW behavior.
    """
    print("NEW BEHAVIOR (After Fix):")
    print("-" * 80)
    print("Step 1: Parse document -> SUCCESS (10 pages)")
    print("Step 2: Download images -> SUCCESS (10 images from Drive)")
    print("Step 3: Validate images -> FOUND MISSING IMAGE")
    print("        Page 5: 'Indian Comfort Food in Hilliard, OH.jpg' NOT FOUND")
    print()
    print("Action: add_warning('Missing 1 images...')")
    print("Result: validation.passed = True")
    print()
    print("OUTCOME: Automation CONTINUES")
    print("  [OK] Page 1 created with image (Paneer Tikka)")
    print("  [OK] Page 2 created with image (Mango Lassi)")
    print("  [OK] Page 3 created with image (Samosas)")
    print("  [OK] Page 4 created with image (North Indian Cuisine)")
    print("  [OK] Page 5 created WITHOUT image (missing image logged as warning)")
    print("  [OK] Page 6 created with image (Vegetable Biryani)")
    print("  [OK] Page 7 created with image (Weekend Indian Dining)")
    print("  [OK] Page 8 created with image (Fresh Naan Bread)")
    print("  [OK] Page 9 created with image (Paneer Butter Masala)")
    print("  [OK] Page 10 created with image (Chicken Tikka)")
    print()
    print("Summary:")
    print("  - 9 pages successfully created with images")
    print("  - 1 page created without image (warning logged)")
    print("  - User can fix missing image later if needed")
    print()


def demo_validation_result():
    """
    Show the actual ValidationResult behavior.
    """
    print()
    print("=" * 80)
    print("VALIDATION RESULT OBJECT BEHAVIOR")
    print("=" * 80)
    print()

    result = ValidationResult("RAJ SHAHHI INDIAN RESTAURANT")

    print("Initial state:")
    print(f"  result.passed = {result.passed}")
    print()

    # Simulate successful parsing and download
    result.page_count = 10
    result.image_count = 10

    print("After parsing 10 pages and downloading 10 images:")
    print(f"  result.passed = {result.passed}")
    print()

    # Add missing image WARNING (not error)
    print("Adding missing image warning:")
    result.add_warning("Missing 1 images referenced in document:")
    result.add_warning("  - Page 5 (Indian Comfort Food): Indian Comfort Food.jpg")

    print(f"  result.add_warning('Missing 1 images...')")
    print()
    print(f"Final state:")
    print(f"  result.passed = {result.passed}")
    print(f"  result.errors = {result.errors}")
    print(f"  result.warnings = {result.warnings}")
    print()

    if result.passed:
        print("[OK] Validation PASSES -> Automation will run!")
    else:
        print("[FAIL] Validation FAILS -> Automation blocked")

    return result.passed


if __name__ == "__main__":
    print("\n" + "=" * 80)
    print("MISSING IMAGE BEHAVIOR DEMONSTRATION")
    print("=" * 80)
    print()

    demo_old_behavior()
    demo_new_behavior()
    success = demo_validation_result()

    print()
    print("=" * 80)
    print("KEY TAKEAWAY")
    print("=" * 80)
    print()
    print("Missing images are now treated as WARNINGS instead of ERRORS.")
    print()
    print("This means:")
    print("  1. Automation continues even if some images are missing")
    print("  2. Pages with valid images are processed normally")
    print("  3. Pages with missing images are still created (just without image)")
    print("  4. Missing images are logged for later review")
    print("  5. Real errors (parsing failures, etc.) still block automation")
    print()
    print("=" * 80)

    exit(0 if success else 1)
