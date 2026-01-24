(() => {
  function ready(fn) {
    if (document.readyState === "loading") {
      document.addEventListener("DOMContentLoaded", fn);
    } else {
      fn();
    }
  }

  function countWords(text) {
    const trimmed = (text || "").trim();
    if (!trimmed) {
      return 0;
    }
    return trimmed.split(/\s+/).length;
  }

  function computeMinutes(words, wpm = 200) {
    if (!Number.isFinite(words) || words <= 0) {
      return 0;
    }
    return Math.max(1, Math.ceil(words / wpm));
  }

  ready(() => {
    const target = document.querySelector(".read-time");

    const content =
      document.querySelector(".post-content") ||
      document.querySelector("main#main");

    // Only show read time on pages that have post content.
    if (!content || !target) {
      return;
    }

    // Prefer innerText (respects visual spacing); fall back to textContent.
    // When using main#main, exclude the read-time bar itself from the count.
    let text = "";
    if (content.matches("main#main")) {
      const clone = content.cloneNode(true);
      const rt = clone.querySelector(".read-time-bar");
      if (rt) {
        rt.remove();
      }
      text = clone.innerText || clone.textContent || "";
    } else {
      text = content.innerText || content.textContent || "";
    }

    const words = countWords(text);
    const minutes = computeMinutes(words);

    // If there's basically no content, keep it hidden.
    if (!minutes) {
      target.hidden = true;
      return;
    }

    target.textContent = `🕒 ${minutes} min read`;
    target.setAttribute("aria-label", `Estimated read time: ${minutes} minute${minutes === 1 ? "" : "s"}`);
    target.hidden = false;
  });
})();

