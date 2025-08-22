from sqlalchemy import create_engine, Column, Integer, String, Float, DateTime, Text, JSON
from sqlalchemy.orm import sessionmaker, declarative_base
from datetime import datetime
import os

Base = declarative_base()
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./chat_history.db")
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

class Conversation(Base):
    __tablename__ = "conversations"
    
    id = Column(Integer, primary_key=True)
    session_id = Column(String, index=True, nullable=False)
    role = Column(String)
    content = Column(Text)
    tokens = Column(Integer)
    cost = Column(Float)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # New fields for logging
    agent_used = Column(String, nullable=True)  # "math", "knowledge", or null for user
    execution_time = Column(Float, nullable=True)  # in seconds
    source = Column(Text, nullable=True)  # source of answer for knowledge agent
    router_decision = Column(JSON, nullable=True)  # router decision details
    agent_log = Column(JSON, nullable=True)  # full agent execution log

Base.metadata.create_all(bind=engine)