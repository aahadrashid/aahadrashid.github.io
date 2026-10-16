# Aahad Rashid — Engineering Portfolio

A responsive portfolio site for university applications, internships and other engineering opportunities. It includes a home page, searchable project index, evidence library, skills page and a case study for every listed activity. The electric race car also has separate pages for powertrain, telemetry, CAD and testing.

The design takes restrained inspiration from Aahad's portfolio PDF: graphite surfaces, warm metal lines, a red accent and a technical build-log structure. The PDF is still in progress, so this site omits its unfinished placeholders. The 2027 telemetry architecture is described as a finalized design planned for use in 2027.

## Open the website

1. Open this folder in VS Code.
2. Run `python -m http.server 5500` in VS Code's terminal.
3. Open `http://localhost:5500/` in your browser.

You can also open `index.html` directly from File Explorer. No packages or accounts are needed.

## Edit content

- `content/projects.json`: titles, roles, technical notes and results.
- `content/skills.json`: skill descriptions and the projects that demonstrate them.
- `content/media.json`: project image groups, captions and alternative text.
- `content/evidence.json`: the evidence library's awards, certificates and engineering artifacts.
- `assets/media/`: copied project photographs, certificates, the Learning Compass demo video and selected images extracted from the supplied portfolio PDF.

After editing a JSON file, run `python build_site.py` from this folder. The generator validates project links and media references and rebuilds the HTML pages. Editing generated HTML directly is possible, but a rebuild overwrites those changes.

## Add proof later

Copy an image or video into `assets/media/`, add it to the matching group in `content/media.json`, and rebuild. Images appear in a gallery and open at full size; MP4 and WebM videos play in place. Projects without media simply show their written case study.

The source photographs in the Desktop `Portfolio` folder and the supplied PDF are untouched. The published site is [aahadrashid.github.io](https://aahadrashid.github.io/). After editing and rebuilding, commit and push the changed files in GitHub Desktop to publish the update.

## Structure

- `index.html`: introduction, selected projects, EV subsystems, recognition and contact.
- `evidence.html`: awards, certificates, engineering artifacts and the project demo.
- `projects/index.html`: searchable and filterable project index.
- `projects/*.html`: individual case studies.
- `skills.html`: skills linked to project evidence.
- `assets/css/style.css`: layout, colors and responsive behavior.
- `assets/js/site.js`: mobile navigation and project filtering.
- `build_site.py`: dependency-free static site generator.
