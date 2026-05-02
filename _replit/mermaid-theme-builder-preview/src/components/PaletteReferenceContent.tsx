const variables = [
  { var: "primaryColor", desc: "Main node fill color — the dominant hue in your diagram." },
  { var: "primaryTextColor", desc: "Text inside primary-colored nodes. Ensure contrast." },
  { var: "primaryBorderColor", desc: "Border/stroke of primary nodes." },
  { var: "secondaryColor", desc: "Secondary node fill — used for alternate node types." },
  { var: "secondaryTextColor", desc: "Text inside secondary nodes." },
  { var: "secondaryBorderColor", desc: "Border of secondary nodes." },
  { var: "tertiaryColor", desc: "Tertiary fill — subgraphs, clusters, grouping elements." },
  { var: "tertiaryTextColor", desc: "Text inside tertiary elements." },
  { var: "tertiaryBorderColor", desc: "Border of tertiary elements." },
  { var: "background", desc: "Canvas/diagram background. Usually the page's background color." },
  { var: "mainBkg", desc: "Default background for most node types." },
  { var: "nodeBorder", desc: "Default border for all node types." },
  { var: "clusterBkg", desc: "Subgraph/cluster fill color." },
  { var: "clusterBorder", desc: "Subgraph/cluster border." },
  { var: "lineColor", desc: "Arrow and edge line color." },
  { var: "edgeLabelBackground", desc: "Background of inline edge labels." },
  { var: "fontFamily", desc: "Font family applied to all diagram text." },
  { var: "fontSize", desc: "Base font size — default 16px." },
  { var: "labelBackground", desc: "Background of standalone labels." },
  { var: "labelTextColor", desc: "Color of standalone label text." },
  { var: "titleColor", desc: "Diagram title text color." },
];

export function PaletteReferenceContent() {
  return (
    <div className="space-y-3 pt-2">
      <p className="text-sm text-muted-foreground">
        All Mermaid themeVariables touched by the builder, and what they control.
      </p>
      <div className="overflow-x-auto -mx-1">
        <table className="w-full text-xs" data-testid="table-palette-reference">
          <thead>
            <tr className="border-b border-border/40">
              <th className="text-left font-mono text-muted-foreground py-2 pr-4 font-medium w-48">Variable</th>
              <th className="text-left font-mono text-muted-foreground py-2 font-medium">Effect</th>
            </tr>
          </thead>
          <tbody>
            {variables.map((v, i) => (
              <tr
                key={v.var}
                className={`border-b border-border/20 ${i % 2 === 0 ? "" : "bg-muted/20"}`}
                data-testid={`palette-row-${v.var}`}
              >
                <td className="py-1.5 pr-4 font-mono text-primary/80 align-top">{v.var}</td>
                <td className="py-1.5 text-muted-foreground align-top">{v.desc}</td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
      <p className="text-xs text-muted-foreground pt-1">
        The builder exports these as a complete <code className="font-mono text-primary/80">themeVariables</code> object. Pass them to{" "}
        <code className="font-mono text-primary/80">mermaid.initialize(&#123; theme: 'base', themeVariables: &#123;...&#125; &#125;)</code>.
      </p>
    </div>
  );
}
