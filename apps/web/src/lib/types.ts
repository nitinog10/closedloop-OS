export type Citation = {
  event_id: string;
  source_type: string;
  source_title: string;
  source_url?: string | null;
  quote: string;
  relevance_score: number;
};

export type ChatResponse = {
  answer: string;
  citations: Citation[];
  trace: Record<string, unknown>;
};

export type Connector = {
  id: string;
  type: string;
  status: string;
  config: Record<string, unknown>;
};

export type NotificationItem = {
  id: string;
  type: string;
  title: string;
  body: string;
  severity: string;
  payload: Record<string, unknown>;
  created_at: string;
};
