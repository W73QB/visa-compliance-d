import time
from playwright.sync_api import sync_playwright

def run(playwright):
    browser = playwright.chromium.launch(headless=True)
    page = browser.new_page()

    print("Navigating to page...")
    # 1. Navigate to the UI
    page.goto("http://localhost:8000/ui/index.html")

    # Wait for data to load
    try:
        page.wait_for_selector("#visaSelect option:not([value=''])", state="attached", timeout=10000)
        page.wait_for_selector("#productSelect option:not([value=''])", state="attached", timeout=10000)
    except Exception as e:
        print(f"Timeout waiting for selectors: {e}")
        # Capture screenshot for debugging
        page.screenshot(path="verification/debug_load_fail.png")
        browser.close()
        return

    # 2. Select Visa and Product to trigger results
    visa_options = page.locator("#visaSelect option")
    if visa_options.count() > 1:
        first_visa = visa_options.nth(1).get_attribute("value")
        print(f"Selecting Visa: {first_visa}")
        page.select_option("#visaSelect", first_visa)

    product_options = page.locator("#productSelect option")
    if product_options.count() > 1:
        first_product = product_options.nth(1).get_attribute("value")
        print(f"Selecting Product: {first_product}")
        page.select_option("#productSelect", first_product)

    # Click Check Compliance
    page.click("#checkBtn")

    # Wait for results
    page.wait_for_selector("#resultArea")

    # 3. Open Modal
    print("Opening modal...")
    try:
        # Try to find a real evidence button
        page.wait_for_selector(".evBtn", timeout=2000)
        page.locator(".evBtn").first.click()
    except:
        print("No evidence button found. Mocking openModal.")
        page.evaluate('openModal([{source_id: "TEST", excerpt: "Test Evidence"}])')

    time.sleep(1) # Wait for animation/display

    # 4. Verify Modal Accessibility Attributes
    modal = page.locator("#modal")
    expect_role = modal.get_attribute("role")
    expect_aria_modal = modal.get_attribute("aria-modal")
    expect_aria_labelledby = modal.get_attribute("aria-labelledby")

    print(f"role: {expect_role}")
    print(f"aria-modal: {expect_aria_modal}")
    print(f"aria-labelledby: {expect_aria_labelledby}")

    if expect_role != "dialog":
        print("FAIL: role is not dialog")
    if expect_aria_modal != "true":
        print("FAIL: aria-modal is not true")
    if expect_aria_labelledby != "modalTitle":
        print("FAIL: aria-labelledby is not modalTitle")

    # 5. Verify Focus Trap
    # Initial focus should be on close button
    active_element_id = page.evaluate("document.activeElement.id")
    print(f"Active element ID on open: {active_element_id}")

    if active_element_id == "closeModal":
        print("PASS: Focus moved to closeModal button")
    else:
        print("FAIL: Focus did not move to closeModal button")

    # Take screenshot of open modal
    page.screenshot(path="verification/verification.png")
    print("Screenshot saved to verification/verification.png")

    # Press Escape to close
    page.keyboard.press("Escape")
    time.sleep(0.5)

    # Check if modal is hidden
    is_hidden = modal.get_attribute("class")
    if "hidden" in is_hidden:
        print("PASS: Modal closed on Escape")
    else:
        print("FAIL: Modal did not close on Escape")

    browser.close()

with sync_playwright() as playwright:
    run(playwright)
