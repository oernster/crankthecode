(() => {
  function getTarget(button) {
    const id = button.getAttribute("data-copy-target");
    if (!id) return null;
    return document.getElementById(id);
  }

  async function copyText(text) {
    if (navigator.clipboard && window.isSecureContext) {
      await navigator.clipboard.writeText(text);
      return;
    }

    // Fallback
    const textarea = document.createElement("textarea");
    textarea.value = text;
    textarea.setAttribute("readonly", "");
    textarea.style.position = "fixed";
    textarea.style.top = "-1000px";
    textarea.style.left = "-1000px";
    document.body.appendChild(textarea);
    textarea.select();
    document.execCommand("copy");
    textarea.remove();
  }

  async function handleCopyClick(ev) {
    const button = ev.target.closest(".code-copy");
    if (!button) return;

    const target = getTarget(button);
    if (!target) return;

    const text = target.textContent || "";
    if (!text.trim()) return;

    const isIconButton = button.classList.contains("code-copy--icon");
    const originalText = button.textContent;
    const originalAriaLabel = button.getAttribute("aria-label");
    const originalTitle = button.getAttribute("title");
    const originalDataCopied = button.getAttribute("data-copied");
    button.disabled = true;
    try {
      await copyText(text.trimEnd() + "\n");
      if (isIconButton) {
        button.setAttribute("data-copied", "true");
        button.setAttribute("aria-label", "Copied");
        button.setAttribute("title", "Copied");
      } else {
        button.textContent = "Copied";
      }
    } catch {
      if (isIconButton) {
        button.setAttribute("aria-label", "Copy failed");
        button.setAttribute("title", "Copy failed");
      } else {
        button.textContent = "Copy failed";
      }
    }

    window.setTimeout(() => {
      if (isIconButton) {
        if (originalDataCopied !== null) button.setAttribute("data-copied", originalDataCopied);
        else button.removeAttribute("data-copied");
        if (originalAriaLabel !== null) button.setAttribute("aria-label", originalAriaLabel);
        else button.removeAttribute("aria-label");
        if (originalTitle !== null) button.setAttribute("title", originalTitle);
        else button.removeAttribute("title");
      } else {
        button.textContent = originalText;
      }
      button.disabled = false;
    }, 1400);
  }

  document.addEventListener("click", (ev) => {
    void handleCopyClick(ev);
  });
})();
