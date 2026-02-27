
import os

INDEX_HTML_PATH = "ui/index.html"

def main():
    if not os.path.exists(INDEX_HTML_PATH):
        print(f"Error: {INDEX_HTML_PATH} not found.")
        return

    with open(INDEX_HTML_PATH, "rb") as f:
        content = f.read()

    # Determine line ending (CRLF or LF)
    if b"\r\n" in content:
        line_ending = b"\r\n"
        print("Detected CRLF line endings.")
    else:
        line_ending = b"\n"
        print("Detected LF line endings.")

    # 1. Update Modal HTML
    # Add role="dialog" aria-modal="true" aria-labelledby="modalTitle"
    # Find: <div id="modal" class="fixed inset-0 bg-black/40 hidden items-center justify-center p-4 z-50">
    # Replace with: <div id="modal" class="fixed inset-0 bg-black/40 hidden items-center justify-center p-4 z-50" role="dialog" aria-modal="true" aria-labelledby="modalTitle">

    search_modal_div = b'<div id="modal" class="fixed inset-0 bg-black/40 hidden items-center justify-center p-4 z-50">'
    replace_modal_div = b'<div id="modal" class="fixed inset-0 bg-black/40 hidden items-center justify-center p-4 z-50" role="dialog" aria-modal="true" aria-labelledby="modalTitle">'

    if search_modal_div in content:
        content = content.replace(search_modal_div, replace_modal_div)
        print("Updated modal div attributes.")
    else:
        print("Warning: Could not find modal div to update.")

    # 2. Add id="modalTitle" to the title div
    # Find: <div class="font-bold text-text-primary dark:text-white">Evidence</div>
    # Replace with: <div id="modalTitle" class="font-bold text-text-primary dark:text-white">Evidence</div>

    search_modal_title = b'<div class="font-bold text-text-primary dark:text-white">Evidence</div>'
    replace_modal_title = b'<div id="modalTitle" class="font-bold text-text-primary dark:text-white">Evidence</div>'

    if search_modal_title in content:
        content = content.replace(search_modal_title, replace_modal_title)
        print("Updated modal title div.")
    else:
        print("Warning: Could not find modal title div to update.")

    # 3. Add lastFocusedElement variable and event listener
    # We can add this before init()
    # Find: async function init() {
    # Replace with:
    # let lastFocusedElement = null;
    # document.addEventListener("keydown", (e) => {
    #   if (e.key === "Escape" && !$("modal").classList.contains("hidden")) {
    #     closeModal();
    #   }
    # });
    #
    # async function init() {

    search_init = b'async function init() {'

    # Construct replacement block using detected line ending
    replacement_code_lines = [
        b'    let lastFocusedElement = null;',
        b'    document.addEventListener("keydown", (e) => {',
        b'      if (e.key === "Escape" && !$("modal").classList.contains("hidden")) {',
        b'        closeModal();',
        b'      }',
        b'    });',
        b'',
        b'    async function init() {'
    ]
    replace_init = line_ending.join(replacement_code_lines)

    if search_init in content:
        content = content.replace(search_init, replace_init)
        print("Added focus tracking variable and Escape listener.")
    else:
        print("Warning: Could not find init() function.")

    # 4. Update openModal to save focus
    # Find: function openModal(evidenceItems) {
    # Replace with:
    # function openModal(evidenceItems) {
    #   lastFocusedElement = document.activeElement;

    search_open_modal = b'function openModal(evidenceItems) {'
    replace_open_modal = b'function openModal(evidenceItems) {' + line_ending + b'      lastFocusedElement = document.activeElement;'

    if search_open_modal in content:
        content = content.replace(search_open_modal, replace_open_modal)
        print("Updated openModal to save focus.")
    else:
        print("Warning: Could not find openModal function.")

    # 5. Update closeModal to restore focus
    # Find: $("modal").classList.remove("flex");
    # Replace:
    # $("modal").classList.remove("flex");
    # if (lastFocusedElement) lastFocusedElement.focus();

    search_close_modal_end = b'      $("modal").classList.remove("flex");'
    replace_close_modal_end = b'      $("modal").classList.remove("flex");' + line_ending + b'      if (lastFocusedElement) lastFocusedElement.focus();'

    if search_close_modal_end in content:
        content = content.replace(search_close_modal_end, replace_close_modal_end)
        print("Updated closeModal to restore focus.")
    else:
        print("Warning: Could not find closeModal end line.")

    with open(INDEX_HTML_PATH, "wb") as f:
        f.write(content)

    print(f"Successfully modified {INDEX_HTML_PATH}")

if __name__ == "__main__":
    main()
