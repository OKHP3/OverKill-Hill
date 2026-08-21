import { useState } from "react";

type IconName =
  | "arrow"
  | "book"
  | "check"
  | "chevron"
  | "code"
  | "copy"
  | "external"
  | "github"
  | "grid"
  | "menu"
  | "refresh"
  | "spark"
  | "swatch"
  | "x";

const colors = [
  { label: "Canvas", value: "#101b1a" },
  { label: "Ink", value: "#e9dfc7" },
  { label: "Signal", value: "#d7763d" },
  { label: "Moss", value: "#9cae82" },
];

const features = [
  ["01", "Live diagram preview", "See flowcharts, sequence diagrams, and more change as you tune a color."],
  ["02", "Complete CSS export", "Leave with a ready-to-paste themeVariables block, not a loose palette."],
  ["03", "Local by default", "No account, no upload, no telemetry. Your theme stays in this browser."],
];

function Icon({ name, size = 16 }: { name: IconName; size?: number }) {
  const common = {
    width: size,
    height: size,
    viewBox: "0 0 24 24",
    fill: "none",
    stroke: "currentColor",
    strokeWidth: 1.8,
    strokeLinecap: "round" as const,
    strokeLinejoin: "round" as const,
    "aria-hidden": true,
  };

  if (name === "arrow") return <svg {...common}><path d="M5 12h13" /><path d="m13 6 6 6-6 6" /></svg>;
  if (name === "book") return <svg {...common}><path d="M4 5.5A2.5 2.5 0 0 1 6.5 3H20v17H6.5A2.5 2.5 0 0 0 4 22V5.5Z" /><path d="M4 5.5v14" /><path d="M8 7h8M8 11h7" /></svg>;
  if (name === "check") return <svg {...common}><path d="m5 12 4 4L19 6" /></svg>;
  if (name === "chevron") return <svg {...common}><path d="m6 9 6 6 6-6" /></svg>;
  if (name === "code") return <svg {...common}><path d="m8 9-4 3 4 3M16 9l4 3-4 3M14 5l-4 14" /></svg>;
  if (name === "copy") return <svg {...common}><rect x="8" y="8" width="11" height="12" rx="1.5" /><path d="M16 8V5.5A1.5 1.5 0 0 0 14.5 4h-9A1.5 1.5 0 0 0 4 5.5v10A1.5 1.5 0 0 0 5.5 17H8" /></svg>;
  if (name === "external") return <svg {...common}><path d="M14 4h6v6M20 4l-9 9" /><path d="M18 13v5a2 2 0 0 1-2 2H6a2 2 0 0 1-2-2V8a2 2 0 0 1 2-2h5" /></svg>;
  if (name === "github") return <svg {...common}><path d="M15 22v-4a4.8 4.8 0 0 0-1-3.5c3.3-.4 6.7-1.6 6.7-7A5.4 5.4 0 0 0 19.2 3.8 5 5 0 0 0 19.1 1S17.9.6 15 2.5a12.5 12.5 0 0 0-6 0C6.1.6 4.9 1 4.9 1a5 5 0 0 0-.1 2.8A5.4 5.4 0 0 0 3.3 7.5c0 5.4 3.4 6.6 6.7 7A4.8 4.8 0 0 0 9 18v4" /><path d="M9 18c-4.5 2-5-2-7-2" /></svg>;
  if (name === "grid") return <svg {...common}><rect x="4" y="4" width="6" height="6" rx="1" /><rect x="14" y="4" width="6" height="6" rx="1" /><rect x="4" y="14" width="6" height="6" rx="1" /><rect x="14" y="14" width="6" height="6" rx="1" /></svg>;
  if (name === "menu") return <svg {...common}><path d="M4 7h16M4 12h16M4 17h16" /></svg>;
  if (name === "refresh") return <svg {...common}><path d="M20 11a8 8 0 0 0-14.8-3.9L3 9" /><path d="M3 4v5h5M4 13a8 8 0 0 0 14.8 3.9L21 15" /><path d="M21 20v-5h-5" /></svg>;
  if (name === "spark") return <svg {...common}><path d="m12 3-1.6 5.4L5 10l5.4 1.6L12 17l1.6-5.4L19 10l-5.4-1.6L12 3Z" /><path d="m19 16-.7 2.3L16 19l2.3.7L19 22l.7-2.3L22 19l-2.3-.7L19 16Z" /></svg>;
  if (name === "swatch") return <svg {...common}><path d="M19.5 3.5a3 3 0 0 0-4.2 0L5.1 13.7a3.8 3.8 0 1 0 5.3 5.3l10.2-10.2a3 3 0 0 0-1.1-5.3Z" /><path d="m13 7 4 4M7 17h.01M11 13h.01M15 9h.01" /></svg>;
  return <svg {...common}><path d="m6 6 12 12M18 6 6 18" /></svg>;
}

export function MermaidThemeBuilderRefined() {
  const [mobileOpen, setMobileOpen] = useState(false);
  const [activeTab, setActiveTab] = useState<"theme" | "preview" | "export">("theme");
  const [activeColor, setActiveColor] = useState(colors[2].value);
  const [copied, setCopied] = useState(false);

  const scrollToTool = () => {
    document.getElementById("builder")?.scrollIntoView({ behavior: "smooth", block: "start" });
  };

  const resetTheme = () => {
    setActiveColor(colors[2].value);
    setCopied(false);
  };

  const copyExport = () => {
    setCopied(true);
    if (navigator.clipboard) {
      navigator.clipboard.writeText(`themeVariables: { primaryColor: '${activeColor}', primaryTextColor: '#e9dfc7' }`).catch(() => undefined);
    }
    window.setTimeout(() => setCopied(false), 1800);
  };

  return (
    <div
      className="min-h-[100dvh] overflow-x-hidden text-[#e9dfc7]"
      style={{
        fontFamily: "'DM Sans', ui-sans-serif, system-ui, sans-serif",
        backgroundColor: "#101b1a",
        backgroundImage:
          "radial-gradient(circle at 80% 8%, rgba(215,118,61,.14), transparent 27rem), linear-gradient(rgba(156,174,130,.055) 1px, transparent 1px), linear-gradient(90deg, rgba(156,174,130,.055) 1px, transparent 1px)",
        backgroundSize: "auto, 48px 48px, 48px 48px",
      }}
    >
      <header className="sticky top-0 z-30 border-b border-[#9cae82]/15 bg-[#101b1a]/90 backdrop-blur-xl">
        <div className="mx-auto flex h-[72px] max-w-[1440px] items-center justify-between px-5 sm:px-8">
          <a href="#top" className="flex items-center gap-3 no-underline" aria-label="OverKill Hill home">
            <span className="grid h-9 w-9 place-items-center rounded-[3px] border border-[#d7763d]/70 bg-[#d7763d]/10 font-mono text-[11px] font-bold tracking-[-.08em] text-[#e69f61]">OK</span>
            <span className="hidden border-l border-[#9cae82]/20 pl-3 font-mono text-[11px] uppercase tracking-[.18em] text-[#e9dfc7]/65 sm:block">OverKill Hill P³</span>
          </a>

          <nav className={`${mobileOpen ? "flex" : "hidden"} absolute left-4 right-4 top-[78px] flex-col gap-1 rounded-md border border-[#9cae82]/20 bg-[#152322] p-2 shadow-2xl sm:static sm:flex sm:flex-row sm:items-center sm:gap-7 sm:border-0 sm:bg-transparent sm:p-0 sm:shadow-none`} aria-label="Main navigation">
            <a href="#builder" onClick={() => setMobileOpen(false)} className="rounded px-3 py-2 font-mono text-[11px] uppercase tracking-[.15em] text-[#e9dfc7]/60 transition-colors hover:bg-[#9cae82]/10 hover:text-[#e9dfc7]">Builder</a>
            <a href="#notes" onClick={() => setMobileOpen(false)} className="rounded px-3 py-2 font-mono text-[11px] uppercase tracking-[.15em] text-[#e9dfc7]/60 transition-colors hover:bg-[#9cae82]/10 hover:text-[#e9dfc7]">Notes</a>
            <a href="https://github.com/OKHP3/mermaid-theme-builder" target="_blank" rel="noreferrer" className="rounded px-3 py-2 font-mono text-[11px] uppercase tracking-[.15em] text-[#e9dfc7]/60 transition-colors hover:bg-[#9cae82]/10 hover:text-[#e9dfc7]">GitHub</a>
            <button onClick={scrollToTool} className="mt-1 inline-flex items-center justify-center gap-2 rounded-[3px] border border-[#d7763d] bg-[#d7763d] px-4 py-2.5 font-mono text-[11px] font-bold uppercase tracking-[.12em] text-[#17201c] transition-transform hover:-translate-y-0.5 sm:mt-0">
              Open builder <Icon name="arrow" size={14} />
            </button>
          </nav>

          <button onClick={() => setMobileOpen((value) => !value)} className="grid h-9 w-9 place-items-center rounded border border-[#9cae82]/25 text-[#e9dfc7]/80 sm:hidden" aria-label={mobileOpen ? "Close menu" : "Open menu"}>
            <Icon name={mobileOpen ? "x" : "menu"} />
          </button>
        </div>
      </header>

      <main id="top">
        <section className="mx-auto max-w-[1440px] px-5 pb-12 pt-10 sm:px-8 sm:pb-20 sm:pt-16 lg:pt-20">
          <div className="mb-8 flex items-center gap-2 font-mono text-[10px] uppercase tracking-[.18em] text-[#9cae82]/65">
            <span>overkillhill.com</span><span className="text-[#d7763d]">/</span><span>projects</span><span className="text-[#d7763d]">/</span><span className="text-[#e9dfc7]/80">mermaid-theme-builder</span>
          </div>
          <div className="grid gap-12 lg:grid-cols-[minmax(0,1.05fr)_minmax(350px,.75fr)] lg:items-end lg:gap-24">
            <div>
              <div className="mb-6 flex flex-wrap gap-2">
                <span className="rounded border border-[#9cae82]/30 bg-[#9cae82]/[.08] px-2.5 py-1 font-mono text-[10px] uppercase tracking-[.14em] text-[#b8c59d]">Community tool</span>
                <span className="rounded border border-[#d7763d]/40 bg-[#d7763d]/[.08] px-2.5 py-1 font-mono text-[10px] uppercase tracking-[.14em] text-[#e69f61]">V0.3 alpha</span>
              </div>
              <h1 className="max-w-[800px] text-[clamp(3.1rem,7vw,7rem)] font-black leading-[.88] tracking-[-.075em] text-[#e9dfc7]">
                Make the<br /><span className="text-[#d7763d]">diagram</span> yours.
              </h1>
              <p className="mt-7 max-w-[600px] text-base leading-7 text-[#e9dfc7]/62 sm:text-lg">
                A visual editor for Mermaid.js themes. Choose a color, watch every diagram respond, and export a production-ready theme without leaving the browser.
              </p>
              <div className="mt-8 flex flex-wrap items-center gap-3">
                <button onClick={scrollToTool} className="inline-flex items-center gap-2 rounded-[3px] border border-[#d7763d] bg-[#d7763d] px-5 py-3 font-mono text-xs font-bold uppercase tracking-[.1em] text-[#17201c] transition-transform hover:-translate-y-0.5">
                  Start designing <Icon name="arrow" size={15} />
                </button>
                <a href="https://github.com/OKHP3/mermaid-theme-builder" target="_blank" rel="noreferrer" className="inline-flex items-center gap-2 rounded-[3px] border border-[#9cae82]/25 px-5 py-3 font-mono text-xs font-bold uppercase tracking-[.1em] text-[#e9dfc7]/75 transition-colors hover:border-[#9cae82]/60 hover:text-[#e9dfc7]">
                  <Icon name="github" size={15} /> View source
                </a>
              </div>
            </div>
            <div className="relative border-l border-[#d7763d]/40 pl-6 lg:mb-2 lg:pl-8">
              <div className="absolute -left-[5px] top-0 h-2 w-2 rounded-full bg-[#d7763d] shadow-[0_0_0_5px_rgba(215,118,61,.12)]" />
              <p className="font-mono text-[10px] uppercase tracking-[.2em] text-[#d7763d]">The short version</p>
              <p className="mt-4 max-w-[360px] text-2xl font-medium leading-snug tracking-[-.03em] text-[#e9dfc7]">
                One round trip from a blank canvas to a theme you can ship.
              </p>
              <p className="mt-5 font-mono text-[10px] uppercase leading-5 tracking-[.13em] text-[#9cae82]/60">No login · no install · no data leaves your machine</p>
            </div>
          </div>
        </section>

        <section id="builder" className="scroll-mt-24 border-y border-[#9cae82]/15 bg-[#0c1515]/55">
          <div className="mx-auto max-w-[1440px] px-5 py-9 sm:px-8 sm:py-12">
            <div className="mb-5 flex flex-wrap items-end justify-between gap-4">
              <div>
                <div className="mb-2 flex items-center gap-2 font-mono text-[10px] uppercase tracking-[.18em] text-[#9cae82]"><span className="h-1.5 w-1.5 animate-pulse rounded-full bg-[#d7763d]" /> Live workspace</div>
                <h2 className="text-2xl font-bold tracking-[-.04em] text-[#e9dfc7] sm:text-3xl">Theme builder <span className="font-mono text-xs font-normal tracking-[.1em] text-[#e9dfc7]/35">/ 01</span></h2>
              </div>
              <div className="flex items-center gap-2 font-mono text-[10px] uppercase tracking-[.12em] text-[#9cae82]/60"><span className="h-1.5 w-1.5 rounded-full bg-[#9cae82]" /> Browser-only session</div>
            </div>

            <div className="overflow-hidden rounded-md border border-[#9cae82]/25 bg-[#14201f] shadow-[0_24px_80px_rgba(0,0,0,.24)]">
              <div className="flex flex-wrap items-center justify-between gap-3 border-b border-[#9cae82]/15 bg-[#192725] px-4 py-3 sm:px-5">
                <div className="flex items-center gap-1 rounded border border-[#9cae82]/15 bg-[#0e1817] p-1">
                  {(["theme", "preview", "export"] as const).map((tab) => (
                    <button key={tab} onClick={() => setActiveTab(tab)} className={`rounded px-3 py-1.5 font-mono text-[10px] uppercase tracking-[.13em] transition-colors ${activeTab === tab ? "bg-[#d7763d] font-bold text-[#17201c]" : "text-[#e9dfc7]/55 hover:text-[#e9dfc7]"}`}>
                      {tab === "theme" ? "Theme" : tab === "preview" ? "Preview" : "Export"}
                    </button>
                  ))}
                </div>
                <div className="flex items-center gap-2">
                  <button onClick={resetTheme} className="inline-flex items-center gap-1.5 rounded border border-[#9cae82]/20 px-3 py-1.5 font-mono text-[10px] uppercase tracking-[.1em] text-[#e9dfc7]/55 transition-colors hover:border-[#9cae82]/50 hover:text-[#e9dfc7]"><Icon name="refresh" size={13} /> Reset</button>
                  <button onClick={() => window.open("https://okhp3.github.io/mermaid-theme-builder/", "_blank", "noopener,noreferrer")} className="inline-flex items-center gap-1.5 rounded border border-[#d7763d]/55 bg-[#d7763d]/10 px-3 py-1.5 font-mono text-[10px] font-bold uppercase tracking-[.1em] text-[#e69f61] transition-colors hover:bg-[#d7763d]/20"><Icon name="external" size={13} /> Full screen</button>
                </div>
              </div>

              {activeTab === "theme" && (
                <div className="grid min-h-[510px] lg:grid-cols-[285px_minmax(0,1fr)]">
                  <aside className="border-b border-[#9cae82]/15 p-5 lg:border-b-0 lg:border-r">
                    <div className="mb-7 flex items-center justify-between"><span className="font-mono text-[10px] uppercase tracking-[.18em] text-[#9cae82]">Theme variables</span><span className="rounded bg-[#9cae82]/10 px-1.5 py-1 font-mono text-[9px] text-[#9cae82]">12 / 12</span></div>
                    <div className="space-y-5">
                      {colors.map((color) => (
                        <button key={color.label} onClick={() => setActiveColor(color.value)} className="group flex w-full items-center justify-between text-left">
                          <span><span className="block font-mono text-[10px] uppercase tracking-[.12em] text-[#e9dfc7]/60">{color.label}</span><span className="mt-1 block font-mono text-[10px] text-[#9cae82]/55">{color.value}</span></span>
                          <span className={`h-8 w-8 rounded-sm border transition-transform group-hover:scale-105 ${activeColor === color.value ? "border-[#e9dfc7] ring-2 ring-[#d7763d]/40 ring-offset-2 ring-offset-[#14201f]" : "border-[#e9dfc7]/20"}`} style={{ backgroundColor: color.value }} />
                        </button>
                      ))}
                    </div>
                    <div className="mt-8 border-t border-[#9cae82]/15 pt-5">
                      <div className="mb-2 flex items-center gap-2 font-mono text-[10px] uppercase tracking-[.12em] text-[#e9dfc7]/50"><Icon name="swatch" size={13} /> Active token</div>
                      <div className="flex items-center gap-2 rounded border border-[#d7763d]/35 bg-[#d7763d]/[.07] p-2.5"><span className="h-5 w-5 rounded-sm" style={{ backgroundColor: activeColor }} /><span className="font-mono text-[10px] text-[#e69f61]">{activeColor}</span></div>
                    </div>
                  </aside>
                  <div className="p-4 sm:p-6">
                    <div className="mb-5 flex items-center justify-between"><div><span className="font-mono text-[10px] uppercase tracking-[.18em] text-[#9cae82]">Canvas preview</span><p className="mt-1 text-xs text-[#e9dfc7]/45">Updates as you tune the palette</p></div><span className="font-mono text-[10px] text-[#e9dfc7]/35">FLOWCHART / 01</span></div>
                    <div className="grid gap-5 xl:grid-cols-[1fr_210px]">
                      <div className="relative min-h-[330px] overflow-hidden rounded border border-[#9cae82]/15 bg-[#101b1a] p-5 sm:p-8">
                        <div className="absolute right-4 top-4 font-mono text-[9px] uppercase tracking-[.16em] text-[#9cae82]/45">live render</div>
                        <div className="flex min-h-[280px] items-center justify-center">
                          <div className="flex w-full max-w-[480px] flex-col items-center gap-4">
                            <div className="w-[min(100%,230px)] rounded border px-5 py-3 text-center font-mono text-xs" style={{ borderColor: activeColor, color: activeColor, backgroundColor: `${activeColor}12` }}>Design your theme</div>
                            <div className="h-7 w-px bg-[#9cae82]/40" />
                            <div className="flex w-full items-start justify-center gap-3">
                              <div className="h-px w-1/4 bg-[#9cae82]/40" /><div className="h-7 w-px bg-[#9cae82]/40" /><div className="h-px w-1/4 bg-[#9cae82]/40" />
                            </div>
                            <div className="grid w-full grid-cols-2 gap-4">
                              <div className="rounded border border-[#9cae82]/50 bg-[#9cae82]/[.08] px-3 py-3 text-center font-mono text-[10px] text-[#b8c59d]">Pick a color</div>
                              <div className="rounded border border-[#9cae82]/50 bg-[#9cae82]/[.08] px-3 py-3 text-center font-mono text-[10px] text-[#b8c59d]">Preview the result</div>
                            </div>
                            <div className="h-7 w-px bg-[#9cae82]/40" />
                            <div className="rounded border border-[#e69f61]/65 bg-[#d7763d]/10 px-6 py-3 text-center font-mono text-[10px] font-bold uppercase tracking-[.08em] text-[#e69f61]">Ship the theme</div>
                          </div>
                        </div>
                      </div>
                      <div className="rounded border border-[#9cae82]/15 bg-[#192725] p-4">
                        <div className="mb-4 flex items-center justify-between"><span className="font-mono text-[10px] uppercase tracking-[.13em] text-[#e9dfc7]/55">Theme health</span><span className="text-lg font-bold text-[#b8c59d]">A−</span></div>
                        <div className="space-y-3">{[["Contrast", "Strong"], ["Coverage", "12 tokens"], ["Mode", "Dark"]].map(([label, value]) => <div key={label} className="flex items-center justify-between border-b border-[#9cae82]/10 pb-3 font-mono text-[10px]"><span className="text-[#e9dfc7]/45">{label}</span><span className="text-[#b8c59d]">{value}</span></div>)}</div>
                        <div className="mt-5 h-1 overflow-hidden rounded-full bg-[#9cae82]/15"><div className="h-full w-[86%] bg-[#d7763d]" /></div><p className="mt-2 font-mono text-[9px] leading-4 text-[#e9dfc7]/40">Good to export. All required variables have a value.</p>
                      </div>
                    </div>
                  </div>
                </div>
              )}

              {activeTab === "preview" && (
                <div className="grid min-h-[510px] place-items-center p-6 sm:p-12">
                  <div className="w-full max-w-[760px] rounded border border-[#9cae82]/20 bg-[#101b1a] p-6 sm:p-9">
                    <div className="mb-8 flex items-center justify-between border-b border-[#9cae82]/15 pb-4"><span className="font-mono text-[10px] uppercase tracking-[.16em] text-[#9cae82]">Sequence diagram</span><span className="font-mono text-[10px] text-[#e9dfc7]/35">PREVIEW / 02</span></div>
                    <div className="grid grid-cols-3 gap-3 text-center font-mono text-[10px] text-[#e9dfc7]/70"><div className="border-b-2 pb-3" style={{ borderColor: activeColor }}>Editor</div><div className="border-b border-[#9cae82]/30 pb-3">Theme API</div><div className="border-b border-[#9cae82]/30 pb-3">Mermaid</div></div>
                    <div className="relative mx-auto my-8 h-44 max-w-[580px] border-x border-dashed border-[#9cae82]/25">
                      <div className="absolute left-1/3 right-1/3 top-5 h-px bg-[#d7763d]" /><div className="absolute left-1/3 top-5 -translate-x-1/2 -translate-y-1/2 rounded-full bg-[#d7763d] p-1" /><div className="absolute right-1/3 top-5 translate-x-1/2 -translate-y-1/2 rounded-full bg-[#d7763d] p-1" />
                      <div className="absolute left-1/3 right-1/3 top-20 h-px bg-[#9cae82]/50" /><div className="absolute left-1/3 top-20 -translate-x-1/2 -translate-y-1/2 rounded-full bg-[#9cae82] p-1" /><div className="absolute right-1/3 top-20 translate-x-1/2 -translate-y-1/2 rounded-full bg-[#9cae82] p-1" />
                      <div className="absolute left-1/3 right-1/3 top-32 h-px bg-[#9cae82]/50" /><span className="absolute left-1/2 top-1 -translate-x-1/2 bg-[#101b1a] px-2 text-[9px] text-[#e69f61]">update(theme)</span><span className="absolute left-1/2 top-[4.25rem] -translate-x-1/2 bg-[#101b1a] px-2 text-[9px] text-[#9cae82]">render()</span>
                    </div>
                    <div className="rounded border border-[#d7763d]/30 bg-[#d7763d]/[.06] px-4 py-3 font-mono text-[10px] text-[#e69f61]">Theme applied in 42ms · all diagram types updated</div>
                  </div>
                </div>
              )}

              {activeTab === "export" && (
                <div className="grid min-h-[510px] gap-5 p-5 sm:p-8 lg:grid-cols-[1fr_270px]">
                  <div className="rounded border border-[#9cae82]/15 bg-[#101b1a] p-5"><div className="mb-5 flex items-center justify-between"><span className="font-mono text-[10px] uppercase tracking-[.15em] text-[#9cae82]">theme.ts</span><button onClick={copyExport} className="inline-flex items-center gap-1.5 rounded border border-[#9cae82]/25 px-2.5 py-1.5 font-mono text-[10px] text-[#e9dfc7]/65 transition-colors hover:border-[#d7763d]/60 hover:text-[#e69f61]"><Icon name={copied ? "check" : "copy"} size={12} /> {copied ? "Copied" : "Copy"}</button></div><pre className="overflow-auto font-mono text-xs leading-7 text-[#b8c59d]"><code>{`const theme = {\n  themeVariables: {\n    primaryColor: '${activeColor}',\n    primaryTextColor: '#e9dfc7',\n    lineColor: '#9cae82',\n    fontFamily: 'DM Sans'\n  }\n}`}</code></pre></div>
                  <div className="border-l border-[#9cae82]/15 pl-5"><span className="font-mono text-[10px] uppercase tracking-[.15em] text-[#9cae82]">Ready to leave</span><p className="mt-4 text-lg leading-7 text-[#e9dfc7]">Your theme is portable, readable, and yours.</p><p className="mt-4 text-sm leading-6 text-[#e9dfc7]/50">Paste the block into mermaid.initialize() and keep moving.</p><button onClick={copyExport} className="mt-7 inline-flex items-center gap-2 rounded-[3px] border border-[#d7763d] bg-[#d7763d] px-4 py-2.5 font-mono text-[10px] font-bold uppercase tracking-[.12em] text-[#17201c]">{copied ? "Copied to clipboard" : "Copy export"} <Icon name="arrow" size={13} /></button></div>
                </div>
              )}
            </div>
            <p className="mt-3 text-center font-mono text-[10px] uppercase tracking-[.1em] text-[#9cae82]/50">Embedded workspace · open full screen for the complete editor</p>
          </div>
        </section>

        <section id="notes" className="mx-auto max-w-[1440px] px-5 py-16 sm:px-8 sm:py-24">
          <div className="grid gap-12 lg:grid-cols-[.7fr_1.3fr] lg:gap-24">
            <div><div className="mb-4 flex items-center gap-2 font-mono text-[10px] uppercase tracking-[.18em] text-[#d7763d]"><Icon name="spark" size={14} /> Why this exists</div><h2 className="max-w-[450px] text-3xl font-bold leading-tight tracking-[-.055em] text-[#e9dfc7] sm:text-4xl">Stop describing the color. Start seeing it.</h2><p className="mt-5 max-w-[380px] text-sm leading-6 text-[#e9dfc7]/52">Prompting can produce a plausible blob of variables. It cannot show you how that choice behaves across a real diagram.</p></div>
            <div className="grid gap-px overflow-hidden rounded border border-[#9cae82]/20 bg-[#9cae82]/20 md:grid-cols-3">{features.map(([number, title, description]) => <div key={number} className="bg-[#14201f] p-5 sm:p-6"><span className="font-mono text-[10px] text-[#d7763d]">{number}</span><h3 className="mt-12 text-lg font-bold leading-snug tracking-[-.025em] text-[#e9dfc7]">{title}</h3><p className="mt-3 text-sm leading-6 text-[#e9dfc7]/50">{description}</p></div>)}</div>
          </div>
        </section>

        <section className="border-y border-[#9cae82]/15 bg-[#192725]/55">
          <div className="mx-auto grid max-w-[1440px] gap-8 px-5 py-12 sm:px-8 sm:py-16 md:grid-cols-[1fr_auto] md:items-center"><div><div className="mb-3 font-mono text-[10px] uppercase tracking-[.18em] text-[#9cae82]">Built for the Mermaid.js ecosystem</div><p className="max-w-[680px] text-2xl font-medium leading-snug tracking-[-.035em] text-[#e9dfc7]">A small tool with a specific job: make the visual part of theming feel as immediate as the code.</p></div><a href="https://mermaid.js.org/config/theming.html" target="_blank" rel="noreferrer" className="inline-flex items-center gap-2 font-mono text-xs uppercase tracking-[.12em] text-[#e69f61] transition-colors hover:text-[#e9dfc7]">Read the theming docs <Icon name="arrow" size={14} /></a></div>
        </section>
      </main>

      <footer className="mx-auto flex w-full max-w-[1440px] flex-col gap-5 px-5 py-8 sm:px-8 md:flex-row md:items-center md:justify-between">
        <div className="flex items-center gap-3"><span className="grid h-7 w-7 place-items-center rounded-sm border border-[#d7763d]/50 font-mono text-[9px] font-bold text-[#e69f61]">OK</span><span className="font-mono text-[10px] uppercase tracking-[.16em] text-[#e9dfc7]/45">OverKill Hill P³ · community contribution</span></div>
        <div className="flex gap-5 font-mono text-[10px] uppercase tracking-[.12em] text-[#e9dfc7]/40"><a href="https://github.com/OKHP3/mermaid-theme-builder" target="_blank" rel="noreferrer" className="transition-colors hover:text-[#e69f61]">MIT license</a><a href="https://github.com/OKHP3/mermaid-theme-builder/issues" target="_blank" rel="noreferrer" className="transition-colors hover:text-[#e69f61]">Report an issue</a></div>
      </footer>
    </div>
  );
}

export default MermaidThemeBuilderRefined;