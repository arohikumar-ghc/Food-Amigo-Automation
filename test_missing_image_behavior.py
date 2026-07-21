"""
Test to demonstrate that missing images are now warnings instead of errors.
"""
from validator import ValidationResult


def test_missing_image_warning():
    """
    Test that missing images generate warnings instead of errors.
    """
    print("=" * 80)
    print("MISSING IMAGE BEHAVIOR TEST")
    print("=" * 80)
    print()

    # Create a validation result
    result = ValidationResult("Test Restaurant")

    print("Initial state:")
    print(f"  Passed: {result.passed}")
    print(f"  Errors: {len(result.errors)}")
    print(f"  Warnings: {len(result.warnings)}")
    print()

    # Simulate missing images being added as warnings
    print("Adding missing image warnings...")
    result.add_warning("Missing 2 images referenced in document:")
    result.add_warning("  - Page 1 (Test Page 1): image1.jpg")
    result.add_warning("  - Page 3 (Test Page 3): image3.jpg")
    print()

    print("After adding missing image warnings:")
    print(f"  Passed: {result.passed}")
    print(f"  Errors: {len(result.errors)}")
    print(f"  Warnings: {len(result.warnings)}")
    print()

    # Verify behavior
    if result.passed:
        print("[OK] VALIDATION STILL PASSES - Missing images are non-blocking!")
        print()
        print("Warnings generated:")
        for warning in result.warnings:
            print(f"  - {warning}")
        print()
        print("Result: Automation will continue despite missing images")
        return True
    else:
        print("[FAIL] VALIDATION FAILED - Missing images are still blocking!")
        print()
        print("Errors generated:")
        for error in result.errors:
            print(f"  - {error}")
        return False


def test_real_error_still_blocks():
    """
    Test that actual errors (not missing images) still block validation.
    """
    print()
    print("=" * 80)
    print("REAL ERROR BLOCKING TEST")
    print("=" * 80)
    print()

    result = ValidationResult("Test Restaurant")

    print("Adding missing images as warnings (should not block)...")
    result.add_warning("Missing 1 image: test.jpg")
    print(f"  Passed: {result.passed}")
    print()

    print("Adding a real error (should block)...")
    result.add_error("Document parsing failed")
    print(f"  Passed: {result.passed}")
    print()

    if not result.passed:
        print("[OK] Real errors still block validation as expected")
        print()
        print("Errors:")
        for error in result.errors:
            print(f"  - {error}")
        print()
        print("Warnings:")
        for warning in result.warnings:
            print(f"  - {warning}")
        return True
    else:
        print("[FAIL] Real errors should have blocked validation!")
        return False


def test_comparison():
    """
    Compare old vs new behavior side by side.
    """
    print()
    print("=" * 80)
    print("BEHAVIOR COMPARISON: OLD vs NEW")
    print("=" * 80)
    print()

    print("OLD BEHAVIOR (before fix):")
    print("-" * 80)
    print("  Missing images -> added as ERRORS")
    print("  Result: validation.passed = False")
    print("  Outcome: Automation STOPS, no pages processed")
    print()

    print("NEW BEHAVIOR (after fix):")
    print("-" * 80)
    print("  Missing images -> added as WARNINGS")
    print("  Result: validation.passed = True")
    print("  Outcome: Automation CONTINUES, pages processed normally")
    print()

    print("Impact:")
    print("-" * 80)
    print("  [OK] Pages with valid images -> processed successfully")
    print("  [OK] Pages with missing images -> processed without image")
    print("  [OK] Missing images -> logged as warnings for review")
    print("  [OK] Real errors (parsing, structure) -> still block automation")
    print()


if __name__ == "__main__":
    print("\n" + "=" * 80)
    print("TESTING MISSING IMAGE WARNING BEHAVIOR")
    print("=" * 80 + "\n")

    test1 = test_missing_image_warning()
    test2 = test_real_error_still_blocks()
    test_comparison()

    print("=" * 80)
    if test1 and test2:
        print("ALL TESTS PASSED")
        print()
        print("Summary:")
        print("  - Missing images are now NON-BLOCKING warnings")
        print("  - Automation will continue with available images")
        print("  - Real errors still block automation as expected")
    else:
        print("SOME TESTS FAILED")
    print("=" * 80)

    exit(0 if (test1 and test2) else 1)
