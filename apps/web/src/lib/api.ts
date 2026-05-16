import { ChatResponse, Connector, NotificationItem } from '@/lib/types';

const API_URL = process.env.NEXT_PUBLIC_API_URL ?? 'http://localhost:8000';
const DEMO_EMAIL = process.env.NEXT_PUBLIC_DEMO_EMAIL ?? 'demo@closedloop.ai';
const DEMO_PASSWORD = process.env.NEXT_PUBLIC_DEMO_PASSWORD ?? 'demo';
const FALLBACK_AUTH_HEADER = 'Bearer demo-token-placeholder';

let cachedAccessToken: string | null = null;
let cachedTokenAt = 0;

const fallbackConnectors: Connector[] = [
  {
    id: 'slack-1',
    type: 'slack',
    status: 'connected',
    config: { channels: ['engineering', 'security', 'product'] }
  },
  {
    id: 'github-1',
    type: 'github',
    status: 'connected',
    config: { repos: ['closedloop/core', 'closedloop/web'] }
  },
  {
    id: 'linear-1',
    type: 'linear',
    status: 'beta',
    config: { teams: ['PLAT', 'OPS'] }
  },
  {
    id: 'notion-1',
    type: 'notion',
    status: 'beta',
    config: { spaces: ['engineering', 'exec'] }
  },
  {
    id: 'zoom-1',
    type: 'zoom',
    status: 'beta',
    config: { transcripts: true }
  }
];

const fallbackNotifications: NotificationItem[] = [
  {
    id: 'notif-1',
    type: 'ingestion.completed',
    title: 'Slack ingestion complete',
    body: 'Processed platform-architecture events and refreshed graph intelligence.',
    severity: 'info',
    payload: { source: 'slack' },
    created_at: new Date().toISOString()
  },
  {
    id: 'notif-2',
    type: 'risk.signal',
    title: 'Decision volatility detected',
    body: 'Multiple auth discussions diverge on provider failover strategy.',
    severity: 'medium',
    payload: { area: 'identity' },
    created_at: new Date(Date.now() - 1000 * 60 * 12).toISOString()
  }
];

export async function fetchConnectors(): Promise<Connector[]> {
  try {
    const authHeader = await getAuthHeader();
    const response = await fetch(`${API_URL}/api/v1/connectors`, {
      headers: { Authorization: authHeader },
      cache: 'no-store'
    });

    if (!response.ok) return fallbackConnectors;
    return response.json();
  } catch {
    return fallbackConnectors;
  }
}

export async function fetchNotifications(): Promise<NotificationItem[]> {
  try {
    const authHeader = await getAuthHeader();
    const response = await fetch(`${API_URL}/api/v1/notifications/recent`, {
      headers: { Authorization: authHeader },
      cache: 'no-store'
    });

    if (!response.ok) return fallbackNotifications;
    return response.json();
  } catch {
    return fallbackNotifications;
  }
}

export async function askClosedLoop(query: string): Promise<ChatResponse> {
  try {
    const authHeader = await getAuthHeader();
    const response = await fetch(`${API_URL}/api/v1/chat/query`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        Authorization: authHeader
      },
      body: JSON.stringify({ query, limit: 6 })
    });

    if (!response.ok) {
      return {
        answer:
          'ClosedLoop OS fallback answer:\n- Live API is not yet authenticated in the preview environment.\n- The Phase 2 scaffold now supports hybrid retrieval, vector indexing, graph extraction, additional connectors, and real-time notifications.\n- Start the API, log in via /api/v1/auth/login using password `demo`, trigger /api/v1/pipeline/reindex, and wire the JWT into the frontend for full functionality.',
        citations: [
          {
            event_id: 'demo-1',
            source_type: 'slack',
            source_title: 'Slack auth thread',
            quote: 'We should centralize token validation in shared middleware.',
            relevance_score: 0.91
          },
          {
            event_id: 'demo-2',
            source_type: 'github',
            source_title: 'PR #418 auth middleware',
            quote: 'Reviewers approved moving provider-specific logic behind a policy abstraction.',
            relevance_score: 0.88
          },
          {
            event_id: 'demo-3',
            source_type: 'linear',
            source_title: 'AUTH-142 Unify authentication middleware',
            quote: 'Goal: complete identity unification before Q4.',
            relevance_score: 0.83
          }
        ],
        trace: { mode: 'fallback-phase-2' }
      };
    }

    return response.json();
  } catch {
    return {
      answer: 'Backend unavailable. This UI scaffold is ready for live API wiring.',
      citations: [],
      trace: {}
    };
  }
}

export function websocketUrl(path: string) {
  return API_URL.replace('http://', 'ws://').replace('https://', 'wss://') + path;
}

async function getAuthHeader(): Promise<string> {
  const now = Date.now();
  if (cachedAccessToken && now - cachedTokenAt < 50 * 60 * 1000) {
    return `Bearer ${cachedAccessToken}`;
  }

  try {
    const response = await fetch(`${API_URL}/api/v1/auth/login`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({
        email: DEMO_EMAIL,
        password: DEMO_PASSWORD
      }),
      cache: 'no-store'
    });

    if (!response.ok) {
      return FALLBACK_AUTH_HEADER;
    }

    const payload = (await response.json()) as { access_token?: string };
    if (!payload.access_token) {
      return FALLBACK_AUTH_HEADER;
    }
    cachedAccessToken = payload.access_token;
    cachedTokenAt = now;
    return `Bearer ${cachedAccessToken}`;
  } catch {
    return FALLBACK_AUTH_HEADER;
  }
}
