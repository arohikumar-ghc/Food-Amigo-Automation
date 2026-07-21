"""
Comprehensive test demonstrating the image validation fix.

This shows that the validator will now correctly match images even when there are
whitespace differences between the document reference and the cached filename.
"""
from pathlib import Path
from google_drive_handler import find_image_case_insensitive


def test_before_and_after():
    """
    Demonstrate the improvement: cases that would have failed before now pass.
    """
    print("=" * 80)
    print("IMAGE VALIDATION: BEFORE vs AFTER FIX")
    print("=" * 80)
    print()

    # Simulate a real-world scenario where filenames might have whitespace variations
    test_cases = [
        {
            "description": "Extra spaces in cached filename",
            "cached_filename": "Paneer  Tikka  in  Hilliard.jpg",  # Double spaces
            "doc_reference": "Paneer Tikka in Hilliard.jpg",        # Single spaces
        },
        {
            "description": "Leading/trailing spaces in document",
            "cached_filename": "Mango Lassi.jpg",
            "doc_reference": "  Mango Lassi.jpg  ",
        },
        {
            "description": "Tab character in document reference",
            "cached_filename": "Chicken Tikka.jpg",
            "doc_reference": "Chicken\tTikka.jpg",
        },
        {
            "description": "Multiple spaces in document reference",
            "cached_filename": "North Indian Cuisine.jpg",
            "doc_reference": "North   Indian   Cuisine.jpg",
        },
        {
            "description": "Case + whitespace differences",
            "cached_filename": "fresh  naan  bread.jpg",  # Lowercase, double spaces
            "doc_reference": "Fresh Naan Bread.JPG",       # Title case, single spaces, different ext
        },
    ]

    print("BEFORE FIX: Strict matching (would fail on whitespace differences)")
    print("-" * 80)
    print("These cases would cause 'Missing images' validation errors:\n")

    for i, case in enumerate(test_cases, 1):
        # Old behavior: exact string match (case-insensitive only)
        old_match = case["cached_filename"].lower() == case["doc_reference"].lower()
        print(f"{i}. {case['description']}")
        print(f"   Cached:    '{case['cached_filename']}'")
        print(f"   Document:  '{case['doc_reference']}'")
        print(f"   Old match: {'PASS' if old_match else 'FAIL [X]'}")
        print()

    print()
    print("=" * 80)
    print("AFTER FIX: Flexible matching (handles whitespace normalization)")
    print("-" * 80)
    print("All cases now pass with whitespace normalization:\n")

    all_passed = True
    for i, case in enumerate(test_cases, 1):
        # Create a mock image_lookup with the cached filename
        image_lookup = {
            case["cached_filename"].lower(): Path(f"cache/test{i}.jpg")
        }

        # Test the new matching logic
        result = find_image_case_insensitive(case["doc_reference"], image_lookup)
        new_match = result is not None

        print(f"{i}. {case['description']}")
        print(f"   Cached:    '{case['cached_filename']}'")
        print(f"   Document:  '{case['doc_reference']}'")
        print(f"   New match: {'PASS [OK]' if new_match else 'FAIL [X]'}")
        if result:
            print(f"   Found at:  {result}")
        print()

        if not new_match:
            all_passed = False

    print("=" * 80)
    if all_passed:
        print("[OK] ALL CASES PASS - Whitespace differences no longer cause validation errors!")
    else:
        print("[X] Some cases failed - this should not happen!")
    print("=" * 80)

    return all_passed


def test_real_validation_scenario():
    """
    Simulate a real validation scenario with multiple images.
    """
    print("\n" + "=" * 80)
    print("REAL VALIDATION SCENARIO")
    print("=" * 80)
    print()
    print("Simulating validator checking 10 pages against cached images...")
    print()

    # Simulate cached images (with potential whitespace variations)
    cached_images = {
        "paneer tikka in hilliard, oh.jpg": Path("cache/raj/paneer.jpg"),
        "mango  lassi  in  hilliard, oh.jpg": Path("cache/raj/mango.jpg"),  # Extra spaces
        "samosas in hilliard, oh.jpg": Path("cache/raj/samosas.jpg"),
        "north indian cuisine in hilliard, oh.jpg": Path("cache/raj/north.jpg"),
        "vegetable biryani.jpg": Path("cache/raj/veg-biryani.jpg"),
        "weekend indian dining in hilliard, oh.jpg": Path("cache/raj/weekend.jpg"),
        "fresh naan bread in hilliard, oh.jpg": Path("cache/raj/naan.jpg"),
        "paneer butter masala.jpg": Path("cache/raj/paneer-masala.jpg"),
        "chicken tikka.jpg": Path("cache/raj/chicken.jpg"),
        "indian food pickup in hilliard, oh.jpg": Path("cache/raj/pickup.jpg"),
    }

    # Simulate document references (might have different whitespace)
    document_references = [
        "Paneer Tikka in Hilliard, OH.jpg",
        "Mango Lassi in Hilliard, OH.jpg",        # Document has single space
        "  Samosas in Hilliard, OH.jpg  ",        # Leading/trailing spaces
        "North   Indian   Cuisine in Hilliard, OH.jpg",  # Multiple spaces
        "Vegetable Biryani.jpg",
        "Weekend Indian Dining in Hilliard, OH.jpg",
        "Fresh Naan Bread in Hilliard, OH.jpg",
        "Paneer Butter Masala.jpg",
        "Chicken Tikka.jpg",
        "Indian Food Pickup in Hilliard, OH.jpg",
    ]

    print(f"Cached images:     {len(cached_images)}")
    print(f"Document pages:    {len(document_references)}")
    print()

    missing_images = []
    for i, doc_ref in enumerate(document_references, 1):
        found = find_image_case_insensitive(doc_ref, cached_images)
        status = "[OK]" if found else "[X]"
        print(f"Page {i:2d}: {status} {doc_ref:45s} -> {'FOUND' if found else 'MISSING'}")

        if not found:
            missing_images.append((i, doc_ref))

    print()
    if not missing_images:
        print("[OK] VALIDATION PASSED - All images found!")
    else:
        print(f"[X] VALIDATION FAILED - {len(missing_images)} missing images:")
        for page_num, filename in missing_images:
            print(f"  - Page {page_num}: {filename}")

    print("=" * 80)

    return len(missing_images) == 0


if __name__ == "__main__":
    test1 = test_before_and_after()
    test2 = test_real_validation_scenario()

    print("\n" + "=" * 80)
    print("SUMMARY")
    print("=" * 80)
    if test1 and test2:
        print("[OK] All tests passed!")
        print()
        print("The image validation is now more flexible and will correctly match")
        print("filenames even when there are whitespace differences between the")
        print("document reference and the cached filename.")
    else:
        print("[X] Some tests failed!")
    print("=" * 80)

    exit(0 if (test1 and test2) else 1)
