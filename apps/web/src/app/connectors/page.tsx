import { ConnectorCard } from '@/components/connector-card';
import { Shell } from '@/components/shell';
import { fetchConnectors } from '@/lib/api';

export default async function ConnectorsPage() {
  const connectors = await fetchConnectors();

  return (
    <Shell>
      <section className="glass rounded-3xl p-6">
        <h2 className="text-2xl font-semibold text-white">Connector management</h2>
        <p className="mt-2 text-sm text-slate-400">OAuth lifecycle, webhook health, and ingestion orchestration.</p>
      </section>
      <section className="grid gap-4 xl:grid-cols-2">
        {connectors.map((connector) => (
          <ConnectorCard key={connector.id} connector={connector} />
        ))}
      </section>
    </Shell>
  );
}
