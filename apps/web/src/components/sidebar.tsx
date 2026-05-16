'use client';

import type { Route } from 'next';
import Link from 'next/link';
import { usePathname } from 'next/navigation';
import { BrainCircuit, Cable, ChartColumnBig, GitBranch, LayoutDashboard, MemoryStick, Rocket } from 'lucide-react';

import { cn } from '@/lib/utils';

const items: Array<{ href: Route; label: string; icon: typeof BrainCircuit }> = [
  { href: '/', label: 'Dashboard', icon: LayoutDashboard },
  { href: '/chat', label: 'AI Chat', icon: BrainCircuit },
  { href: '/graph', label: 'Graph Explorer', icon: GitBranch },
  { href: '/connectors', label: 'Connectors', icon: Cable },
  { href: '/insights', label: 'Insights', icon: ChartColumnBig },
  { href: '/memory', label: 'Memory', icon: MemoryStick },
  { href: '/actions', label: 'AI Actions', icon: Rocket }
];

export function Sidebar() {
  const pathname = usePathname();

  return (
    <aside className="glass hidden h-[calc(100vh-2rem)] w-72 shrink-0 rounded-3xl p-4 shadow-glow lg:block">
      <div className="mb-8 flex items-center gap-3 px-3 py-2">
        <div className="flex h-11 w-11 items-center justify-center rounded-2xl bg-cyan-400/15 text-cyan-300 ring-1 ring-cyan-200/20">
          <BrainCircuit className="h-5 w-5" />
        </div>
        <div>
          <p className="text-xs uppercase tracking-[0.3em] text-slate-400">ClosedLoop</p>
          <h1 className="text-lg font-semibold text-white">Operating System</h1>
        </div>
      </div>
      <nav className="space-y-2">
        {items.map((item) => {
          const Icon = item.icon;
          const active = pathname === item.href;
          return (
            <Link
              key={item.href}
              href={item.href}
              className={cn(
                'flex items-center gap-3 rounded-2xl px-4 py-3 text-sm text-slate-300 transition hover:bg-white/5 hover:text-white',
                active && 'bg-cyan-400/10 text-cyan-200 ring-1 ring-cyan-300/20'
              )}
            >
              <Icon className="h-4 w-4" />
              {item.label}
            </Link>
          );
        })}
      </nav>
      <div className="mt-8 rounded-2xl border border-cyan-400/10 bg-cyan-400/5 p-4 text-sm text-slate-300">
        <p className="mb-1 text-cyan-200">Phase 2 status</p>
        <p>Hybrid retrieval, graph extraction, Linear/Notion/Zoom ingestion, tenant reindexing, and realtime notifications are now scaffolded.</p>
      </div>
    </aside>
  );
}
