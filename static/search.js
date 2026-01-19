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
    const form = panel ? panel.querySelector("form") : null;
    const input = document.getElementById("site-search");
    const closeBtn = document.querySelector(".search-close");
    const items = Array.from(document.querySelectorAll(".post-item"));
    const separators = Array.from(document.querySelectorAll(".post-separator"));
    const suggestionsBox = document.getElementById("search-suggestions");

    if (!toggleBtn || !panel || !input || !closeBtn) {
      return;
    }

    let suggestionIndex = null;

    const isPostsIndex = window.location.pathname === "/posts";
    const params = new URLSearchParams(window.location.search);
    const initialQuery = (params.get("q") || "").trim();

    function applyFilter(rawQuery) {
      if (items.length === 0) {
        return;
      }
      const q = (rawQuery || "").trim().toLowerCase();

      const terms = q
        .split("|")
        .map((t) => t.trim())
        .filter((t) => t.length > 0);

      const isOrQuery = terms.length > 1;

      const visibleItems = [];
      for (const li of items) {
        const haystack = (li.dataset.search || "").toLowerCase();
        let visible = true;
        if (q.length > 0) {
          if (isOrQuery) {
            visible = terms.some((t) => haystack.includes(t));
          } else {
            visible = haystack.includes(q);
          }
        }
        li.hidden = !visible;
        if (visible) {
          visibleItems.push(li);
        }
      }

      // Keep separators only between visible posts.
      if (separators.length > 0) {
        for (const hr of separators) {
          hr.hidden = true;
        }
        for (let i = 0; i < visibleItems.length - 1; i += 1) {
          const next = visibleItems[i].nextElementSibling;
          if (next && next.classList && next.classList.contains("post-separator")) {
            next.hidden = false;
          }
        }
      }
    }

    function openSearch() {
      panel.hidden = false;
      toggleBtn.setAttribute("aria-expanded", "true");
      input.focus();
      void loadAutocompleteIndex();
    }

    async function loadAutocompleteIndex() {
      if (suggestionIndex !== null) {
        return;
      }

      // Posts index: we can build directly from the DOM (no extra request).
      if (items.length > 0) {
        suggestionIndex = items
          .map((el) => {
            const a = el.querySelector(".btn-link");
            if (!a) {
              return null;
            }
            const title = (a.textContent || "").trim();
            return {
              title,
              href: a.getAttribute("href"),
              titleLower: title.toLowerCase(),
            };
          })
          .filter((x) => x && x.title && x.href);
        return;
      }

      // Homepage: fetch titles from the API.
      try {
        const res = await fetch("/api/posts", {
          headers: { Accept: "application/json" },
        });
        if (!res.ok) {
          suggestionIndex = [];
          return;
        }
        const posts = await res.json();
        suggestionIndex = (posts || [])
          .map((p) => {
            const title = (p && p.title ? String(p.title) : "").trim();
            const slug = (p && p.slug ? String(p.slug) : "").trim();
            if (!title || !slug) {
              return null;
            }
            return {
              title,
              href: `/posts/${slug}`,
              titleLower: title.toLowerCase(),
            };
          })
          .filter(Boolean);
      } catch {
        suggestionIndex = [];
      }
    }

    function hideAutocomplete() {
      if (!suggestionsBox) {
        return;
      }
      suggestionsBox.hidden = true;
      suggestionsBox.innerHTML = "";
    }

    function renderAutocomplete(rawQuery) {
      if (!suggestionsBox || !suggestionIndex || suggestionIndex.length === 0) {
        return;
      }
      const q = (rawQuery || "").trim().toLowerCase();
      if (q.length === 0) {
        hideAutocomplete();
        return;
      }

      // Autocomplete is intentionally title-only to avoid surprising matches
      // (e.g., tags, summaries, or other metadata).
      const matches = suggestionIndex
        .map((x) => ({ x, idx: (x.titleLower || "").indexOf(q) }))
        .filter((m) => m.idx >= 0)
        .sort((a, b) => {
          if (a.idx !== b.idx) {
            return a.idx - b.idx;
          }
          if (a.x.title.length !== b.x.title.length) {
            return a.x.title.length - b.x.title.length;
          }
          return a.x.title.localeCompare(b.x.title);
        })
        .slice(0, 6)
        .map((m) => m.x);

      if (matches.length === 0) {
        hideAutocomplete();
        return;
      }

      suggestionsBox.innerHTML = matches
        .map(
          (m) =>
            `<a href="${m.href}">${escapeHtml(m.title)}<span class="search-suggestion-sub">${escapeHtml(m.href)}</span></a>`
        )
        .join("");
      suggestionsBox.hidden = false;
    }

    function escapeHtml(str) {
      return String(str)
        .replaceAll("&", "&amp;")
        .replaceAll("<", "&lt;")
        .replaceAll(">", "&gt;")
        .replaceAll('"', "&quot;")
        .replaceAll("'", "&#039;");
    }

    function closeSearch() {
      panel.hidden = true;
      toggleBtn.setAttribute("aria-expanded", "false");
      input.value = "";
      applyFilter("");
      hideAutocomplete();

      if (isPostsIndex) {
        // Clear deep-linked query when the user closes search.
        window.history.replaceState(null, "", "/posts");
      }
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

    input.addEventListener("input", (e) => {
      const q = (e.target.value || "").trim();
      applyFilter(q);
      void loadAutocompleteIndex();
      renderAutocomplete(q);

      if (isPostsIndex) {
        if (q.length === 0) {
          window.history.replaceState(null, "", "/posts");
        } else {
          window.history.replaceState(null, "", `/posts?q=${encodeURIComponent(q)}`);
        }
      }
    });

    if (form) {
      form.addEventListener("submit", (e) => {
        const q = (input.value || "").trim();
        if (!q) {
          e.preventDefault();
          return;
        }

        if (isPostsIndex) {
          // Keep everything client-side on the posts index; just update URL + filter.
          e.preventDefault();
          applyFilter(q);
          openSearch();
          window.history.replaceState(null, "", `/posts?q=${encodeURIComponent(q)}`);
          return;
        }

        // Homepage: only navigate when a non-empty search has been submitted.
        e.preventDefault();
        window.location.assign(`/posts?q=${encodeURIComponent(q)}`);
      });
    }

    document.addEventListener("keydown", (e) => {
      if (e.key === "Escape" && !panel.hidden) {
        e.preventDefault();
        closeSearch();
      }
    });

    document.addEventListener("click", (e) => {
      if (panel.hidden) {
        return;
      }
      if (!suggestionsBox || suggestionsBox.hidden) {
        return;
      }
      if (e.target === input || suggestionsBox.contains(e.target)) {
        return;
      }
      hideAutocomplete();
    });

    // Posts index: support deep-links like /posts?q=stellody.
    // When navigating via the sidebar, we want the filtering but we *don't* want
    // to auto-open the search UI or populate the search field.
    if (isPostsIndex && initialQuery.length > 0) {
      applyFilter(initialQuery);
    }
  });
})();
