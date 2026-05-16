# ClosedLoop OS - Swagger API Documentation Access

## 🚀 API Server is Running!

The FastAPI backend is now running with comprehensive Swagger documentation.

---

## 📍 Access Points

### **Interactive Swagger UI**
🔗 **http://localhost:8000/docs**

Features:
- ✅ Interactive API testing
- ✅ Try out endpoints directly in browser
- ✅ See request/response schemas
- ✅ Test authentication flows
- ✅ View example payloads
- ✅ Download OpenAPI spec

### **ReDoc Documentation**
🔗 **http://localhost:8000/redoc**

Features:
- ✅ Clean, readable documentation
- ✅ Detailed endpoint descriptions
- ✅ Request/response examples
- ✅ Schema definitions
- ✅ Search functionality

### **OpenAPI JSON Spec**
🔗 **http://localhost:8000/openapi.json**

Use this to:
- Generate client SDKs
- Import into Postman
- Use with API testing tools

### **Root Endpoint**
🔗 **http://localhost:8000/**

Simple status check

---

## 🎯 Quick Start Testing

### 1. Open Swagger UI
Navigate to: **http://localhost:8000/docs**

### 2. Test Health Endpoint
1. Find the **health** section
2. Click on `GET /health`
3. Click "Try it out"
4. Click "Execute"
5. See the response: `{"status": "healthy"}`

### 3. Test Webhook Ingestion (No Auth Required)
1. Find the **events** section
2. Click on `POST /api/v1/webhooks/slack`
3. Click "Try it out"
4. Use this test payload:

```json
{
  "event_id": "test-123",
  "event": {
    "type": "message",
    "user": "U123456",
    "text": "Decision: We will use PostgreSQL for the main database. Goal: ship v1 by Q2.",
    "channel": "engineering",
    "ts": "1234567890.123456"
  },
  "source_url": "https://company.slack.com/archives/C123/p1234567890"
}
```

5. Click "Execute"
6. See the ingestion results with event IDs and graph updates

### 4. Test Semantic Search (Requires Auth)
1. First, get a JWT token (see Authentication section below)
2. Click the "Authorize" button at the top right
3. Enter: `Bearer YOUR_TOKEN_HERE`
4. Find `POST /api/v1/search/semantic`
5. Use this payload:

```json
{
  "query": "What did we decide about the database?",
  "limit": 5
}
```

6. See semantic search results with citations

---

## 🔐 Authentication

Most endpoints require JWT authentication.

### Demo Credentials
```
Email: demo@closedloop.ai
Password: demo123
Organization ID: 00000000-0000-0000-0000-000000000001
```

### Get JWT Token

**Option 1: Using Swagger UI**
1. Go to **auth** section
2. Click `POST /api/v1/auth/login`
3. Try it out with:
```json
{
  "email": "demo@closedloop.ai",
  "password": "demo123"
}
```
4. Copy the `access_token` from the response
5. Click "Authorize" button (top right)
6. Enter: `Bearer YOUR_ACCESS_TOKEN`
7. Click "Authorize"

**Option 2: Using curl**
```bash
curl -X POST http://localhost:8000/api/v1/auth/login \
  -H "Content-Type: application/json" \
  -d '{
    "email": "demo@closedloop.ai",
    "password": "demo123"
  }'
```

---

## 📚 API Endpoints Overview

### **Health** (No Auth)
- `GET /health` - Health check

### **Auth**
- `POST /api/v1/auth/login` - Get JWT token
- `POST /api/v1/auth/register` - Register new user

### **Connectors** (Requires Auth)
- `GET /api/v1/connectors` - List all connectors
- `POST /api/v1/connectors` - Create/update connector
- `GET /api/v1/connectors/{provider}/authorize` - Get OAuth URL
- `GET /api/v1/connectors/{provider}/callback` - OAuth callback

### **Webhooks** (No Auth - uses X-Organization-Id header)
- `POST /api/v1/webhooks/slack` - Ingest Slack events
- `POST /api/v1/webhooks/github` - Ingest GitHub events
- `POST /api/v1/webhooks/linear` - Ingest Linear events
- `POST /api/v1/webhooks/notion` - Ingest Notion events
- `POST /api/v1/webhooks/zoom` - Ingest Zoom events

### **Search** (Requires Auth)
- `POST /api/v1/search/semantic` - Semantic search across all data

### **Graph** (Requires Auth)
- `GET /api/v1/graph/neighborhood/{entity_id}` - Get entity neighborhood
- `GET /api/v1/graph/unlinked-work` - Find unlinked work items

### **Chat** (Requires Auth)
- `POST /api/v1/chat/query` - AI-powered query with reasoning
- `POST /api/v1/chat/stream` - Streaming query response

### **Notifications** (Requires Auth)
- `GET /api/v1/notifications/recent` - Get recent notifications
- `WS /api/v1/notifications/ws/{org_id}` - WebSocket for real-time updates

### **Pipeline** (Requires Auth - Admin only)
- `POST /api/v1/pipeline/reindex` - Reindex organization data

---

## 🧪 Example Test Scenarios

### Scenario 1: Ingest and Search
1. Ingest a Slack message: `POST /api/v1/webhooks/slack`
2. Wait 2 seconds for processing
3. Search for it: `POST /api/v1/search/semantic`
4. Query AI about it: `POST /api/v1/chat/query`

### Scenario 2: Graph Exploration
1. Ingest events with entities (tickets, goals, decisions)
2. Get an entity ID from search results
3. Explore neighborhood: `GET /api/v1/graph/neighborhood/{id}`
4. Find unlinked work: `GET /api/v1/graph/unlinked-work`

### Scenario 3: Real-time Monitoring
1. Connect to WebSocket: `ws://localhost:8000/api/v1/notifications/ws/{org_id}`
2. Ingest events via webhooks
3. See real-time notifications in WebSocket

---

## 🛠️ Advanced Features

### Request Examples in Swagger
Every endpoint shows:
- ✅ Request body schema
- ✅ Response schema
- ✅ Example values
- ✅ Validation rules
- ✅ Error responses

### Schema Definitions
Scroll down in Swagger UI to see:
- All data models
- Field types and constraints
- Nested object structures
- Enum values

### Download OpenAPI Spec
Click "Download" in Swagger UI to get the OpenAPI 3.0 spec for:
- Postman import
- Client SDK generation
- API documentation tools

---

## 📊 Monitoring

### Check Server Logs
The terminal running the server shows:
- Request logs
- Response times
- Error messages
- Database queries

### Check Database
```bash
psql -U closedloop -d closedloop
```

```sql
-- See ingested events
SELECT id, source, event_type, title, created_at 
FROM canonical_events 
ORDER BY created_at DESC 
LIMIT 10;

-- See entities
SELECT id, type, name, created_at 
FROM entities 
ORDER BY created_at DESC 
LIMIT 10;

-- See relationships
SELECT r.relationship_type, e1.name as from_entity, e2.name as to_entity
FROM relationships r
JOIN entities e1 ON r.from_entity_id = e1.id
JOIN entities e2 ON r.to_entity_id = e2.id
LIMIT 10;
```

---

## 🚨 Troubleshooting

### Server won't start
```bash
# Check if port 8000 is in use
netstat -ano | findstr :8000

# Kill the process if needed
taskkill /F /PID <PID>
```

### Database connection error
```bash
# Check PostgreSQL is running
psql -U closedloop -d closedloop -c "SELECT 1"

# Check .env file has correct DATABASE_URL
```

### Empty search results
1. Ingest some events first
2. Run reindexing: `POST /api/v1/pipeline/reindex`
3. Wait for embeddings to be generated

---

## 📖 Additional Resources

- **Full API Testing Guide**: See `API_TESTING_GUIDE.md`
- **Architecture Documentation**: See `CLAUDE.md`
- **Setup Instructions**: See `setup.md`

---

## 🎉 You're Ready!

Open **http://localhost:8000/docs** and start exploring the API!

The Swagger UI provides everything you need to:
- ✅ Understand the API
- ✅ Test endpoints interactively
- ✅ See request/response formats
- ✅ Build integrations
- ✅ Debug issues

Happy testing! 🚀
