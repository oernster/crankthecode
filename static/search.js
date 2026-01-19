(() => {
  function ready(fn) {
    if (document.readyState === "loading") {
      document.addEventListener("DOMContentLoaded", fn);
    } else {
      fn();
    }
  }

  ready(() => {
    const toggleBtn = document.querySelector(".search-toggle");
    const panel = document.getElementById("search-panel");
    const input = document.getElementById("site-search");
    const closeBtn = document.querySelector(".search-close");
    const items = Array.from(document.querySelectorAll(".post-item"));

    // Not on the homepage.
    if (!toggleBtn || !panel || !input || !closeBtn || items.length === 0) {
      return;
    }

    function applyFilter(rawQuery) {
      const q = (rawQuery || "").trim().toLowerCase();
      for (const li of items) {
        const haystack = (li.dataset.search || "").toLowerCase();
        li.hidden = q.length > 0 && !haystack.includes(q);
      }
    }

    function openSearch() {
      panel.hidden = false;
      toggleBtn.setAttribute("aria-expanded", "true");
      input.focus();
    }

    function closeSearch() {
      panel.hidden = true;
      toggleBtn.setAttribute("aria-expanded", "false");
      input.value = "";
      applyFilter("");
    }

    function toggleSearch() {
      if (panel.hidden) {
        openSearch();
      } else {
        closeSearch();
      }
    }

    toggleBtn.addEventListener("click", toggleSearch);
    closeBtn.addEventListener("click", closeSearch);
    input.addEventListener("input", (e) => applyFilter(e.target.value));

    document.addEventListener("keydown", (e) => {
      if (e.key === "Escape" && !panel.hidden) {
        e.preventDefault();
        closeSearch();
      }
    });
  });
})();
