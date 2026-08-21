import { useState } from "react";

const presets = [
  { name: "Ocean Depth", code: "ocean", colors: ["#0d324d", "#167d9a", "#8ed1c7", "#f3c969"] },
  { name: "Slate Ember", code: "ember", colors: ["#252932", "#c46a2c", "#e6a03c", "#f0dfc2"] },
  { name: "Forest Sage", code: "sage", colors: ["#20382f", "#688c62", "#c5d7a4", "#e4bd78"] },
  { name: "Violet Mist", code: "violet", colors: ["#30283f", "#7e6ba8", "#c8b8df", "#efa990"] },
];

const diagramByPreset: Record<string, string[]> = {
  ocean: ["flowchart TD", "  A[Theme tokens] --> B{Renderer}", "  B --> C[Classic]", "  B --> D[Neo]", "  C --> E[Export CSS]", "  D --> E"],
  ember: ["flowchart TD", "  A[Brand palette] --> B{Governance}", "  B --> C[Prompt scaffold]", "  B --> D[themeVariables]", "  C --> E[AI output]", "  D --> E"],
  sage: ["flowchart TD", "  A[Source diagram] --> B[Apply preset]", "  B --> C[Validate tokens]", "  C --> D[Render preview]", "  D --> E[Ship with confidence]"],
  violet: ["flowchart TD", "  A[Ask your model] --> B[Style contract]", "  B --> C[Mermaid code]", "  C --> D[Preview]", "  D --> E[Share the system]"],
};

function ArrowUpRight() {
  return <svg viewBox="0 0 20 20" aria-hidden="true"><path d="M5 15 15 5M7 5h8v8" /></svg>;
}

function Chevron() {
  return <svg viewBox="0 0 20 20" aria-hidden="true"><path d="m7 8 3 3 3-3" /></svg>;
}

function CopyIcon() {
  return <svg viewBox="0 0 20 20" aria-hidden="true"><rect x="6.5" y="6.5" width="9" height="9" rx="1.5" /><path d="M13.5 6.5V5A1.5 1.5 0 0 0 12 3.5H5A1.5 1.5 0 0 0 3.5 5v7A1.5 1.5 0 0 0 5 13.5h1.5" /></svg>;
}

export default function MermaidThemeBuilderOrbit() {
  const [preset, setPreset] = useState("ember");
  const [activeTab, setActiveTab] = useState<"preview" | "code">("preview");
  const [copied, setCopied] = useState(false);
  const [fresh, setFresh] = useState(false);
  const selected = presets.find((item) => item.code === preset) ?? presets[1];

  const copyCode = () => {
    setCopied(true);
    window.setTimeout(() => setCopied(false), 1800);
  };

  return (
    <div className="mtb-orbit">
      <style>{`
        @import url('https://fonts.googleapis.com/css2?family=Alfa+Slab+One&family=DM+Sans:wght@400;500;600;700&family=JetBrains+Mono:wght@400;500;700&display=swap');
        .mtb-orbit, .mtb-orbit * { box-sizing: border-box; }
        .mtb-orbit {
          --ink: #eee9df; --paper: #111416; --panel: #181c1d; --panel-2: #202526;
          --line: rgba(232, 221, 204, .15); --quiet: #9a9f9a; --orange: #d47c3e;
          min-height: 100vh; color: var(--ink); background: #111416;
          font-family: 'DM Sans', sans-serif; overflow: hidden;
          background-image: linear-gradient(rgba(212,124,62,.035) 1px, transparent 1px), linear-gradient(90deg, rgba(212,124,62,.035) 1px, transparent 1px);
          background-size: 44px 44px;
        }
        .mtb-shell { width: min(1480px, 100%); min-height: 100vh; margin: 0 auto; display: grid; grid-template-columns: 238px minmax(0, 1fr); }
        .mtb-rail { border-right: 1px solid var(--line); padding: 24px 18px; display: flex; flex-direction: column; gap: 28px; background: rgba(12, 15, 16, .66); }
        .mtb-brand { display: flex; align-items: center; gap: 10px; color: var(--ink); text-decoration: none; }
        .mtb-mark { width: 30px; height: 30px; display: grid; place-items: center; border: 1px solid var(--orange); color: var(--orange); font: 700 10px 'JetBrains Mono', monospace; letter-spacing: -.06em; }
        .mtb-brand span { font: 500 12px 'JetBrains Mono', monospace; letter-spacing: .04em; }
        .mtb-rail-label, .mtb-kicker { color: var(--quiet); font: 700 10px 'JetBrains Mono', monospace; letter-spacing: .16em; text-transform: uppercase; }
        .mtb-rail-label { padding: 0 10px; margin-bottom: -14px; }
        .mtb-nav { display: grid; gap: 4px; }
        .mtb-nav button { border: 0; text-align: left; display: flex; align-items: center; gap: 11px; width: 100%; padding: 10px; border-radius: 3px; background: transparent; color: var(--quiet); font: 500 12px 'JetBrains Mono', monospace; cursor: pointer; }
        .mtb-nav button:hover, .mtb-nav button.active { color: var(--ink); background: rgba(232,221,204,.08); }
        .mtb-nav button.active { box-shadow: inset 2px 0 var(--orange); }
        .mtb-nav i { width: 7px; height: 7px; border: 1px solid currentColor; display: block; }
        .mtb-rail-foot { margin-top: auto; border-top: 1px solid var(--line); padding: 18px 10px 0; color: var(--quiet); font: 11px/1.55 'JetBrains Mono', monospace; }
        .mtb-rail-foot strong { display: block; color: var(--ink); font-weight: 500; margin-bottom: 6px; }
        .mtb-main { min-width: 0; padding: 22px clamp(22px, 4vw, 62px) 48px; }
        .mtb-topbar { display: flex; justify-content: space-between; align-items: center; gap: 20px; padding-bottom: 20px; border-bottom: 1px solid var(--line); }
        .mtb-breadcrumb { color: var(--quiet); font: 11px 'JetBrains Mono', monospace; }
        .mtb-breadcrumb b { color: var(--ink); font-weight: 500; }
        .mtb-actions { display: flex; gap: 8px; }
        .mtb-button { appearance: none; border: 1px solid var(--line); color: var(--ink); background: var(--panel); display: inline-flex; align-items: center; justify-content: center; gap: 8px; min-height: 34px; padding: 0 12px; border-radius: 3px; font: 600 11px 'JetBrains Mono', monospace; cursor: pointer; transition: background .18s ease, border-color .18s ease, transform .18s ease; }
        .mtb-button:hover { background: var(--panel-2); border-color: rgba(232,221,204,.35); transform: translateY(-1px); }
        .mtb-button.primary { color: #171310; border-color: var(--orange); background: var(--orange); }
        .mtb-button svg { width: 14px; height: 14px; fill: none; stroke: currentColor; stroke-width: 1.5; stroke-linecap: round; stroke-linejoin: round; }
        .mtb-intro { padding: clamp(32px, 6vw, 78px) 0 46px; display: grid; grid-template-columns: minmax(0, 1.15fr) minmax(250px, .85fr); gap: 48px; align-items: end; }
        .mtb-intro h1 { margin: 12px 0 18px; max-width: 650px; font: 400 clamp(42px, 5.3vw, 82px)/.98 'Alfa Slab One', serif; letter-spacing: -.035em; }
        .mtb-intro h1 em { color: var(--orange); font-style: normal; }
        .mtb-intro p { max-width: 570px; margin: 0; color: #b9b9b0; font-size: clamp(15px, 1.5vw, 19px); line-height: 1.55; }
        .mtb-intro-note { border-left: 1px solid var(--orange); padding: 6px 0 6px 18px; color: var(--quiet); font: 12px/1.7 'JetBrains Mono', monospace; }
        .mtb-intro-note strong { display: block; color: var(--ink); font-size: 13px; font-weight: 500; margin-bottom: 7px; }
        .mtb-workspace { display: grid; grid-template-columns: minmax(0, 1fr) 255px; gap: 14px; align-items: start; }
        .mtb-preview { min-height: 485px; border: 1px solid var(--line); background: var(--panel); position: relative; overflow: hidden; }
        .mtb-preview-head { padding: 15px 18px; display: flex; justify-content: space-between; align-items: center; border-bottom: 1px solid var(--line); }
        .mtb-preview-title { display: flex; align-items: center; gap: 9px; font: 500 12px 'JetBrains Mono', monospace; }
        .mtb-live { width: 7px; height: 7px; background: #9ac889; border-radius: 50%; box-shadow: 0 0 0 3px rgba(154,200,137,.1); }
        .mtb-preview-meta { color: var(--quiet); font: 10px 'JetBrains Mono', monospace; }
        .mtb-tabs { display: flex; gap: 17px; padding: 0 18px; border-bottom: 1px solid var(--line); }
        .mtb-tab { padding: 12px 0 10px; border: 0; border-bottom: 2px solid transparent; background: transparent; color: var(--quiet); font: 11px 'JetBrains Mono', monospace; cursor: pointer; }
        .mtb-tab.active { color: var(--ink); border-color: var(--orange); }
        .mtb-canvas { min-height: 375px; position: relative; padding: 40px 32px; display: grid; place-items: center; }
        .mtb-canvas:before { content: ''; position: absolute; inset: 0; opacity: .6; background-image: radial-gradient(rgba(232,221,204,.16) .75px, transparent .75px); background-size: 16px 16px; }
        .mtb-diagram { width: min(470px, 100%); position: relative; z-index: 1; display: grid; gap: 12px; }
        .mtb-node { border: 1px solid ${selected.colors[1]}; min-height: 43px; padding: 11px 14px; background: ${selected.colors[0]}; color: #f5ede1; font: 11px 'JetBrains Mono', monospace; position: relative; }
        .mtb-node.center { width: 72%; margin: 0 auto; text-align: center; border-color: ${selected.colors[2]}; background: ${selected.colors[1]}; color: #101515; }
        .mtb-node.row { display: grid; grid-template-columns: 1fr 1fr; gap: 12px; padding: 0; border: 0; background: transparent; }
        .mtb-node.row span { border: 1px solid ${selected.colors[2]}; padding: 11px 8px; text-align: center; background: ${selected.colors[0]}; color: #d7ece5; }
        .mtb-connector { width: 1px; height: 16px; background: ${selected.colors[2]}; margin: -12px auto; opacity: .7; position: relative; z-index: 2; }
        .mtb-code { min-height: 375px; padding: 30px; background: #0e1112; color: #d7d1c5; font: 12px/1.8 'JetBrains Mono', monospace; white-space: pre-wrap; }
        .mtb-code .accent { color: ${selected.colors[2]}; }
        .mtb-side { border: 1px solid var(--line); background: rgba(24,28,29,.82); }
        .mtb-side-section { padding: 18px; border-bottom: 1px solid var(--line); }
        .mtb-side-section:last-child { border-bottom: 0; }
        .mtb-side h2 { margin: 0 0 15px; font: 400 20px/1 'Alfa Slab One', serif; }
        .mtb-preset { width: 100%; display: grid; grid-template-columns: 1fr auto; gap: 10px; align-items: center; border: 0; border-bottom: 1px solid rgba(232,221,204,.08); padding: 11px 0; color: var(--quiet); background: transparent; text-align: left; cursor: pointer; font: 11px 'JetBrains Mono', monospace; }
        .mtb-preset:last-child { border-bottom: 0; }
        .mtb-preset:hover, .mtb-preset.active { color: var(--ink); }
        .mtb-preset.active { color: var(--orange); }
        .mtb-swatches { display: flex; gap: 3px; }
        .mtb-swatch { width: 11px; height: 11px; display: block; }
        .mtb-stat { display: flex; justify-content: space-between; gap: 10px; color: var(--quiet); font: 10px 'JetBrains Mono', monospace; padding: 7px 0; }
        .mtb-stat b { color: var(--ink); font-weight: 500; }
        .mtb-footerline { display: flex; align-items: center; justify-content: space-between; gap: 16px; margin-top: 24px; padding-top: 15px; border-top: 1px solid var(--line); color: var(--quiet); font: 10px 'JetBrains Mono', monospace; }
        .mtb-footerline span:last-child { color: var(--orange); }
        @media (max-width: 850px) {
          .mtb-shell { display: block; }
          .mtb-rail { border-right: 0; border-bottom: 1px solid var(--line); padding: 14px 18px; display: block; }
          .mtb-rail-label, .mtb-rail-foot { display: none; }
          .mtb-brand { display: inline-flex; }
          .mtb-nav { display: inline-flex; float: right; gap: 2px; }
          .mtb-nav button { width: auto; padding: 9px 8px; }
          .mtb-nav button span { display: none; }
          .mtb-main { padding: 16px 18px 34px; }
          .mtb-intro { grid-template-columns: 1fr; gap: 22px; padding-top: 40px; }
          .mtb-workspace { grid-template-columns: 1fr; }
          .mtb-side { display: grid; grid-template-columns: 1fr 1fr; }
          .mtb-side-section { min-width: 0; }
          .mtb-side-section:last-child { grid-column: 1 / -1; }
        }
        @media (max-width: 520px) {
          .mtb-topbar { align-items: flex-start; }
          .mtb-actions .mtb-button:first-child { display: none; }
          .mtb-intro h1 { font-size: 44px; }
          .mtb-side { display: block; }
          .mtb-canvas { padding: 36px 16px; }
        }
      `}</style>
      <div className="mtb-shell">
        <aside className="mtb-rail">
          <a className="mtb-brand" href="https://overkillhill.com" target="_blank" rel="noreferrer">
            <span className="mtb-mark">OK</span>
            <span>OVERKILL HILL P³</span>
          </a>
          <div className="mtb-rail-label">Workbench</div>
          <nav className="mtb-nav" aria-label="Workbench sections">
            <button className="active" onClick={() => document.getElementById("mtb-preview")?.scrollIntoView({ behavior: "smooth" })}><i /> <span>Theme canvas</span></button>
            <button onClick={() => document.getElementById("mtb-presets")?.scrollIntoView({ behavior: "smooth" })}><i /> <span>Palette library</span></button>
            <button onClick={() => document.getElementById("mtb-export")?.scrollIntoView({ behavior: "smooth" })}><i /> <span>Export surface</span></button>
          </nav>
          <div className="mtb-rail-foot">
            <strong>V0.3 / PUBLIC ALPHA</strong>
            Browser-only governance for Mermaid.js themes. No login. No install.
          </div>
        </aside>
        <main className="mtb-main">
          <div className="mtb-topbar">
            <div className="mtb-breadcrumb">PROJECTS / <b>MERMAID THEME BUILDER</b></div>
            <div className="mtb-actions">
              <button className="mtb-button" onClick={() => setFresh(true)} aria-label="Refresh preview">{fresh ? "REFRESHED" : "RENDER AGAIN"}</button>
              <a className="mtb-button primary" href="https://okhp3.github.io/mermaid-theme-builder/" target="_blank" rel="noreferrer">OPEN TOOL <ArrowUpRight /></a>
            </div>
          </div>
          <section className="mtb-intro">
            <div>
              <div className="mtb-kicker">Visual governance / Mermaid.js</div>
              <h1>Give every diagram a <em>point of view.</em></h1>
              <p>Build a theme once, see it move through your diagram, then export the exact tokens your team can trust.</p>
            </div>
            <div className="mtb-intro-note">
              <strong>THE WORKBENCH, REORDERED</strong>
              Presets sit beside the live canvas, not beneath it. The decision and its consequence stay in one glance.
            </div>
          </section>
          <section className="mtb-workspace" id="mtb-preview">
            <div className="mtb-preview" aria-label="Live Mermaid theme preview">
              <div className="mtb-preview-head">
                <div className="mtb-preview-title"><span className="mtb-live" /> LIVE DIAGRAM</div>
                <div className="mtb-preview-meta">{fresh ? "rendered just now" : "auto-render enabled"}</div>
              </div>
              <div className="mtb-tabs">
                <button className={`mtb-tab ${activeTab === "preview" ? "active" : ""}`} onClick={() => setActiveTab("preview")}>PREVIEW</button>
                <button className={`mtb-tab ${activeTab === "code" ? "active" : ""}`} onClick={() => setActiveTab("code")}>MERMAID CODE</button>
              </div>
              {activeTab === "preview" ? (
                <div className="mtb-canvas">
                  <div className="mtb-diagram">
                    <div className="mtb-node">{selected.name} / palette loaded</div>
                    <div className="mtb-connector" />
                    <div className="mtb-node center">themeVariables</div>
                    <div className="mtb-connector" />
                    <div className="mtb-node row"><span>AI prompt</span><span>CSS export</span></div>
                    <div className="mtb-connector" />
                    <div className="mtb-node">SHARED LANGUAGE → SHIPPED DIAGRAM</div>
                  </div>
                </div>
              ) : (
                <pre className="mtb-code"><span className="accent">{"flowchart TD"}</span>{"\n  A["}{selected.name}{" tokens] --> B{Renderer}\n  B --> C[Classic]\n  B --> D[Neo]\n  C --> E[Export]\n  D --> E"}</pre>
              )}
              <div className="mtb-preview-head" style={{ borderTop: "1px solid var(--line)", borderBottom: 0 }}>
                <div className="mtb-preview-meta">MERMAID 11.16 / 31 DIAGRAM FAMILIES</div>
                <button className="mtb-button" onClick={copyCode}><CopyIcon /> {copied ? "COPIED" : "COPY CODE"}</button>
              </div>
            </div>
            <aside className="mtb-side">
              <div className="mtb-side-section" id="mtb-presets">
                <div className="mtb-kicker">01 / Preset</div>
                <h2>Choose a mood.</h2>
                {presets.map((item) => (
                  <button key={item.code} className={`mtb-preset ${item.code === preset ? "active" : ""}`} onClick={() => { setPreset(item.code); setFresh(false); }}>
                    <span>{item.name}</span>
                    <span className="mtb-swatches">{item.colors.map((color) => <i className="mtb-swatch" key={color} style={{ background: color }} />)}</span>
                  </button>
                ))}
              </div>
              <div className="mtb-side-section" id="mtb-export">
                <div className="mtb-kicker">02 / Output</div>
                <h2>Ready to ship.</h2>
                <div className="mtb-stat"><span>CSS variables</span><b>38 / 38</b></div>
                <div className="mtb-stat"><span>Renderer profile</span><b>Neo</b></div>
                <div className="mtb-stat"><span>Prompt scaffold</span><b>Available</b></div>
                <button className="mtb-button primary" style={{ width: "100%", marginTop: 12 }} onClick={copyCode}>{copied ? "COPIED TO CLIPBOARD" : "EXPORT THEME"} <ArrowUpRight /></button>
              </div>
            </aside>
          </section>
          <div className="mtb-footerline"><span>MIT LICENSE / OPEN SOURCE / 100% CLIENT-SIDE</span><span>THE STYLE LAYER FOR DIAGRAM-AS-CODE <Chevron /></span></div>
        </main>
      </div>
    </div>
  );
}