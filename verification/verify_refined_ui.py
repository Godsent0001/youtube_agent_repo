from playwright.sync_api import sync_playwright
import os

def run_verification(page):
    # Navigate to landing page
    page.goto("http://localhost:5173")
    page.wait_for_timeout(2000)

    # 1. Take screenshot of Refined Home Page
    page.screenshot(path="/home/jules/verification/screenshots/home_refined.png")
    print("Screenshot: home_refined.png")

    # 2. Click on Aspect Ratio Dropdown
    page.click("text=Ratio")
    page.wait_for_timeout(1000)
    page.screenshot(path="/home/jules/verification/screenshots/aspect_dropdown.png")
    print("Screenshot: aspect_dropdown.png")

    # 3. Click on Duration Dropdown
    page.click("text=Ratio") # Close first
    page.wait_for_timeout(500)
    page.click("text=Length")
    page.wait_for_timeout(1000)
    page.screenshot(path="/home/jules/verification/screenshots/duration_dropdown.png")
    print("Screenshot: duration_dropdown.png")

if __name__ == "__main__":
    os.makedirs("/home/jules/verification/screenshots", exist_ok=True)

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        context = browser.new_context()
        page = context.new_page()
        try:
            run_verification(page)
        finally:
            context.close()
            browser.close()
