
from playwright.sync_api import sync_playwright, expect

def test_ux(page):
    page.goto("http://localhost:8000/ui/index.html")

    # 1. Test Label Association
    # Find the label "I am applying for"
    label = page.get_by_text("I am applying for", exact=True)

    # Click it
    label.click()

    # Check if visaSelect is focused
    # We can check if the active element is the select
    is_focused = page.evaluate("document.activeElement.id === 'visaSelect'")
    print(f"Label click focuses select: {is_focused}")

    # 2. Test Modal Accessibility
    # Wait for options to populate
    # The error was waiting for visibility of option. Options in select are not "visible" in the traditional sense unless expanded.
    # We should wait for the select to have children > 1
    page.wait_for_function("document.getElementById('visaSelect').options.length > 1")

    # Select first real option
    page.select_option("#visaSelect", index=1)
    page.select_option("#productSelect", index=1)

    # Click Check
    page.click("#checkBtn")

    # Wait for results
    page.wait_for_selector("#resultArea")

    # Find an "View Evidence" button.
    # They are dynamically added.
    # We need to wait for one.
    page.wait_for_selector(".evBtn")
    evidence_btn = page.locator(".evBtn").first

    if evidence_btn.count() > 0:
        evidence_btn.click()

        # Check modal attributes
        modal = page.locator("#modal")
        expect(modal).to_be_visible()

        role = modal.get_attribute("role")
        aria_modal = modal.get_attribute("aria-modal")
        print(f"Modal role: {role}")
        print(f"Modal aria-modal: {aria_modal}")

        # Press Escape
        page.keyboard.press("Escape")

        # Check if closed.
        # Note: The implementation might not support Escape key yet.
        # We'll check visibility after a short delay
        page.wait_for_timeout(500)
        is_visible = modal.is_visible()
        print(f"Modal visible after Escape: {is_visible}")

    else:
        print("No evidence buttons found to test modal")

    page.screenshot(path="ux_before.png")

if __name__ == "__main__":
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        try:
            test_ux(page)
        except Exception as e:
            print(f"Error: {e}")
        finally:
            browser.close()
