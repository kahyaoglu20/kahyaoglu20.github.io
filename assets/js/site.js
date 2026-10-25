// Ömer Kahyaoğlu — portfolio interactions. No dependencies.
(() => {
  const root = document.documentElement;
  root.classList.remove("no-js");
  const store = {
    get(k) { try { return localStorage.getItem(k); } catch { return null; } },
    set(k, v) { try { localStorage.setItem(k, v); } catch { /* storage unavailable */ } },
  };

  // ---- theme ------------------------------------------------------------------
  const saved = store.get("theme");
  if (saved === "light" || saved === "dark") root.dataset.theme = saved;
  const prefersDark = matchMedia("(prefers-color-scheme: dark)");
  const isDark = () => root.dataset.theme ? root.dataset.theme === "dark" : prefersDark.matches;
  document.querySelectorAll(".theme-btn").forEach((b) => b.addEventListener("click", () => {
    root.dataset.theme = isDark() ? "light" : "dark";
    store.set("theme", root.dataset.theme);
    window.dispatchEvent(new Event("themechange"));
  }));
  prefersDark.addEventListener?.("change", () => window.dispatchEvent(new Event("themechange")));

  // ---- navigation -------------------------------------------------------------
  const nav = document.querySelector(".nav");
  const links = document.querySelector(".nav-links");
  const menu = document.querySelector(".menu-btn");
  menu?.addEventListener("click", () => {
    const open = links.classList.toggle("open");
    menu.setAttribute("aria-expanded", String(open));
  });
  links?.addEventListener("click", (e) => {
    if (e.target.closest("a")) { links.classList.remove("open"); menu?.setAttribute("aria-expanded", "false"); }
  });
  const onScroll = () => nav?.classList.toggle("scrolled", scrollY > 8);
  addEventListener("scroll", onScroll, { passive: true });
  onScroll();

  const sections = [...document.querySelectorAll("main section[id]")];
  const navMap = new Map([...document.querySelectorAll('.nav-links a[href^="#"]')].map((a) => [a.getAttribute("href").slice(1), a]));
  if (sections.length && navMap.size && "IntersectionObserver" in window) {
    const seen = new Map();
    const io = new IntersectionObserver((entries) => {
      entries.forEach((en) => seen.set(en.target.id, en.isIntersecting ? en.intersectionRatio : 0));
      let best = null, ratio = 0;
      seen.forEach((r, id) => { if (r > ratio && navMap.has(id)) { ratio = r; best = id; } });
      navMap.forEach((a, id) => a.classList.toggle("active", id === best));
    }, { rootMargin: "-30% 0px -55% 0px", threshold: [0, .01, .2, .5] });
    sections.forEach((s) => io.observe(s));
  }

  // ---- reveal on scroll ---------------------------------------------------------
  const reveals = document.querySelectorAll(".reveal");
  if ("IntersectionObserver" in window && !matchMedia("(prefers-reduced-motion: reduce)").matches) {
    const ro = new IntersectionObserver((entries) => entries.forEach((en) => {
      if (en.isIntersecting) { en.target.classList.add("in"); ro.unobserve(en.target); }
    }), { rootMargin: "0px 0px -8% 0px" });
    reveals.forEach((el) => ro.observe(el));
  } else reveals.forEach((el) => el.classList.add("in"));

  // ---- lightbox -----------------------------------------------------------------
  const box = document.createElement("div");
  box.className = "lightbox";
  box.setAttribute("role", "dialog");
  box.setAttribute("aria-modal", "true");
  box.innerHTML = '<button class="close" aria-label="Close">×</button><div><img alt=""><p></p></div>';
  document.body.appendChild(box);
  const boxImg = box.querySelector("img"), boxCap = box.querySelector("p");
  let lastFocus = null;
  const close = () => { box.classList.remove("open"); lastFocus?.focus(); };
  document.addEventListener("click", (e) => {
    const t = e.target.closest("[data-zoom]");
    if (!t) return;
    lastFocus = t;
    boxImg.src = t.dataset.zoom;
    boxImg.alt = t.dataset.caption || "";
    boxCap.textContent = t.dataset.caption || "";
    box.classList.add("open");
    box.querySelector(".close").focus();
  });
  box.addEventListener("click", close);
  addEventListener("keydown", (e) => { if (e.key === "Escape" && box.classList.contains("open")) close(); });

  // ---- copy buttons -------------------------------------------------------------
  document.querySelectorAll("[data-copy]").forEach((btn) => btn.addEventListener("click", async () => {
    const text = document.getElementById(btn.dataset.copy)?.innerText ?? "";
    try { await navigator.clipboard.writeText(text); btn.textContent = "Copied"; }
    catch { btn.textContent = "Select & copy"; }
    setTimeout(() => (btn.textContent = "Copy"), 1600);
  }));

  // ---- hero: X = L + S --------------------------------------------------------------
  const canvas = document.getElementById("lowrank");
  if (canvas) heroMatrices(canvas);

  function heroMatrices(cv) {
    const ctx = cv.getContext("2d");
    const ROWS = 12, COLS = 12;
    const still = matchMedia("(prefers-reduced-motion: reduce)").matches;
    let W = 0, H = 0, dpr = 1, colors = {}, running = true, t0 = performance.now();

    const css = (n) => getComputedStyle(root).getPropertyValue(n).trim();
    const readColors = () => { colors = { ink: css("--ink"), muted: css("--muted"), line: css("--line"), bg: css("--bg"), accent: css("--accent"), amber: css("--amber") }; };
    const hexA = (c, a) => {
      if (c.startsWith("#")) {
        const n = parseInt(c.slice(1), 16);
        return `rgba(${n >> 16 & 255},${n >> 8 & 255},${n & 255},${a})`;
      }
      return c.replace(/rgba?\(([^)]+)\)/, (_, v) => `rgba(${v.split(",").slice(0, 3).join(",")},${a})`);
    };
    const size = () => {
      dpr = Math.min(devicePixelRatio || 1, 2);
      W = cv.clientWidth;
      const gap = W * 0.085, panel = (W - 2 * gap) / 3;
      H = panel * ROWS / COLS + 46;
      cv.style.height = H + "px";
      cv.width = Math.round(W * dpr); cv.height = Math.round(H * dpr);
      ctx.setTransform(dpr, 0, 0, dpr, 0, 0);
    };

    // A rank-2 background drifting slowly, a target moving through it, and sparse flicker.
    const frame = (t) => {
      const s = t / 1000;
      const L = [], S = [];
      for (let i = 0; i < ROWS; i++) {
        L.push([]); S.push([]);
        for (let j = 0; j < COLS; j++) {
          const u1 = Math.sin(i / ROWS * Math.PI), v1 = 0.55 + 0.45 * Math.cos(j / COLS * 2.2 + s * 0.35);
          const u2 = Math.cos(i / ROWS * 4.0 + s * 0.22), v2 = Math.sin(j / COLS * 3.1 - s * 0.18);
          L[i].push(Math.max(0, Math.min(1, 0.62 * u1 * v1 + 0.22 * u2 * v2 + 0.14)));
          S[i].push(0);
        }
      }
      const path = (s * 1.35) % (COLS + 6) - 3;
      const row = Math.round(ROWS / 2 + Math.sin(s * 0.7) * 2.2);
      for (let di = -1; di <= 0; di++) for (let dj = -1; dj <= 1; dj++) {
        const i = row + di, j = Math.round(path) + dj;
        if (i >= 0 && i < ROWS && j >= 0 && j < COLS) S[i][j] = 0.95;
      }
      const tick = Math.floor(s * 2.5);
      for (let k = 0; k < 4; k++) {
        const h = Math.sin((tick + k * 17) * 12.9898) * 43758.5453;
        const r = Math.floor((h - Math.floor(h)) * ROWS), c = Math.floor(((h * 7) - Math.floor(h * 7)) * COLS);
        S[r][c] = Math.max(S[r][c], 0.65);
      }
      return { L, S };
    };

    const draw = (t) => {
      const { L, S } = frame(t);
      ctx.clearRect(0, 0, W, H);
      const gap = W * 0.085, panel = (W - 2 * gap) / 3, cell = panel / COLS, ph = cell * ROWS;
      const panels = [
        { x: 0, label: "X", sub: "observed frames", f: (i, j) => [L[i][j], S[i][j]] },
        { x: panel + gap, label: "L", sub: "low-rank background", f: (i, j) => [L[i][j], 0] },
        { x: 2 * (panel + gap), label: "S", sub: "sparse targets", f: (i, j) => [0, S[i][j]] },
      ];
      const r = Math.max(1, cell * 0.16);
      panels.forEach((p) => {
        for (let i = 0; i < ROWS; i++) for (let j = 0; j < COLS; j++) {
          const [l, sp] = p.f(i, j);
          const x = p.x + j * cell + 1, y = i * cell + 1, w = cell - 2;
          ctx.fillStyle = hexA(colors.line, 0.55);
          roundRect(x, y, w, w, r); ctx.fill();
          if (l > 0) { ctx.fillStyle = hexA(colors.accent, 0.12 + 0.78 * l); roundRect(x, y, w, w, r); ctx.fill(); }
          if (sp > 0) { ctx.fillStyle = hexA(colors.amber, sp); roundRect(x, y, w, w, r); ctx.fill(); }
        }
        ctx.fillStyle = colors.ink;
        ctx.font = `italic 500 ${Math.round(Math.max(18, W * 0.034))}px Newsreader, Georgia, serif`;
        ctx.textAlign = "center"; ctx.textBaseline = "alphabetic";
        ctx.fillText(p.label, p.x + panel / 2, ph + 24);
        ctx.fillStyle = colors.muted;
        ctx.font = `500 ${Math.round(Math.max(9.5, W * 0.0165))}px "JetBrains Mono", Consolas, monospace`;
        ctx.fillText(p.sub.toUpperCase(), p.x + panel / 2, ph + 42);
      });
      ctx.fillStyle = colors.muted;
      ctx.font = `400 ${Math.round(Math.max(22, W * 0.062))}px Newsreader, Georgia, serif`;
      ctx.textBaseline = "middle";
      ctx.fillText("=", panel + gap / 2, ph / 2);
      ctx.fillText("+", 2 * panel + 1.5 * gap, ph / 2);
    };
    function roundRect(x, y, w, h, r) {
      ctx.beginPath();
      ctx.moveTo(x + r, y); ctx.arcTo(x + w, y, x + w, y + h, r); ctx.arcTo(x + w, y + h, x, y + h, r);
      ctx.arcTo(x, y + h, x, y, r); ctx.arcTo(x, y, x + w, y, r); ctx.closePath();
    }

    const loop = (now) => { if (running) { draw(now - t0); requestAnimationFrame(loop); } };
    readColors(); size(); draw(9000);
    addEventListener("resize", () => { size(); draw(performance.now() - t0); });
    addEventListener("themechange", () => { readColors(); draw(performance.now() - t0); });
    document.fonts?.ready.then(() => draw(performance.now() - t0));
    if (still) return;
    new IntersectionObserver(([en]) => {
      const was = running; running = en.isIntersecting && !document.hidden;
      if (running && !was) requestAnimationFrame(loop);
    }).observe(cv);
    document.addEventListener("visibilitychange", () => {
      const was = running; running = !document.hidden;
      if (running && !was) requestAnimationFrame(loop);
    });
    requestAnimationFrame(loop);
  }
})();
