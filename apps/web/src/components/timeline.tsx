const items = [
  {
    time: '09:41',
    title: 'Slack auth discussion ingested',
    description: 'Decision fragments indexed from #platform-architecture.'
  },
  {
    time: '10:12',
    title: 'GitHub PR review analyzed',
    description: 'PR #418 on auth middleware linked to ticket AUTH-142.'
  },
  {
    time: '10:44',
    title: 'Linear roadmap issue linked',
    description: 'Goal alignment detected for AUTH-142 and identity unification.'
  },
  {
    time: '11:03',
    title: 'Reasoning graph refreshed',
    description: 'Entity edges updated for people, repos, decisions, tickets, and goals.'
  }
];

export function Timeline() {
  return (
    <div className="glass rounded-3xl p-6">
      <div className="mb-6 flex items-center justify-between">
        <h3 className="text-lg font-semibold text-white">Operational timeline</h3>
        <span className="text-xs uppercase tracking-[0.3em] text-slate-500">Live</span>
      </div>
      <div className="space-y-5">
        {items.map((item) => (
          <div key={item.time} className="flex gap-4">
            <div className="mt-1 h-3 w-3 rounded-full bg-cyan-300 shadow-[0_0_24px_rgba(112,240,255,0.65)]" />
            <div>
              <p className="text-xs uppercase tracking-[0.25em] text-slate-500">{item.time}</p>
              <p className="mt-1 font-medium text-white">{item.title}</p>
              <p className="text-sm text-slate-400">{item.description}</p>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
}
