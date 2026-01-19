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
