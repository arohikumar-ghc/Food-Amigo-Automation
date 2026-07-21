"""
Test image filename matching with whitespace normalization.
"""
from pathlib import Path
from google_drive_handler import find_image_case_insensitive, _normalize_whitespace


def test_whitespace_normalization():
    """Test the whitespace normalization function."""
    print("Testing whitespace normalization:")
    print("=" * 80)

    test_cases = [
        ("Indian Comfort Food.jpg", "indian comfort food.jpg"),
        ("Indian  Comfort  Food.jpg", "indian comfort food.jpg"),
        ("  Indian Comfort Food.jpg  ", "indian comfort food.jpg"),
        ("Indian   Comfort    Food.jpg", "indian comfort food.jpg"),
        ("\tIndian\tComfort\tFood.jpg", "indian comfort food.jpg"),
        ("Paneer  Tikka.jpg", "paneer tikka.jpg"),
        ("INDIAN COMFORT FOOD.JPG", "indian comfort food.jpg"),
    ]

    all_passed = True
    for input_name, expected in test_cases:
        result = _normalize_whitespace(input_name)
        passed = result == expected
        status = "[OK]" if passed else "[FAIL]"
        print(f"{status} {repr(input_name):50s} -> {repr(result)}")
        if not passed:
            print(f"     Expected: {repr(expected)}")
            all_passed = False

    print()
    return all_passed


def test_image_matching():
    """Test image matching with whitespace variations."""
    print("Testing image matching with whitespace variations:")
    print("=" * 80)

    # Simulate image_lookup with various filenames
    image_lookup = {
        "indian comfort food in hilliard, oh.jpg": Path("cache/test/indian-comfort-food.jpg"),
        "paneer tikka.jpg": Path("cache/test/paneer-tikka.jpg"),
        "mango lassi.jpg": Path("cache/test/mango-lassi.jpg"),
        "north indian cuisine.jpg": Path("cache/test/north-indian.jpg"),
    }

    # Test cases: (query_filename, should_find)
    test_cases = [
        # Exact matches
        ("Indian Comfort Food in Hilliard, OH.jpg", True),
        ("Paneer Tikka.jpg", True),

        # Multiple spaces
        ("Indian  Comfort  Food  in Hilliard, OH.jpg", True),
        ("Paneer  Tikka.jpg", True),

        # Leading/trailing spaces
        ("  Indian Comfort Food in Hilliard, OH.jpg  ", True),
        ("  Paneer Tikka.jpg  ", True),

        # Case variations
        ("INDIAN COMFORT FOOD IN HILLIARD, OH.JPG", True),
        ("paneer tikka.JPG", True),

        # Extension variations
        ("Indian Comfort Food in Hilliard, OH.png", True),
        ("Paneer Tikka.PNG", True),

        # Should not find
        ("Butter Chicken.jpg", False),
        ("Nonexistent File.jpg", False),
    ]

    all_passed = True
    for query, should_find in test_cases:
        result = find_image_case_insensitive(query, image_lookup)
        found = result is not None
        passed = found == should_find

        status = "[OK]" if passed else "[FAIL]"
        found_str = "FOUND" if found else "NOT FOUND"
        expected_str = "should find" if should_find else "should NOT find"

        print(f"{status} {repr(query):50s} -> {found_str:10s} ({expected_str})")
        if not passed:
            all_passed = False

    print()
    return all_passed


def test_real_scenario():
    """Test the actual scenario from the error message."""
    print("Testing real scenario from error message:")
    print("=" * 80)

    # Simulate the actual cache with filenames that have potential whitespace issues
    image_lookup = {
        "paneer tikka in hilliard, oh.jpg": Path("cache/raj/paneer.jpg"),
        "mango lassi in hilliard, oh.jpg": Path("cache/raj/mango.jpg"),
        "samosas in hilliard, oh.jpg": Path("cache/raj/samosas.jpg"),
        "north indian cuisine in hilliard, oh.jpg": Path("cache/raj/north.jpg"),
        # Simulate a file with extra spaces in the cached name
        "indian  comfort  food  in hilliard, oh.jpg": Path("cache/raj/comfort.jpg"),
    }

    # Document references (might have different whitespace)
    queries = [
        "Paneer Tikka in Hilliard, OH.jpg",
        "Mango Lassi in Hilliard, OH.jpg",
        "Samosas in Hilliard, OH.jpg",
        "North Indian Cuisine in Hilliard, OH.jpg",
        "Indian Comfort Food in Hilliard, OH.jpg",  # This should now match!
    ]

    all_passed = True
    for query in queries:
        result = find_image_case_insensitive(query, image_lookup)
        found = result is not None
        status = "[OK]" if found else "[FAIL]"

        print(f"{status} {query:50s} -> {'FOUND' if found else 'NOT FOUND'}")
        if result:
            print(f"     Path: {result}")

        # All should be found in this test
        if not found:
            all_passed = False
            print(f"     ERROR: Expected to find this image!")

    print()
    return all_passed


if __name__ == "__main__":
    print("\n" + "=" * 80)
    print("IMAGE FILENAME MATCHING TESTS")
    print("=" * 80 + "\n")

    test1 = test_whitespace_normalization()
    test2 = test_image_matching()
    test3 = test_real_scenario()

    print("=" * 80)
    if test1 and test2 and test3:
        print("ALL TESTS PASSED!")
    else:
        print("SOME TESTS FAILED!")
        if not test1:
            print("  - Whitespace normalization tests failed")
        if not test2:
            print("  - Image matching tests failed")
        if not test3:
            print("  - Real scenario test failed")
    print("=" * 80)

    exit(0 if (test1 and test2 and test3) else 1)
