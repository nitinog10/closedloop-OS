import { ReactNode } from 'react';

export function MetricsCard({
  label,
  value,
  delta,
  icon
}: {
  label: string;
  value: string;
  delta: string;
  icon: ReactNode;
}) {
  return (
    <div className="glass rounded-3xl p-5 shadow-glow">
      <div className="mb-4 flex items-center justify-between text-slate-300">
        <span className="text-sm">{label}</span>
        <div className="rounded-2xl border border-white/10 bg-white/5 p-2">{icon}</div>
      </div>
      <div className="flex items-end justify-between gap-4">
        <h3 className="text-3xl font-semibold text-white">{value}</h3>
        <span className="text-sm text-emerald-300">{delta}</span>
      </div>
    </div>
  );
}
