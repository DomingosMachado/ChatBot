# API Documentation

Base URL: `http://localhost:8000`

## Challenge Endpoint

### POST /chat

Main endpoint for CloudWalk challenge compliance.

**Headers:**

```
Content-Type: application/json
```

**Request Body:**
| Field | Type | Required | Description |
|-------|------|----------|-------------|
| message | string | Yes | User's question |
| user_id | string | Yes | Unique user identifier |
| conversation_id | string | Yes | Conversation session ID |

**Response 200:**
| Field | Type | Description |
|-------|------|-------------|
| response | string | Agent's answer |
| source_agent_response | string | Source information |
| agent_workflow | array | Routing decisions |

**Example:**

```bash
curl -X POST http://localhost:8000/chat \
  -H "Content-Type: application/json" \
  -d '{
    "message": "Quanto é 150 + 350?",
    "user_id": "user123",
    "conversation_id": "conv456"
  }'
```

## Streaming Endpoint

### POST /api/chat

WebSocket streaming for real-time responses.

**Request Body:**

```json
{
  "messages": [{ "role": "user", "content": "Your question" }],
  "session_id": "optional_session_id"
}
```

**Response:** Server-Sent Events stream

```
data: {"content": "Response text", "session_id": "abc123"}
data: [DONE]
```

## Analytics Endpoints

### GET /api/history/{session_id}

Retrieve conversation history with metadata.

**Response:**

```json
{
  "session_id": "abc123",
  "messages": [
    {
      "role": "user",
      "content": "Question",
      "timestamp": "2024-01-20T10:30:00Z",
      "tokens": 10,
      "agent_used": null
    },
    {
      "role": "assistant",
      "content": "Answer",
      "timestamp": "2024-01-20T10:30:01Z",
      "tokens": 50,
      "agent_used": "KnowledgeAgent",
      "execution_time": 0.5
    }
  ]
}
```

### GET /api/analytics

System performance metrics.

**Response:**

```json
{
  "total_interactions": 150,
  "agent_usage": {
    "math": 45,
    "knowledge": 105
  },
  "average_execution_time": {
    "math": 0.2,
    "knowledge": 0.5
  },
  "total_tokens_used": 15000
}
```

### GET /api/logs/recent

Recent execution logs with optional filtering.

**Query Parameters:**
| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| limit | int | 20 | Number of logs |
| agent_type | string | null | Filter by agent |

**Response:**

```json
{
  "logs": [
    {
      "id": 1,
      "session_id": "abc123",
      "timestamp": "2024-01-20T10:30:00Z",
      "agent": "KnowledgeAgent",
      "execution_time": 0.5,
      "content_preview": "Response preview..."
    }
  ],
  "total": 20
}
```

## Error Responses

All endpoints return consistent error format:

**400 Bad Request:**

```json
{
  "detail": "Missing required field: user_id"
}
```

**422 Validation Error:**

```json
{
  "detail": [
    {
      "loc": ["body", "message"],
      "msg": "field required",
      "type": "value_error.missing"
    }
  ]
}
```

**500 Internal Server Error:**

```json
{
  "detail": "Error processing request: [error details]"
}
```

## Rate Limits

Currently no rate limiting implemented. Recommended for production:

- 100 requests/minute per IP
- 1000 requests/hour per user_id
