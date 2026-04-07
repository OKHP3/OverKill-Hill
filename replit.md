# OverKill Hill P³™

## Project Overview
A pure static HTML/CSS/JS portfolio and documentation site for a "digital forge" specializing in custom GPT systems, prompt engineering, and intelligent architectures.

## Tech Stack
- **Frontend:** Static HTML5, CSS3, vanilla JavaScript (ES6+)
- **No build system** — no package manager, no bundler
- **Dev Server:** Python's built-in HTTP server (`python3 -m http.server 5000 --bind 0.0.0.0`)
- **Deployment:** Static site deployment (`publicDir: "."`)

## Project Layout
```
.
├── assets/             # Static assets (CSS, JS, images)
│   ├── css/theme.css   # Global styles with CSS variables
│   ├── js/app.js       # Theme toggle, scroll animations
│   └── img/            # Brand images and icons
├── about/              # About page
├── contact/            # Contact page
├── found-ry/           # Internal project area
├── legal/              # Legal/Privacy docs
├── manifesto/          # Philosophy section
├── projects/           # GPT/AI project portfolio
├── prompt-forge/       # Prompt engineering section
├── universe/           # Brand ecosystem
├── writings/           # Articles and essays
├── index.html          # Main landing page
├── 404.html            # Error page
├── under-construction.html
├── site.webmanifest    # PWA manifest
└── CNAME               # Custom domain: overkillhill.com
```

## SEO Status
A comprehensive SEO audit and remediation pass has been completed across all pages.

### robots.txt & sitemap.xml
- `robots.txt`: Added at root, allows all crawlers, disallows `/under-construction.html`, references sitemap
- `sitemap.xml`: Created with 9 indexable URLs only (home, about, contact, legal, manifesto, universe, projects/, bfs project, first-diagram article)

### Canonical URLs
All pages now have correct self-referencing canonical tags (no page points to the homepage incorrectly).

### Under-Construction Pages (noindex)
All incomplete pages carry `noindex, nofollow`:
- `found-ry/`, `projects/abrahamic-reference-engine/`, `projects/hometools/`, `projects/pathscrib-r/`, `projects/un-nocked-truth/`, `writings/magnus-saga/`, `writings/biases-as-constants/`, `writings/index.html`, `prompt-forge/`, `404.html`, `under-construction.html`

### OG Image URL Encoding
All OG image URLs now use percent-encoded `%C2%B3` instead of raw Unicode `³` for maximum compatibility. Fixed across all HTML files.

### Open Graph & Twitter Card Completeness
All pages now carry: `og:site_name`, `og:locale`, `og:url`, `og:image` (encoded), `twitter:site`.

### prompt-forge
Rebuilt as a branded "coming soon" placeholder with proper header/footer/nav rather than a bare "Hello, World!".

### writings/index.html
Fixed to be a proper hub page (title "Writings & Essays", H1 "Writings from the Hill") — no longer a duplicate of the magnus-saga page.

## Running Locally
The workflow "Start application" serves the site on port 5000:
```
python3 -m http.server 5000 --bind 0.0.0.0
```
