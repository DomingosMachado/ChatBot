# domingosmachado/chatbot/ChatBot-c52a09916732c591151116fd44bf41bbdf5f54e5/backend/app.py
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
from rag import query_rag

load_dotenv()

app = FastAPI()
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

app.add_middleware(
    CORSMiddleware, allow_origins=["http://localhost:3000"],
    allow_credentials=True, allow_methods=["*"], allow_headers=["*"],
)

CONTEXT_SESSION_ID = "infinitepay-context"

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

    history_stmt = select(Conversation).where(Conversation.session_id == session_id).order_by(Conversation.created_at)
    history = db.execute(history_stmt).scalars().all()
    
    context = query_rag(user_message.content, CONTEXT_SESSION_ID)
    
    prompt = user_message.content
    if context:
        prompt = f"Use the following context to answer the question:\n\nContext: {context}\n\nQuestion: {user_message.content}"

    messages_for_api = []
    for msg in history:
        role = "model" if msg.role == "assistant" else "user"
        messages_for_api.append({"role": role, "parts": [msg.content]})

    db_user_msg = Conversation(
        session_id=session_id, role=user_message.role, content=user_message.content,
        tokens=count_tokens(prompt), cost=0
    )
    db.add(db_user_msg)
    db.commit()

    try:
        def generate():
            model = genai.GenerativeModel('gemini-1.5-flash')
            # The history is passed here, and the new prompt is passed to send_message
            chat_session = model.start_chat(history=messages_for_api)
            stream = chat_session.send_message(prompt, stream=True)
            
            full_response = ""
            for chunk in stream:
                content = chunk.text
                full_response += content
                yield f"data: {json.dumps({'content': content, 'session_id': session_id})}\n\n"
            
            assistant_tokens = count_tokens(full_response)
            
            db_assistant_msg = Conversation(
                session_id=session_id, role='assistant', content=full_response,
                tokens=assistant_tokens, cost=0
            )
            db.add(db_assistant_msg)
            db.commit()
            yield "data: [DONE]\n\n"
        
        return StreamingResponse(generate(), media_type="text/event-stream")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))