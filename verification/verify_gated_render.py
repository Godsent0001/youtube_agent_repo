from playwright.sync_api import sync_playwright
import os

def run_cuj(page):
    # Navigate to the landing page
    # Since we're in a sandbox, we'll try to reach the dev server if it started,
    # but more reliably we can check if it's running.
    # For verification in this environment, I'll use the localhost URL
    try:
        page.goto("http://localhost:5173", timeout=10000)
    except Exception as e:
        print(f"Could not connect to dev server: {e}")
        return

    page.wait_for_timeout(2000)  # Wait for preloader

    # Take screenshot to verify background and overlay
    page.screenshot(path="verification/gated_render_verify.png")
    print("Screenshot saved to verification/gated_render_verify.png")

if __name__ == "__main__":
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        context = browser.new_context(
            record_video_dir="verification/videos"
        )
        page = context.new_page()
        try:
            run_cuj(page)
        finally:
            context.close()
            browser.close()
