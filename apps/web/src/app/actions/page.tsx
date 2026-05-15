import { Shell } from '@/components/shell';

const actions = [
  ['Open Linear issue', 'Create a follow-up for unresolved auth provider ambiguity.'],
  ['Notify Slack', 'Post summary to #platform-architecture with cited decision trace.'],
  ['Request review', 'Assign security lead to PRs affecting auth middleware.']
];

export default function ActionsPage() {
  return (
    <Shell>
      <section className="glass rounded-3xl p-6">
        <h2 className="text-2xl font-semibold text-white">AI actions center</h2>
        <p className="mt-2 text-sm text-slate-400">Governed operational recommendations with human approval loops.</p>
      </section>
      <section className="grid gap-4 xl:grid-cols-3">
        {actions.map(([title, body]) => (
          <div key={title} className="glass rounded-3xl p-5">
            <h3 className="font-semibold text-white">{title}</h3>
            <p className="mt-2 text-sm leading-7 text-slate-400">{body}</p>
            <button className="mt-4 rounded-2xl border border-cyan-300/20 bg-cyan-400/10 px-4 py-2 text-sm text-cyan-100">
              Review action
            </button>
          </div>
        ))}
      </section>
    </Shell>
  );
}
