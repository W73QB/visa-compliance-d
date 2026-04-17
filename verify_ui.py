from playwright.sync_api import sync_playwright
import os

def run_cuj(page):
    page.goto("http://localhost:8000/ui/")
    page.wait_for_timeout(1000)

    # Click the "I am applying for" label to see if it focuses the visa select
    page.get_by_text("I am applying for").click()
    page.wait_for_timeout(500)

    # Take a screenshot to show the focus state
    os.makedirs("/app/verification", exist_ok=True)
    page.screenshot(path="/app/verification/verification.png")
    page.wait_for_timeout(500)

    # Click the "I want to use" label
    page.get_by_text("I want to use").click()
    page.wait_for_timeout(500)

if __name__ == "__main__":
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        context = browser.new_context(
            record_video_dir="/app/verification"
        )
        page = context.new_page()
        try:
            run_cuj(page)
        finally:
            context.close()
            browser.close()
