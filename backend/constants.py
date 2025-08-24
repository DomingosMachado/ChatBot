"""Application constants and configuration."""

class APIConfig:
    """API configuration constants."""
    DEFAULT_PORT = 8000
    MAX_REQUEST_SIZE = 1024 * 1024  # 1MB
    REQUEST_TIMEOUT = 30  # seconds
    CORS_ORIGINS = [
        "http://localhost:3000",
        "http://127.0.0.1:3000",
        "http://192.168.1.67:3000"
    ]

class AgentConfig:
    """Agent configuration constants."""
    ROUTER_VERSION = "1.0.0"
    KNOWLEDGE_VERSION = "1.0.0"
    MATH_VERSION = "1.0.0"
    
    DEFAULT_MODEL = "gemini-1.5-flash"
    EMBEDDING_MODEL = "models/text-embedding-004"
    
    MAX_CONTEXT_LENGTH = 2000
    RAG_CHUNKS_TO_RETRIEVE = 3
    
    MIN_CONFIDENCE_SCORE = 0.3
    MAX_CONFIDENCE_SCORE = 0.95
    CONFIDENCE_INCREMENT = 0.1

class QueryLimits:
    """Query processing limits."""
    MAX_QUERY_LENGTH = 1000
    MIN_QUERY_LENGTH = 1
    MAX_MATH_EXPRESSION_LENGTH = 100
    MAX_SESSION_ID_LENGTH = 100
    MAX_USER_ID_LENGTH = 100
    
    QUERY_PREVIEW_LENGTH = 50
    CONTEXT_PREVIEW_LENGTH = 100
    RESPONSE_PREVIEW_LENGTH = 50

class ResponseLimits:
    """Response size limits."""
    MAX_RESPONSE_LENGTH = 5000
    MAX_TOKEN_COUNT = 2000
    MAX_WORKFLOW_STEPS = 10

class DatabaseConfig:
    """Database configuration."""
    DEFAULT_DB_URL = "sqlite:///./chat_history.db"
    MAX_QUERY_RESULTS = 100
    RECENT_LOGS_DEFAULT_LIMIT = 20
    SESSION_PREVIEW_LENGTH = 100

class LoggingConfig:
    """Logging configuration."""
    LOG_LEVEL = "INFO"
    JSON_FORMAT = True
    HASH_LENGTH = 8

class ErrorMessages:
    """Standard error messages."""
    GENERIC_ERROR = "Desculpe, ocorreu um erro ao processar sua solicitação."
    NO_CONTEXT_FOUND = "Desculpe, não encontrei informações sobre isso na base de conhecimento da InfinitePay."
    INVALID_REQUEST = "Requisição inválida. Verifique os dados enviados."
    SESSION_NOT_FOUND = "Sessão não encontrada."
    MATH_ERROR = "Erro ao processar cálculo matemático."
    TIMEOUT_ERROR = "A operação excedeu o tempo limite."