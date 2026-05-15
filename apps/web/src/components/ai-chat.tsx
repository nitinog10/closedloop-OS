'use client';

import { useState } from 'react';
import { Loader2, Sparkles } from 'lucide-react';

import { askClosedLoop } from '@/lib/api';
import { ChatResponse } from '@/lib/types';
import { StreamingMessage } from './streaming-message';

const starter = 'What did we decide about authentication architecture?';

export function AIChat() {
  const [query, setQuery] = useState(starter);
  const [loading, setLoading] = useState(false);
  const [response, setResponse] = useState<ChatResponse | null>(null);

  async function handleAsk() {
    setLoading(true);
    const result = await askClosedLoop(query);
    setResponse(result);
    setLoading(false);
  }

  return (
    <div className="space-y-6">
      <div className="glass rounded-3xl p-6">
        <div className="mb-4 flex items-center gap-3">
          <div className="rounded-2xl bg-cyan-400/10 p-3 text-cyan-200 ring-1 ring-cyan-300/20">
            <Sparkles className="h-4 w-4" />
          </div>
          <div>
            <h3 className="text-lg font-semibold text-white">AI operational reasoning</h3>
            <p className="text-sm text-slate-400">Ask across Slack, GitHub, tickets, and institutional memory.</p>
          </div>
        </div>
        <textarea
          value={query}
          onChange={(event) => setQuery(event.target.value)}
          className="min-h-[140px] w-full rounded-3xl border border-white/10 bg-slate-950/60 p-4 text-sm text-white outline-none placeholder:text-slate-500"
          placeholder="What did we decide about authentication architecture?"
        />
        <div className="mt-4 flex items-center justify-between">
          <div className="text-sm text-slate-500">Semantic retrieval + graph expansion + citation engine</div>
          <button
            onClick={handleAsk}
            disabled={loading}
            className="flex items-center gap-2 rounded-2xl bg-cyan-400/15 px-4 py-3 text-sm text-cyan-100 ring-1 ring-cyan-300/20 hover:bg-cyan-400/20 disabled:opacity-60"
          >
            {loading ? <Loader2 className="h-4 w-4 animate-spin" /> : <Sparkles className="h-4 w-4" />}
            Ask ClosedLoop
          </button>
        </div>
      </div>
      {response ? <StreamingMessage answer={response.answer} citations={response.citations} /> : null}
    </div>
  );
}
