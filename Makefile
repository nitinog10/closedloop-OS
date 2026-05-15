up:
	docker compose -f infra/docker-compose.yml up -d

down:
	docker compose -f infra/docker-compose.yml down

api:
	cd apps/api && uvicorn app.main:app --reload --port 8000

web:
	cd apps/web && npm run dev

seed-webhooks:
	curl -X POST http://localhost:8000/api/v1/webhooks/slack \
	  -H 'Content-Type: application/json' \
	  -H 'x-organization-id: 00000000-0000-0000-0000-000000000001' \
	  -d @examples/slack-webhook.json && echo && \
	curl -X POST http://localhost:8000/api/v1/webhooks/github \
	  -H 'Content-Type: application/json' \
	  -H 'x-organization-id: 00000000-0000-0000-0000-000000000001' \
	  -d @examples/github-webhook.json

seed-phase2:
	curl -X POST http://localhost:8000/api/v1/webhooks/linear \
	  -H 'Content-Type: application/json' \
	  -H 'x-organization-id: 00000000-0000-0000-0000-000000000001' \
	  -d @examples/linear-webhook.json && echo && \
	curl -X POST http://localhost:8000/api/v1/webhooks/notion \
	  -H 'Content-Type: application/json' \
	  -H 'x-organization-id: 00000000-0000-0000-0000-000000000001' \
	  -d @examples/notion-webhook.json && echo && \
	curl -X POST http://localhost:8000/api/v1/webhooks/zoom \
	  -H 'Content-Type: application/json' \
	  -H 'x-organization-id: 00000000-0000-0000-0000-000000000001' \
	  -d @examples/zoom-webhook.json

reindex:
	curl -X POST 'http://localhost:8000/api/v1/pipeline/reindex?limit=100' \
	  -H 'Authorization: Bearer REPLACE_WITH_JWT'
