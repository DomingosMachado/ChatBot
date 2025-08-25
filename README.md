# SWE Coding Challenge - Multi-Agent Chat System

A distributed chat system with intelligent agents, conversation routing, and real-time logging.

## Architecture

**Router**: Load balances requests across agent instances  
**Agents**: Process conversations with AI capabilities  
**Logs**: Centralized logging with Redis storage  
**Redis**: Message queue and conversation state management

## Running Locally (Docker + docker-compose)

```bash
# Clone and start all services
git clone <repository-url>
cd swe-coding-challenge
docker-compose up -d

# Verify services are running
docker-compose ps
```

Services will be available at:

- Frontend: http://localhost:3000
- API Router: http://localhost:8000
- Redis: localhost:6379

## Running on Kubernetes

```bash
# Apply all manifests
kubectl apply -f k8s/

# Check deployment status
kubectl get pods
kubectl get services

# Port forward to access locally
kubectl port-forward service/frontend 3000:3000
kubectl port-forward service/api-router 8000:8000
```

## Frontend Access & Testing

Access the chat interface at http://localhost:3000

**Multiple Conversations:**

1. Open multiple browser tabs/windows
2. Start different conversations in each tab
3. Verify each conversation maintains separate context
4. Test concurrent message sending
5. Check conversation history persistence

**API Endpoints:**

- `POST /chat` - Send message
- `GET /conversations` - List conversations
- `GET /conversations/{id}` - Get conversation history

## Example Logs (JSON)

```json
{
  "timestamp": "2024-08-24T15:30:45Z",
  "level": "INFO",
  "service": "agent-1",
  "conversation_id": "conv_123",
  "message": "Processing user message",
  "user_input": "Hello, how are you?",
  "response_time_ms": 245,
  "metadata": {
    "agent_version": "1.0.0",
    "model": "gpt-4"
  }
}
```

```json
{
  "timestamp": "2024-08-24T15:30:47Z",
  "level": "INFO",
  "service": "router",
  "conversation_id": "conv_123",
  "message": "Request routed to agent",
  "agent_id": "agent-1",
  "load_balance_method": "round_robin",
  "active_agents": 3
}
```

## Sanitization & Prompt Injection Protection

**Input Sanitization:**

- HTML/script tag removal
- SQL injection pattern detection
- Malicious payload filtering
- Input length validation

**Prompt Injection Protection:**

- System prompt isolation
- User input sandboxing
- Context boundary enforcement
- Adversarial prompt detection

**Implementation:**

```python
def sanitize_input(user_input: str) -> str:
    # Remove HTML tags and dangerous patterns
    sanitized = re.sub(r'<[^>]+>', '', user_input)
    # Filter prompt injection attempts
    dangerous_patterns = ['ignore previous', 'system:', 'assistant:']
    for pattern in dangerous_patterns:
        sanitized = sanitized.replace(pattern, '[FILTERED]')
    return sanitized[:1000]  # Limit length
```

## Running Tests

```bash
# Unit tests
pytest tests/unit/

# Integration tests
pytest tests/integration/

# Load tests
pytest tests/load/ --workers=10

# All tests with coverage
pytest --cov=src tests/
```

**Test Categories:**

- Unit: Individual component testing
- Integration: Multi-service communication
- Load: Performance under concurrent users
- Security: Sanitization and injection protection

## Development

```bash
# Install dependencies
pip install -r requirements.txt

# Run in development mode
docker-compose -f docker-compose.dev.yml up

# View logs
docker-compose logs -f agent
docker-compose logs -f router
```

## Environment Variables

- `REDIS_URL`: Redis connection string
- `AGENT_COUNT`: Number of agent replicas
- `LOG_LEVEL`: Logging verbosity (INFO/DEBUG)
- `API_KEY`: Authentication key (if enabled)
