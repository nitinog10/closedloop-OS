import { Citation } from '@/lib/types';

export function StreamingMessage({ answer, citations }: { answer: string; citations: Citation[] }) {
  return (
    <div className="glass rounded-3xl p-6">
      <div className="mb-4 flex items-center justify-between">
        <h3 className="text-lg font-semibold text-white">Answer</h3>
        <span className="rounded-full border border-cyan-300/20 bg-cyan-400/10 px-3 py-1 text-xs text-cyan-100">
          Cited response
        </span>
      </div>
      <div className="whitespace-pre-wrap text-sm leading-7 text-slate-200">{answer}</div>
      <div className="mt-6 flex flex-wrap gap-3">
        {citations.map((citation, index) => (
          <div key={citation.event_id} className="rounded-2xl border border-white/10 bg-white/5 px-4 py-3 text-sm text-slate-300">
            <span className="mr-2 text-cyan-300">[{index + 1}]</span>
            {citation.source_title}
          </div>
        ))}
      </div>
    </div>
  );
}
