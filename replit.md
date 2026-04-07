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

## Running Locally
The workflow "Start application" serves the site on port 5000:
```
python3 -m http.server 5000 --bind 0.0.0.0
```
