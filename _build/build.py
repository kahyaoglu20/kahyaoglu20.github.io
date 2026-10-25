"""Render the site from content.py.

    python _build/build.py

Writes index.html and projects/<slug>/index.html. Static output, no dependencies.
"""
from __future__ import annotations

import html
import json
from pathlib import Path

import content as C

ROOT = Path(__file__).resolve().parent.parent
P = C.PERSON
esc = html.escape

# ---- icons (24px, stroke) ------------------------------------------------------------
_ICON = {
    "github": '<path d="M9 19c-4.3 1.4-4.3-2.5-6-3m12 5v-3.5c0-1 .1-1.4-.5-2 2.8-.3 5.5-1.4 5.5-6a4.6 4.6 0 0 0-1.3-3.2 4.2 4.2 0 0 0-.1-3.2s-1.1-.3-3.5 1.3a12.3 12.3 0 0 0-6.2 0C6.5 2.8 5.4 3.1 5.4 3.1a4.2 4.2 0 0 0-.1 3.2A4.6 4.6 0 0 0 4 9.5c0 4.6 2.7 5.7 5.5 6-.6.6-.6 1.2-.5 2V21"/>',
    "file": '<path d="M14 3H6a2 2 0 0 0-2 2v14a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V9z"/><path d="M14 3v6h6M8 13h8M8 17h5"/>',
    "external": '<path d="M14 4h6v6M20 4 10 14M18 14v5a1 1 0 0 1-1 1H5a1 1 0 0 1-1-1V7a1 1 0 0 1 1-1h5"/>',
    "arrow": '<path d="M5 12h14M13 6l6 6-6 6"/>',
    "download": '<path d="M12 4v11M7 10l5 5 5-5M5 20h14"/>',
    "mail": '<rect x="3" y="5" width="18" height="14" rx="2"/><path d="m3 7 9 6 9-6"/>',
    "linkedin": '<rect x="3" y="3" width="18" height="18" rx="3"/><path d="M8 10v7M8 7v.01M12 17v-4a2 2 0 0 1 4 0v4M12 10v7"/>',
    "instagram": '<rect x="3" y="3" width="18" height="18" rx="5"/><circle cx="12" cy="12" r="4"/><path d="M17.5 6.5v.01"/>',
    "moon": '<path d="M20 14.5A8 8 0 0 1 9.5 4 8 8 0 1 0 20 14.5z"/>',
    "sun": '<circle cx="12" cy="12" r="4"/><path d="M12 2v2M12 20v2M4.9 4.9l1.4 1.4M17.7 17.7l1.4 1.4M2 12h2M20 12h2M4.9 19.1l1.4-1.4M17.7 6.3l1.4-1.4"/>',
    "menu": '<path d="M4 7h16M4 12h16M4 17h16"/>',
    "info": '<circle cx="12" cy="12" r="9"/><path d="M12 11v5M12 8v.01"/>',
    "play": '<circle cx="12" cy="12" r="9"/><path d="m10 8.5 5.5 3.5-5.5 3.5z"/>',
}


def icon(name: str, cls: str = "") -> str:
    c = f' class="{cls}"' if cls else ""
    return (f'<svg{c} viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" '
            f'stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">{_ICON[name]}</svg>')


FONTS = ("https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600&family=JetBrains+Mono:wght@500;600"
         "&family=Newsreader:ital,opsz,wght@0,6..72,400;0,6..72,500;0,6..72,600;1,6..72,400;1,6..72,500&display=swap")


def head(title: str, desc: str, base: str, path: str, image: str) -> str:
    url = C.SITE_URL + "/" + path
    person = {
        "@context": "https://schema.org", "@type": "Person", "name": P["name"],
        "jobTitle": "Mathematical Engineering student", "url": C.SITE_URL,
        "email": "mailto:" + P["email"],
        "affiliation": {"@type": "CollegeOrUniversity", "name": "İstanbul Technical University"},
        "sameAs": [P["github"], P["linkedin"], P["instagram"]],
    }
    return f"""<!doctype html>
<html lang="en" class="no-js">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{esc(title)}</title>
<meta name="description" content="{esc(desc)}">
<meta name="author" content="{esc(P['name'])}">
<link rel="canonical" href="{url}">
<meta property="og:type" content="website">
<meta property="og:title" content="{esc(title)}">
<meta property="og:description" content="{esc(desc)}">
<meta property="og:url" content="{url}">
<meta property="og:image" content="{C.SITE_URL}/{image}">
<meta name="twitter:card" content="summary_large_image">
<meta name="theme-color" content="#f8f7f3" media="(prefers-color-scheme: light)">
<meta name="theme-color" content="#0c0e12" media="(prefers-color-scheme: dark)">
<link rel="icon" href="{base}favicon.svg" type="image/svg+xml">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="{FONTS}">
<link rel="stylesheet" href="{base}assets/css/site.css">
<script>try{{var t=localStorage.getItem("theme");if(t==="light"||t==="dark")document.documentElement.dataset.theme=t}}catch(e){{}}</script>
<script type="application/ld+json">{json.dumps(person, ensure_ascii=False)}</script>
</head>
<body>
<a class="skip" href="#main">Skip to content</a>
"""


def navbar(base: str, home: bool) -> str:
    pre = "" if home else base
    items = [("about", "About"), ("research", "Research"), ("projects", "Projects"),
             ("notes", "Notes"), ("cv", "CV"), ("contact", "Contact")]
    li = "".join(f'<li><a href="{pre}#{i}">{t}</a></li>' if home else f'<li><a href="{pre}index.html#{i}">{t}</a></li>'
                 for i, t in items)
    return f"""<header class="nav">
  <div class="wrap">
    <a class="brand" href="{pre or './'}{'' if home else 'index.html'}#top" aria-label="Home">
      <span class="mono-mark">ÖK</span>
      <span>{esc(P['name'])}<small>Mathematical Engineering · ITU</small></span>
    </a>
    <ul class="nav-links" id="nav-links">{li}</ul>
    <button class="icon-btn theme-btn" type="button" aria-label="Toggle dark mode">{icon('moon', 'moon')}{icon('sun', 'sun')}</button>
    <button class="icon-btn menu-btn" type="button" aria-label="Menu" aria-controls="nav-links" aria-expanded="false">{icon('menu')}</button>
  </div>
</header>
"""


def footer(base: str) -> str:
    return f"""<footer class="site">
  <div class="wrap">
    <span>© 2026 {esc(P['name'])} · {esc(P['location'])}</span>
    <span><a href="{P['github']}/kahyaoglu20.github.io">Site source</a> · Built by hand, hosted on GitHub Pages</span>
  </div>
</footer>
<script src="{base}assets/js/site.js" defer></script>
</body>
</html>
"""


def status_badge(p) -> str:
    kind, label = p["status"]
    return f'<span class="badge {kind}">{esc(label)}</span>'


def link_buttons(p, base: str, small=True, primary_page=True) -> str:
    sm = " sm" if small else ""
    out = []
    if primary_page:
        out.append(f'<a class="btn primary{sm}" href="{base}projects/{p["slug"]}/">Read more {icon("arrow")}</a>')
    out.append(f'<a class="btn{sm}" href="{p["repo"]}">{icon("github")} Code</a>')
    label = "Manuscript" if p["kind"] == "research" else "Report"
    out.append(f'<a class="btn{sm}" href="{base}{p["pdf"]}">{icon("file")} {label}</a>')
    if "live" in p:
        out.append(f'<a class="btn{sm}" href="{base}{p["live"][1]}">{icon("play")} {esc(p["live"][0].replace("Open the ", "").capitalize())}</a>')
    return '<div class="btn-row">' + "".join(out) + "</div>"


def metrics_grid(metrics) -> str:
    return '<div class="metrics">' + "".join(
        f'<div class="metric"><b>{esc(v)}</b><span>{esc(k)}</span></div>' for v, k in metrics) + "</div>"


def chips(tags) -> str:
    return '<div class="chips">' + "".join(f'<span class="chip">{esc(t)}</span>' for t in tags) + "</div>"


# =========================================================================================
# Home page
# =========================================================================================
def home() -> str:
    b = ""
    research = [p for p in C.PROJECTS if p["kind"] == "research"]
    featured = next(p for p in C.PROJECTS if p.get("featured"))
    others = [p for p in C.PROJECTS if p["kind"] == "project" and not p.get("featured")]

    stats = "".join(f'<div class="stat"><b>{esc(n)}</b><span>{esc(l)}</span><small>{esc(s)}</small></div>'
                    for n, l, s in C.STATS)

    path = """
      <li><b>Electronics &amp; Communication Eng.</b><span>ITU · 2020 – 2024</span><p>Circuits, digital systems, computer architecture; 169 ECTS.</p></li>
      <li><b>Lateral transfer</b><span>2024</span><p>From building the hardware to understanding the mathematics it runs.</p></li>
      <li class="now"><b>Mathematical Engineering</b><span>ITU · final year · graduating 2027</span><p>Graduation project on the statistics of generative-model evaluation.</p></li>
      <li class="next"><b>M.Sc. → Ph.D.</b><span>next</span><p>The mathematics of AI, in academia and in a research-driven venture.</p></li>"""

    principles = "".join(
        f'<div class="principle reveal"><span class="k">{i:02d}</span><h4>{esc(t)}</h4><p>{esc(d)}</p></div>'
        for i, (t, d) in enumerate(C.PRINCIPLES, 1))

    papers = ""
    for p in research:
        extra = ""
        if "pdf2" in p:
            extra = f'<a class="btn sm" href="{p["pdf2"][1]}">{icon("file")} {esc(p["pdf2"][0])}</a>'
        btns = link_buttons(p, b).replace("</div>", extra + "</div>", 1) if extra else link_buttons(p, b)
        papers += f"""
      <article class="paper reveal" id="{p['slug']}">
        <a class="thumb" href="projects/{p['slug']}/" aria-label="{esc(p['short'])}: project page"><img src="assets/img/{p['page']}" alt="First page of the manuscript" loading="lazy" width="1100" height="1424"></a>
        <div>
          <div class="meta">{status_badge(p)}<span class="ctx">{esc(p['context'])}</span></div>
          <h3><a href="projects/{p['slug']}/">{esc(p['title'])}</a></h3>
          <p class="sub">{esc(p['card'])}</p>
          {metrics_grid(p['metrics'])}
          {chips(p['tags'])}
          {btns}
        </div>
      </article>"""

    f = featured
    strip = "".join(
        f'<button type="button" data-zoom="assets/img/{src}" data-caption="{esc(cap)}" aria-label="Enlarge: {esc(cap)}"><img src="assets/img/{src}" alt="{esc(cap)}" loading="lazy"></button>'
        for src, cap in f["figures"][:3])
    feat = f"""
      <article class="featured reveal" id="{f['slug']}">
        <a class="shot" href="projects/{f['slug']}/"><img src="assets/img/{f['cover']}" alt="MTH Tracker interactive simulator" loading="lazy" width="1800" height="1095"><span class="label">python -m mth_tracker gui</span></a>
        <div class="body">
          <div class="meta">{status_badge(f)}</div>
          <h3><a href="projects/{f['slug']}/">{esc(f['short'])}</a></h3>
          <p>{esc(f['card'])}</p>
          {metrics_grid(f['metrics'])}
          {link_buttons(f, b)}
        </div>
        <div class="strip">{strip}</div>
      </article>"""

    cards = ""
    for p in others:
        kp = "".join(f'<div><b>{esc(v)}</b><span>{esc(k)}</span></div>' for v, k in p["metrics"][:2])
        contain = "" if p["slug"] == "char-gpt" else " contain"
        cards += f"""
      <article class="card reveal" id="{p['slug']}">
        <a class="cover{contain}" href="projects/{p['slug']}/"><img src="assets/img/{p['cover']}" alt="{esc(p['short'])}" loading="lazy"></a>
        <div class="body">
          <div class="meta">{status_badge(p)}</div>
          <h3><a href="projects/{p['slug']}/">{esc(p['title'])}</a></h3>
          <p>{esc(p['card'])}</p>
          <div class="kpis">{kp}</div>
          {link_buttons(p, b)}
        </div>
      </article>"""

    n = C.NOTES
    steps = "".join(f'<div class="step"><div><b>{esc(t)}</b><span>{esc(d)}</span></div></div>' for t, d in n["steps"])
    other = "".join(f'<article class="reveal"><h4>{esc(t)}</h4><span class="when">{esc(w)}</span><p>{esc(d)}</p></article>'
                    for t, w, d in C.OTHER_WORK)

    def entries(items):
        return "".join(f'<li class="entry"><time>{esc(d)}</time><div><b>{esc(t)}</b><em>{esc(o)}</em><p>{esc(x)}</p></div></li>'
                       for d, t, o, x in items)

    skills = "".join(f'<div><h4>{esc(h)}</h4><ul>' + "".join(f"<li>{esc(s)}</li>" for s in items) + "</ul></div>"
                     for h, items in C.SKILLS)
    langs = "".join(f"<div><b>{esc(l)}</b><span>{esc(v)}</span></div>" for l, v in C.LANGUAGES)
    interests = chips(C.INTERESTS)

    return head(f"{P['name']} — Mathematical Engineering · Mathematics of AI",
                "Portfolio of Ömer Kahyaoğlu, final-year Mathematical Engineering student at İstanbul Technical "
                "University working on the mathematics of AI: research preprints, projects, notes and CV.",
                b, "", "assets/img/og.png") + navbar(b, True) + f"""
<main id="main">
  <section class="hero" id="top">
    <div class="wrap">
      <div class="hero-grid">
        <div>
          <div class="eyebrow">{esc(C.HERO['eyebrow'])}</div>
          <h1>Ömer <span class="accent">Kahyaoğlu</span></h1>
          <p class="role">{esc(P['role'])}</p>
          <p class="lead">{esc(C.HERO['lead'])}</p>
          <div class="btn-row">
            <a class="btn primary" href="#research">View research {icon('arrow')}</a>
            <a class="btn" href="{P['cv']}" download>{icon('download')} Download CV</a>
            <a class="btn" href="{P['github']}">{icon('github')} GitHub</a>
          </div>
          <div class="socials">
            <a class="icon-btn" href="mailto:{P['email']}" aria-label="Email">{icon('mail')}</a>
            <a class="icon-btn" href="{P['linkedin']}" aria-label="LinkedIn">{icon('linkedin')}</a>
            <a class="icon-btn" href="{P['instagram']}" aria-label="Instagram">{icon('instagram')}</a>
            <a class="icon-btn" href="{P['github']}" aria-label="GitHub">{icon('github')}</a>
          </div>
        </div>
        <figure class="matrix-card" style="margin:0">
          <canvas id="lowrank" role="img" aria-label="Animated decomposition of a data matrix X into a low-rank background L and a sparse target matrix S"></canvas>
          <figcaption class="matrix-caption">Robust PCA separates a slowly changing background from sparse moving targets. My <a href="projects/abksvd-rpca/">absorption analysis</a> asks what happens when a target stops.</figcaption>
        </figure>
      </div>
      <div class="stats">{stats}</div>
    </div>
  </section>

  <section class="block" id="about">
    <div class="wrap">
      <div class="section-head">
        <div class="num"><b>01</b> / About</div>
        <div><h2>From microchips to the mathematics of learning</h2>
        <p>Who I am, why I changed course, and where I am going.</p></div>
      </div>
      <div class="about-grid">
        <div class="spacer"></div>
        <div class="story">{''.join(f'<p>{s}</p>' for s in C.STORY)}</div>
        <aside>
          <div class="side-card"><h3>Path</h3><ol class="path">{path}</ol></div>
          <div class="side-card"><h3>Research interests</h3>{interests}</div>
        </aside>
      </div>
      <div class="principles">{principles}</div>
    </div>
  </section>

  <section class="block tint" id="research">
    <div class="wrap">
      <div class="section-head">
        <div class="num"><b>02</b> / Research</div>
        <div><h2>Manuscripts in preparation</h2>
        <p>Two single-author manuscripts, each released with the complete code, raw results and the scripts that regenerate every number, table and figure.</p></div>
      </div>
      {papers}
      <div class="notice reveal">{icon('info')}<span><strong>Work in progress.</strong> Both manuscripts are preprints that have not yet been peer-reviewed or reviewed by my advisor. Methods, results and wording may change before submission.</span></div>
    </div>
  </section>

  <section class="block" id="projects">
    <div class="wrap">
      <div class="section-head">
        <div class="num"><b>03</b> / Projects</div>
        <div><h2>Projects and course work</h2>
        <p>Software I designed, tested and documented: estimation and tracking, a GPT built from first principles, and a controlled study of class imbalance.</p></div>
      </div>
      {feat}
      <div class="cards">{cards}</div>
    </div>
  </section>

  <section class="block tint" id="notes">
    <div class="wrap">
      <div class="section-head">
        <div class="num"><b>04</b> / Notes &amp; other work</div>
        <div><h2>{esc(n['title'])}</h2>
        <p>A personal and educational project: turning lecture notes into structured, typeset course documents.</p></div>
      </div>
      <div class="notes">
        <div>
          <div class="doc-stack" aria-hidden="true">
            <div class="doc"><h5>Chapter 3 · Spectral Theorem</h5><i></i><i class="m"></i><i class="s"></i><div class="eq">A = QΛQ<sup>⊤</sup></div><i></i><i class="m"></i><i></i><i class="s"></i></div>
            <div class="doc"><h5>Lecture 7 · Martingales</h5><i class="m"></i><i></i><div class="eq">E[X<sub>n+1</sub> | 𝓕<sub>n</sub>] = X<sub>n</sub></div><i></i><i class="s"></i><i class="m"></i><i></i></div>
            <div class="doc"><h5>Week 5 · KKT Conditions</h5><i></i><i class="s"></i><i class="m"></i><div class="eq">∇f + Σ λ<sub>i</sub>∇g<sub>i</sub> = 0</div><i></i><i class="m"></i><i class="s"></i></div>
          </div>
          <div class="story">{''.join(f'<p>{s}</p>' for s in n['body'])}</div>
          {chips(n['areas'])}
        </div>
        <div class="steps">{steps}</div>
      </div>
      <div class="other">{other}</div>
    </div>
  </section>

  <section class="block" id="cv">
    <div class="wrap">
      <div class="section-head">
        <div class="num"><b>05</b> / Curriculum vitae</div>
        <div><h2>Education and experience</h2>
        <p>The short version is below; the full CV is available as a PDF.</p></div>
      </div>
      <div class="cv-grid">
        <div class="reveal"><h3>Education</h3><ul class="entries">{entries(C.EDUCATION)}</ul></div>
        <div class="reveal"><h3>Experience</h3><ul class="entries">{entries(C.EXPERIENCE)}</ul></div>
      </div>
      <div class="skills reveal">{skills}</div>
      <div class="cv-foot reveal">
        <div class="langs">{langs}</div>
        <a class="btn primary" href="{P['cv']}" download>{icon('download')} Download full CV (PDF)</a>
      </div>
    </div>
  </section>

  <section class="block tint" id="contact">
    <div class="wrap contact">
      <div>
        <div class="eyebrow">06 / Contact</div>
        <h2 style="margin-top:14px">Let's talk about the <em>mathematics</em> of AI.</h2>
        <p>I am looking for graduate positions, research collaborations and teams working on the foundations of machine learning. I am happy to share code, data or notes on request.</p>
        <a class="btn primary" href="mailto:{P['email']}">{icon('mail')} {esc(P['email'])}</a>
      </div>
      <div class="links">
        <a class="link-row" href="mailto:{P['email']}">{icon('mail')}<b>Email</b><span>{esc(P['email'])}</span></a>
        <a class="link-row" href="mailto:{P['email_academic']}">{icon('mail')}<b>Academic email</b><span>{esc(P['email_academic'])}</span></a>
        <a class="link-row" href="{P['linkedin']}">{icon('linkedin')}<b>LinkedIn</b><span>in/omerkahyaoglu</span></a>
        <a class="link-row" href="{P['github']}">{icon('github')}<b>GitHub</b><span>kahyaoglu20</span></a>
        <a class="link-row" href="{P['instagram']}">{icon('instagram')}<b>Instagram</b><span>@omerkahyaoglu_</span></a>
      </div>
    </div>
  </section>
</main>
""" + footer(b)


# =========================================================================================
# Project pages
# =========================================================================================
def project(p, prev, nxt) -> str:
    b = "../../"
    dark_shots = {"mth-tracker/gui_urban.webp", "mth-tracker/gui_zigzag.webp", "mth-tracker/gui_default.webp",
                  "abksvd-rpca/console.webp", "char-gpt/atlas.webp"}
    hero_src = p["cover"]
    hero_cls = "p-hero" if hero_src in dark_shots else "p-hero pad"

    aside_btns = [f'<a class="btn primary" href="{p["repo"]}">{icon("github")} View code on GitHub</a>',
                  f'<a class="btn" href="{b}{p["pdf"]}">{icon("file")} {"Read the manuscript" if p["kind"] == "research" else "Read the report"}</a>']
    if "pdf2" in p:
        aside_btns.append(f'<a class="btn" href="{b}{p["pdf2"][1]}">{icon("file")} {esc(p["pdf2"][0])}</a>')
    if "live" in p:
        aside_btns.append(f'<a class="btn" href="{b}{p["live"][1]}">{icon("play")} {esc(p["live"][0])}</a>')
    metric_list = "".join(f"<div><b>{esc(v)}</b><span>{esc(k)}</span></div>" for v, k in p["metrics"])

    notice = ""
    if p["status"][0] == "preprint":
        notice = (f'<div class="notice">{icon("info")}<span><strong>Preprint, work in progress.</strong> '
                  "This manuscript has not yet been peer-reviewed or reviewed by my advisor; its methods, "
                  "results and wording may change. Please cite it as a preprint.</span></div>")

    table = ""
    if "results_table" in p:
        t = p["results_table"]
        table = ('<section><h2>Results</h2><div class="table-wrap"><table><thead><tr>'
                 + "".join(f"<th>{esc(h)}</th>" for h in t["head"]) + "</tr></thead><tbody>"
                 + "".join("<tr>" + "".join(f"<td>{c}</td>" for c in r) + "</tr>" for r in t["rows"])
                 + f'</tbody></table></div><p class="table-note">{esc(t["note"])}</p></section>')

    sample = ""
    if "sample" in p:
        sample = f'<section><h2>A sample</h2><p class="sample">{esc(p["sample"])}</p><p class="table-note">200-character sample from the MATLAB model, prompt “ROMEO: ”, temperature 1.</p></section>'

    figs = ""
    for i, (src, cap) in enumerate([f for f in p["figures"] if f[0] != hero_src], 1):
        wide = ""
        dark = " dark" if src in dark_shots else ""
        figs += (f'<figure class="reveal{wide}{dark}"><button type="button" data-zoom="{b}assets/img/{src}" data-caption="{esc(cap)}" '
                 f'aria-label="Enlarge figure {i}"><img src="{b}assets/img/{src}" alt="{esc(cap)}" loading="lazy"></button>'
                 f"<figcaption><b>Fig. {i}</b>{esc(cap)}</figcaption></figure>")
    gallery_title = p.get("gallery_lead", "Figures")

    code = "".join(f'<span class="p">$ </span>{esc(line)}\n' if not line.startswith(" ") else esc(line) + "\n"
                   for line in p["code"].splitlines())
    cite = ""
    if "bibtex" in p:
        cite = (f'<section><h2>Cite</h2><div class="cite"><button class="copy" type="button" data-copy="bib-{p["slug"]}">Copy</button>'
                f'<pre class="code" id="bib-{p["slug"]}">{esc(p["bibtex"])}</pre></div></section>')
    credit = f'<p class="credit">{esc(p["credit"])}</p>' if "credit" in p else ""

    pn = ""
    if prev:
        pn += f'<a href="{b}projects/{prev["slug"]}/"><span>← Previous</span><b>{esc(prev["short"])}</b></a>'
    else:
        pn += f'<a href="{b}index.html#research"><span>← Back</span><b>All work</b></a>'
    if nxt:
        pn += f'<a class="next" href="{b}projects/{nxt["slug"]}/"><span>Next →</span><b>{esc(nxt["short"])}</b></a>'
    else:
        pn += f'<a class="next" href="{b}index.html#contact"><span>Next →</span><b>Get in touch</b></a>'

    section_name = "Research" if p["kind"] == "research" else "Projects"
    anchor = "research" if p["kind"] == "research" else "projects"
    return head(f"{p['short']} — {P['name']}", p["card"], b, f"projects/{p['slug']}/",
                f"assets/img/{p['cover']}") + navbar(b, False) + f"""
<main id="main">
  <div class="wrap">
    <nav class="crumbs" aria-label="Breadcrumb"><a href="{b}index.html">Home</a> / <a href="{b}index.html#{anchor}">{section_name}</a> / {esc(p['short'])}</nav>
    <header class="p-head">
      <div class="meta">{status_badge(p)}<span class="ctx">{esc(p['context'])}</span></div>
      <h1>{esc(p['title'])}</h1>
      <p class="sub">{esc(p['subtitle'])}</p>
      <div class="chips">{''.join(f'<span class="chip">{esc(t)}</span>' for t in p['tags'])}</div>
      {notice}
    </header>
    <div class="{hero_cls}"><img src="{b}assets/img/{hero_src}" alt="{esc(p['figures'][0][1])}"></div>
    <div class="p-body">
      <div>
        <section class="prose"><h2>Overview</h2>{''.join(f'<p>{x}</p>' for x in p['overview'])}</section>
        <section><h2>What I built</h2><ul class="ticks">{''.join(f'<li>{x}</li>' for x in p['built'])}</ul></section>
        {table}
        {sample}
        <section><h2>{esc(gallery_title)}</h2><div class="gallery">{figs}</div></section>
        <section><h2>Run it</h2><pre class="code">{code}</pre></section>
        {cite}
      </div>
      <aside class="p-aside">
        <div class="metric-list">{metric_list}</div>
        {''.join(aside_btns)}
        {credit}
      </aside>
    </div>
    <nav class="pn" aria-label="More projects">{pn}</nav>
  </div>
</main>
""" + footer(b)


def main() -> None:
    (ROOT / "index.html").write_text(home(), encoding="utf-8", newline="\n")
    order = [p for p in C.PROJECTS if p["kind"] == "research"] + [p for p in C.PROJECTS if p["kind"] == "project"]
    for i, p in enumerate(order):
        out = ROOT / "projects" / p["slug"] / "index.html"
        out.parent.mkdir(parents=True, exist_ok=True)
        out.write_text(project(p, order[i - 1] if i else None, order[i + 1] if i + 1 < len(order) else None),
                       encoding="utf-8", newline="\n")
    print("built", 1 + len(order), "pages")


if __name__ == "__main__":
    main()
