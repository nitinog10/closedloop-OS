# ClosedLoop OS Architecture

## 1. Connector Layer

Responsibilities:
- OAuth onboarding for external systems
- Webhook ingestion for Slack and GitHub MVP
- Pull sync workers for backfill and replay
- Retry, dead-letter, and idempotency support
- Conversion of source-specific payloads into canonical events

Current connectors:
- Slack events + message history pull
- GitHub webhooks + repository backfill
- Linear issue and comment normalization
- Notion page/document normalization
- Zoom transcript ingestion normalization

## 2. Unified Event Stream

Canonical stream properties:
- Tenant-scoped topics or tenant metadata envelopes
- Kafka-compatible producers/consumers
- Deduplication key per source event
- Importance scoring to drive retrieval relevance
- Replayable ingestion for model re-indexing

Primary event stages:
1. raw source event
2. normalized canonical event
3. enrichment event
4. embedding generated event
5. graph upsert event
6. notification event

## 3. Semantic Intelligence Layer

Core capabilities:
- Azure OpenAI embeddings or deterministic local embeddings for development
- pgvector persistence with hybrid retrieval hooks
- Hybrid retrieval over vector + metadata filters + keyword signals
- Citation extraction from event fragments
- Context ranking by recency, authority, and graph centrality

## 4. Knowledge Graph Layer

Entities:
- person
- team
- repository
- ticket
- pull_request
- decision
- goal
- document
- conversation
- artifact

Relationships:
- authored
- mentioned
- assigned_to
- depends_on
- references
- decided_in
- aligns_with
- blocks
- implemented_in

Phase 2 graph services:
- regex + heuristic entity extraction
- identity alias mapping
- decision / goal / ticket linking
- graph neighborhood API for UI exploration

## 5. Reasoning Engine

LangGraph workflow stages:
1. Understand query intent
2. Perform hybrid retrieval
3. Expand graph neighborhood
4. Re-rank evidence
5. Build answer plan
6. Generate cited answer
7. Emit trace for observability

## 6. Interface Layer

Frontend surfaces:
- Dashboard
- AI Chat
- Graph Explorer
- Connector Management
- Operational Insights
- Organization Memory
- AI Actions Center

Interaction model:
- streaming answer tokens
- source chips and citations
- evidence timeline
- graph exploration
- workspace switching
- real-time notification feed
