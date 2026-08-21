import { useState } from "react";
import "./OverKillHillVibeVariant.css";

const navigation = [
  { label: "The Forge", href: "#forge" },
  { label: "Projects", href: "#projects" },
  { label: "Writings", href: "#latest" },
  { label: "About", href: "#about" },
];

const principles = [
  {
    title: "Protocols, not prompts",
    body: "A clever question is a spark. A protocol is what keeps the room lit when the input gets strange.",
  },
  {
    title: "Proof before polish",
    body: "We put systems through the awkward cases first: ambiguity, edge conditions, the handoff nobody documented.",
  },
  {
    title: "Tools with a human pulse",
    body: "The point is not to automate the person away. It is to leave more attention for the work that actually matters.",
  },
];

const projects = [
  {
    index: "01 / LIVE",
    title: "Glee-fully Tools",
    body: "A bright little constellation of personal tools for career, food, travel, health and identity.",
    href: "https://glee-fully.tools/",
  },
  {
    index: "02 / LIVE",
    title: "AskJamie",
    body: "A considered second opinion for complex questions, tradeoffs and next-step decisions.",
    href: "https://askjamie.bot",
  },
  {
    index: "03 / OPEN",
    title: "The Prompt Forge",
    body: "A workshop where one-off prompts become governed systems, audit contracts and ready-to-run specs.",
    href: "#latest",
  },
];

export function OverKillHillVibeVariant() {
  const [menuOpen, setMenuOpen] = useState(false);
  const [nightMode, setNightMode] = useState(false);

  const closeMenu = () => setMenuOpen(false);

  return (
    <div className={`okh-vibe${nightMode ? " okh-vibe--night" : ""}`}>
      <div className="okh-vibe__grain" aria-hidden="true" />

      <header className="okh-vibe__header" id="top">
        <div className="okh-vibe__container okh-vibe__header-row">
          <a className="okh-vibe__brand" href="#top" onClick={closeMenu}>
            <span className="okh-vibe__brand-mark" aria-hidden="true">
              P³
            </span>
            <span>OverKill Hill</span>
          </a>

          <nav
            id="okh-vibe-navigation"
            className="okh-vibe__nav"
            aria-label="Primary navigation"
            data-open={menuOpen}
          >
            {navigation.map((item, index) => (
              <a
                key={item.label}
                href={item.href}
                aria-current={index === 0 ? "page" : undefined}
                onClick={closeMenu}
              >
                {item.label}
              </a>
            ))}
          </nav>

          <div className="okh-vibe__header-actions">
            <button
              className="okh-vibe__palette"
              type="button"
              onClick={() => setNightMode((current) => !current)}
              aria-pressed={nightMode}
            >
              {nightMode ? "Paper mode" : "Night notes"}
            </button>
            <button
              className="okh-vibe__menu"
              type="button"
              onClick={() => setMenuOpen((current) => !current)}
              aria-expanded={menuOpen}
              aria-controls="okh-vibe-navigation"
              aria-label={menuOpen ? "Close navigation" : "Open navigation"}
            >
              <span className="okh-vibe__menu-lines" aria-hidden="true">
                <span />
                <span />
                <span />
              </span>
            </button>
          </div>
        </div>

        <div className="okh-vibe__dispatch">
          <span className="okh-vibe__dispatch-label">Latest dispatch</span>
          <a href="#latest" onClick={closeMenu}>
            The Council scored its own diagrams. The useful part was what happened next.
          </a>
        </div>
      </header>

      <main>
        <section className="okh-vibe__hero" id="forge">
          <div className="okh-vibe__container okh-vibe__hero-grid">
            <div>
              <p className="okh-vibe__eyebrow">Field report 06 / The Forge</p>
              <h1>
                Precision.
                <br />
                Protocol.
                <br />
                <em>Promptcraft.</em>
              </h1>
              <p className="okh-vibe__subline">A working studio for AI systems</p>
              <p className="okh-vibe__tagline">
                We design the parts that have to hold: local inference, agentic
                coordination and the quiet governance layer beneath the shiny demo.
              </p>

              <div className="okh-vibe__status" aria-label="Current forge status">
                <p className="okh-vibe__status-title">Bench status / actively iterated</p>
                <p>
                  These are working notes, not a museum display. Protocols are
                  versioned mid-draft, stress-tested in the open and revised when
                  reality finds a seam.
                </p>
              </div>

              <div className="okh-vibe__actions">
                <a className="okh-vibe__button okh-vibe__button--primary" href="#projects">
                  Explore the projects
                </a>
                <a className="okh-vibe__button okh-vibe__button--quiet" href="#about">
                  Read the working notes
                </a>
              </div>
            </div>

            <div className="okh-vibe__hero-side">
              <figure className="okh-vibe__visual">
                <img
                  src="/__mockup/images/overkill-hill-archival-sentinel.png"
                  alt="Editorial screenprint of a mechanical raven perched on a vintage terminal"
                />
                <figcaption className="okh-vibe__visual-caption">
                  <span>Sentinel / study 02</span>
                  <span>Do not ship the sketch</span>
                </figcaption>
              </figure>
              <aside className="okh-vibe__forge-card">
                <h3>What happens at the Hill?</h3>
                <p>
                  Prompts become protocols here. We prototype, break, document and
                  harden systems until they can carry human context without pretending
                  the messy parts do not exist.
                </p>
              </aside>
            </div>
          </div>
        </section>

        <section className="okh-vibe__section" id="latest">
          <div className="okh-vibe__container">
            <header className="okh-vibe__section-heading">
              <h2>Fresh from the forge</h2>
              <p>The most recent thing to clear the workbench and earn a public label.</p>
            </header>
            <article className="okh-vibe__latest">
              <div className="okh-vibe__latest-copy">
                <p className="okh-vibe__pill">Dispatch / v0.5</p>
                <h3>The first diagram is usually a liar.</h3>
                <p>
                  What happens when diagrams get cheap enough to be wrong on purpose?
                  A Council of AIs ran seven platforms against the same brief, then
                  scored themselves with the architect&apos;s rubric. Every model was
                  harder on itself than the architect was. The finding was not about
                  picking a winner. It was about learning where confidence hides.
                </p>
              </div>
              <figure className="okh-vibe__latest-image">
                <img
                  src="/__mockup/images/overkill-hill-archival-sentinel.png"
                  alt="Print texture and mechanical raven detail from the latest forge study"
                />
                <a href="#projects">Read the article</a>
              </figure>
            </article>
          </div>
        </section>

        <section className="okh-vibe__section" id="about">
          <div className="okh-vibe__container">
            <header className="okh-vibe__section-heading">
              <h2>How the Hill thinks</h2>
              <p>
                Overkill is not complexity for its own sake. It is the distance we
                travel into the details so the system can be trusted when everything
                moves fast.
              </p>
            </header>
            <div className="okh-vibe__cards">
              {principles.map((principle) => (
                <article className="okh-vibe__card" key={principle.title}>
                  <h3>{principle.title}</h3>
                  <p>{principle.body}</p>
                </article>
              ))}
            </div>
          </div>
        </section>

        <section className="okh-vibe__section okh-vibe__stripe" id="projects">
          <div className="okh-vibe__container">
            <header className="okh-vibe__section-heading">
              <h2>Projects from the forge</h2>
              <p>Blueprints you can walk into: documented, road-tested and ready to plug into a daily stack.</p>
            </header>
            <div className="okh-vibe__project-grid">
              {projects.map((project) => (
                <article className="okh-vibe__project" key={project.title}>
                  <span className="okh-vibe__project-index">{project.index}</span>
                  <h3>{project.title}</h3>
                  <p>{project.body}</p>
                  <a className="okh-vibe__project-link" href={project.href}>
                    Enter the project
                  </a>
                </article>
              ))}
            </div>
          </div>
        </section>

        <section className="okh-vibe__cta">
          <div className="okh-vibe__container">
            <span className="okh-vibe__cta-kicker okh-vibe__micro">A good system leaves a trace</span>
            <h2>Let&apos;s build something that can carry the weight.</h2>
            <p>
              Bring the knotty question, the half-built workflow or the stack that
              cannot quite explain itself yet. We will find the load-bearing shape.
            </p>
            <a className="okh-vibe__button okh-vibe__button--primary" href="mailto:contact@overkillhill.com">
              Start a project conversation
            </a>
          </div>
        </section>
      </main>

      <footer className="okh-vibe__footer">
        <div className="okh-vibe__container okh-vibe__footer-grid">
          <div>
            <h3>OverKill Hill P³</h3>
            <p>
              Protocol-first AI systems design: local inference, multi-model
              coordination and the governance layer the platforms forgot to build.
            </p>
          </div>
          <div>
            <h4>Navigate</h4>
            <ul>
              {navigation.map((item) => (
                <li key={item.label}>
                  <a href={item.href}>{item.label}</a>
                </li>
              ))}
            </ul>
          </div>
          <div>
            <h4>Keep in touch</h4>
            <ul>
              <li><a href="mailto:contact@overkillhill.com">contact@overkillhill.com</a></li>
              <li><a href="https://www.linkedin.com/company/overkillhillp3">LinkedIn</a></li>
              <li><a href="https://x.com/OverKillHillP3">X / OverKillHillP3</a></li>
            </ul>
          </div>
        </div>
        <div className="okh-vibe__container okh-vibe__footer-bottom">
          <span>Built in public / P³ field notes</span>
          <span>© 2026 OverKill Hill P³</span>
        </div>
      </footer>
    </div>
  );
}