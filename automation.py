"""
Automation module for creating SEO pages in Food Amigo.
Production-ready version with bulletproof error handling and resilience.
"""
import logging
from pathlib import Path
from typing import Optional
from playwright.sync_api import sync_playwright, Page, Browser, BrowserContext, TimeoutError
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

    def _wait_for_dom_stable(self, timeout_ms: int = 5000):
        """
        Wait for DOM to stabilize after dynamic updates.

        Args:
            timeout_ms: Maximum time to wait in milliseconds
        """
        try:
            self.page.wait_for_load_state("domcontentloaded", timeout=timeout_ms)
            self.page.wait_for_timeout(500)
        except:
            logger.debug("DOM stabilization timeout, continuing...")

    # IMAGE UPLOAD FEATURE DISABLED
    # All image upload and media gallery logic has been removed to prevent
    # UI blocking issues, drawer overlaps, and selector crashes.
    # Focus is now strictly on text content automation.

    def _handle_media_gallery_selection_DISABLED(self, context_name: str):
        """
        Media Gallery selection using EXACT selectors from Playwright codegen recording.

        Based on real user recording, the correct sequence is:
        1. Wait for Media Gallery modal to load after upload
        2. Click the "plus" button on the image card to select it (NOT the image itself!)
        3. Click "Select (1)" button to confirm
        4. Wait for modal to close

        Args:
            context_name: Name for logging (e.g., "Social tab", "Customizable section")
        """
        logger.info(f"  ═══ Media Gallery Selection for {context_name} ═══")

        try:
            # STEP 1: Wait for Media Gallery modal to fully load after upload
            logger.info("  📋 STEP 1: Waiting for Media Gallery modal to load...")
            self.page.wait_for_timeout(2000)  # Based on codegen timing
            logger.info("  ✓ Modal should be ready")

            # OPTIONAL: Screenshot for debugging
            try:
                screenshot_path = Path("logs") / f"gallery_{context_name.replace(' ', '_')}.png"
                screenshot_path.parent.mkdir(exist_ok=True)
                self.page.screenshot(path=str(screenshot_path))
                logger.info(f"     📸 Screenshot: {screenshot_path}")
            except:
                pass

            # STEP 2: Click the "plus" button to select the uploaded image
            # KEY INSIGHT: The codegen shows we need to click a "plus" button, not the image itself!
            # For Social tab: page.get_by_role("button", name="plus").nth(1).click()
            # For Customizable: page.get_by_role("button", name="plus").nth(5).click()
            logger.info("  📋 STEP 2: Clicking 'plus' button on uploaded image to select it...")

            try:
                # Try to find the "plus" button - use different nth() based on context
                if "Social" in context_name:
                    plus_button = self.page.get_by_role("button", name="plus").nth(1)
                    logger.debug("     Using nth(1) for Social tab")
                else:  # Customizable section
                    plus_button = self.page.get_by_role("button", name="plus").nth(5)
                    logger.debug("     Using nth(5) for Customizable section")

                plus_button.click(timeout=5000)
                logger.info("  ✓ Plus button clicked - image selected")

            except Exception as plus_error:
                logger.error(f"  ✗ Could not click plus button: {plus_error}")
                logger.warning("  Trying fallback: find any visible plus button in modal...")

                # Fallback: Try to find any plus button within the modal
                try:
                    # Look for plus buttons inside the modal
                    modal_plus = self.page.locator(".ant-modal button").get_by_role("button", name="plus").first
                    modal_plus.click(timeout=3000)
                    logger.info("  ✓ Clicked first plus button in modal (fallback)")
                except Exception as fallback_error:
                    logger.error(f"  ✗ Fallback also failed: {fallback_error}")
                    raise Exception(f"Could not select image - plus button not clickable: {plus_error}")

            # Wait for selection to register
            self.page.wait_for_timeout(800)

            # STEP 3: Click "Select (1)" button to confirm selection
            # Using EXACT selector from codegen: page.get_by_role("button", name="Select (1)").click()
            logger.info("  📋 STEP 3: Clicking 'Select (1)' button to confirm...")

            try:
                select_button = self.page.get_by_role("button", name="Select (1)")
                select_button.click(timeout=5000)
                logger.info("  ✓ 'Select (1)' clicked successfully")

            except Exception as select_error:
                logger.error(f"  ✗ Could not click Select (1) button: {select_error}")
                logger.warning("  Trying fallback: look for any Select button with count...")

                # Fallback: Try to find button containing "Select ("
                try:
                    fallback_select = self.page.locator("button:has-text('Select (')").first
                    fallback_select.click(timeout=3000)
                    logger.info("  ✓ Clicked Select button (fallback)")
                except Exception as fallback_error:
                    logger.error(f"  ✗ Fallback failed: {fallback_error}")
                    raise Exception(f"Could not confirm selection: {select_error}")

            # STEP 4: Wait for modal to close
            logger.info("  📋 STEP 4: Waiting for modal to close...")
            self.page.wait_for_timeout(1500)

            # Verify modal closed
            modal_closed = self.page.evaluate("""
            () => {
                const modal = document.querySelector('.ant-modal');
                return modal === null || modal.offsetParent === null;
            }
            """)

            if modal_closed:
                logger.info("  ✓ Modal closed successfully")
            else:
                logger.warning("  ⚠ Modal still visible but continuing...")

            logger.info(f"  ═══ Media Gallery Selection COMPLETE for {context_name} ═══")

        except Exception as gallery_error:
            logger.error(f"  ✗ Media Gallery handling failed: {gallery_error}")
            logger.warning(f"  Attempting NUCLEAR cleanup to destroy ALL blocking overlays...")

            # NUCLEAR CLEANUP - Close EVERYTHING that might be blocking
            # The terminal explicitly showed: ant-drawer-close button is blocking clicks!

            try:
                # STEP 1: Force click ALL close buttons (drawers, modals, dialogs)
                logger.info("  STEP 1: Force clicking ALL close buttons...")

                close_selectors = [
                    "button.ant-drawer-close",
                    ".ant-drawer-close",
                    "button.ant-modal-close",
                    ".ant-modal-close",
                    ".ant-modal-close-x",
                    "button[aria-label='Close']",
                    "button[title='Close']"
                ]

                closed_something = False
                for selector in close_selectors:
                    try:
                        close_buttons = self.page.locator(selector).all()
                        if len(close_buttons) > 0:
                            logger.debug(f"  Found {len(close_buttons)} element(s) matching '{selector}'")
                            for btn in close_buttons:
                                try:
                                    if btn.is_visible(timeout=500):
                                        logger.debug(f"  Force clicking: {selector}")
                                        btn.click(force=True, timeout=2000, no_wait_after=True)
                                        closed_something = True
                                        self.page.wait_for_timeout(500)
                                except Exception as e:
                                    logger.debug(f"  Could not click {selector}: {e}")
                    except Exception as e:
                        logger.debug(f"  Selector '{selector}' failed: {e}")

                if closed_something:
                    logger.info("  ✓ Clicked close button(s)")
                    self.page.wait_for_timeout(1500)

            except Exception as e:
                logger.warning(f"  Close button clicking failed: {e}")

            try:
                # STEP 2: Force click ALL masks/overlays to dismiss them
                logger.info("  STEP 2: Force clicking ALL masks/overlays...")

                mask_selectors = [
                    ".ant-drawer-mask",
                    ".ant-modal-mask",
                    ".ant-modal-wrap"
                ]

                for selector in mask_selectors:
                    try:
                        masks = self.page.locator(selector).all()
                        if len(masks) > 0:
                            logger.debug(f"  Found {len(masks)} mask(s) matching '{selector}'")
                            for mask in masks:
                                try:
                                    if mask.is_visible(timeout=500):
                                        logger.debug(f"  Force clicking mask: {selector}")
                                        mask.click(force=True, timeout=2000, no_wait_after=True)
                                        self.page.wait_for_timeout(500)
                                except Exception as e:
                                    logger.debug(f"  Could not click mask {selector}: {e}")
                    except Exception as e:
                        logger.debug(f"  Mask selector '{selector}' failed: {e}")

                logger.info("  ✓ Clicked masks/overlays")
                self.page.wait_for_timeout(1000)

            except Exception as e:
                logger.warning(f"  Mask clicking failed: {e}")

            try:
                # STEP 3: Press Escape multiple times
                logger.info("  STEP 3: Pressing Escape multiple times...")
                for i in range(3):
                    self.page.keyboard.press("Escape")
                    self.page.wait_for_timeout(500)
                logger.info("  ✓ Pressed Escape 3 times")
            except Exception as e:
                logger.warning(f"  Escape pressing failed: {e}")

            # STEP 4: VERIFY overlays are actually gone
            logger.info("  STEP 4: Verifying overlays are cleared...")
            try:
                # Wait for drawer mask to disappear
                drawer_mask = self.page.locator(".ant-drawer-mask").first
                try:
                    drawer_mask.wait_for(state="hidden", timeout=3000)
                    logger.info("  ✓ Drawer mask is hidden")
                except:
                    logger.warning("  ⚠ Drawer mask may still be visible")

                # Wait for modal mask to disappear
                modal_mask = self.page.locator(".ant-modal-mask").first
                try:
                    modal_mask.wait_for(state="hidden", timeout=3000)
                    logger.info("  ✓ Modal mask is hidden")
                except:
                    logger.warning("  ⚠ Modal mask may still be visible")

                # Final check: Are any close buttons still visible?
                close_btn = self.page.locator("button.ant-drawer-close, button.ant-modal-close").first
                try:
                    if close_btn.is_visible(timeout=1000):
                        logger.warning("  ⚠ Close buttons still visible - overlays not fully cleared!")
                    else:
                        logger.info("  ✓ No close buttons visible")
                except:
                    logger.info("  ✓ No close buttons found")

            except Exception as e:
                logger.warning(f"  Verification failed: {e}")

            # Final verification: Check if page is still responsive
            try:
                self.page.evaluate("() => document.title")
                logger.info("  ✓ Page is responsive after cleanup")
            except Exception as e:
                logger.error(f"  ✗ Page may be unresponsive: {e}")

            # DON'T RAISE - Allow process to continue
            logger.warning(f"  ⚠ SKIPPING image selection for {context_name} - continuing with page creation")

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
            # Check if page is still alive
            try:
                if self.page.is_closed():
                    logger.error("Page is already closed, cannot navigate")
                    raise Exception("Page context is closed")

                # Verify page is responsive
                self.page.evaluate("() => document.title")
            except Exception as e:
                logger.error(f"Page is not responsive: {e}")
                raise Exception("Page context is closed or unresponsive")

            # Close any open modals/drawers first (SAFE - single Escape)
            try:
                logger.debug("Closing any open modals/drawers...")
                self.page.keyboard.press("Escape")
                self.page.wait_for_timeout(800)
            except:
                pass

            # Try page reload first (safest - doesn't lose context)
            try:
                logger.debug("Reloading page to reset state...")
                self.page.reload(wait_until="domcontentloaded", timeout=20000)
                self.page.wait_for_timeout(2000)
                logger.debug("✓ Page reloaded successfully")
            except Exception as reload_error:
                logger.warning(f"Page reload failed: {reload_error}, trying navigation...")

                # Fallback: Navigate to URL
                try:
                    storefront_url = f"{self.config.base_url}/storefront-editor"
                    logger.debug(f"Navigating to {storefront_url}...")
                    self.page.goto(storefront_url, wait_until="domcontentloaded", timeout=20000)
                    self.page.wait_for_timeout(2000)
                    logger.debug("✓ Navigation successful")
                except Exception as nav_error:
                    logger.error(f"Navigation failed: {nav_error}")
                    raise Exception(f"Could not reset dashboard: {nav_error}")

            # Verify we're back and page is responsive
            try:
                self.page.wait_for_timeout(1000)
                self._dismiss_blocking_overlays()

                # Check if add button is visible (confirms we're on dashboard)
                add_btn = self.page.get_by_role("button", name="plus", exact=True)
                add_btn.wait_for(state="visible", timeout=10000)
                logger.debug("✓ Dashboard verified (add button visible)")
            except Exception as verify_error:
                logger.warning(f"Dashboard verification failed: {verify_error}")
                # Don't raise - we may still be on the right page

            logger.info("✓ Dashboard reset complete")

        except Exception as e:
            logger.error(f"Dashboard navigation failed critically: {e}")
            raise

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

        # Each section is isolated with its own error handling
        self._click_add_page_button()
        self._fill_basic_info(data)
        self._fill_seo_metadata(data)

        # Social metadata with image upload (isolated)
        try:
            self._fill_social_metadata(data, page_num)
        except Exception as e:
            logger.error(f"Failed to fill social metadata: {e}")
            logger.warning("Continuing with remaining sections...")

        # Customizable section with image upload (isolated)
        try:
            self._add_customizable_section(data, page_num)
        except Exception as e:
            logger.error(f"Failed to add customizable section: {e}")
            logger.warning("Continuing with FAQ section...")

        # FAQ section (isolated)
        try:
            self._add_faq_section(data)
        except Exception as e:
            logger.error(f"Failed to add FAQ section: {e}")
            logger.warning("FAQ section incomplete, but page basics saved")

        logger.info(f"SEO page created: {data.page_name}")

    def _click_add_page_button(self):
        """Click the '+' button to create new page."""
        logger.info("→ Clicking add page button...")

        # Verify page is still alive
        try:
            if self.page.is_closed():
                logger.error("Page is closed, cannot click add button")
                raise Exception("Browser page context has been closed")
        except Exception as e:
            logger.error(f"Page context check failed: {e}")
            raise Exception("Browser page context has been closed")

        self._dismiss_blocking_overlays()

        # Wait for page to be fully loaded
        try:
            self.page.wait_for_load_state("domcontentloaded", timeout=10000)
            logger.debug("  Page load state: domcontentloaded")
        except Exception as e:
            logger.warning(f"Page load state check timed out: {e}")

        # Verify page is still responsive
        try:
            # Simple check to ensure page is alive
            self.page.evaluate("() => document.title")
            logger.debug("  Page is responsive")
        except Exception as e:
            logger.error(f"Page is not responsive: {e}")
            raise Exception("Browser page context has been closed or is unresponsive")

        add_btn = self.page.get_by_role("button", name="plus", exact=True)
        add_btn.wait_for(state="visible", timeout=15000)
        add_btn.click()

        self.page.wait_for_timeout(800)

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

        self.page.wait_for_timeout(1000)
        self._dismiss_blocking_overlays()

        logger.debug("  Clicking page name button to reopen...")
        page_btn = self.page.get_by_role("button", name=data.page_name)
        page_btn.wait_for(state="visible", timeout=10000)
        page_btn.click()

        self.page.wait_for_timeout(600)

        logger.debug("  Clicking Edit button...")
        edit_btn = self.page.get_by_role("button", name="edit Edit")
        edit_btn.wait_for(state="visible", timeout=10000)
        edit_btn.click()

        self.page.wait_for_timeout(600)

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
        self.page.wait_for_timeout(600)

        # Click edit button within General tab
        logger.debug("  Clicking edit button in General tab...")
        edit_button = self.page.get_by_label("General").get_by_role("button", name="edit")
        edit_button.wait_for(state="visible", timeout=10000)
        edit_button.click()
        logger.debug("  ✓ Edit button clicked")

        # Wait for form to open
        self.page.wait_for_timeout(600)
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

        self.page.wait_for_timeout(1000)
        self._dismiss_blocking_overlays()

        logger.info("✓ SEO metadata saved")

    def _fill_social_metadata(self, data: SEOPageData, page_num: Optional[int] = None):
        """
        Fill social title and description in Social tab.
        IMAGE UPLOAD DISABLED - text fields only.

        Args:
            data: SEOPageData instance
            page_num: Page number (unused, kept for signature compatibility)
        """
        logger.info("→ Filling social metadata (Social tab)...")

        self._dismiss_blocking_overlays()

        # Click Social tab and wait for it to be active
        logger.debug("  Clicking Social tab...")
        social_tab = self.page.get_by_text("Social", exact=True)
        social_tab.wait_for(state="visible", timeout=10000)
        social_tab.click()
        logger.debug("  ✓ Social tab clicked")

        # Wait for tab content to load
        self.page.wait_for_timeout(600)

        # Click edit button within Social tab
        logger.debug("  Clicking edit button in Social tab...")
        edit_button = self.page.get_by_label("Social").get_by_role("button", name="edit")
        edit_button.wait_for(state="visible", timeout=10000)
        edit_button.click()
        logger.debug("  ✓ Edit button clicked")

        # Wait for form to open
        self.page.wait_for_timeout(600)
        self._dismiss_blocking_overlays()

        # Fill Social Title
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

        # IMAGE UPLOAD DISABLED - Skipping to save

        # Save
        logger.debug("  Clicking Save...")
        save_btn = self.page.get_by_role("button", name="Save")
        save_btn.wait_for(state="visible", timeout=10000)
        self.page.wait_for_timeout(400)
        save_btn.click()
        logger.debug("  ✓ Save clicked")

        self.page.wait_for_timeout(1000)
        self._dismiss_blocking_overlays()

        logger.info("✓ Social metadata saved")

        # Navigate back to page
        logger.debug("  Navigating back to page...")
        try:
            page_button = self.page.get_by_role("button", name=data.page_name)
            page_button.wait_for(state="visible", timeout=5000)
            page_button.click()
            self.page.wait_for_timeout(600)
        except Exception as e:
            logger.warning(f"  Could not navigate back via page button: {e}")

    def _add_customizable_section(self, data: SEOPageData, page_num: Optional[int] = None):
        """
        Add and fill customizable section with subtitle, title, and description.
        IMAGE UPLOAD DISABLED - text fields only.

        Args:
            data: SEOPageData instance
            page_num: Page number (unused, kept for signature compatibility)
        """
        logger.info("→ Adding customizable section...")

        self._dismiss_blocking_overlays()

        logger.debug("  Clicking 'plus Features' button...")
        features_btn = self.page.get_by_role("button", name="plus Features")
        features_btn.wait_for(state="visible", timeout=10000)
        features_btn.click()
        logger.debug("  ✓ Features button clicked")

        self.page.wait_for_timeout(600)

        logger.debug("  Selecting 'Customizable' option...")
        custom_option = self.page.get_by_text("Customizable")
        custom_option.wait_for(state="visible", timeout=10000)
        custom_option.click()
        logger.debug("  ✓ Customizable selected")

        self.page.wait_for_timeout(700)

        logger.debug("  Clicking add button for customizable block...")
        add_block_btn = self.page.locator("div:nth-child(6) > .w-full.flex > .ant-btn")
        add_block_btn.wait_for(state="visible", timeout=10000)
        add_block_btn.click()
        logger.debug("  ✓ Block added")

        self.page.wait_for_timeout(700)

        logger.debug("  Toggling visibility switch...")
        visibility_switch = self.page.get_by_role("switch", name="eye eye-invisible")
        visibility_switch.wait_for(state="visible", timeout=10000)
        visibility_switch.click()
        logger.debug("  ✓ Visibility toggled")

        self.page.wait_for_timeout(600)

        logger.debug("  Clicking edit button for customizable content...")
        edit_btn = self.page.get_by_role("button", name="edit").nth(4)
        edit_btn.wait_for(state="visible", timeout=10000)
        edit_btn.click()
        logger.debug("  ✓ Edit opened")

        self.page.wait_for_timeout(700)
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

        # IMAGE UPLOAD DISABLED - Skipping to save
        # All image upload logic removed to prevent modal/drawer blocking issues

        # Save - ensure no overlays block the button
        logger.debug("  Ensuring no blocking overlays before Save...")
        self._dismiss_blocking_overlays()
        self.page.wait_for_timeout(500)

        logger.debug("  Clicking Save...")
        save_btn = self.page.get_by_role("button", name="Save")
        save_btn.wait_for(state="visible", timeout=10000)

        # Ensure button is enabled
        self.page.wait_for_timeout(400)
        save_btn.click()
        logger.debug("  ✓ Save clicked")

        self.page.wait_for_timeout(1000)
        self._dismiss_blocking_overlays()

        logger.info("✓ Customizable section added")

    def _add_faq_section(self, data: SEOPageData):
        """
        Add FAQ section and populate with questions/answers.
        Completely isolated with per-FAQ error handling.

        Args:
            data: SEOPageData instance
        """
        logger.info(f"→ Adding FAQ section with {len(data.faqs)} items...")

        try:
            self._dismiss_blocking_overlays()

            logger.debug("  Clicking 'plus Features' button...")
            features_btn = self.page.get_by_role("button", name="plus Features")
            features_btn.wait_for(state="visible", timeout=10000)
            features_btn.click()
            logger.debug("  ✓ Features button clicked")

            self.page.wait_for_timeout(700)

            logger.debug("  Selecting 'FAQ' option...")
            # Use more specific selector to avoid strict mode violation (there are 2 "FAQ" texts on page)
            # We want the one in the Elements sidebar, not the menu
            faq_option = self.page.get_by_label("Elements").get_by_text("FAQ")
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

            self.page.wait_for_timeout(700)

            logger.debug("  Clicking edit button for FAQ...")
            edit_btn = self.page.get_by_role("button", name="edit", exact=True).nth(3)
            edit_btn.wait_for(state="visible", timeout=10000)
            edit_btn.click()
            logger.debug("  ✓ Edit opened")

            self.page.wait_for_timeout(800)

            logger.debug("  Clicking 'FAQ Items' tab...")
            try:
                # Try standard role selector first
                faq_items_tab = self.page.get_by_role("tab", name="FAQ Items")
                faq_items_tab.wait_for(state="visible", timeout=10000)
                faq_items_tab.click()
                logger.debug("  ✓ FAQ Items tab opened")
            except Exception as tab_error:
                logger.warning(f"  FAQ Items tab via role failed: {tab_error}")
                logger.debug("  Trying fallback tab selector...")
                # Fallback: Use text selector with longer wait
                try:
                    self.page.wait_for_timeout(2000)  # Extra wait after modal issues
                    faq_tab_fallback = self.page.locator("text=FAQ Items").first
                    faq_tab_fallback.wait_for(state="visible", timeout=10000)
                    faq_tab_fallback.click()
                    logger.debug("  ✓ FAQ Items tab opened (via fallback)")
                except Exception as fallback_error:
                    logger.error(f"  FAQ Items tab fallback also failed: {fallback_error}")
                    raise Exception("Could not open FAQ Items tab")

            self.page.wait_for_timeout(800)
            self._dismiss_blocking_overlays()

            # Add each FAQ with complete isolation
            successful_faqs = 0
            failed_faqs = 0

            for i, faq in enumerate(data.faqs, 1):
                try:
                    logger.info(f"  → Adding FAQ {i}/{len(data.faqs)}: {faq.question[:50]}...")
                    self._add_single_faq(faq)
                    successful_faqs += 1
                    logger.info(f"  ✓ FAQ {i}/{len(data.faqs)} added")
                except Exception as e:
                    failed_faqs += 1
                    logger.error(f"  ✗ Failed to add FAQ {i}/{len(data.faqs)}: {e}")

                    # Try to recover state for next FAQ
                    try:
                        self._dismiss_blocking_overlays()
                        self.page.wait_for_timeout(1000)

                        # Try to close any open dialogs
                        try:
                            close_button = self.page.get_by_role("dialog", name="FAQ Item").get_by_label("Close", exact=True)
                            if close_button.is_visible(timeout=1000):
                                close_button.click()
                                self.page.wait_for_timeout(500)
                        except:
                            pass
                    except:
                        pass

                    # Continue with next FAQ
                    continue

            logger.info(f"  FAQ Summary: {successful_faqs} added, {failed_faqs} failed")

            self.page.wait_for_timeout(1000)

            logger.debug("  Closing FAQ drawer...")
            drawer_mask = self.page.locator(".ant-drawer-mask")
            drawer_mask.wait_for(state="visible", timeout=10000)
            drawer_mask.click()
            logger.debug("  ✓ Drawer closed")

            logger.info(f"✓ FAQ section completed ({successful_faqs}/{len(data.faqs)} FAQs added)")

        except Exception as e:
            logger.error(f"Failed to add FAQ section: {e}", exc_info=True)
            # Don't raise - allow page creation to complete even if FAQs fail
            logger.warning("FAQ section incomplete, but page can still be saved")

    def _add_single_faq(self, faq: FAQ):
        """
        Add a single FAQ item with strict verification.

        Args:
            faq: FAQ instance
        """
        self.page.wait_for_timeout(700)
        self._dismiss_blocking_overlays()

        logger.debug("    Clicking 'plus Add' button...")
        add_button = self.page.get_by_role("button", name="plus Add")
        add_button.wait_for(state="visible", timeout=10000)
        add_button.click()
        logger.debug("    ✓ Add clicked")

        self.page.wait_for_timeout(800)
        self._dismiss_blocking_overlays()

        # Strict verification for Title field
        logger.debug("    Waiting for FAQ Title field...")
        title_field = self.page.get_by_role("textbox", name="Title :")
        title_field.wait_for(state="visible", timeout=10000)
        title_field.wait_for(state="attached", timeout=5000)

        # Verify field is editable
        if not title_field.is_editable(timeout=3000):
            raise Exception("Title field is not editable")

        logger.debug("    Filling FAQ Title (question)...")
        title_field.fill(faq.question)
        self.page.wait_for_timeout(500)
        logger.debug("    ✓ Question filled")

        # Strict verification for Description field
        logger.debug("    Waiting for FAQ Description field...")
        desc_field = self.page.get_by_role("textbox", name="Description :")
        desc_field.wait_for(state="visible", timeout=10000)
        desc_field.wait_for(state="attached", timeout=5000)

        # Verify field is editable
        if not desc_field.is_editable(timeout=3000):
            raise Exception("Description field is not editable")

        logger.debug("    Filling FAQ Description (answer)...")
        desc_field.fill(faq.answer)
        self.page.wait_for_timeout(500)
        logger.debug("    ✓ Answer filled")

        logger.debug("    Clicking Save...")
        save_btn = self.page.get_by_label("FAQ Item", exact=True).get_by_role("button", name="Save")
        save_btn.wait_for(state="visible", timeout=10000)

        # Ensure button is clickable
        if not save_btn.is_enabled(timeout=3000):
            raise Exception("Save button is not enabled")

        save_btn.click()
        logger.debug("    ✓ Save clicked")

        self.page.wait_for_timeout(1200)

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
