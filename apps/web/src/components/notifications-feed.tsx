'use client';

import { useEffect, useMemo, useState } from 'react';
import { BellRing } from 'lucide-react';

import { websocketUrl } from '@/lib/api';
import { NotificationItem } from '@/lib/types';

export function NotificationsFeed({ initialItems }: { initialItems: NotificationItem[] }) {
  const [items, setItems] = useState<NotificationItem[]>(initialItems);

  useEffect(() => {
    const socket = new WebSocket(websocketUrl('/api/v1/notifications/ws/00000000-0000-0000-0000-000000000001'));

    socket.onmessage = (event) => {
      try {
        const payload = JSON.parse(event.data) as NotificationItem;
        setItems((current) => [payload, ...current].slice(0, 8));
      } catch {
        // ignore malformed payloads
      }
    };

    return () => socket.close();
  }, []);

  const visibleItems = useMemo(() => items.slice(0, 5), [items]);

  return (
    <div className="glass rounded-3xl p-6">
      <div className="mb-6 flex items-center justify-between">
        <div className="flex items-center gap-3">
          <div className="rounded-2xl bg-cyan-400/10 p-3 text-cyan-200 ring-1 ring-cyan-300/20">
            <BellRing className="h-4 w-4" />
          </div>
          <div>
            <h3 className="text-lg font-semibold text-white">Realtime operational feed</h3>
            <p className="text-sm text-slate-400">Live notifications from ingestion and graph intelligence.</p>
          </div>
        </div>
        <span className="rounded-full border border-emerald-400/20 bg-emerald-400/10 px-3 py-1 text-xs text-emerald-200">
          streaming
        </span>
      </div>
      <div className="space-y-4">
        {visibleItems.map((item) => (
          <div key={`${item.id}-${item.created_at}`} className="rounded-2xl border border-white/10 bg-slate-950/40 p-4">
            <div className="mb-2 flex items-center justify-between gap-3">
              <p className="font-medium text-white">{item.title}</p>
              <span className="rounded-full border border-white/10 px-2 py-1 text-[10px] uppercase tracking-[0.25em] text-slate-400">
                {item.severity}
              </span>
            </div>
            <p className="text-sm leading-6 text-slate-400">{item.body}</p>
          </div>
        ))}
      </div>
    </div>
  );
}
