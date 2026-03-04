import sys
import os
import subprocess
import time
from playwright.sync_api import sync_playwright

def main():
    # Start the local server
    server_process = subprocess.Popen(["python3", "-m", "http.server", "8080"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    time.sleep(2)  # Give server time to start

    try:
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=True)
            page = browser.new_page()

            # Navigate to the UI page
            print("Navigating to local UI...")
            page.goto("http://localhost:8080/ui/")

            # Wait for dynamic elements to attach
            print("Waiting for selects to attach...")
            page.wait_for_selector("#visaSelect option:not([value=''])", state="attached", timeout=5000)
            page.wait_for_selector("#productSelect option:not([value=''])", state="attached", timeout=5000)

            # Check visaSelect aria-describedby
            print("Checking visaSelect aria-describedby...")
            visa_select = page.locator("#visaSelect")
            aria_desc_visa = visa_select.get_attribute("aria-describedby")
            if aria_desc_visa != "visaHint":
                print(f"FAIL: visaSelect aria-describedby is '{aria_desc_visa}', expected 'visaHint'")
                sys.exit(1)

            # Check productSelect aria-describedby
            print("Checking productSelect aria-describedby...")
            product_select = page.locator("#productSelect")
            aria_desc_prod = product_select.get_attribute("aria-describedby")
            if aria_desc_prod != "productHint":
                print(f"FAIL: productSelect aria-describedby is '{aria_desc_prod}', expected 'productHint'")
                sys.exit(1)

            # Check explicit labels working by clicking them
            print("Checking label clicks set focus...")

            # Click the 'I am applying for' label
            visa_label = page.locator("label[for='visaSelect']")
            visa_label.click()
            is_visa_focused = page.evaluate("document.activeElement.id === 'visaSelect'")
            if not is_visa_focused:
                print("FAIL: Clicking visaSelect label did not focus visaSelect input.")
                sys.exit(1)

            # Click the 'I want to use' label
            product_label = page.locator("label[for='productSelect']")
            product_label.click()
            is_product_focused = page.evaluate("document.activeElement.id === 'productSelect'")
            if not is_product_focused:
                print("FAIL: Clicking productSelect label did not focus productSelect input.")
                sys.exit(1)

            print("SUCCESS: All accessibility verification checks passed!")
            browser.close()
    finally:
        server_process.terminate()

if __name__ == "__main__":
    main()
