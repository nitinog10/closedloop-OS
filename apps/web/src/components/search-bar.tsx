'use client';

import { Search } from 'lucide-react';

export function SearchBar() {
  return (
    <div className="glass flex items-center gap-3 rounded-3xl px-5 py-4">
      <Search className="h-4 w-4 text-slate-400" />
      <input
        className="w-full bg-transparent text-sm text-white outline-none placeholder:text-slate-500"
        placeholder="Ask ClosedLoop about decisions, incidents, PRs, teams, or architecture..."
      />
    </div>
  );
}
