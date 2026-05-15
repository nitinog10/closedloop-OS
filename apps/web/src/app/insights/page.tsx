import { Shell } from '@/components/shell';

const cards = [
  ['Alignment drift', 'Auth migration is 2 sprint points behind identity roadmap.', 'medium'],
  ['Decision volatility', 'Multiple Slack threads mention auth provider changes with inconsistent language.', 'high'],
  ['Review bottleneck', 'PR review latency rose 18% in the platform repository.', 'medium']
];

export default function InsightsPage() {
  return (
    <Shell>
      <section className="glass rounded-3xl p-6">
        <h2 className="text-2xl font-semibold text-white">Operational insights</h2>
        <p className="mt-2 text-sm text-slate-400">Predictive risk, anomaly detection, and goal alignment signals.</p>
      </section>
      <section className="grid gap-4 xl:grid-cols-3">
        {cards.map(([title, body, severity]) => (
          <div key={title} className="glass rounded-3xl p-5">
            <div className="mb-3 flex items-center justify-between">
              <h3 className="font-semibold text-white">{title}</h3>
              <span className="rounded-full border border-white/10 px-3 py-1 text-xs uppercase text-slate-300">{severity}</span>
            </div>
            <p className="text-sm leading-7 text-slate-400">{body}</p>
          </div>
        ))}
      </section>
    </Shell>
  );
}
