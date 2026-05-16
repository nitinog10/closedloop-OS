# ClosedLoop OS API Testing Guide

## Quick Start

### 1. Start the API Server

```bash
cd apps/api
python -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

### 2. Access Swagger UI

Open your browser and navigate to:

**Swagger UI (Interactive):** http://localhost:8000/docs

**ReDoc (Documentation):** http://localhost:8000/redoc

**OpenAPI JSON:** http://localhost:8000/openapi.json

---

## API Overview

ClosedLoop OS provides a comprehensive REST API for:
- **Connector Management**: OAuth flows and configuration
- **Event Ingestion**: Webhooks for Slack, GitHub, Linear, Notion, Zoom
- **Semantic Search**: Vector-based search across all data
- **Knowledge Graph**: Entity and relationship queries
- **AI Reasoning**: Query answering with citations
- **Real-time Notifications**: WebSocket updates

---

## Authentication

Most endpoints require JWT authentication. For testing, you can use the demo organization:

```
Organization ID: 00000000-0000-0000-0000-000000000001
User ID: 00000000-0000-0000-0000-000000000101
Email: demo@closedloop.ai
Password: demo123
```

### Get JWT Token

```bash
curl -X POST http://localhost:8000/api/v1/auth/login \
  -H "Content-Type: application/json" \
  -d '{
    "email": "demo@closedloop.ai",
    "password": "demo123"
  }'
```

Response:
```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "token_type": "bearer"
}
```

### Use Token in Requests

```bash
curl -X GET http://localhost:8000/api/v1/connectors \
  -H "Authorization: Bearer YOUR_TOKEN_HERE"
```

---

## Testing Endpoints

### 1. Health Check

```bash
curl http://localhost:8000/health
```

Expected response:
```json
{
  "status": "healthy"
}
```

---

### 2. List Connectors

```bash
curl -X GET http://localhost:8000/api/v1/connectors \
  -H "Authorization: Bearer YOUR_TOKEN"
```

Expected response:
```json
[
  {
    "id": "00000000-0000-0000-0000-000000000201",
    "type": "slack",
    "status": "connected",
    "config": {
      "channels": ["platform-architecture", "security"]
    }
  },
  {
    "id": "00000000-0000-0000-0000-000000000202",
    "type": "github",
    "status": "connected",
    "config": {
      "repos": ["closedloop/core"]
    }
  }
]
```

---

### 3. Ingest Slack Event

```bash
curl -X POST http://localhost:8000/api/v1/webhooks/slack \
  -H "Content-Type: application/json" \
  -H "X-Organization-Id: 00000000-0000-0000-0000-000000000001" \
  -d '{
    "event_id": "test-123",
    "event": {
      "type": "message",
      "user": "U123456",
      "text": "Decision: We will use PostgreSQL for the main database. This aligns with our goal to ship v1 by Q2.",
      "channel": "C123456",
      "ts": "1234567890.123456"
    },
    "source_url": "https://company.slack.com/archives/C123/p1234567890"
  }'
```

Expected response:
```json
{
  "accepted": 1,
  "event_ids": ["uuid-of-created-event"],
  "embeddings_generated": 1,
  "graph_updates": [
    {
      "event_id": "uuid-of-created-event",
      "created_entities": ["person-uuid", "artifact-uuid", "decision-uuid"],
      "created_relationships": ["authored-uuid", "decided_in-uuid"]
    }
  ]
}
```

---

### 4. Ingest GitHub Event

```bash
curl -X POST http://localhost:8000/api/v1/webhooks/github \
  -H "Content-Type: application/json" \
  -H "X-Organization-Id: 00000000-0000-0000-0000-000000000001" \
  -d '{
    "action": "opened",
    "pull_request": {
      "id": 12345,
      "title": "Add user authentication",
      "body": "Implements AUTH-142. Decision: use JWT tokens with Redis caching.",
      "html_url": "https://github.com/company/repo/pull/123"
    },
    "repository": {
      "full_name": "company/repo"
    },
    "sender": {
      "login": "developer123"
    }
  }'
```

---

### 5. Semantic Search

```bash
curl -X POST http://localhost:8000/api/v1/search/semantic \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -d '{
    "query": "What did we decide about authentication?",
    "limit": 5
  }'
```

Expected response:
```json
{
  "results": [
    {
      "event_id": "uuid",
      "source_type": "slack",
      "source_title": "Slack message in #platform-architecture",
      "source_url": "https://company.slack.com/archives/C123/p172000000",
      "quote": "Decision: centralize token validation in shared middleware...",
      "relevance_score": 0.95
    }
  ]
}
```

---

### 6. AI Query with Reasoning

```bash
curl -X POST http://localhost:8000/api/v1/chat/query \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -d '{
    "query": "Why did we choose PostgreSQL?",
    "limit": 8
  }'
```

Expected response:
```json
{
  "answer": "Based on the evidence, PostgreSQL was chosen for the following reasons:\n\n1. [1] Strong ACID compliance for financial transactions\n2. [2] Excellent JSON support via JSONB for flexible schemas\n3. [3] pgvector extension enables semantic search capabilities\n\nThe decision was made in the #architecture channel on March 15.",
  "citations": [
    {
      "event_id": "uuid",
      "source_type": "slack",
      "source_title": "Architecture discussion",
      "source_url": "https://...",
      "quote": "PostgreSQL gives us ACID guarantees...",
      "relevance_score": 0.92
    }
  ],
  "trace": {
    "query": "Why did we choose PostgreSQL?",
    "evidence_count": 3,
    "workflow": ["retrieve", "rank", "generate"],
    "graph_context": {
      "expanded_entities": [],
      "decision_threads": ["Architecture discussion", "Database selection"]
    }
  }
}
```

---

### 7. Graph Neighborhood Query

```bash
curl -X GET "http://localhost:8000/api/v1/graph/neighborhood/ENTITY_UUID?depth=2" \
  -H "Authorization: Bearer YOUR_TOKEN"
```

Expected response:
```json
{
  "nodes": [
    {
      "id": "uuid-1",
      "type": "person",
      "label": "John Doe",
      "attributes": {"email": "john@company.com"}
    },
    {
      "id": "uuid-2",
      "type": "decision",
      "label": "Use PostgreSQL",
      "attributes": {"status": "approved"}
    }
  ],
  "edges": [
    {
      "source": "uuid-1",
      "target": "uuid-2",
      "type": "made"
    }
  ]
}
```

---

### 8. Find Unlinked Work

```bash
curl -X GET "http://localhost:8000/api/v1/graph/unlinked-work?limit=10" \
  -H "Authorization: Bearer YOUR_TOKEN"
```

Expected response:
```json
{
  "count": 3,
  "items": [
    {
      "entity_id": "uuid",
      "type": "ticket",
      "name": "PLAT-456",
      "attributes": {
        "ticket_id": "uuid",
        "status": "in_progress"
      }
    }
  ]
}
```

---

### 9. Reindex Organization

```bash
curl -X POST "http://localhost:8000/api/v1/pipeline/reindex?limit=100" \
  -H "Authorization: Bearer YOUR_TOKEN"
```

Expected response:
```json
{
  "events_processed": 100,
  "embeddings_generated": 100,
  "graph_updates": [...]
}
```

---

### 10. Get Recent Notifications

```bash
curl -X GET http://localhost:8000/api/v1/notifications/recent \
  -H "Authorization: Bearer YOUR_TOKEN"
```

Expected response:
```json
[
  {
    "id": "uuid",
    "type": "ingestion.completed",
    "title": "Slack ingestion complete",
    "body": "Processed 5 slack event(s)...",
    "severity": "info",
    "payload": {"source": "slack", "events": ["uuid1", "uuid2"]},
    "created_at": "2024-01-15T10:30:00Z"
  }
]
```

---

## WebSocket Testing

### Connect to Notifications WebSocket

Using `wscat` (install with `npm install -g wscat`):

```bash
wscat -c "ws://localhost:8000/api/v1/notifications/ws/00000000-0000-0000-0000-000000000001"
```

You'll receive real-time notifications as they occur:

```json
{
  "id": "uuid",
  "type": "ingestion.completed",
  "title": "GitHub ingestion complete",
  "body": "Processed 1 github event(s)...",
  "severity": "info",
  "created_at": "2024-01-15T10:35:00Z"
}
```

---

## Testing Workflow: End-to-End

### Complete Integration Test

1. **Ingest a Slack message with a decision**
```bash
curl -X POST http://localhost:8000/api/v1/webhooks/slack \
  -H "Content-Type: application/json" \
  -H "X-Organization-Id: 00000000-0000-0000-0000-000000000001" \
  -d '{
    "event_id": "test-e2e-001",
    "event": {
      "type": "message",
      "user": "U999",
      "text": "Decision: We will migrate to microservices architecture. Goal: improve scalability for Q3 launch. Ticket ARCH-500 tracks this.",
      "channel": "architecture",
      "ts": "1234567890.999"
    }
  }'
```

2. **Search for the decision**
```bash
curl -X POST http://localhost:8000/api/v1/search/semantic \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -d '{
    "query": "microservices architecture decision",
    "limit": 5
  }'
```

3. **Ask AI about it**
```bash
curl -X POST http://localhost:8000/api/v1/chat/query \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -d '{
    "query": "Why are we moving to microservices?",
    "limit": 8
  }'
```

4. **Check the graph**
```bash
# First, get the entity ID from the search results
# Then query the neighborhood
curl -X GET "http://localhost:8000/api/v1/graph/neighborhood/ENTITY_ID?depth=2" \
  -H "Authorization: Bearer YOUR_TOKEN"
```

---

## Common Issues & Solutions

### Issue: "Unauthorized" Error

**Solution:** Make sure you're including the JWT token in the Authorization header:
```bash
-H "Authorization: Bearer YOUR_TOKEN_HERE"
```

### Issue: "Organization not found"

**Solution:** Use the correct organization ID in the X-Organization-Id header or ensure your JWT token contains the right organization_id.

### Issue: Empty search results

**Solution:** 
1. Ingest some events first using the webhook endpoints
2. Run reindexing: `POST /api/v1/pipeline/reindex`
3. Wait a few seconds for embeddings to be generated

### Issue: Database connection error

**Solution:** Ensure PostgreSQL is running and the DATABASE_URL in .env is correct:
```bash
# Check if PostgreSQL is running
psql -U closedloop -d closedloop -c "SELECT 1"
```

---

## Performance Testing

### Load Test with Apache Bench

```bash
# Test health endpoint
ab -n 1000 -c 10 http://localhost:8000/health

# Test search endpoint (requires auth token)
ab -n 100 -c 5 -T application/json -H "Authorization: Bearer YOUR_TOKEN" \
  -p search_payload.json \
  http://localhost:8000/api/v1/search/semantic
```

### Monitor API Performance

Check the logs for timing information:
```bash
tail -f logs/api.log | grep "duration"
```

---

## Next Steps

1. **Explore the Swagger UI** at http://localhost:8000/docs
   - Try out endpoints interactively
   - See request/response schemas
   - Test authentication flows

2. **Read the ReDoc** at http://localhost:8000/redoc
   - Comprehensive API documentation
   - Detailed descriptions and examples

3. **Build a client application**
   - Use the OpenAPI spec to generate client SDKs
   - Integrate with your frontend or automation tools

4. **Set up webhooks**
   - Configure Slack, GitHub, Linear webhooks to point to your API
   - Start ingesting real organizational data

---

## Support

For issues or questions:
- Check the logs: `tail -f logs/api.log`
- Review the database: `psql -U closedloop -d closedloop`
- Open an issue on GitHub
- Contact: support@closedloop.ai
