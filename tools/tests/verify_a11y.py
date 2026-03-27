from bs4 import BeautifulSoup
import sys

def verify_a11y():
    try:
        with open("ui/index.html", "r", encoding="utf-8") as f:
            html = f.read()
    except FileNotFoundError:
        print("ui/index.html not found")
        sys.exit(1)

    soup = BeautifulSoup(html, "html.parser")
    errors = []

    # Check modal attributes
    modal = soup.find(id="modal")
    if not modal:
        errors.append("Modal element not found")
    else:
        if modal.get("role") != "dialog":
            errors.append("Modal missing role='dialog'")
        if modal.get("aria-modal") != "true":
            errors.append("Modal missing aria-modal='true'")
        if not modal.get("aria-labelledby"):
            errors.append("Modal missing aria-labelledby")

    # Check modal title
    modal_title = soup.find(id="modalTitle")
    if not modal_title:
        errors.append("Modal title with id='modalTitle' not found")

    # Check labels for selects
    visa_label = soup.find("label", attrs={"for": "visaSelect"})
    if not visa_label:
        errors.append("Label for visaSelect not found")

    product_label = soup.find("label", attrs={"for": "productSelect"})
    if not product_label:
        errors.append("Label for productSelect not found")

    if errors:
        print("Accessibility Verification Failed:")
        for err in errors:
            print(f"- {err}")
        sys.exit(1)

    print("Accessibility Verification Passed!")

if __name__ == "__main__":
    verify_a11y()
