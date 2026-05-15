import { Shell } from '@/components/shell';

const memoryEntries = [
  {
    title: 'Authentication architecture decision',
    body: 'Organization converged on centralized token validation middleware and service-scoped authorization policies.'
  },
  {
    title: 'PR review consensus on auth caching',
    body: 'Cache JWKS metadata with bounded TTL to reduce latency and external dependency pressure.'
  },
  {
    title: 'Incident follow-up for identity outage',
    body: 'Backoff and failover strategy should be implemented before full migration.'
  }
];

export default function MemoryPage() {
  return (
    <Shell>
      <section className="glass rounded-3xl p-6">
        <h2 className="text-2xl font-semibold text-white">Organization memory</h2>
        <p className="mt-2 text-sm text-slate-400">Durable institutional knowledge built from conversations, decisions, and artifacts.</p>
      </section>
      <section className="space-y-4">
        {memoryEntries.map((entry) => (
          <div key={entry.title} className="glass rounded-3xl p-5">
            <h3 className="font-semibold text-white">{entry.title}</h3>
            <p className="mt-2 text-sm leading-7 text-slate-400">{entry.body}</p>
          </div>
        ))}
      </section>
    </Shell>
  );
}
