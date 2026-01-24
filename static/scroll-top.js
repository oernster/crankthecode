(() => {
  function ready(fn) {
    if (document.readyState === "loading") {
      document.addEventListener("DOMContentLoaded", fn);
    } else {
      fn();
    }
  }

  ready(() => {
    const btn = document.getElementById("scroll-top");
    if (!btn) {
      return;
    }

    // Show earlier so it's available on more pages (some pages simply don't
    // scroll 420px, especially on smaller viewports).
    const SHOW_AFTER_MIN_PX = 80;
    const SHOW_AFTER_MAX_PX = 240;
    let ticking = false;

    const scrollingEl = document.scrollingElement || document.documentElement;

    function currentScrollTop() {
      return scrollingEl ? scrollingEl.scrollTop || 0 : 0;
    }

    function showAfterPx() {
      const dynamic = Math.floor((window.innerHeight || 600) * 0.35);
      return Math.max(SHOW_AFTER_MIN_PX, Math.min(SHOW_AFTER_MAX_PX, dynamic));
    }

    function updateVisibility() {
      const y = currentScrollTop();
      const shouldShow = y >= showAfterPx();
      btn.hidden = !shouldShow;
      btn.classList.toggle("is-visible", shouldShow);
    }

    function onScroll() {
      if (ticking) {
        return;
      }
      ticking = true;
      window.requestAnimationFrame(() => {
        ticking = false;
        updateVisibility();
      });
    }

    btn.addEventListener("click", () => {
      window.scrollTo({ top: 0, behavior: "smooth" });

      // Accessibility: after sending the user to the top, move focus to a
      // predictable, top-of-page control so keyboard navigation continues from
      // the start (rather than from whichever link was next in DOM order).
      //
      // We prefer the skip link (present on every page). Using a short timeout
      // allows the smooth scroll to start; focusing immediately also works but
      // can feel “jumpy” in some browsers.
      window.setTimeout(() => {
        const focusTarget =
          document.getElementById("skip-link") ||
          document.querySelector(".skip-link") ||
          document.body;

        if (focusTarget && typeof focusTarget.focus === "function") {
          focusTarget.focus({ preventScroll: true });
        }
      }, 50);
    });

    // Listen on both window + document in case any page uses a non-window
    // scrolling element.
    window.addEventListener("scroll", onScroll, { passive: true });
    document.addEventListener("scroll", onScroll, { passive: true });
    window.addEventListener("resize", updateVisibility, { passive: true });
    window.addEventListener("pageshow", updateVisibility);
    updateVisibility();
  });
})();
