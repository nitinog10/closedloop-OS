'use client';

import { Bell, Search, Sparkles } from 'lucide-react';

import { useAppStore } from '@/lib/store';

export function Header() {
  const workspace = useAppStore((state) => state.workspace);

  return (
    <header className="glass flex items-center justify-between rounded-3xl px-6 py-4">
      <div>
        <p className="text-xs uppercase tracking-[0.3em] text-slate-400">Workspace</p>
        <div className="mt-1 flex items-center gap-3">
          <h2 className="text-xl font-semibold text-white">{workspace}</h2>
          <span className="rounded-full border border-emerald-400/20 bg-emerald-400/10 px-3 py-1 text-xs text-emerald-200">
            Live reasoning mesh
          </span>
        </div>
      </div>
      <div className="flex items-center gap-3">
        <button className="rounded-2xl border border-white/10 bg-white/5 p-3 text-slate-300 hover:text-white">
          <Search className="h-4 w-4" />
        </button>
        <button className="rounded-2xl border border-white/10 bg-white/5 p-3 text-slate-300 hover:text-white">
          <Bell className="h-4 w-4" />
        </button>
        <button className="flex items-center gap-2 rounded-2xl bg-cyan-400/10 px-4 py-3 text-sm text-cyan-200 ring-1 ring-cyan-300/20">
          <Sparkles className="h-4 w-4" />
          AI ready
        </button>
      </div>
    </header>
  );
}
