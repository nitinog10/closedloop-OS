# ClosedLoop OS Data Model

## Tenant Isolation Strategy

Every multi-tenant table carries `organization_id`. Queries are filtered through request context dependencies. Cross-tenant access is prohibited at the application layer and should be reinforced via Row Level Security in production.

## Core Tables

- `organizations`
- `users`
- `connectors`
- `canonical_events`
- `embeddings`
- `entities`
- `identity_aliases`
- `relationships`
- `tickets`
- `goals`
- `decisions`
- `conversations`
- `citations`
- `notifications`
- `audit_logs`

## Citation Model

A citation points to a canonical evidence fragment:
- source type
- source title
- source url
- quoted excerpt
- event id
- fragment offsets
- relevance score

## Phase 2 Additions

### `identity_aliases`
Cross-tool identity stitching for people and service accounts:
- source
- external_id
- display_name
- entity_id
- confidence_score

### `notifications`
Tenant-scoped operational feed for live updates:
- type
- title
- body
- severity
- payload

### Embeddings
Embeddings are stored in `pgvector` format to support:
- nearest-neighbor retrieval
- hybrid search ranking
- re-indexing during model upgrades
