import { Activity, Bot, DatabaseZap, ShieldCheck } from 'lucide-react';

import { GraphPanel } from '@/components/graph-panel';
import { MetricsCard } from '@/components/metrics-card';
import { NotificationsFeed } from '@/components/notifications-feed';
import { SearchBar } from '@/components/search-bar';
import { Shell } from '@/components/shell';
import { Timeline } from '@/components/timeline';
import { fetchNotifications } from '@/lib/api';

export default async function DashboardPage() {
  const notifications = await fetchNotifications();

  return (
    <Shell>
      <SearchBar />
      <section className="grid gap-4 md:grid-cols-2 xl:grid-cols-4">
        <MetricsCard label="Connected signals" value="52.1M" delta="+18.4%" icon={<DatabaseZap className="h-4 w-4" />} />
        <MetricsCard label="Reasoning requests" value="24,291" delta="+31%" icon={<Bot className="h-4 w-4" />} />
        <MetricsCard label="Decision confidence" value="96.1%" delta="+1.4%" icon={<ShieldCheck className="h-4 w-4" />} />
        <MetricsCard label="Risk anomalies" value="05" delta="-28%" icon={<Activity className="h-4 w-4" />} />
      </section>
      <section className="grid gap-6 xl:grid-cols-[1.3fr_0.7fr]">
        <GraphPanel />
        <Timeline />
      </section>
      <section className="grid gap-6 xl:grid-cols-[1fr_1fr]">
        <NotificationsFeed initialItems={notifications} />
        <section className="glass rounded-3xl p-6">
          <div className="flex items-start justify-between gap-6">
            <div>
              <p className="text-xs uppercase tracking-[0.3em] text-slate-500">ClosedLoop OS</p>
              <h3 className="mt-2 text-2xl font-semibold text-white">Phase 2 organizational intelligence mesh</h3>
              <p className="mt-3 max-w-3xl text-sm leading-7 text-slate-400">
                ClosedLoop OS now extends beyond MVP ingestion into hybrid vector retrieval, graph extraction, identity resolution, realtime notifications, and additional connectors for Linear, Notion, and Zoom transcripts.
              </p>
            </div>
            <div className="rounded-3xl border border-cyan-300/20 bg-cyan-400/10 px-5 py-4 text-sm text-cyan-100">
              Hybrid retrieval • Graph upserts • Realtime feed
            </div>
          </div>
        </section>
      </section>
    </Shell>
  );
}
