import { useState, useRef, useCallback } from "react";
import SiteHeader from "@/components/SiteHeader";
import SiteFooter from "@/components/SiteFooter";
import Hero from "@/components/Hero";
import EmbedSection from "@/components/EmbedSection";
import WhySection from "@/components/WhySection";
import FeatureList from "@/components/FeatureList";
import CollapsibleSection from "@/components/CollapsibleSection";
import ProjectSidebar from "@/components/ProjectSidebar";
import BuilderNote from "@/components/BuilderNote";
import StoryPlaceholder from "@/components/StoryPlaceholder";
import { UserGuideContent } from "@/components/UserGuideContent";
import { PaletteReferenceContent } from "@/components/PaletteReferenceContent";
import { FaqContent } from "@/components/FaqContent";

export default function ProjectPage() {
  const iframeRef = useRef<HTMLIFrameElement>(null);
  const [iframeKey, setIframeKey] = useState(0);

  const handleReload = useCallback(() => {
    setIframeKey(k => k + 1);
  }, []);

  const handleFullscreen = useCallback(() => {
    window.open("https://okhp3.github.io/mermaid-theme-builder/", "_blank", "noopener,noreferrer");
  }, []);

  return (
    <div className="min-h-screen bg-background flex flex-col">
      <SiteHeader />
      <main className="flex-1">
        <Hero />

        <section className="container mx-auto px-4 py-8 max-w-7xl">
          <div className="grid grid-cols-1 xl:grid-cols-[1fr_320px] gap-8 items-start">
            {/* Main column */}
            <div className="space-y-10">
              <EmbedSection
                iframeRef={iframeRef}
                iframeKey={iframeKey}
                onReload={handleReload}
                onFullscreen={handleFullscreen}
              />

              <WhySection />
              <FeatureList />

              <div className="space-y-3">
                <CollapsibleSection title="User Guide" id="user-guide">
                  <UserGuideContent />
                </CollapsibleSection>

                <CollapsibleSection title="Palette Reference" id="palette-reference">
                  <PaletteReferenceContent />
                </CollapsibleSection>

                <CollapsibleSection title="FAQ" id="faq">
                  <FaqContent />
                </CollapsibleSection>
              </div>

              <BuilderNote />
              <StoryPlaceholder />
            </div>

            {/* Right rail */}
            <aside className="xl:sticky xl:top-6">
              <ProjectSidebar onOpenTool={handleFullscreen} />
            </aside>
          </div>
        </section>
      </main>
      <SiteFooter />
    </div>
  );
}
