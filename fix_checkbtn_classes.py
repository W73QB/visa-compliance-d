import re

with open('ui/index.html', 'rb') as f:
    content = f.read().decode('utf-8')

new_func = """    function setCheckBtnEnabled() {
      const v = $("visaSelect").value;
      const p = $("productSelect").value;
      const btn = $("checkBtn");
      if (v && p) {
        btn.disabled = false;
        btn.setAttribute("aria-disabled", "false");
        btn.classList.remove("bg-primary/50", "cursor-not-allowed");
        btn.classList.add("bg-primary", "hover:bg-primary-hover", "hover:-translate-y-0.5", "hover:shadow-lg", "active:translate-y-0");
      } else {
        btn.disabled = true;
        btn.setAttribute("aria-disabled", "true");
        btn.classList.add("bg-primary/50", "cursor-not-allowed");
        btn.classList.remove("bg-primary", "hover:bg-primary-hover", "hover:-translate-y-0.5", "hover:shadow-lg", "active:translate-y-0");
      }
    }"""

content = re.sub(
    r'    function setCheckBtnEnabled\(\) \{[\s\S]*?\}',
    new_func,
    content
)

with open('ui/index.html', 'wb') as f:
    f.write(content.encode('utf-8'))
