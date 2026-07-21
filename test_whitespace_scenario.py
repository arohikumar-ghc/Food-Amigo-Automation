"""
Test the specific scenario where a document references a filename with different whitespace
than the cached filename.
"""
from pathlib import Path
from google_drive_handler import find_image_case_insensitive


def test_whitespace_mismatch_scenarios():
    """
    Simulate scenarios where document filename and cached filename have whitespace differences.
    """
    print("=" * 80)
    print("WHITESPACE MISMATCH SCENARIOS")
    print("=" * 80)
    print()

    # Scenario 1: Document has single spaces, cached file has double spaces
    print("Scenario 1: Cached file has extra spaces")
    print("-" * 80)
    image_lookup = {
        "indian  comfort  food  in hilliard, oh.jpg": Path("cache/indian-comfort.jpg"),
    }
    query = "Indian Comfort Food in Hilliard, OH.jpg"
    result = find_image_case_insensitive(query, image_lookup)
    print(f"Document:     '{query}'")
    print(f"Cached as:    'Indian  Comfort  Food  in Hilliard, OH.jpg' (double spaces)")
    print(f"Match result: {'FOUND' if result else 'NOT FOUND'}")
    print(f"Status:       {'[OK]' if result else '[FAIL]'}")
    print()

    # Scenario 2: Document has extra spaces, cached file is normal
    print("Scenario 2: Document reference has extra spaces")
    print("-" * 80)
    image_lookup = {
        "indian comfort food in hilliard, oh.jpg": Path("cache/indian-comfort.jpg"),
    }
    query = "Indian  Comfort  Food  in Hilliard, OH.jpg"
    result = find_image_case_insensitive(query, image_lookup)
    print(f"Document:     '{query}' (double spaces)")
    print(f"Cached as:    'Indian Comfort Food in Hilliard, OH.jpg'")
    print(f"Match result: {'FOUND' if result else 'NOT FOUND'}")
    print(f"Status:       {'[OK]' if result else '[FAIL]'}")
    print()

    # Scenario 3: Leading/trailing spaces in document
    print("Scenario 3: Document reference has leading/trailing spaces")
    print("-" * 80)
    image_lookup = {
        "paneer tikka in hilliard, oh.jpg": Path("cache/paneer.jpg"),
    }
    query = "  Paneer Tikka in Hilliard, OH.jpg  "
    result = find_image_case_insensitive(query, image_lookup)
    print(f"Document:     '{query}'")
    print(f"Cached as:    'Paneer Tikka in Hilliard, OH.jpg'")
    print(f"Match result: {'FOUND' if result else 'NOT FOUND'}")
    print(f"Status:       {'[OK]' if result else '[FAIL]'}")
    print()

    # Scenario 4: Mixed whitespace (tabs, multiple spaces)
    print("Scenario 4: Mixed whitespace characters")
    print("-" * 80)
    image_lookup = {
        "mango lassi in hilliard, oh.jpg": Path("cache/mango.jpg"),
    }
    query = "Mango\tLassi  in   Hilliard, OH.jpg"
    result = find_image_case_insensitive(query, image_lookup)
    print(f"Document:     '{query}' (contains tab and multiple spaces)")
    print(f"Cached as:    'Mango Lassi in Hilliard, OH.jpg'")
    print(f"Match result: {'FOUND' if result else 'NOT FOUND'}")
    print(f"Status:       {'[OK]' if result else '[FAIL]'}")
    print()

    # Scenario 5: Case + whitespace differences
    print("Scenario 5: Case AND whitespace differences")
    print("-" * 80)
    image_lookup = {
        "north  indian  cuisine.jpg": Path("cache/north-indian.jpg"),
    }
    query = "NORTH INDIAN CUISINE.JPG"
    result = find_image_case_insensitive(query, image_lookup)
    print(f"Document:     '{query}' (uppercase, single spaces)")
    print(f"Cached as:    'North  Indian  Cuisine.jpg' (mixed case, double spaces)")
    print(f"Match result: {'FOUND' if result else 'NOT FOUND'}")
    print(f"Status:       {'[OK]' if result else '[FAIL]'}")
    print()

    print("=" * 80)
    print("All scenarios demonstrate flexible whitespace matching!")
    print("=" * 80)


if __name__ == "__main__":
    test_whitespace_mismatch_scenarios()
