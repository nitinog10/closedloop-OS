# Phase 2 Implementation Notes

## Delivered Capabilities

- Additional connector adapters for Linear, Notion, and Zoom
- Ingestion pipeline service that normalizes, persists, embeds, extracts graph structure, and publishes notifications
- `pgvector` embedding persistence model and hybrid retrieval service
- Knowledge graph extraction for:
  - people
  - repositories
  - tickets
  - decisions
  - goals
  - source artifacts
- Identity alias table and resolution service for cross-tool actor stitching
- Tenant reindex endpoint for backfilling embeddings and graph structure
- WebSocket notification manager and dashboard feed
- Kafka-compatible event bus abstraction and worker entrypoints

## Recommended Next Phase 3 Work

1. Replace heuristic graph extraction with LLM-assisted structured extraction
2. Add connector backfill workers and cursor checkpoints
3. Introduce durable Kafka consumers for normalized/enriched topics
4. Add policy engine for action execution approvals
5. Implement graph-aware re-ranking and temporal reasoning in LangGraph
6. Add observability dashboards, tracing, and workload SLOs
