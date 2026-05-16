(function () {
  "use strict";

  const THEME_KEY = "us-stock-theme";
  const root = document.documentElement;

  function applyTheme(theme) {
    root.dataset.theme = theme;
    document.querySelectorAll("[data-theme-toggle]").forEach((btn) => {
      const isDark = theme === "dark";
      btn.setAttribute("aria-pressed", isDark ? "true" : "false");
      btn.innerHTML = isDark
        ? '<span aria-hidden="true">☀</span> 浅色'
        : '<span aria-hidden="true">☾</span> 深色';
    });
  }

  const stored = localStorage.getItem(THEME_KEY);
  const initial =
    stored || (window.matchMedia("(prefers-color-scheme: dark)").matches ? "dark" : "light");
  applyTheme(initial);

  function showToast(message) {
    let toast = document.querySelector(".toast");
    if (!toast) {
      toast = document.createElement("div");
      toast.className = "toast";
      toast.setAttribute("role", "status");
      document.body.appendChild(toast);
    }
    toast.textContent = message;
    requestAnimationFrame(() => toast.classList.add("is-visible"));
    clearTimeout(toast._timer);
    toast._timer = setTimeout(() => toast.classList.remove("is-visible"), 1800);
  }

  function initThemeToggle() {
    document.querySelectorAll("[data-theme-toggle]").forEach((btn) => {
      btn.addEventListener("click", () => {
        const next = root.dataset.theme === "dark" ? "light" : "dark";
        applyTheme(next);
        localStorage.setItem(THEME_KEY, next);
      });
    });
  }

  function initOverviewTable() {
    const table = document.querySelector("[data-sortable]");
    if (!table) return;

    const tbody = table.tBodies[0];
    const rows = Array.from(tbody.rows);

    const search = document.querySelector("[data-table-search]");
    const clearBtn = document.querySelector("[data-filter-clear]");
    let signalFilter = null;
    let lastDir = {};

    function syncCounts() {
      document.querySelectorAll("[data-signal-filter]").forEach((card) => {
        const value = card.dataset.signalFilter;
        const count = rows.filter((r) => r.dataset.signal === value).length;
        const badge = card.querySelector(".signal-count");
        if (badge) badge.textContent = count;
      });
    }

    function apply() {
      const q = (search?.value || "").trim().toLowerCase();
      rows.forEach((row) => {
        const matchText = !q || row.textContent.toLowerCase().includes(q);
        const matchSignal = !signalFilter || row.dataset.signal === signalFilter;
        row.classList.toggle("is-hidden", !(matchText && matchSignal));
      });
      const filtered = !!q || !!signalFilter;
      if (clearBtn) clearBtn.hidden = !filtered;
    }

    search?.addEventListener("input", apply);

    clearBtn?.addEventListener("click", () => {
      if (search) search.value = "";
      signalFilter = null;
      document
        .querySelectorAll("[data-signal-filter]")
        .forEach((c) => c.classList.remove("is-active"));
      apply();
    });

    document.querySelectorAll("[data-signal-filter]").forEach((card) => {
      card.addEventListener("click", () => {
        const value = card.dataset.signalFilter;
        if (signalFilter === value) {
          signalFilter = null;
          card.classList.remove("is-active");
        } else {
          signalFilter = value;
          document
            .querySelectorAll("[data-signal-filter]")
            .forEach((c) => c.classList.toggle("is-active", c === card));
        }
        apply();
        // Scroll table into view on small screens
        if (window.innerWidth < 980) {
          table.scrollIntoView({ behavior: "smooth", block: "start" });
        }
      });
    });

    table.querySelectorAll("th[data-sort]").forEach((th, idx) => {
      th.addEventListener("click", () => {
        const type = th.dataset.sort;
        const dir = lastDir[idx] === "asc" ? "desc" : "asc";
        lastDir = { [idx]: dir };
        const mul = dir === "asc" ? 1 : -1;

        const sorted = rows.slice().sort((a, b) => {
          const av = a.cells[idx].dataset.sortValue ?? a.cells[idx].textContent.trim();
          const bv = b.cells[idx].dataset.sortValue ?? b.cells[idx].textContent.trim();
          if (type === "number") return (parseFloat(av) - parseFloat(bv)) * mul;
          return av.localeCompare(bv, "zh-Hans-CN") * mul;
        });

        sorted.forEach((r) => tbody.appendChild(r));
        table
          .querySelectorAll("th")
          .forEach((h) => h.removeAttribute("aria-sort"));
        th.setAttribute("aria-sort", dir === "asc" ? "ascending" : "descending");
      });
    });

    syncCounts();
    apply();
  }

  function initHeadingAnchors() {
    document
      .querySelectorAll(".detail-content h2[id], .detail-content h3[id]")
      .forEach((heading) => {
        if (heading.querySelector(".heading-anchor")) return;
        const link = document.createElement("a");
        link.className = "heading-anchor";
        link.href = "#" + heading.id;
        link.setAttribute("aria-label", "复制此节链接");
        link.textContent = "#";
        link.addEventListener("click", (e) => {
          e.preventDefault();
          const url = location.origin + location.pathname + "#" + heading.id;
          history.replaceState(null, "", "#" + heading.id);
          if (navigator.clipboard) {
            navigator.clipboard.writeText(url).then(
              () => showToast("链接已复制"),
              () => showToast("已跳转到本节")
            );
          } else {
            showToast("已跳转到本节");
          }
        });
        heading.prepend(link);
      });
  }

  function initTocScrollSpy() {
    const links = document.querySelectorAll(".toc a[href^='#']");
    if (!links.length) return;

    const map = new Map();
    links.forEach((a) => {
      const id = decodeURIComponent(a.getAttribute("href").slice(1));
      const target = document.getElementById(id);
      if (target) map.set(target, a);
    });

    if (!map.size) return;

    let current = null;
    const observer = new IntersectionObserver(
      (entries) => {
        entries.forEach((entry) => {
          if (entry.isIntersecting) {
            if (current) current.classList.remove("is-active");
            const link = map.get(entry.target);
            if (link) {
              link.classList.add("is-active");
              current = link;
            }
          }
        });
      },
      { rootMargin: "-30% 0px -60% 0px", threshold: [0, 1] }
    );

    map.forEach((_, target) => observer.observe(target));
  }

  window.matchMedia("(prefers-color-scheme: dark)").addEventListener("change", (e) => {
    if (!localStorage.getItem(THEME_KEY)) {
      applyTheme(e.matches ? "dark" : "light");
    }
  });

  document.addEventListener("DOMContentLoaded", () => {
    initThemeToggle();
    initOverviewTable();
    initHeadingAnchors();
    initTocScrollSpy();
  });
})();
