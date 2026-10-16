"""Build Aahad Rashid's dependency-free engineering portfolio website."""

from __future__ import annotations

import html
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent
PROJECTS = json.loads((ROOT / "content/projects.json").read_text(encoding="utf-8"))
MEDIA = json.loads((ROOT / "content/media.json").read_text(encoding="utf-8"))
EVIDENCE = json.loads((ROOT / "content/evidence.json").read_text(encoding="utf-8"))
SKILL_GROUPS = json.loads((ROOT / "content/skills.json").read_text(encoding="utf-8"))
BY_SLUG = {project["slug"]: project for project in PROJECTS}
NUMBER = {project["slug"]: index + 1 for index, project in enumerate(PROJECTS)}

NAME = "Aahad Rashid"
EMAIL = "aahadrashid540@gmail.com"
LINKEDIN = "https://www.linkedin.com/in/aahadrashid/"

MENU = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" aria-hidden="true"><path d="M4 7h16M4 12h16M4 17h16"/></svg>'


def e(value: object) -> str:
    return html.escape(str(value), quote=True)


def cover_for(slug: str, root: str, *, alt: str = "", eager: bool = False) -> str:
    info = MEDIA.get(slug)
    if not info:
        return '<span class="media-abstract" aria-hidden="true"><span></span></span>'
    loading = 'fetchpriority="high"' if eager else 'loading="lazy" decoding="async"'
    return f'<img src="{root}assets/media/{e(info["cover"])}" alt="{e(alt)}" {loading}>'


def page_shell(*, title: str, description: str, body: str, root: str = "", current: str = "") -> str:
    nav = "".join(
        f'<a href="{root}{href}"{" aria-current=\"page\"" if current == label else ""}>{label}</a>'
        for label, href in [
            ("Home", "index.html"),
            ("Projects", "projects/index.html"),
            ("Evidence", "evidence.html"),
            ("Skills", "skills.html"),
        ]
    )
    return f'''<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <meta name="theme-color" content="#101318">
  <meta name="description" content="{e(description)}">
  <title>{e(title)} | {NAME}</title>
  <link rel="icon" type="image/svg+xml" href="{root}assets/favicon.svg">
  <link rel="stylesheet" href="{root}assets/css/style.css?v=4">
  <noscript><style>@media(max-width:760px){{.menu-toggle{{display:none}}.site-nav{{display:flex;position:static;flex-wrap:wrap;width:100%;padding:.5rem 0;border:0;background:transparent}}.header-inner{{flex-wrap:wrap}}}}</style></noscript>
</head>
<body>
  <a class="skip-link" href="#main-content">Skip to main content</a>
  <header class="site-header">
    <div class="container header-inner">
      <a class="brand" href="{root}index.html" aria-label="Aahad Rashid, home"><span class="brand-symbol" aria-hidden="true">AR</span><span class="brand-type"><strong>AAHAD RASHID</strong><small>ENGINEERING PORTFOLIO</small></span></a>
      <button class="menu-toggle" type="button" data-menu-toggle aria-expanded="false" aria-controls="site-navigation" aria-label="Open navigation"><span data-menu-label>Menu</span>{MENU}</button>
      <nav class="site-nav" id="site-navigation" data-navigation aria-label="Main navigation">{nav}<a class="nav-contact" href="{root}index.html#contact">Contact</a></nav>
    </div>
  </header>
{body}
  <footer class="site-footer">
    <div class="container footer-main"><div><span class="footer-kicker">BUILD / MEASURE / IMPROVE</span><strong>Aahad Rashid</strong><p>Aspiring electrical engineer in Dubai, UAE.</p></div><div class="footer-nav"><a href="{root}projects/index.html">Projects</a><a href="{root}evidence.html">Evidence</a><a href="{root}skills.html">Skills</a><a href="mailto:{EMAIL}">Email</a><a href="{LINKEDIN}" rel="noopener noreferrer">LinkedIn</a></div></div>
    <div class="container footer-bottom"><span>© 2026 Aahad Rashid</span><span>Built as a record of real engineering work.</span></div>
  </footer>
  <script src="{root}assets/js/site.js?v=4" defer></script>
</body>
</html>'''


def project_card(project: dict, root: str, *, heading: int = 3, compact: bool = False) -> str:
    slug = project["slug"]
    cls = "project-card compact" if compact else "project-card"
    query = " ".join((project["title"], project["summary"], project["category"], project["period"])).lower()
    image = cover_for(slug, root)
    return f'''<a class="{cls}" href="{root}projects/{e(slug)}.html" data-project-card data-category="{e(project['category'])}" data-search="{e(query)}">
  <div class="project-card-image">{image}</div>
  <div class="project-card-copy"><div class="card-meta"><span>{e(project['category'])}</span><span>{e(project['period'])}</span></div><h{heading}>{e(project['title'])}</h{heading}><p>{e(project['summary'])}</p><span class="card-action">View project</span></div>
</a>'''


def render_home() -> str:
    featured = [BY_SLUG[slug] for slug in ("ev-grand-prix", "ev-telemetry", "ev-cad-scanning", "vex-robotics")]
    featured_html = "".join(project_card(p, "") for p in featured)
    systems = [
        ("01", "Electrical & powertrain", "The 48 V system, protection path and repair work.", "ev-electrical-powertrain"),
        ("02", "Telemetry", "Vehicle measurements and the finalized 2027 design.", "ev-telemetry"),
        ("03", "Digital model", "From the original scan to revised body geometry.", "ev-cad-scanning"),
        ("04", "Design & testing", "Packaging, airflow study and repeatable checks.", "ev-mechanical-testing"),
    ]
    systems_html = "".join(
        f'<a class="system-link" href="projects/{slug}.html"><span>{num} / SUBSYSTEM</span><strong>{title}</strong><p>{desc}</p><span class="system-link-cta">View details</span></a>'
        for num, title, desc, slug in systems
    )
    awards = [
        ("02", "Best Use of AI for Race Strategy"),
        ("03", "Promotion & Outreach"),
        ("03", "Social Media Outreach"),
        ("01", "Best Photo"),
    ]
    awards_html = "".join(f'<li><b>{place}</b><span>{name}</span></li>' for place, name in awards)
    experience = [BY_SLUG[slug] for slug in ("adnoc-placement", "qer-internship", "mbzuai-bootcamp")]
    experience_html = "".join(project_card(p, "", compact=True) for p in experience)
    body = f'''<main id="main-content" tabindex="-1">
  <section class="hero">
    <div class="container hero-grid">
      <div class="hero-copy"><p class="eyebrow"><span class="signal-dot" aria-hidden="true"></span> AAHAD RASHID / DUBAI, UAE</p><h1>Build. Measure.<br><em>Improve.</em></h1><p class="hero-lead">I’m an aspiring electrical engineer working on electric vehicles, telemetry, robotics and applied design. This is a record of what I built, tested and learned.</p><div class="hero-actions"><a class="button button-primary" href="projects/index.html">Explore the work</a><a class="button button-ghost" href="#about">Meet the engineer</a></div><div class="hero-note"><span>Current focus</span><a href="projects/ev-grand-prix.html">Electric Vehicle Grand Prix</a></div></div>
      <figure class="hero-visual">{cover_for("ev-grand-prix", "", alt="Aahad working beside the electric race car", eager=True)}<figcaption><span>01 / FIELD NOTES</span><span>Electric Vehicle Grand Prix · 2026</span></figcaption></figure>
    </div>
    <div class="container hero-tracks"><span>Electrical systems</span><span>Embedded data</span><span>Robotics</span><span>CAD & testing</span></div>
  </section>

  <section class="section selected-work" id="selected-work" aria-labelledby="selected-title"><div class="container"><div class="section-head"><div><p class="eyebrow">SELECTED CASE STUDIES</p><h2 id="selected-title">Engineering in the details.</h2><p>Start with the projects that best show my process, decisions and hands-on work.</p></div><a class="text-link" href="projects/index.html">Browse all work</a></div><div class="featured-grid">{featured_html}</div></div></section>

  <section class="section system-section" aria-labelledby="systems-title"><div class="container system-layout"><div class="system-intro"><p class="eyebrow">INSIDE THE RACE CAR</p><h2 id="systems-title">One vehicle.<br>Connected systems.</h2><p>My EVGP work is easiest to understand as a set of linked engineering problems. Open a subsystem for the design, the practical work and the evidence.</p><a class="text-link" href="projects/ev-grand-prix.html">Read the vehicle overview</a></div><div class="system-list">{systems_html}</div></div></section>

  <section class="section recognition" aria-labelledby="recognition-title"><div class="container recognition-layout"><div class="recognition-copy"><p class="eyebrow">2026 COMPETITION RESULTS</p><h2 id="recognition-title">Recognition backed by the work.</h2><p>At the Electric Vehicle Grand Prix in Karting Town, Sharjah, the team earned four awards. The car also placed third overall at the separate 2026 SABIS STEAM competition at SIS Yas Island, where it was highest ranked in the Unmodified category.</p><a class="text-link" href="evidence.html">View awards and certificates</a></div><ol class="award-list">{awards_html}</ol></div></section>

  <section class="section experience-section" aria-labelledby="experience-title"><div class="container"><div class="section-head"><div><p class="eyebrow">BEYOND THE BUILD</p><h2 id="experience-title">Learning across environments.</h2><p>Industry placements and an applied AI program added different ways to observe, test and communicate technical work.</p></div></div><div class="experience-grid">{experience_html}</div></div></section>

  <section class="section about-section" id="about" aria-labelledby="about-title"><div class="container about-layout"><div><p class="eyebrow">ABOUT ME</p><h2 id="about-title">Curiosity with a test plan.</h2><p>I’m interested in the point where electrical, mechanical and software systems meet. I like taking a problem from research and calculations to wiring, code or CAD, then checking the result against real behavior.</p><p>My strongest lessons came from faults, revisions and team work: tracing a broken power path, improving a signal, refining a robot mechanism and explaining a technical decision clearly.</p><a class="text-link" href="skills.html">Explore my skills</a></div><div class="process-panel"><div class="process-ring" aria-hidden="true"><span></span></div><ol><li><b>01</b><span>Understand the constraint</span></li><li><b>02</b><span>Build or model a solution</span></li><li><b>03</b><span>Measure what happens</span></li><li><b>04</b><span>Revise and verify</span></li></ol></div></div></section>

  <section class="contact-section" id="contact" aria-labelledby="contact-title"><div class="container contact-layout"><div><p class="eyebrow">CONTACT</p><h2 id="contact-title">Let’s talk engineering.</h2><p>For university programs, internships and technical collaboration.</p></div><div><a class="button button-light" href="mailto:{EMAIL}">Email Aahad</a><a class="contact-secondary" href="{LINKEDIN}" rel="noopener noreferrer">LinkedIn</a></div></div></section>
</main>'''
    return page_shell(title="Engineering Portfolio", description="Aahad Rashid's engineering portfolio: electric vehicles, telemetry, CAD, robotics, technical placements and applied AI.", body=body, current="Home")


def render_index() -> str:
    categories = ("all", "Engineering", "Robotics", "AI and Software", "Industry", "Leadership", "Service")
    filters = "".join(
        f'<option value="{e(cat)}">{"All categories" if cat=="all" else e(cat)}</option>'
        for cat in categories
    )
    cards = "".join(project_card(p, "../", heading=2) for p in PROJECTS)
    body = f'''<main id="main-content" tabindex="-1"><header class="page-hero"><div class="container"><p class="eyebrow">PROJECT LIBRARY</p><h1>Projects.</h1><p>Find a case study by topic, or search for a system, skill or activity.</p></div></header><section class="section index-section"><div class="container"><div class="index-toolbar"><div class="search-wrap"><label for="project-search">Search projects</label><input id="project-search" type="search" placeholder="Try telemetry, CAD or robotics" autocomplete="off" data-project-search></div><div class="filter-wrap"><label for="category-filter">Category</label><select id="category-filter" data-filter-select>{filters}</select></div></div><p class="results-count" data-results-count role="status" aria-live="polite"></p><div class="work-grid">{cards}</div><p class="no-results" data-no-results hidden>No projects match that search. Try a different term or category.</p></div></section></main>'''
    return page_shell(title="Projects", description="Explore Aahad Rashid's engineering projects, placements, skills and leadership activities.", body=body, root="../", current="Projects")


def render_skills() -> str:
    category_links = "".join(f'<a href="#{e(g["slug"])}">{e(g["title"])}</a>' for g in SKILL_GROUPS)
    sections = []
    for group in SKILL_GROUPS:
        cards = []
        for skill in group["skills"]:
            links = "".join(f'<a href="projects/{e(slug)}.html">{e(BY_SLUG[slug]["shortTitle"])}</a>' for slug in skill["projects"])
            cards.append(f'<article class="skill-card"><h3>{e(skill["name"])}</h3><p>{e(skill["detail"])}</p><div class="skill-evidence"><span>Shown in</span>{links}</div></article>')
        sections.append(f'<section class="skill-section" id="{e(group["slug"])}" aria-labelledby="{e(group["slug"])}-title"><div class="skill-group-heading"><p class="eyebrow">SKILL AREA</p><h2 id="{e(group["slug"])}-title">{e(group["title"])}</h2><p>{e(group["intro"])}</p></div><div class="skill-grid">{"".join(cards)}</div></section>')
    body = f'''<main id="main-content" tabindex="-1"><header class="page-hero skills-hero"><div class="container"><p class="eyebrow">SKILLS / EVIDENCE</p><h1>Skills built through <em>doing.</em></h1><p>Electrical work, telemetry, robotics, design and leadership. Each skill links to a project that shows where I used it; industry exposure is described as learning.</p></div></header><nav class="skills-nav" aria-label="Skill areas"><div class="container"><span>Jump to</span>{category_links}</div></nav><div class="container skill-sections">{"".join(sections)}</div><section class="skills-end"><div class="container"><p class="eyebrow">GO DEEPER</p><h2>See the skills in context.</h2><a class="button button-primary" href="projects/index.html">Browse the build log</a></div></section></main>'''
    return page_shell(title="Skills", description="Technical and practical skills developed by Aahad Rashid through engineering projects and placements.", body=body, current="Skills")


def render_evidence() -> str:
    jump = "".join(f'<a href="#proof-{i}">{e(group["title"])}</a>' for i, group in enumerate(EVIDENCE, 1))
    sections = []
    for i, group in enumerate(EVIDENCE, 1):
        cards = []
        for item in group["items"]:
            project = BY_SLUG[item["project"]]
            cards.append(
                f'<article class="proof-card"><a class="proof-image" href="assets/media/{e(item["file"])}" '
                f'target="_blank" rel="noopener noreferrer" aria-label="Open full-size image: {e(item["title"])}">'
                f'<img src="assets/media/{e(item["file"])}" alt="{e(item["title"])} — {e(item["detail"])}" '
                f'loading="lazy" decoding="async"></a><div class="proof-copy"><span>{e(project["category"])}</span>'
                f'<h3>{e(item["title"])}</h3><p>{e(item["detail"])}</p>'
                f'<a href="projects/{e(item["project"])}.html">Read the case study</a></div></article>'
            )
        sections.append(
            f'<section class="proof-group section" id="proof-{i}" aria-labelledby="proof-{i}-title"><div class="container">'
            f'<div class="section-head"><div><p class="eyebrow">{i:02d} / DOCUMENTED</p><h2 id="proof-{i}-title">{e(group["title"])}</h2>'
            f'<p>{e(group["intro"])}</p></div></div><div class="proof-grid">{"".join(cards)}</div></div></section>'
        )
    body = f'''<main id="main-content" tabindex="-1">
  <header class="page-hero evidence-hero"><div class="container"><p class="eyebrow">THE EVIDENCE</p><h1>Proof behind<br><em>the projects.</em></h1><p>Awards, certificates and engineering artifacts, each connected to the project behind it. Open any image at full size or follow its case study for context.</p></div></header>
  <nav class="skills-nav" aria-label="Evidence categories"><div class="container"><span>Jump to</span>{jump}</div></nav>
  {"".join(sections)}
  <section class="proof-video section" aria-labelledby="proof-video-title"><div class="container proof-video-layout"><div><p class="eyebrow">PROJECT IN MOTION</p><h2 id="proof-video-title">Learning Compass, demonstrated.</h2><p>A screen recording of the accessible learning website developed during the MBZUAI Hybrid Intelligence Bootcamp.</p><a class="text-link" href="projects/mbzuai-bootcamp.html">Read the bootcamp case study</a></div><video controls preload="metadata" aria-label="Learning Compass accessible learning website demonstration"><source src="assets/media/mbzuai-learning-compass-demo.mp4" type="video/mp4">Your browser does not support this video.</video></div></section>
  <section class="skills-end"><div class="container"><p class="eyebrow">GO DEEPER</p><h2>See how the work was done.</h2><a class="button button-primary" href="projects/index.html">Browse every case study</a></div></section>
</main>'''
    return page_shell(title="Evidence", description="Awards, certificates, photographs and engineering artifacts supporting Aahad Rashid's portfolio.", body=body, current="Evidence")


def render_media_item(item: dict) -> str:
    path = f'../assets/media/{e(item["file"])}'
    if item["file"].lower().endswith((".mp4", ".webm")):
        visual = f'<video controls preload="metadata" aria-label="{e(item["alt"])}"><source src="{path}">Your browser does not support this video.</video>'
    else:
        visual = f'<a href="{path}" target="_blank" rel="noopener noreferrer" aria-label="Open full image: {e(item["alt"])}"><img src="{path}" alt="{e(item["alt"])}" loading="lazy" decoding="async"></a>'
    file_lower = item["file"].lower()
    kind = " media-card-document" if any(word in file_lower for word in ("award", "certificate", "schematic", "diagram")) else ""
    return f'<figure class="media-card{kind}">{visual}<figcaption>{e(item["caption"])}</figcaption></figure>'


def render_system_map(slug: str) -> str:
    maps = {
        "ev-electrical-powertrain": ("48 V traction path", "Built and tested", ["Battery pack", "Kill switch + fuse", "Contactor + precharge", "Motor controller", "Rear motor"]),
        "ev-telemetry": ("2027 telemetry architecture", "Finalized design · planned for 2027", ["Vehicle signals", "ESP32-C3 + ADS1115", "Raspberry Pi 4B", "Cellular / GNSS", "Data for analysis"]),
        "ev-cad-scanning": ("Digital modelling workflow", "Design process", ["Physical car", "3D scan", "Original mesh", "Revised body", "Design review"]),
    }
    if slug not in maps:
        return ""
    title, status, steps = maps[slug]
    items = "".join(f'<li><span>{i:02d}</span><strong>{e(step)}</strong></li>' for i, step in enumerate(steps, 1))
    return f'<section class="system-map" aria-labelledby="system-map-title"><div class="container"><div><p class="eyebrow">SYSTEM VIEW</p><h2 id="system-map-title">{e(title)}</h2><p>{e(status)}</p></div><ol>{items}</ol></div></section>'


def render_project(project: dict) -> str:
    slug = project["slug"]
    info = MEDIA.get(slug)
    n = NUMBER[slug]
    title = e(project["title"])
    results = project["results"]
    evidence = ""
    if info:
        groups = []
        for group in info["groups"]:
            cards = "".join(render_media_item(item) for item in group["items"])
            if group.get("collapsed"):
                groups.append(f'<details class="gallery-group gallery-more"><summary><span>{e(group["title"])}</span><small>{len(group["items"])} more photographs</small></summary><div class="media-grid">{cards}</div></details>')
            else:
                groups.append(f'<section class="gallery-group" aria-label="{e(group["title"])}"><h3>{e(group["title"])}</h3><div class="media-grid">{cards}</div></section>')
        evidence = f'<section class="evidence-section" id="evidence" aria-labelledby="evidence-title"><div class="container"><div class="section-head"><div><p class="eyebrow">PROJECT EVIDENCE</p><h2 id="evidence-title">The work, documented.</h2><p>Photographs, diagrams and certificates from this project. Open an image to see it at full size.</p></div></div>{"".join(groups)}</div></section>'
    cover = cover_for(slug, "../", alt=info["coverAlt"] if info else "")
    contributions = "".join(f'<li><span>{i:02d}</span><p>{e(text)}</p></li>' for i, text in enumerate(project["contributions"], 1))
    technical = "".join(f'<article class="technical-note"><h3>{e(item["heading"])}</h3><p>{e(item["text"])}</p></article>' for item in project["technical"])
    result_html = ""
    if results:
        rows = "".join(f'<li>{e(row)}</li>' for row in results)
        result_html = f'<section class="detail-section" id="outcomes" aria-labelledby="outcomes-title"><div class="detail-section-heading"><span>04 / OUTCOMES</span><h2 id="outcomes-title">Results and recognition</h2></div><ul class="result-list">{rows}</ul></section>'
    sections = [("Overview", "overview"), ("My work", "contribution"), ("Technical notes", "technical")]
    if results: sections.append(("Outcomes", "outcomes"))
    if info: sections.append(("Evidence", "evidence"))
    jump = "".join(f'<a href="#{anchor}">{label}</a>' for label, anchor in sections)
    related = "".join(f'<a class="related-card" href="{e(BY_SLUG[s]["slug"])}.html"><span>{e(BY_SLUG[s]["category"])}</span><strong>{e(BY_SLUG[s]["title"])}</strong><small>View project</small></a>' for s in project["related"])
    system_links = ""
    if slug == "ev-grand-prix":
        systems = "".join(f'<a href="{e(s)}.html"><span>{i:02d}</span><strong>{e(BY_SLUG[s]["shortTitle"])}</strong><small>View system</small></a>' for i, s in enumerate(("ev-electrical-powertrain", "ev-telemetry", "ev-cad-scanning", "ev-mechanical-testing"), 1))
        system_links = f'<section class="ev-systems" aria-labelledby="ev-systems-title"><div class="container"><p class="eyebrow">EXPLORE THE CAR</p><h2 id="ev-systems-title">Four connected systems.</h2><div>{systems}</div></div></section>'
    body = f'''<main id="main-content" tabindex="-1">
  <div class="container breadcrumbs" aria-label="Breadcrumb"><a href="../index.html">Home</a><span aria-hidden="true">/</span><a href="index.html">Projects</a><span aria-hidden="true">/</span><span aria-current="page">{e(project['shortTitle'])}</span></div>
  <header class="detail-hero"><div class="container detail-hero-grid"><div class="detail-intro"><p class="eyebrow">BUILD {n:02d} / {e(project['category']).upper()}</p><h1>{title}</h1><p>{e(project['summary'])}</p><a class="text-link" href="#overview">Read the case study</a></div><figure class="detail-cover">{cover}<figcaption><span>{e(project['period'])}</span><span>{e(project['status'])}</span></figcaption></figure></div></header>
  <div class="detail-facts"><div class="container"><dl><div><dt>ROLE</dt><dd>{e(project['role'])}</dd></div><div><dt>PERIOD</dt><dd>{e(project['period'])}</dd></div><div><dt>STATUS</dt><dd>{e(project['status'])}</dd></div><div><dt>SETTING</dt><dd>{e(project['location'])}</dd></div></dl></div></div>
  <nav class="detail-jump" aria-label="On this page"><div class="container"><span>ON THIS PAGE</span>{jump}</div></nav>
  <div class="container detail-layout"><div class="detail-content"><section class="detail-section" id="overview" aria-labelledby="overview-title"><div class="detail-section-heading"><span>01 / CONTEXT</span><h2 id="overview-title">The project</h2></div><p class="overview-copy">{e(project['overview'])}</p></section><section class="detail-section" id="contribution" aria-labelledby="contribution-title"><div class="detail-section-heading"><span>02 / MY ROLE</span><h2 id="contribution-title">What I did</h2></div><ol class="contribution-list">{contributions}</ol></section><section class="detail-section" id="technical" aria-labelledby="technical-title"><div class="detail-section-heading"><span>03 / ENGINEERING NOTES</span><h2 id="technical-title">Technical detail</h2></div><div class="technical-list">{technical}</div></section>{result_html}</div></div>
  {render_system_map(slug)}
  {system_links}
  {evidence}
  <section class="related-section" aria-labelledby="related-title"><div class="container"><div class="section-head"><div><p class="eyebrow">CONTINUE EXPLORING</p><h2 id="related-title">Related work.</h2></div><a class="text-link" href="index.html">All projects</a></div><div class="related-grid">{related}</div></div></section>
</main>'''
    return page_shell(title=project["title"], description=project["summary"], body=body, root="../", current="Projects")


def validate() -> None:
    assert len(PROJECTS) == 18, "Expected 18 case studies"
    assert len(BY_SLUG) == len(PROJECTS), "Duplicate project slug"
    assert len({group["slug"] for group in SKILL_GROUPS}) == len(SKILL_GROUPS), "Duplicate skill group slug"
    for project in PROJECTS:
        assert all(slug in BY_SLUG and slug != project["slug"] for slug in project["related"]), project["slug"]
    for group in SKILL_GROUPS:
        for skill in group["skills"]:
            assert skill["projects"] and all(slug in BY_SLUG for slug in skill["projects"]), skill["name"]
    for slug, info in MEDIA.items():
        assert slug in BY_SLUG and info["groups"] and info["coverAlt"], slug
        assert Path(info["cover"]).suffix.lower() in {".jpg", ".jpeg", ".png", ".webp"}, info["cover"]
        assert (ROOT / "assets/media" / info["cover"]).is_file(), info["cover"]
        for group in info["groups"]:
            assert group["title"] and group["items"], slug
            for item in group["items"]:
                assert item["alt"] and item["caption"], item["file"]
                assert Path(item["file"]).suffix.lower() in {".jpg", ".jpeg", ".png", ".webp", ".mp4", ".webm"}, item["file"]
                assert (ROOT / "assets/media" / item["file"]).is_file(), item["file"]
    for group in EVIDENCE:
        assert group["title"] and group["intro"] and group["items"]
        for item in group["items"]:
            assert item["project"] in BY_SLUG, item
            assert (ROOT / "assets/media" / item["file"]).is_file(), item


def build() -> None:
    validate()
    (ROOT / "projects").mkdir(exist_ok=True)
    (ROOT / "index.html").write_text(render_home(), encoding="utf-8")
    (ROOT / "evidence.html").write_text(render_evidence(), encoding="utf-8")
    (ROOT / "skills.html").write_text(render_skills(), encoding="utf-8")
    (ROOT / "projects/index.html").write_text(render_index(), encoding="utf-8")
    for project in PROJECTS:
        (ROOT / "projects" / f"{project['slug']}.html").write_text(render_project(project), encoding="utf-8")
    print(f"Built home, evidence, skills, project index and {len(PROJECTS)} case studies")


if __name__ == "__main__":
    build()
