# Deployment

## Runtime Topology

- `web`: Next.js UI
- `api`: FastAPI control plane and AI orchestration
- `postgres`: metadata + pgvector
- `redis`: cache / rate limit / queue state
- `redpanda`: Kafka-compatible event stream
- `neo4j` (optional): graph exploration at scale
- `workers`: embedding / graph / pipeline workers

## Production Recommendations

- Deploy frontend and backend independently
- Use Azure Database for PostgreSQL
- Use Azure Cache for Redis
- Use Azure Event Hubs / Confluent Kafka-compatible service
- Use Azure OpenAI private networking
- Use AKS with Workload Identity
- Store connector secrets in Key Vault
- Separate API and worker autoscaling profiles
- Run scheduled reindex jobs for schema/model upgrades
