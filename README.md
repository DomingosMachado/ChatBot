# CloudWalk AI Chat Assistant

A multi-agent chatbot that intelligently routes queries between specialized agents for math calculations and InfinitePay knowledge base questions.

## Quick Start

```bash
# Clone and setup
git clone <repo>
cd chatbot

# Backend (Terminal 1)
cd backend
pip install -r requirements.txt
python load_context.py
uvicorn app:app --reload

# Frontend (Terminal 2)
cd frontend
npm install
npm run dev
```

Access the chat at http://localhost:3000

## Architecture

The system uses three agents:

- **RouterAgent**: Classifies incoming queries and routes to appropriate agent
- **KnowledgeAgent**: Handles InfinitePay questions using RAG (vector search)
- **MathAgent**: Processes mathematical calculations using Gemini LLM

## API

### POST /chat

Challenge-compliant endpoint for the CloudWalk test.

**Request:**

```json
{
  "message": "O que é a maquininha Smart?",
  "user_id": "user123",
  "conversation_id": "conv456"
}
```

**Response:**

```json
{
  "response": "A maquininha Smart é nossa solução...",
  "source_agent_response": "Retrieved from 3 chunks in knowledge base",
  "agent_workflow": [
    { "agent": "RouterAgent", "decision": "KnowledgeAgent" },
    { "agent": "KnowledgeAgent", "decision": "" }
  ]
}
```

### Additional Endpoints

- `POST /api/chat` - Streaming chat for frontend
- `GET /api/history/{session_id}` - Conversation history
- `GET /api/analytics` - Agent performance metrics
- `GET /api/logs/recent` - Recent execution logs

## Testing

```bash
cd backend

# Test API contract compliance
python test_chat_endpoint.py

# Full system test
python test_complete_system.py

# Test individual components
python test_rag_system.py
python test_models.py
```

## Environment Variables

Create `.env` file in backend directory:

```
GOOGLE_API_KEY=your_gemini_api_key
DATABASE_URL=sqlite:///./chat_history.db
```

## Requirements

- Python 3.8+
- Node.js 18+
- Google Gemini API key

## Project Structure

```
backend/
├── app.py              # FastAPI server and endpoints
├── agents.py           # Router, Knowledge, and Math agents
├── rag.py              # Vector search implementation
├── database.py         # SQLAlchemy models
├── models.py           # Pydantic schemas
├── logger_config.py    # JSON structured logging
└── context/            # InfinitePay knowledge base

frontend/
├── src/app/
│   └── page.tsx        # Chat interface
└── package.json
```

## Logging

All agents produce structured JSON logs with correlation IDs for request tracking:

```json
{
  "timestamp": "2024-01-20T10:30:00Z",
  "level": "INFO",
  "logger": "KnowledgeAgent",
  "correlation_id": "abc123",
  "execution_time_ms": 150,
  "message": "Query processed successfully"
}
```

## Performance

Average response times:

- KnowledgeAgent: ~500ms (includes vector search)
- MathAgent: ~200ms
- RouterAgent: <50ms
