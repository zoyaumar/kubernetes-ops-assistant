# API Reference

Base URL: `/api/v1`

All responses follow standard JSON formatting. Authentication is performed via HTTP Bearer token (`Authorization: Bearer <access_token>`).

---

## Auth Endpoints

### `POST /api/v1/auth/register`
Creates a new user account.
* **Request**: `{ "email": "admin@local.dev", "password": "securepassword" }`
* **Response**: `201 Created` — `{ "access_token": "...", "token_type": "bearer", "expires_in": 3600 }`

### `POST /api/v1/auth/login`
Authenticates user and issues access token.
* **Request**: `{ "email": "admin@local.dev", "password": "securepassword" }`
* **Response**: `200 OK` — `{ "access_token": "...", "token_type": "bearer", "expires_in": 3600 }`

---

## Cluster & Event Endpoints

### `GET /api/v1/clusters`
List registered clusters.

### `GET /api/v1/clusters/:clusterId/events`
Query structured Kubernetes events with metadata filters.
* **Query Parameters**:
  * `namespace` (string)
  * `resource` (string)
  * `severity` (`Warning` | `Normal`)
  * `startTime` (ISO 8601 string)
  * `endTime` (ISO 8601 string)

---

## Chat & RAG Endpoints

### `POST /api/v1/conversations`
Create a new investigation conversation context.
* **Request**: `{ "cluster_id": "local-kind", "title": "payments-api crash investigation" }`

### `POST /api/v1/conversations/:conversationId/messages`
Submit a natural language question for RAG processing.
* **Request**:
```json
{
  "content": "Why did payments-api crash around 2:14 AM?",
  "cluster_id": "local-kind",
  "context": {
    "namespace": "payments"
  }
}
```
* **Response**:
```json
{
  "answer": "The payments-api pod was OOMKilled because container memory exceeded its 256Mi limit.",
  "confidence": "high",
  "citations": [
    {
      "document_id": "8f1a2b...",
      "source_type": "cluster_event",
      "score": 0.93
    }
  ],
  "timeline": [
    {
      "timestamp": "2026-08-18T02:13:51Z",
      "description": "Memory usage spike detected"
    },
    {
      "timestamp": "2026-08-18T02:14:32Z",
      "description": "Container killed by OOMKiller"
    }
  ]
}
```

---

## Health & Operations

* `GET /api/v1/health` — Service liveness probe (`200 OK`)
* `GET /api/v1/ready` — Service readiness probe (verifies database connection)
* `GET /api/v1/dead-letters` — List failed messages in DLQ
* `POST /api/v1/dead-letters/:id/retry` — Re-queue DLQ message for processing
