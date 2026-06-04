"""
Automation module for creating SEO pages in Food Amigo.
"""
import logging
from pathlib import Path
from typing import Optional
from playwright.sync_api import sync_playwright, Page, Browser, BrowserContext
from models import SEOPageData, FAQ
from config import AutomationConfig


logger = logging.getLogger("foodamigo_automation.automation")


class FoodAmigoAutomation:
    """Automation class for Food Amigo SEO page creation."""

    def __init__(self, config: AutomationConfig):
        """
        Initialize automation with configuration.

        Args:
            config: AutomationConfig instance
        """
        self.config = config
        self.browser: Optional[Browser] = None
        self.context: Optional[BrowserContext] = None
        self.page: Optional[Page] = None

    def __enter__(self):
        """Context manager entry."""
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """Context manager exit."""
        self.close()

    def _dismiss_blocking_overlays(self):
        """
        Dismiss any blocking overlays, modals, or alerts that might prevent interaction.
        """
        try:
            # Check for success notifications/toasts
            success_notif = self.page.locator(".ant-notification-notice, .ant-message-notice")
            if success_notif.first.is_visible(timeout=500):
                logger.debug("Found notification overlay, dismissing...")
                # Click close button if exists
                close_btn = success_notif.locator(".ant-notification-close-x, .anticon-close").first
                if close_btn.is_visible(timeout=500):
                    close_btn.click()
                    self.page.wait_for_timeout(300)
        except:
            pass

        try:
            # Check for modal masks
            mask = self.page.locator(".ant-modal-mask, .ant-drawer-mask")
            if mask.first.is_visible(timeout=500):
                logger.debug("Found blocking mask overlay")
        except:
            pass

        try:
            # Check for confirmation dialogs
            confirm_ok = self.page.locator(".ant-modal-confirm-btns button").first
            if confirm_ok.is_visible(timeout=500):
                logger.debug("Found confirmation dialog, clicking OK...")
                confirm_ok.click()
                self.page.wait_for_timeout(500)
        except:
            pass

    def _find_image_for_page_number(self, page_num: int) -> Optional[str]:
        """
        Find image for a specific page number.

        Looks for: images/blog page {page_num} image.jpg or .png

        Args:
            page_num: Page number (1, 2, 3, etc.)

        Returns:
            Full path to image if found, None otherwise
        """
        images_dir = Path("images")

        # Check for .jpg first, then .png
        for ext in ['.jpg', '.png']:
            image_name = f"blog page {page_num} image{ext}"
            image_path = images_dir / image_name
            if image_path.exists():
                logger.debug(f"Found image: {image_path}")
                return str(image_path.absolute())

        logger.info(f"Image for Page {page_num} not found, skipping upload...")
        return None

    def start_browser(self):
        """Launch browser and create page."""
        logger.info("Starting browser...")

        self.playwright = sync_playwright().start()
        self.browser = self.playwright.chromium.launch(
            headless=self.config.headless,
            slow_mo=self.config.slow_mo
        )
        self.context = self.browser.new_context()
        self.page = self.context.new_page()
        self.page.set_default_timeout(self.config.timeout)

        logger.info("Browser started successfully")

    def close(self):
        """Close browser and cleanup."""
        if self.page:
            self.page.close()
        if self.context:
            self.context.close()
        if self.browser:
            self.browser.close()
        if hasattr(self, 'playwright'):
            self.playwright.stop()

        logger.info("Browser closed")

    def login(self):
        """
        Login to Food Amigo platform.

        Raises:
            Exception: If login fails
        """
        logger.info("Logging in to Food Amigo...")

        self.page.goto(f"{self.config.base_url}/login")

        self.page.get_by_role("textbox", name="Enter Email").fill(self.config.email)
        self.page.get_by_role("textbox", name="Enter Password").fill(self.config.password)
        self.page.get_by_role("button", name="Login").click()

        self.page.wait_for_load_state("networkidle")

        logger.info("Login successful")

    def select_restaurant(self):
        """
        Search and select restaurant.

        Raises:
            Exception: If restaurant not found
        """
        logger.info(f"Selecting restaurant: {self.config.restaurant_name}")

        self.page.locator(".css-19bb58m").click()
        self.page.get_by_role("option", name=self.config.restaurant_name).click()

        self.page.wait_for_load_state("networkidle")

        logger.info("Restaurant selected")

    def open_storefront_editor(self):
        """
        Navigate to storefront editor.

        Raises:
            Exception: If navigation fails
        """
        logger.info("Opening storefront editor...")

        self.page.get_by_role("img", name="global").locator("svg").click()
        self.page.get_by_role("link", name="Storefront").click()

        self.page.wait_for_load_state("networkidle")

        self.page.get_by_role("link", name="edit Open editor").click()

        self.page.wait_for_load_state("networkidle")

        logger.info("Storefront editor opened")

    def navigate_to_dashboard(self):
        """
        Navigate back to storefront editor dashboard.

        This ensures clean state before creating the next page.
        """
        logger.info("Resetting to storefront editor dashboard...")

        try:
            # Close any open modals/drawers first
            try:
                mask = self.page.locator(".ant-drawer-mask")
                if mask.is_visible(timeout=1000):
                    mask.click()
                    self.page.wait_for_timeout(500)
            except:
                pass

            # Navigate to the storefront editor URL (force reload)
            storefront_url = f"{self.config.base_url}/storefront-editor"
            self.page.goto(storefront_url, wait_until="networkidle")

            self.page.wait_for_timeout(1500)

            logger.info("Dashboard reset complete")

        except Exception as e:
            logger.warning(f"Dashboard navigation warning: {e}")
            # Force reload as fallback
            self.page.reload(wait_until="networkidle")
            self.page.wait_for_timeout(1500)

    def create_seo_page(self, data: SEOPageData, page_num: Optional[int] = None):
        """
        Create a new SEO page with provided data.

        Args:
            data: SEOPageData containing all page information
            page_num: Page number for image matching (1, 2, 3, etc.)

        Raises:
            Exception: If page creation fails
        """
        logger.info(f"Creating SEO page: {data.page_name}")

        self._click_add_page_button()
        self._fill_basic_info(data)
        self._fill_seo_metadata(data)
        self._fill_social_metadata(data, page_num)
        self._add_customizable_section(data, page_num)
        self._add_faq_section(data)

        logger.info(f"SEO page created successfully: {data.page_name}")

    def _click_add_page_button(self):
        """Click the '+' button to create new page."""
        logger.info("→ Clicking add page button...")

        self._dismiss_blocking_overlays()

        add_btn = self.page.get_by_role("button", name="plus", exact=True)
        add_btn.wait_for(state="visible", timeout=10000)
        add_btn.click()

        logger.info("✓ Add page button clicked")

    def _fill_basic_info(self, data: SEOPageData):
        """
        Fill href and name fields.

        Args:
            data: SEOPageData instance
        """
        logger.info("→ Filling basic info (href, name)...")

        # Ensure href starts with '/' (final safety check)
        href = data.href if data.href.startswith('/') else '/' + data.href
        logger.debug(f"  Href value: {href}")

        self._dismiss_blocking_overlays()

        logger.debug("  Waiting for Href field...")
        href_field = self.page.get_by_role("textbox", name="* Href in English")
        href_field.wait_for(state="visible", timeout=10000)
        href_field.fill(href)
        logger.debug("  ✓ Href filled")

        logger.debug("  Waiting for Name field...")
        name_field = self.page.get_by_role("textbox", name="* Name in English")
        name_field.wait_for(state="visible", timeout=10000)
        name_field.fill(data.page_name)
        logger.debug("  ✓ Name filled")

        logger.debug("  Clicking Save button...")
        save_btn = self.page.get_by_role("button", name="Save")
        save_btn.wait_for(state="visible", timeout=10000)
        save_btn.click()
        logger.debug("  ✓ Save clicked")

        self.page.wait_for_timeout(1500)
        self._dismiss_blocking_overlays()

        logger.debug("  Clicking page name button to reopen...")
        page_btn = self.page.get_by_role("button", name=data.page_name)
        page_btn.wait_for(state="visible", timeout=10000)
        page_btn.click()

        logger.debug("  Clicking Edit button...")
        edit_btn = self.page.get_by_role("button", name="edit Edit")
        edit_btn.wait_for(state="visible", timeout=10000)
        edit_btn.click()

        logger.info("✓ Basic info saved and page reopened for editing")

    def _fill_seo_metadata(self, data: SEOPageData):
        """
        Fill SEO title and description in General tab.

        Args:
            data: SEOPageData instance
        """
        logger.info("→ Filling SEO metadata (General tab)...")

        self._dismiss_blocking_overlays()

        # Explicitly click General tab and wait for it to be active
        logger.debug("  Clicking General tab...")
        general_tab = self.page.get_by_text("General", exact=True)
        general_tab.wait_for(state="visible", timeout=10000)
        general_tab.click()
        logger.debug("  ✓ General tab clicked")

        # Wait for tab content to load
        self.page.wait_for_timeout(800)

        # Click edit button within General tab
        logger.debug("  Clicking edit button in General tab...")
        edit_button = self.page.get_by_label("General").get_by_role("button", name="edit")
        edit_button.wait_for(state="visible", timeout=10000)
        edit_button.click()
        logger.debug("  ✓ Edit button clicked")

        # Wait for form to open
        self.page.wait_for_timeout(800)
        self._dismiss_blocking_overlays()

        # Wait for Title field to be visible and fill
        logger.debug("  Filling General Title...")
        title_field = self.page.get_by_role("textbox", name="Title :")
        title_field.wait_for(state="visible", timeout=10000)
        title_field.fill(data.seo_title)
        logger.debug("  ✓ Title filled")

        # Fill Description
        logger.debug("  Filling General Description...")
        description_field = self.page.get_by_role("textbox", name="Description :")
        description_field.wait_for(state="visible", timeout=10000)
        description_field.fill(data.seo_description)
        logger.debug("  ✓ Description filled")

        # Save
        logger.debug("  Clicking Save...")
        save_btn = self.page.get_by_role("button", name="Save")
        save_btn.wait_for(state="visible", timeout=10000)
        save_btn.click()
        logger.debug("  ✓ Save clicked")

        self.page.wait_for_timeout(1500)
        self._dismiss_blocking_overlays()

        logger.info("✓ SEO metadata saved")

    def _fill_social_metadata(self, data: SEOPageData, page_num: Optional[int] = None):
        """
        Fill social title and description in Social tab.

        Args:
            data: SEOPageData instance
            page_num: Page number for image matching
        """
        logger.info("→ Filling social metadata (Social tab)...")

        self._dismiss_blocking_overlays()

        # Explicitly click Social tab and wait for it to be active
        logger.debug("  Clicking Social tab...")
        social_tab = self.page.get_by_text("Social", exact=True)
        social_tab.wait_for(state="visible", timeout=10000)
        social_tab.click()
        logger.debug("  ✓ Social tab clicked")

        # Wait for tab content to load
        self.page.wait_for_timeout(800)

        # Click edit button within Social tab
        logger.debug("  Clicking edit button in Social tab...")
        edit_button = self.page.get_by_label("Social").get_by_role("button", name="edit")
        edit_button.wait_for(state="visible", timeout=10000)
        edit_button.click()
        logger.debug("  ✓ Edit button clicked")

        # Wait for form to open
        self.page.wait_for_timeout(800)
        self._dismiss_blocking_overlays()

        # Wait for Social Title field to be visible and fill
        logger.debug("  Filling Social Title...")
        social_title_field = self.page.get_by_role("textbox", name="Social Title :")
        social_title_field.wait_for(state="visible", timeout=10000)
        social_title_field.fill(data.seo_title)
        logger.debug("  ✓ Social Title filled")

        # Fill Social Description
        logger.debug("  Filling Social Description...")
        social_description_field = self.page.get_by_role("textbox", name="Social Description :")
        social_description_field.wait_for(state="visible", timeout=10000)
        social_description_field.fill(data.seo_description)
        logger.debug("  ✓ Social Description filled")

        # Upload image if available (Location 2: Social tab)
        if page_num:
            image_path = self._find_image_for_page_number(page_num)
            if image_path:
                logger.info(f"  → Uploading image for Page {page_num} in Social tab...")
                try:
                    # Locate the file upload input in Social section
                    upload_input = self.page.locator("input[type='file']").first
                    upload_input.set_input_files(image_path)

                    logger.debug("  Waiting for image upload to process...")
                    self.page.wait_for_timeout(2000)

                    logger.info(f"  ✓ Image uploaded in Social tab")
                except Exception as e:
                    logger.warning(f"  Failed to upload image in Social tab: {e}")

        # Save
        logger.debug("  Clicking Save...")
        save_btn = self.page.get_by_role("button", name="Save")
        save_btn.wait_for(state="visible", timeout=10000)
        save_btn.click()
        logger.debug("  ✓ Save clicked")

        self.page.wait_for_timeout(1500)
        self._dismiss_blocking_overlays()

        logger.info("✓ Social metadata saved")

        # Navigate back to page
        logger.debug("Navigating back to page")
        self.page.get_by_role("button", name=data.page_name).click()

        self.page.wait_for_timeout(500)

    def _add_customizable_section(self, data: SEOPageData, page_num: Optional[int] = None):
        """
        Add and fill customizable section with subtitle, title, description.

        Args:
            data: SEOPageData instance
            page_num: Page number for image matching
        """
        logger.info("→ Adding customizable section...")

        self._dismiss_blocking_overlays()

        logger.debug("  Clicking 'plus Features' button...")
        features_btn = self.page.get_by_role("button", name="plus Features")
        features_btn.wait_for(state="visible", timeout=10000)
        features_btn.click()
        logger.debug("  ✓ Features button clicked")

        self.page.wait_for_timeout(500)

        logger.debug("  Selecting 'Customizable' option...")
        custom_option = self.page.get_by_text("Customizable")
        custom_option.wait_for(state="visible", timeout=10000)
        custom_option.click()
        logger.debug("  ✓ Customizable selected")

        self.page.wait_for_timeout(800)

        logger.debug("  Clicking add button for customizable block...")
        add_block_btn = self.page.locator("div:nth-child(6) > .w-full.flex > .ant-btn")
        add_block_btn.wait_for(state="visible", timeout=10000)
        add_block_btn.click()
        logger.debug("  ✓ Block added")

        self.page.wait_for_timeout(800)

        logger.debug("  Toggling visibility switch...")
        visibility_switch = self.page.get_by_role("switch", name="eye eye-invisible")
        visibility_switch.wait_for(state="visible", timeout=10000)
        visibility_switch.click()
        logger.debug("  ✓ Visibility toggled")

        self.page.wait_for_timeout(500)

        logger.debug("  Clicking edit button for customizable content...")
        edit_btn = self.page.get_by_role("button", name="edit").nth(4)
        edit_btn.wait_for(state="visible", timeout=10000)
        edit_btn.click()
        logger.debug("  ✓ Edit opened")

        self.page.wait_for_timeout(800)
        self._dismiss_blocking_overlays()

        logger.debug("  Filling Subtitle...")
        subtitle_field = self.page.get_by_role("textbox", name="Subtitle")
        subtitle_field.wait_for(state="visible", timeout=10000)
        subtitle_field.fill(data.subtitle)
        logger.debug("  ✓ Subtitle filled")

        logger.debug("  Filling Title...")
        title_field = self.page.get_by_role("textbox", name="Title", exact=True)
        title_field.wait_for(state="visible", timeout=10000)
        title_field.fill(data.title)
        logger.debug("  ✓ Title filled")

        logger.debug("  Filling Description...")
        desc_field = self.page.get_by_role("textbox", name="Description")
        desc_field.wait_for(state="visible", timeout=10000)
        desc_field.fill(data.description)
        logger.debug("  ✓ Description filled")

        # Upload image if available (Location 1: Customizable section)
        if page_num:
            image_path = self._find_image_for_page_number(page_num)
            if image_path:
                logger.info(f"  → Uploading image for Page {page_num} in Customizable section...")
                try:
                    # Locate the file upload input in Customizable section
                    upload_input = self.page.locator("input[type='file']").first
                    upload_input.set_input_files(image_path)

                    logger.debug("  Waiting for image upload to process...")
                    self.page.wait_for_timeout(2000)

                    logger.info(f"  ✓ Image uploaded in Customizable section")
                except Exception as e:
                    logger.warning(f"  Failed to upload image in Customizable section: {e}")

        logger.debug("  Clicking Save...")
        save_btn = self.page.get_by_role("button", name="Save")
        save_btn.wait_for(state="visible", timeout=10000)
        save_btn.click()
        logger.debug("  ✓ Save clicked")

        self.page.wait_for_timeout(1000)
        self._dismiss_blocking_overlays()

        logger.info("✓ Customizable section added")

    def _add_faq_section(self, data: SEOPageData):
        """
        Add FAQ section and populate with questions/answers.

        Args:
            data: SEOPageData instance
        """
        logger.info(f"→ Adding FAQ section with {len(data.faqs)} items...")

        self._dismiss_blocking_overlays()

        logger.debug("  Clicking 'plus Features' button...")
        features_btn = self.page.get_by_role("button", name="plus Features")
        features_btn.wait_for(state="visible", timeout=10000)
        features_btn.click()
        logger.debug("  ✓ Features button clicked")

        self.page.wait_for_timeout(500)

        logger.debug("  Selecting 'FAQ' option...")
        faq_option = self.page.get_by_text("FAQ")
        faq_option.wait_for(state="visible", timeout=10000)
        faq_option.click()
        logger.debug("  ✓ FAQ selected")

        self.page.wait_for_timeout(800)

        logger.debug("  Clicking plus button in Elements...")
        elements_plus = self.page.get_by_label("Elements").get_by_role("button", name="plus")
        elements_plus.wait_for(state="visible", timeout=10000)
        elements_plus.click()
        logger.debug("  ✓ Elements plus clicked")

        self.page.wait_for_timeout(800)

        logger.debug("  Toggling FAQ visibility switch...")
        faq_switch = self.page.get_by_role("button", name="appstore FAQ eye eye-").get_by_role("switch")
        faq_switch.wait_for(state="visible", timeout=10000)
        faq_switch.click()
        logger.debug("  ✓ Visibility toggled")

        self.page.wait_for_timeout(500)

        logger.debug("  Clicking edit button for FAQ...")
        edit_btn = self.page.get_by_role("button", name="edit", exact=True).nth(3)
        edit_btn.wait_for(state="visible", timeout=10000)
        edit_btn.click()
        logger.debug("  ✓ Edit opened")

        self.page.wait_for_timeout(800)

        logger.debug("  Clicking 'FAQ Items' tab...")
        faq_items_tab = self.page.get_by_role("tab", name="FAQ Items")
        faq_items_tab.wait_for(state="visible", timeout=10000)
        faq_items_tab.click()
        logger.debug("  ✓ FAQ Items tab opened")

        self.page.wait_for_timeout(800)
        self._dismiss_blocking_overlays()

        for i, faq in enumerate(data.faqs, 1):
            logger.info(f"  → Adding FAQ {i}/{len(data.faqs)}: {faq.question[:50]}...")
            self._add_single_faq(faq)
            logger.info(f"  ✓ FAQ {i}/{len(data.faqs)} added")

        self.page.wait_for_timeout(500)

        logger.debug("  Closing FAQ drawer...")
        drawer_mask = self.page.locator(".ant-drawer-mask")
        drawer_mask.wait_for(state="visible", timeout=10000)
        drawer_mask.click()
        logger.debug("  ✓ Drawer closed")

        logger.info("✓ FAQ section completed")

    def _add_single_faq(self, faq: FAQ):
        """
        Add a single FAQ item.

        Args:
            faq: FAQ instance
        """
        self.page.wait_for_timeout(500)
        self._dismiss_blocking_overlays()

        logger.debug("    Clicking 'plus Add' button...")
        add_button = self.page.get_by_role("button", name="plus Add")
        add_button.wait_for(state="visible", timeout=10000)
        add_button.click()
        logger.debug("    ✓ Add clicked")

        self.page.wait_for_timeout(800)

        logger.debug("    Filling FAQ Title (question)...")
        title_field = self.page.get_by_role("textbox", name="Title :")
        title_field.wait_for(state="visible", timeout=10000)
        title_field.fill(faq.question)
        logger.debug("    ✓ Question filled")

        logger.debug("    Filling FAQ Description (answer)...")
        desc_field = self.page.get_by_role("textbox", name="Description :")
        desc_field.wait_for(state="visible", timeout=10000)
        desc_field.fill(faq.answer)
        logger.debug("    ✓ Answer filled")

        logger.debug("    Clicking Save...")
        save_btn = self.page.get_by_label("FAQ Item", exact=True).get_by_role("button", name="Save")
        save_btn.wait_for(state="visible", timeout=10000)
        save_btn.click()
        logger.debug("    ✓ Save clicked")

        self.page.wait_for_timeout(1000)

        # Try to close dialog if it's still open
        try:
            logger.debug("    Checking for dialog close button...")
            close_button = self.page.get_by_role("dialog", name="FAQ Item").get_by_label("Close", exact=True)
            if close_button.is_visible(timeout=2000):
                logger.debug("    Closing dialog...")
                close_button.click()
                self.page.wait_for_timeout(500)
                logger.debug("    ✓ Dialog closed")
        except:
            logger.debug("    (No dialog to close)")

    def _submit_page(self):
        """Submit/publish the page."""
        logger.debug("Submitting page")

        logger.info("Page configuration complete - review and submit manually if needed")

    def take_screenshot(self, filename: str):
        """
        Take a screenshot for debugging.

        Args:
            filename: Path to save screenshot
        """
        if self.page:
            screenshot_path = Path("logs") / filename
            screenshot_path.parent.mkdir(exist_ok=True)
            self.page.screenshot(path=str(screenshot_path))
            logger.info(f"Screenshot saved: {screenshot_path}")

    def create_page_from_data(self, data: SEOPageData) -> bool:
        """
        Complete workflow to create SEO page from parsed data.

        Args:
            data: SEOPageData instance

        Returns:
            True if successful, False otherwise
        """
        try:
            missing_fields = data.validate()
            if missing_fields:
                logger.error(f"Invalid data: missing fields {missing_fields}")
                return False

            self.start_browser()
            self.login()
            self.select_restaurant()
            self.open_storefront_editor()
            self.create_seo_page(data)

            return True

        except Exception as e:
            logger.error(f"Failed to create page: {e}", exc_info=True)

            if self.config.screenshot_on_error:
                self.take_screenshot(f"error_{data.page_name}.png")

            return False

        finally:
            self.close()
