import { GraphPanel } from '@/components/graph-panel';
import { Shell } from '@/components/shell';

export default function GraphPage() {
  return (
    <Shell>
      <GraphPanel />
      <section className="glass rounded-3xl p-6 text-sm leading-7 text-slate-300">
        The graph explorer surface is designed to visualize entity resolution across people, tickets, repositories, goals, and decisions. In production, this panel should be powered by a graph traversal API and support path queries, temporal filters, and centrality-based ranking.
      </section>
    </Shell>
  );
}
