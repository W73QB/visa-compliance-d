import re

with open("ui/index.html", "rb") as f:
    content = f.read().decode("utf-8")

# Fix the bug with aria-expanded toggling inversion
content = re.sub(
    r'(menu\.classList\.toggle\("hidden"\);\r?\n\s*btn\.setAttribute\("aria-expanded", String\()isOpen(\)\);)',
    r'\g<1>!isOpen\g<2>',
    content
)

with open("ui/index.html", "wb") as f:
    f.write(content.encode("utf-8"))
