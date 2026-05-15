CREATE EXTENSION IF NOT EXISTS vector;

CREATE TABLE organizations (
  id UUID PRIMARY KEY,
  name VARCHAR(255) NOT NULL,
  slug VARCHAR(255) UNIQUE NOT NULL,
  plan VARCHAR(50) NOT NULL DEFAULT 'enterprise',
  created_at TIMESTAMPTZ DEFAULT now(),
  updated_at TIMESTAMPTZ DEFAULT now()
);

CREATE TABLE users (
  id UUID PRIMARY KEY,
  organization_id UUID NOT NULL REFERENCES organizations(id),
  email VARCHAR(255) NOT NULL,
  full_name VARCHAR(255) NOT NULL,
  hashed_password VARCHAR(255) NOT NULL,
  role VARCHAR(50) NOT NULL DEFAULT 'member',
  created_at TIMESTAMPTZ DEFAULT now(),
  updated_at TIMESTAMPTZ DEFAULT now()
);

CREATE TABLE connectors (
  id UUID PRIMARY KEY,
  organization_id UUID NOT NULL REFERENCES organizations(id),
  type VARCHAR(50) NOT NULL,
  status VARCHAR(50) NOT NULL DEFAULT 'connected',
  config JSONB NOT NULL DEFAULT '{}'::jsonb,
  encrypted_secret VARCHAR(1024),
  created_at TIMESTAMPTZ DEFAULT now(),
  updated_at TIMESTAMPTZ DEFAULT now()
);

CREATE TABLE canonical_events (
  id UUID PRIMARY KEY,
  organization_id UUID NOT NULL REFERENCES organizations(id),
  connector_id UUID REFERENCES connectors(id),
  source VARCHAR(50) NOT NULL,
  source_event_id VARCHAR(255) NOT NULL,
  source_url VARCHAR(1024),
  event_type VARCHAR(100) NOT NULL,
  actor_external_id VARCHAR(255),
  channel_external_id VARCHAR(255),
  title VARCHAR(500),
  content TEXT NOT NULL,
  metadata JSONB NOT NULL DEFAULT '{}'::jsonb,
  importance_score DOUBLE PRECISION NOT NULL DEFAULT 0.5,
  dedupe_key VARCHAR(255) NOT NULL,
  created_at TIMESTAMPTZ DEFAULT now(),
  updated_at TIMESTAMPTZ DEFAULT now()
);

CREATE TABLE embeddings (
  id UUID PRIMARY KEY,
  organization_id UUID NOT NULL REFERENCES organizations(id),
  event_id UUID NOT NULL UNIQUE REFERENCES canonical_events(id),
  model VARCHAR(255) NOT NULL,
  dimensions INTEGER NOT NULL DEFAULT 3072,
  vector VECTOR(3072),
  created_at TIMESTAMPTZ DEFAULT now(),
  updated_at TIMESTAMPTZ DEFAULT now()
);

CREATE TABLE entities (
  id UUID PRIMARY KEY,
  organization_id UUID NOT NULL REFERENCES organizations(id),
  type VARCHAR(100) NOT NULL,
  name VARCHAR(255) NOT NULL,
  external_key VARCHAR(255),
  attributes JSONB NOT NULL DEFAULT '{}'::jsonb,
  created_at TIMESTAMPTZ DEFAULT now(),
  updated_at TIMESTAMPTZ DEFAULT now()
);

CREATE TABLE identity_aliases (
  id UUID PRIMARY KEY,
  organization_id UUID NOT NULL REFERENCES organizations(id),
  entity_id UUID NOT NULL REFERENCES entities(id),
  source VARCHAR(50) NOT NULL,
  external_id VARCHAR(255) NOT NULL,
  display_name VARCHAR(255),
  confidence_score DOUBLE PRECISION NOT NULL DEFAULT 0.9,
  created_at TIMESTAMPTZ DEFAULT now(),
  updated_at TIMESTAMPTZ DEFAULT now()
);

CREATE TABLE relationships (
  id UUID PRIMARY KEY,
  organization_id UUID NOT NULL REFERENCES organizations(id),
  from_entity_id UUID NOT NULL REFERENCES entities(id),
  to_entity_id UUID NOT NULL REFERENCES entities(id),
  relationship_type VARCHAR(100) NOT NULL,
  created_at TIMESTAMPTZ DEFAULT now(),
  updated_at TIMESTAMPTZ DEFAULT now()
);

CREATE TABLE decisions (
  id UUID PRIMARY KEY,
  organization_id UUID NOT NULL REFERENCES organizations(id),
  title VARCHAR(255) NOT NULL,
  summary TEXT NOT NULL,
  status VARCHAR(50) NOT NULL DEFAULT 'open',
  created_at TIMESTAMPTZ DEFAULT now(),
  updated_at TIMESTAMPTZ DEFAULT now()
);

CREATE TABLE goals (
  id UUID PRIMARY KEY,
  organization_id UUID NOT NULL REFERENCES organizations(id),
  title VARCHAR(255) NOT NULL,
  description TEXT NOT NULL,
  status VARCHAR(50) NOT NULL DEFAULT 'on_track',
  created_at TIMESTAMPTZ DEFAULT now(),
  updated_at TIMESTAMPTZ DEFAULT now()
);

CREATE TABLE tickets (
  id UUID PRIMARY KEY,
  organization_id UUID NOT NULL REFERENCES organizations(id),
  external_id VARCHAR(100) NOT NULL,
  title VARCHAR(255) NOT NULL,
  description TEXT NOT NULL,
  status VARCHAR(50) NOT NULL DEFAULT 'open',
  created_at TIMESTAMPTZ DEFAULT now(),
  updated_at TIMESTAMPTZ DEFAULT now()
);

CREATE TABLE conversations (
  id UUID PRIMARY KEY,
  organization_id UUID NOT NULL REFERENCES organizations(id),
  user_id UUID NOT NULL REFERENCES users(id),
  title VARCHAR(255) NOT NULL DEFAULT 'New conversation',
  state JSONB NOT NULL DEFAULT '{}'::jsonb,
  created_at TIMESTAMPTZ DEFAULT now(),
  updated_at TIMESTAMPTZ DEFAULT now()
);

CREATE TABLE citations (
  id UUID PRIMARY KEY,
  organization_id UUID NOT NULL REFERENCES organizations(id),
  event_id UUID NOT NULL REFERENCES canonical_events(id),
  source_type VARCHAR(50) NOT NULL,
  source_title VARCHAR(255) NOT NULL,
  source_url VARCHAR(1024),
  quote TEXT NOT NULL,
  start_offset INTEGER NOT NULL DEFAULT 0,
  end_offset INTEGER NOT NULL DEFAULT 0,
  relevance_score DOUBLE PRECISION NOT NULL DEFAULT 0,
  created_at TIMESTAMPTZ DEFAULT now(),
  updated_at TIMESTAMPTZ DEFAULT now()
);

CREATE TABLE notifications (
  id UUID PRIMARY KEY,
  organization_id UUID NOT NULL REFERENCES organizations(id),
  type VARCHAR(100) NOT NULL,
  title VARCHAR(255) NOT NULL,
  body TEXT NOT NULL,
  severity VARCHAR(50) NOT NULL DEFAULT 'info',
  payload JSONB NOT NULL DEFAULT '{}'::jsonb,
  created_at TIMESTAMPTZ DEFAULT now(),
  updated_at TIMESTAMPTZ DEFAULT now()
);

CREATE TABLE audit_logs (
  id UUID PRIMARY KEY,
  organization_id UUID NOT NULL REFERENCES organizations(id),
  user_id UUID REFERENCES users(id),
  action VARCHAR(100) NOT NULL,
  resource_type VARCHAR(100) NOT NULL,
  resource_id VARCHAR(255) NOT NULL,
  payload JSONB NOT NULL DEFAULT '{}'::jsonb,
  created_at TIMESTAMPTZ DEFAULT now(),
  updated_at TIMESTAMPTZ DEFAULT now()
);

CREATE INDEX idx_canonical_events_tenant_source ON canonical_events (organization_id, source, event_type);
CREATE UNIQUE INDEX idx_canonical_events_dedupe ON canonical_events (organization_id, dedupe_key);
CREATE INDEX idx_embeddings_event ON embeddings (organization_id, event_id);
CREATE INDEX idx_entities_type_name ON entities (organization_id, type, name);
CREATE INDEX idx_identity_aliases_lookup ON identity_aliases (organization_id, source, external_id);
CREATE INDEX idx_relationships_lookup ON relationships (organization_id, from_entity_id, to_entity_id);
CREATE INDEX idx_citations_lookup ON citations (organization_id, event_id);
CREATE INDEX idx_notifications_lookup ON notifications (organization_id, created_at DESC);
CREATE INDEX idx_embeddings_vector ON embeddings USING ivfflat (vector vector_cosine_ops) WITH (lists = 100);

INSERT INTO organizations (id, name, slug)
VALUES ('00000000-0000-0000-0000-000000000001', 'Acme Enterprise', 'acme-enterprise')
ON CONFLICT (id) DO NOTHING;

INSERT INTO users (id, organization_id, email, full_name, hashed_password, role)
VALUES ('00000000-0000-0000-0000-000000000101', '00000000-0000-0000-0000-000000000001', 'demo@closedloop.ai', 'Demo User', '$2b$12$KIXQ4RO0V7iJ8QKQXQdTNO0HTGvM5QJp8avVnM7oW6J4xDgFJ7b2m', 'admin')
ON CONFLICT (id) DO NOTHING;

INSERT INTO connectors (id, organization_id, type, status, config)
VALUES
  ('00000000-0000-0000-0000-000000000201', '00000000-0000-0000-0000-000000000001', 'slack', 'connected', '{"channels": ["platform-architecture", "security"]}'::jsonb),
  ('00000000-0000-0000-0000-000000000202', '00000000-0000-0000-0000-000000000001', 'github', 'connected', '{"repos": ["closedloop/core"]}'::jsonb),
  ('00000000-0000-0000-0000-000000000203', '00000000-0000-0000-0000-000000000001', 'linear', 'beta', '{"teams": ["PLAT", "OPS"]}'::jsonb),
  ('00000000-0000-0000-0000-000000000204', '00000000-0000-0000-0000-000000000001', 'notion', 'beta', '{"spaces": ["engineering", "exec"]}'::jsonb),
  ('00000000-0000-0000-0000-000000000205', '00000000-0000-0000-0000-000000000001', 'zoom', 'beta', '{"transcripts": true}'::jsonb)
ON CONFLICT (id) DO NOTHING;

INSERT INTO canonical_events (id, organization_id, connector_id, source, source_event_id, source_url, event_type, actor_external_id, channel_external_id, title, content, metadata, importance_score, dedupe_key)
VALUES
  (
    '00000000-0000-0000-0000-000000000301',
    '00000000-0000-0000-0000-000000000001',
    '00000000-0000-0000-0000-000000000201',
    'slack',
    'EvSeedSlack1',
    'https://company.slack.com/archives/C123/p172000000',
    'message',
    'U123',
    'platform-architecture',
    'Slack message in #platform-architecture',
    'Decision: centralize token validation in shared middleware, while keeping authorization policies service-local. Goal: complete identity unification before Q4. AUTH-142 tracks rollout sequencing.',
    '{}'::jsonb,
    0.92,
    'slack:EvSeedSlack1'
  ),
  (
    '00000000-0000-0000-0000-000000000302',
    '00000000-0000-0000-0000-000000000001',
    '00000000-0000-0000-0000-000000000202',
    'github',
    '418',
    'https://github.com/closedloop/core/pull/418',
    'pull_request',
    'arch-lead',
    'closedloop/core',
    'Refactor auth middleware',
    'PR discussion approved introducing provider abstraction, cache-aware JWKS lookup, and centralized token validation. Reviewers requested citations back to the Slack decision thread before merge. References AUTH-142.',
    '{"repository": "closedloop/core", "action": "opened"}'::jsonb,
    0.95,
    'github:418:opened'
  ),
  (
    '00000000-0000-0000-0000-000000000303',
    '00000000-0000-0000-0000-000000000001',
    '00000000-0000-0000-0000-000000000203',
    'linear',
    'AUTH-142',
    'https://linear.app/acme/issue/AUTH-142',
    'issue',
    'linear-user-1',
    'PLAT',
    'AUTH-142 Unify authentication middleware',
    'Goal: complete identity unification before Q4. Blocked by provider-specific token validation paths that still exist in legacy services.',
    '{}'::jsonb,
    0.89,
    'linear:AUTH-142:create'
  ),
  (
    '00000000-0000-0000-0000-000000000304',
    '00000000-0000-0000-0000-000000000001',
    '00000000-0000-0000-0000-000000000204',
    'notion',
    'page-auth-001',
    'https://notion.so/acme/auth-architecture',
    'document',
    'notion-editor-1',
    'engineering',
    'Authentication Architecture Decision Record',
    'Decision: use centralized token validation middleware and service-scoped policy evaluation. This ADR supersedes ad hoc validation spread across services.',
    '{}'::jsonb,
    0.93,
    'notion:page-auth-001'
  )
ON CONFLICT DO NOTHING;

INSERT INTO notifications (id, organization_id, type, title, body, severity, payload)
VALUES
  (
    '00000000-0000-0000-0000-000000000401',
    '00000000-0000-0000-0000-000000000001',
    'system.bootstrap',
    'Phase 2 capabilities available',
    'Linear, Notion, Zoom, graph extraction, vector indexing, and real-time notifications are enabled in the scaffold.',
    'info',
    '{}'::jsonb
  )
ON CONFLICT DO NOTHING;
