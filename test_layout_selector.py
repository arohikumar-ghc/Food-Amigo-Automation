"""
Interactive test script to find the correct Layout 6 selector.
Opens browser, lets you manually navigate, then test selectors.
"""
import sys
from playwright.sync_api import sync_playwright

def main():
    print("="*70)
    print("LAYOUT 6 SELECTOR TEST")
    print("="*70)
    print()
    print("This script will:")
    print("1. Open a browser")
    print("2. Let you manually navigate to the Customizable editor")
    print("3. Pause so you can test clicking Layout: 1 and Layout 6")
    print("4. Show you what selectors work")
    print()
    input("Press Enter to start...")

    with sync_playwright() as p:
        # Launch browser
        browser = p.chromium.launch(
            headless=False,
            slow_mo=1000  # Slow down so you can see what's happening
        )

        context = browser.new_context(
            viewport={"width": 1920, "height": 1080}
        )

        page = context.new_page()

        # Navigate to Food Amigo
        print("\n1. Navigating to Food Amigo...")
        page.goto("https://website-staging.foodamigos.io/login")

        print("\n2. Please log in manually and navigate to:")
        print("   - Select 'HWY TO INDIA' restaurant")
        print("   - Go to Storefront Editor")
        print("   - Open 'Lamb Vindaloo' page")
        print("   - Click 'edit' on Customizable section")
        print()
        input("Press Enter when you see 'Layout: 1' button...")

        # Test clicking Layout: 1
        print("\n3. Testing selectors for 'Layout: 1' button...")
        print()

        # Strategy 1: Click h6
        try:
            print("   Testing: page.locator('h6:text-is(\"Layout: 1\")')")
            layout_h6 = page.locator('h6:text-is("Layout: 1")').first
            if layout_h6.is_visible(timeout=2000):
                print("   ✓ Found with h6 selector")
                layout_h6.click()
                page.wait_for_timeout(2000)
                print("   ✓ Clicked successfully!")
            else:
                print("   ✗ Not visible")
        except Exception as e:
            print(f"   ✗ Failed: {e}")

        # Check if modal opened
        page.wait_for_timeout(1000)

        # Try to find Layout 6
        print("\n4. Looking for Layout 6 in the modal...")

        # Strategy 1: Click image
        try:
            print("   Testing: img[src*='customizable/6.png']")
            layout_6_img = page.locator('img[src*="customizable/6.png"]')
            if layout_6_img.is_visible(timeout=2000):
                print("   ✓ Found Layout 6 image!")
                layout_6_img.click()
                page.wait_for_timeout(2000)
                print("   ✓ Clicked Layout 6!")
            else:
                print("   ✗ Not visible")
        except Exception as e:
            print(f"   ✗ Failed: {e}")

        print("\n5. Check in the browser - did Layout 6 get selected?")
        print("   Look at the top of the editor - does it say 'Layout: 6'?")
        print()

        result = input("Did it work? (yes/no): ").lower()

        if result == "yes":
            print("\n✓ SUCCESS! The selectors work!")
            print("\nWorking selectors:")
            print("  1. Open modal: page.locator('h6:text-is(\"Layout: 1\")').first.click()")
            print("  2. Select Layout 6: page.locator('img[src*=\"customizable/6.png\"]').click()")
        else:
            print("\n✗ Need to try different selectors")
            print("\nPlease:")
            print("1. Right-click on 'Layout: 1' → Inspect")
            print("2. Copy the HTML")
            print("3. Right-click on Layout 6 card → Inspect")
            print("4. Copy the HTML")
            print("5. Share both with me")

        input("\nPress Enter to close browser...")
        browser.close()

if __name__ == "__main__":
    main()
