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

    const SHOW_AFTER_PX = 420;
    let ticking = false;

    function updateVisibility() {
      const y = window.scrollY || document.documentElement.scrollTop || 0;
      const shouldShow = y >= SHOW_AFTER_PX;
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

    window.addEventListener("scroll", onScroll, { passive: true });
    updateVisibility();
  });
})();
