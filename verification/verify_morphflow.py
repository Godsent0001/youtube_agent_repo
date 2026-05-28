from playwright.sync_api import sync_playwright
import os

def run_verification(page):
    # Navigate to landing page
    page.goto("http://localhost:5173")
    page.wait_for_timeout(2000)

    # 1. Take screenshot of Landing Page (Logged Out)
    page.screenshot(path="/home/jules/verification/screenshots/home_logged_out.png")
    print("Screenshot: home_logged_out.png")

    # 2. Go to Login Page
    page.click("text=Login")
    page.wait_for_timeout(1000)
    page.screenshot(path="/home/jules/verification/screenshots/login_page.py.png")
    print("Screenshot: login_page.png")

    # 3. Go to Pricing Page
    page.goto("http://localhost:5173/pricing")
    page.wait_for_timeout(1000)
    page.screenshot(path="/home/jules/verification/screenshots/pricing_page.png")
    print("Screenshot: pricing_page.png")

if __name__ == "__main__":
    os.makedirs("/home/jules/verification/screenshots", exist_ok=True)
    os.makedirs("/home/jules/verification/videos", exist_ok=True)

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        context = browser.new_context(record_video_dir="/home/jules/verification/videos")
        page = context.new_page()
        try:
            run_verification(page)
        finally:
            context.close()
            browser.close()
