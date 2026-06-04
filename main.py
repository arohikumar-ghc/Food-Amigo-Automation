"""
Main entry point for Food Amigo SEO page automation.
Supports both single-page and multi-page Word documents.
Production-ready version with bulletproof error handling.
"""
import sys
from pathlib import Path
from config import AutomationConfig
from parser import parse_seo_document_all
from automation import FoodAmigoAutomation
from utils import setup_logging, get_docx_files, ProgressTracker


def process_single_file(doc_path: str, config: AutomationConfig) -> dict:
    """
    Process a single Word document and create all SEO pages within it.

    Args:
        doc_path: Path to .docx file
        config: AutomationConfig instance

    Returns:
        Dictionary with results: {"total": int, "success": int, "failed": int, "pages": [...]}
    """
    logger = setup_logging(log_dir=config.logs_dir)

    # Ensure images directory exists
    images_dir = Path("images")
    images_dir.mkdir(exist_ok=True)
    logger.info(f"Images directory ready: {images_dir.absolute()}")

    logger.info("=" * 80)
    logger.info(f"Processing: {doc_path}")
    logger.info("=" * 80)

    try:
        logger.info("Parsing Word document...")
        pages = parse_seo_document_all(doc_path)

        logger.info(f"Found {len(pages)} page(s) in document")

        success_count = 0
        failed_count = 0
        partial_count = 0
        results = []

        # Start automation once for all pages
        automation = FoodAmigoAutomation(config)

        try:
            automation.start_browser()
            automation.login()
            automation.select_restaurant()
            automation.open_storefront_editor()

            # Process each page
            for page_num, page_data in enumerate(pages, 1):
                logger.info(f"\n{'=' * 80}")
                logger.info(f"PROCESSING PAGE {page_num} OF {len(pages)}")
                logger.info(f"Page Name: {page_data.page_name}")
                logger.info("=" * 80)

                logger.info(f"  - Href: {page_data.href}")
                logger.info(f"  - SEO Title: {page_data.seo_title}")
                logger.info(f"  - FAQs: {len(page_data.faqs)} items")

                # Validate
                missing = page_data.validate()
                if missing:
                    logger.error(f"Validation failed for page {page_num}. Missing fields: {missing}")
                    failed_count += 1
                    results.append({
                        "page_name": page_data.page_name,
                        "success": False,
                        "partial": False,
                        "error": f"Missing fields: {missing}"
                    })
                    continue

                # Create page
                try:
                    # Navigate back to dashboard before processing each page (except first)
                    if page_num > 1:
                        try:
                            automation.navigate_to_dashboard()
                        except Exception as e:
                            logger.warning(f"Dashboard navigation failed: {e}, continuing anyway...")

                    logger.info(f"Creating SEO page {page_num}...")

                    # create_seo_page now returns status: "success", "partial", or "failed"
                    status = automation.create_seo_page(page_data, page_num=page_num)

                    if status == "success":
                        logger.info(f"SUCCESS: Page {page_num} created - {page_data.page_name}")
                        success_count += 1
                        results.append({
                            "page_name": page_data.page_name,
                            "success": True,
                            "partial": False,
                            "error": None
                        })
                    elif status == "partial":
                        logger.warning(f"PARTIAL SUCCESS: Page {page_num} created with some sections incomplete - {page_data.page_name}")
                        partial_count += 1
                        results.append({
                            "page_name": page_data.page_name,
                            "success": True,
                            "partial": True,
                            "error": "Some sections incomplete (see logs)"
                        })
                    else:  # "failed"
                        logger.error(f"FAILED: Page {page_num} - {page_data.page_name}")
                        failed_count += 1
                        results.append({
                            "page_name": page_data.page_name,
                            "success": False,
                            "partial": False,
                            "error": "Page creation failed (see logs)"
                        })

                except Exception as e:
                    logger.error(f"FAILED: Page {page_num} - {page_data.page_name}: {e}", exc_info=True)
                    failed_count += 1
                    results.append({
                        "page_name": page_data.page_name,
                        "success": False,
                        "partial": False,
                        "error": str(e)
                    })

                    if config.screenshot_on_error:
                        try:
                            automation.take_screenshot(f"error_page{page_num}_{page_data.page_name[:30]}.png")
                        except:
                            logger.warning("Could not take error screenshot")

        finally:
            try:
                automation.close()
            except Exception as e:
                logger.warning(f"Error closing browser: {e}")

        logger.info(f"\n{'=' * 80}")
        logger.info(f"DOCUMENT PROCESSING COMPLETE")
        logger.info(f"Total pages: {len(pages)}")
        logger.info(f"Success: {success_count}")
        logger.info(f"Partial: {partial_count}")
        logger.info(f"Failed: {failed_count}")
        logger.info("=" * 80)

        return {
            "total": len(pages),
            "success": success_count,
            "partial": partial_count,
            "failed": failed_count,
            "pages": results
        }

    except Exception as e:
        logger.error(f"Error processing {doc_path}: {e}", exc_info=True)
        return {
            "total": 0,
            "success": 0,
            "partial": 0,
            "failed": 0,
            "pages": [],
            "error": str(e)
        }


def process_batch(seo_files_dir: str, config: AutomationConfig) -> dict:
    """
    Process all Word documents in the SEO files directory.

    Each document can contain multiple pages.

    Args:
        seo_files_dir: Directory containing .docx files
        config: AutomationConfig instance

    Returns:
        Dictionary with success/failure counts and lists
    """
    logger = setup_logging(log_dir=config.logs_dir)

    logger.info("=" * 80)
    logger.info("BATCH PROCESSING MODE")
    logger.info("=" * 80)

    docx_files = get_docx_files(seo_files_dir)

    if not docx_files:
        logger.warning(f"No .docx files found in {seo_files_dir}")
        return {
            "total_files": 0,
            "total_pages": 0,
            "success": 0,
            "partial": 0,
            "failed": 0,
            "files": []
        }

    logger.info(f"Found {len(docx_files)} document(s) to process")

    tracker = ProgressTracker(len(docx_files), "Processing documents")

    total_pages = 0
    total_success = 0
    total_partial = 0
    total_failed = 0
    file_results = []

    for doc_path in docx_files:
        logger.info(f"\n{tracker.get_progress_message()}")

        result = process_single_file(str(doc_path), config)

        total_pages += result.get("total", 0)
        total_success += result.get("success", 0)
        total_partial += result.get("partial", 0)
        total_failed += result.get("failed", 0)

        file_results.append({
            "file": doc_path.name,
            "pages": result.get("total", 0),
            "success": result.get("success", 0),
            "partial": result.get("partial", 0),
            "failed": result.get("failed", 0),
            "details": result.get("pages", [])
        })

        tracker.update()

    logger.info("\n" + "=" * 80)
    logger.info("BATCH PROCESSING SUMMARY")
    logger.info("=" * 80)
    logger.info(tracker.get_summary())
    logger.info(f"Files processed: {len(docx_files)}")
    logger.info(f"Total pages: {total_pages}")
    logger.info(f"Success: {total_success}")
    logger.info(f"Partial: {total_partial}")
    logger.info(f"Failed: {total_failed}")

    logger.info("\n" + "-" * 80)
    logger.info("FILE BREAKDOWN")
    logger.info("-" * 80)

    for file_result in file_results:
        logger.info(f"\n{file_result['file']}:")
        logger.info(f"  Pages: {file_result['pages']}")
        logger.info(f"  Success: {file_result['success']}")
        logger.info(f"  Partial: {file_result['partial']}")
        logger.info(f"  Failed: {file_result['failed']}")

        if file_result['details']:
            for page in file_result['details']:
                if page['success']:
                    if page.get('partial'):
                        status = "[PARTIAL]"
                    else:
                        status = "[OK]"
                else:
                    status = "[FAIL]"

                logger.info(f"    {status} {page['page_name']}")

                if not page['success'] or page.get('partial'):
                    error = page.get('error', 'Unknown error')
                    logger.info(f"      Note: {error}")

    return {
        "total_files": len(docx_files),
        "total_pages": total_pages,
        "success": total_success,
        "partial": total_partial,
        "failed": total_failed,
        "files": file_results
    }


def main():
    """Main entry point."""
    print("Food Amigo SEO Page Automation")
    print("=" * 80)
    print("Multi-page document support enabled")
    print("Image upload feature enabled (bulletproof mode)")
    print("=" * 80)

    try:
        config = AutomationConfig.from_env()
    except ValueError as e:
        print(f"\nError: {e}")
        print("\nPlease set the required environment variables:")
        print("  - FOODAMIGO_EMAIL")
        print("  - FOODAMIGO_PASSWORD")
        print("  - FOODAMIGO_RESTAURANT")
        print("\nOr create a .env file (see .env.example)")
        sys.exit(1)

    validation_errors = config.validate()
    if validation_errors:
        print("\nConfiguration errors:")
        for error in validation_errors:
            print(f"  - {error}")
        sys.exit(1)

    print(f"\nConfiguration loaded:")
    print(f"  Email: {config.email}")
    print(f"  Restaurant: {config.restaurant_name}")
    print(f"  SEO Files Dir: {config.seo_files_dir}")
    print(f"  Headless: {config.headless}")

    if len(sys.argv) > 1:
        doc_path = sys.argv[1]
        print(f"\nSingle file mode: {doc_path}")
        print("(Will process ALL pages within the file)")
        print("(Partial success = page created but some sections incomplete)\n")

        result = process_single_file(doc_path, config)

        print("\n" + "=" * 80)
        print("RESULT")
        print("=" * 80)
        print(f"Total pages in document: {result.get('total', 0)}")
        print(f"Successfully created: {result.get('success', 0)}")
        print(f"Partially created: {result.get('partial', 0)}")
        print(f"Failed: {result.get('failed', 0)}")

        if result.get('pages'):
            print("\nPage details:")
            for page in result['pages']:
                if page['success']:
                    if page.get('partial'):
                        status = "[PARTIAL]"
                    else:
                        status = "[OK]"
                else:
                    status = "[FAIL]"

                print(f"  {status} {page['page_name']}")

                if not page['success'] or page.get('partial'):
                    error = page.get('error', 'Unknown error')
                    print(f"      Note: {error}")

        # Exit with success if at least some pages were created
        exit_code = 0 if (result.get('success', 0) + result.get('partial', 0)) > 0 else 1
        sys.exit(exit_code)
    else:
        print(f"\nBatch mode: Processing all files in {config.seo_files_dir}/")
        print("(Each file can contain multiple pages)")
        print("(Partial success = page created but some sections incomplete)\n")

        result = process_batch(config.seo_files_dir, config)

        print("\n" + "=" * 80)
        print("RESULT")
        print("=" * 80)
        print(f"Files processed: {result.get('total_files', 0)}")
        print(f"Total pages: {result.get('total_pages', 0)}")
        print(f"Successfully created: {result.get('success', 0)}")
        print(f"Partially created: {result.get('partial', 0)}")
        print(f"Failed: {result.get('failed', 0)}")

        # Exit with success if at least some pages were created
        exit_code = 0 if (result.get('success', 0) + result.get('partial', 0)) > 0 else 1
        sys.exit(exit_code)


if __name__ == "__main__":
    main()
