"""
Test script to verify Href validation and auto-correction.
"""
from models import SEOPageData, FAQ

print("=" * 80)
print("HREF VALIDATION TEST")
print("=" * 80)

# Test Case 1: Href WITHOUT leading slash
print("\nTest Case 1: Href WITHOUT leading slash")
print("-" * 80)

data1 = SEOPageData(
    href="blog-post",  # Missing leading slash
    page_name="blog-post",
    seo_title="Test Title",
    seo_description="Test Description",
    subtitle="Test Subtitle",
    title="Test Title",
    description="Test Description",
    faqs=[FAQ(question="Q?", answer="A")]
)

print(f"Input:  href = 'blog-post'")
print(f"Output: href = '{data1.href}'")
print(f"✓ Automatically added '/' prefix!" if data1.href.startswith('/') else "✗ Failed to add '/'")

# Test Case 2: Href WITH leading slash
print("\n\nTest Case 2: Href WITH leading slash")
print("-" * 80)

data2 = SEOPageData(
    href="/blog-post",  # Already has leading slash
    page_name="blog-post",
    seo_title="Test Title",
    seo_description="Test Description",
    subtitle="Test Subtitle",
    title="Test Title",
    description="Test Description",
    faqs=[FAQ(question="Q?", answer="A")]
)

print(f"Input:  href = '/blog-post'")
print(f"Output: href = '{data2.href}'")
print(f"✓ Kept existing '/' prefix!" if data2.href == '/blog-post' else "✗ Incorrectly modified")

# Test Case 3: Complex href without slash
print("\n\nTest Case 3: Complex href without slash")
print("-" * 80)

data3 = SEOPageData(
    href="lamb-vindaloo-lancaster-pa",  # No leading slash
    page_name="lamb-vindaloo-lancaster-pa",
    seo_title="Test Title",
    seo_description="Test Description",
    subtitle="Test Subtitle",
    title="Test Title",
    description="Test Description",
    faqs=[FAQ(question="Q?", answer="A")]
)

print(f"Input:  href = 'lamb-vindaloo-lancaster-pa'")
print(f"Output: href = '{data3.href}'")
print(f"✓ Automatically added '/' prefix!" if data3.href.startswith('/') else "✗ Failed to add '/'")

# Test Case 4: URL-style href
print("\n\nTest Case 4: URL-style href")
print("-" * 80)

data4 = SEOPageData(
    href="best-lamb-vindaloo",
    page_name="best-lamb-vindaloo",
    seo_title="Test Title",
    seo_description="Test Description",
    subtitle="Test Subtitle",
    title="Test Title",
    description="Test Description",
    faqs=[FAQ(question="Q?", answer="A")]
)

print(f"Input:  href = 'best-lamb-vindaloo'")
print(f"Output: href = '{data4.href}'")
print(f"✓ Automatically added '/' prefix!" if data4.href.startswith('/') else "✗ Failed to add '/'")

# Validation Test
print("\n\n" + "=" * 80)
print("VALIDATION TEST")
print("=" * 80)

validation_errors = data1.validate()
print(f"\nValidation errors for corrected href: {validation_errors}")
print(f"✓ Validation passed!" if not validation_errors else f"✗ Validation failed: {validation_errors}")

print("\n" + "=" * 80)
print("SUMMARY")
print("=" * 80)

test_cases = [
    ("blog-post", data1.href),
    ("/blog-post", data2.href),
    ("lamb-vindaloo-lancaster-pa", data3.href),
    ("best-lamb-vindaloo", data4.href)
]

all_passed = True
for input_val, output_val in test_cases:
    expected = input_val if input_val.startswith('/') else '/' + input_val
    passed = output_val == expected
    status = "✓" if passed else "✗"
    print(f"{status} '{input_val}' -> '{output_val}' (expected: '{expected}')")
    if not passed:
        all_passed = False

print("\n" + "=" * 80)
if all_passed:
    print("✓ ALL TESTS PASSED!")
    print("\nThe automation will now automatically add '/' to any href that doesn't have it.")
    print("This fixes the Food Amigo validation error: 'Href must start with /'")
else:
    print("✗ SOME TESTS FAILED")

print("=" * 80)
