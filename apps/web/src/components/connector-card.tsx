import { PlugZap } from 'lucide-react';

import { Connector } from '@/lib/types';

export function ConnectorCard({ connector }: { connector: Connector }) {
  return (
    <div className="glass rounded-3xl p-5">
      <div className="mb-4 flex items-center justify-between">
        <div className="flex items-center gap-3">
          <div className="rounded-2xl bg-cyan-400/10 p-3 text-cyan-200 ring-1 ring-cyan-300/20">
            <PlugZap className="h-4 w-4" />
          </div>
          <div>
            <h3 className="font-semibold capitalize text-white">{connector.type}</h3>
            <p className="text-sm text-slate-400">Connector orchestration</p>
          </div>
        </div>
        <span className="rounded-full border border-emerald-400/20 bg-emerald-400/10 px-3 py-1 text-xs text-emerald-200">
          {connector.status}
        </span>
      </div>
      <pre className="overflow-x-auto rounded-2xl bg-slate-950/60 p-4 text-xs text-slate-300">{JSON.stringify(connector.config, null, 2)}</pre>
    </div>
  );
}
