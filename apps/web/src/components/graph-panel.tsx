const nodes = [
  { left: '12%', top: '30%', label: 'Slack', color: 'bg-cyan-400/80' },
  { left: '44%', top: '18%', label: 'Decision', color: 'bg-violet-400/80' },
  { left: '73%', top: '36%', label: 'GitHub PR', color: 'bg-sky-400/80' },
  { left: '55%', top: '68%', label: 'AUTH-142', color: 'bg-emerald-400/80' },
  { left: '25%', top: '70%', label: 'Goal', color: 'bg-fuchsia-400/80' }
];

export function GraphPanel() {
  return (
    <div className="glass relative min-h-[340px] overflow-hidden rounded-3xl p-6">
      <div className="absolute inset-0 opacity-30">
        <svg className="h-full w-full" viewBox="0 0 800 400" fill="none">
          <path d="M140 120C240 70 290 90 370 120C470 160 540 140 650 150" stroke="rgba(112,240,255,0.45)" strokeWidth="2" />
          <path d="M360 120C390 180 430 210 490 270" stroke="rgba(196,181,253,0.45)" strokeWidth="2" />
          <path d="M180 270C270 240 390 230 490 270" stroke="rgba(134,239,172,0.35)" strokeWidth="2" />
          <path d="M120 130C110 190 120 230 180 270" stroke="rgba(244,114,182,0.35)" strokeWidth="2" />
        </svg>
      </div>
      <div className="relative z-10 flex items-center justify-between">
        <div>
          <h3 className="text-lg font-semibold text-white">Knowledge graph intelligence</h3>
          <p className="text-sm text-slate-400">Cross-tool entity mapping and decision lineage.</p>
        </div>
        <span className="rounded-full border border-white/10 px-3 py-1 text-xs text-slate-300">Multi-hop ready</span>
      </div>
      <div className="relative mt-6 h-[240px] rounded-3xl border border-white/10 bg-slate-950/40">
        {nodes.map((node) => (
          <div
            key={node.label}
            className="absolute -translate-x-1/2 -translate-y-1/2"
            style={{ left: node.left, top: node.top }}
          >
            <div className={`rounded-full ${node.color} px-4 py-2 text-sm font-medium text-slate-950 shadow-glow`}>
              {node.label}
            </div>
          </div>
        ))}
      </div>
    </div>
  );
}
