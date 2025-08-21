import os
import uuid
import json
from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse
from sqlalchemy.orm import Session
from sqlalchemy import select
from dotenv import load_dotenv
import google.generativeai as genai
from typing import List

from database import SessionLocal, Conversation
from models import ChatRequest, ChatMessage
from utils.token_counter import count_tokens
from agents import AgentRouter, KnowledgeAgent, MathAgent

load_dotenv()

app = FastAPI()
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

app.add_middleware(
    CORSMiddleware, 
    allow_origins=["http://localhost:3000", "http://127.0.0.1:3000", "http://192.168.1.67:3000"],
    allow_credentials=True, 
    allow_methods=["*"], 
    allow_headers=["*"],
)

agent_router = AgentRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.post("/api/chat")
async def chat(request: ChatRequest, db: Session = Depends(get_db)):
    session_id = request.session_id or str(uuid.uuid4())
    user_message = request.messages[-1]

    db_user_msg = Conversation(
        session_id=session_id, 
        role=user_message.role, 
        content=user_message.content,
        tokens=count_tokens(user_message.content), 
        cost=0
    )
    db.add(db_user_msg)
    db.commit()

    try:
        def generate():
            agent_type = agent_router.classify_query(user_message.content)
            
            if agent_type == "math":
                agent = MathAgent()
            else:
                agent = KnowledgeAgent()
            
            full_response = agent.process(user_message.content, session_id)
            
            yield f"data: {json.dumps({'content': full_response, 'session_id': session_id})}\n\n"
            
            assistant_tokens = count_tokens(full_response)
            db_assistant_msg = Conversation(
                session_id=session_id, 
                role='assistant', 
                content=full_response,
                tokens=assistant_tokens, 
                cost=0
            )
            db.add(db_assistant_msg)
            db.commit()
            
            yield "data: [DONE]\n\n"
        
        return StreamingResponse(generate(), media_type="text/event-stream")
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/history/{session_id}")
async def get_history(session_id: str, db: Session = Depends(get_db)):
    try:
        stmt = select(Conversation).where(
            Conversation.session_id == session_id
        ).order_by(Conversation.created_at)
        
        conversations = db.execute(stmt).scalars().all()
        
        return {
            "session_id": session_id,
            "messages": [
                {
                    "role": conv.role,
                    "content": conv.content,
                    "timestamp": conv.created_at.isoformat(),
                    "tokens": conv.tokens
                }
                for conv in conversations
            ]
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/test")
async def test_agents():
    test_queries = [
        "O que é a maquininha Smart da InfinitePay?",
        "Quanto é 25 + 37?",
        "Como funciona o InfiniteTap?",
        "Calcule 15% de 200"
    ]
    
    results = []
    for query in test_queries:
        agent_type = agent_router.classify_query(query)
        if agent_type == "math":
            agent = MathAgent()
        else:
            agent = KnowledgeAgent()
        
        response = agent.process(query, "test-session")
        results.append({
            "query": query,
            "agent_type": agent_type,
            "response": response[:100] + "..." if len(response) > 100 else response
        })
    
    return {"test_results": results}