# CloudWalk AI Chat Challenge

## Setup

1. Backend: `cd Backend && pip install -r requirements.txt && uvicorn app:app --reload`
2. Frontend: `cd Frontend && npm install && npm run dev`

## Features

- ✅ OpenAI GPT-4o-mini integration
- ✅ Streaming responses
- ✅ Conversation history
- ✅ Token counting & cost calculation
- ✅ Clean, maintainable code

## API Endpoints

- POST /api/chat - Send messages
- GET /api/history/{session_id} - Get conversation history
