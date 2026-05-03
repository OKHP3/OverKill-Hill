import { RefObject, useState, useCallback, useRef, useEffect } from "react";

interface EmbedSectionProps {
  iframeRef: RefObject<HTMLIFrameElement | null>;
  iframeKey: number;
  onReload: () => void;
  onFullscreen: () => void;
}

export default function EmbedSection({ iframeRef, iframeKey, onReload, onFullscreen }: EmbedSectionProps) {
  const [loaded, setLoaded] = useState(false);
  const [slow, setSlow] = useState(false);
  const slowTimerRef = useRef<ReturnType<typeof setTimeout> | null>(null);

  const startSlowTimer = useCallback(() => {
    if (slowTimerRef.current) clearTimeout(slowTimerRef.current);
    slowTimerRef.current = setTimeout(() => setSlow(true), 8000);
  }, []);

  const clearSlowTimer = useCallback(() => {
    if (slowTimerRef.current) clearTimeout(slowTimerRef.current);
  }, []);

  useEffect(() => {
    setLoaded(false);
    setSlow(false);
    startSlowTimer();
    return clearSlowTimer;
  }, [iframeKey, startSlowTimer, clearSlowTimer]);

  const handleLoad = useCallback(() => {
    clearSlowTimer();
    setLoaded(true);
    setSlow(false);
  }, [clearSlowTimer]);

  const handleReload = useCallback(() => {
    setLoaded(false);
    setSlow(false);
    startSlowTimer();
    onReload();
  }, [onReload, startSlowTimer]);

  return (
    <section id="embed-tool" className="scroll-mt-20" data-testid="section-embed">
      {/* Toolbar */}
      <div className="flex items-center justify-between mb-3">
        <div className="flex items-center gap-2">
          <span className="okhp3-label">Live Tool</span>
          <span className="inline-flex items-center gap-1 font-mono text-xs text-primary/80">
            <span className="w-1.5 h-1.5 rounded-full bg-primary animate-pulse" />
            okhp3.github.io
          </span>
        </div>
        <div className="flex items-center gap-2">
          <button
            onClick={handleReload}
            className="flex items-center gap-1.5 px-3 py-1.5 rounded border border-border/60 bg-card text-muted-foreground hover:text-foreground hover:border-border transition-all text-xs font-mono"
            data-testid="button-iframe-reload"
            title="Reload tool"
          >
            <svg viewBox="0 0 24 24" className="w-3.5 h-3.5 fill-none stroke-current stroke-2" aria-hidden="true">
              <polyline points="23 4 23 10 17 10" />
              <polyline points="1 20 1 14 7 14" />
              <path d="M3.51 9a9 9 0 0 1 14.85-3.36L23 10M1 14l4.64 4.36A9 9 0 0 0 20.49 15" />
            </svg>
            Reload
          </button>
          <button
            onClick={onFullscreen}
            className="flex items-center gap-1.5 px-3 py-1.5 rounded border border-primary/50 bg-primary/10 text-primary hover:bg-primary/20 transition-all text-xs font-mono font-semibold"
            data-testid="button-iframe-fullscreen"
            title="Open in new tab"
          >
            <svg viewBox="0 0 24 24" className="w-3.5 h-3.5 fill-none stroke-current stroke-2" aria-hidden="true">
              <path d="M18 13v6a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2V8a2 2 0 0 1 2-2h6" />
              <polyline points="15 3 21 3 21 9" />
              <line x1="10" y1="14" x2="21" y2="3" />
            </svg>
            Full Screen
          </button>
        </div>
      </div>

      {/* Fallback CTA — always visible above iframe */}
      <div className="flex justify-center mb-3">
        <a
          href="https://okhp3.github.io/mermaid-theme-builder/"
          target="_blank"
          rel="noopener noreferrer"
          className="inline-flex items-center gap-1.5 px-4 py-2 rounded border border-primary bg-primary text-primary-foreground font-mono font-semibold text-xs hover:bg-primary/90 transition-all"
          data-testid="button-iframe-fullscreen-cta"
        >
          <svg viewBox="0 0 24 24" className="w-3.5 h-3.5 fill-none stroke-current stroke-2" aria-hidden="true">
            <path d="M18 13v6a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2V8a2 2 0 0 1 2-2h6" />
            <polyline points="15 3 21 3 21 9" />
            <line x1="10" y1="14" x2="21" y2="3" />
          </svg>
          Open Mermaid Theme Builder Full Screen
        </a>
      </div>

      {/* Iframe container */}
      <div className="iframe-wrapper okhp3-glow rounded-md relative">
        {/* Loading overlay — hidden once iframe fires onLoad */}
        {!loaded && (
          <div
            className="absolute inset-0 z-10 flex flex-col items-center justify-center gap-4 bg-background rounded-md"
            style={{ minHeight: "900px" }}
            aria-hidden="true"
            data-testid="iframe-loading-overlay"
          >
            <div className="w-9 h-9 rounded-full border-[3px] border-primary/20 border-t-primary animate-spin" />
            <span className="font-mono text-xs text-primary/70 tracking-wide">Loading Mermaid Theme Builder…</span>
            {slow && (
              <div className="flex flex-col items-center gap-1.5 mt-1">
                <span className="font-mono text-xs text-muted-foreground">Taking longer than expected?</span>
                <button
                  onClick={onFullscreen}
                  className="font-mono text-xs text-primary underline underline-offset-2 hover:text-primary/80 transition-colors"
                  data-testid="iframe-fallback-open"
                >
                  Open the tool in a new tab →
                </button>
              </div>
            )}
          </div>
        )}
        <iframe
          key={iframeKey}
          ref={iframeRef}
          src="https://okhp3.github.io/mermaid-theme-builder/"
          title="Mermaid Theme Builder"
          loading="lazy"
          allow="clipboard-read; clipboard-write; fullscreen"
          referrerPolicy="no-referrer-when-downgrade"
          style={{ width: "100%", minHeight: "900px", border: 0 }}
          onLoad={handleLoad}
          data-testid="iframe-tool"
        />
      </div>

      <p className="mt-2 text-xs text-muted-foreground font-mono text-center">
        Embedded from{" "}
        <a
          href="https://okhp3.github.io/mermaid-theme-builder/"
          target="_blank"
          rel="noopener noreferrer"
          className="text-primary/80 hover:text-primary transition-colors"
          data-testid="link-tool-source"
        >
          okhp3.github.io/mermaid-theme-builder
        </a>
        {" "}— open in new tab for best experience
      </p>
    </section>
  );
}
