"""
Debug script to open Food Amigo with Playwright inspector.
This helps identify the correct selectors for Layout 6.
"""
import sys
from playwright.sync_api import sync_playwright

def main():
    print("Opening Food Amigo with Playwright inspector...")
    print("=" * 70)

    with sync_playwright() as p:
        # Launch browser with inspector
        browser = p.chromium.launch(
            headless=False,
            slow_mo=500,  # Slow down actions for visibility
            devtools=True  # Open DevTools automatically
        )

        context = browser.new_context(
            viewport={"width": 1920, "height": 1080},
            locale="en-US"
        )

        page = context.new_page()

        # Enable inspector (PWDEBUG mode)
        page.pause()

        print("\n✓ Browser opened with Playwright Inspector")
        print("=" * 70)
        print("\nInstructions:")
        print("1. In the browser, manually navigate to Food Amigo and log in")
        print("2. Go to Storefront Editor")
        print("3. Open 'Lamb Vindaloo' page")
        print("4. Click edit on Customizable section")
        print("5. Click 'Layout: 1' to open the selector")
        print("6. In the Inspector, use the 'Explore' button to find Layout 6")
        print("7. Click on Layout 6 in the browser")
        print("8. The Inspector will show the selector used")
        print("9. Copy the selector and paste it here")
        print("\nPress Ctrl+C in terminal to exit when done")
        print("=" * 70)

        # Navigate to Food Amigo
        try:
            print("\nNavigating to Food Amigo...")
            page.goto("https://restaurant.foodamigos.io/login", timeout=30000)
            print("✓ Page loaded")
        except Exception as e:
            print(f"⚠ Navigation warning: {e}")
            print("You can manually navigate in the browser")

        # Keep browser open until user closes it
        input("\nPress Enter when you're done recording the selector...")

        browser.close()

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n✓ Browser closed")
        sys.exit(0)
