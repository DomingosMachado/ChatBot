import logging
import json
import sys
from datetime import datetime

class JSONFormatter(logging.Formatter):
    """
    Custom JSON formatter for structured logging
    """
    def format(self, record):
        log_obj = {
            "timestamp": datetime.utcnow().isoformat() + "Z",
            "level": record.levelname,
            "logger": record.name,
            "message": record.getMessage(),
            "module": record.module,
            "function": record.funcName,
            "line": record.lineno
        }
        
        if hasattr(record, 'correlation_id'):
            log_obj['correlation_id'] = record.correlation_id
        if hasattr(record, 'agent'):
            log_obj['agent'] = record.agent
        if hasattr(record, 'execution_time_ms'):
            log_obj['execution_time_ms'] = record.execution_time_ms
        if hasattr(record, 'decision'):
            log_obj['decision'] = record.decision
        if hasattr(record, 'confidence'):
            log_obj['confidence'] = record.confidence
        if hasattr(record, 'source'):
            log_obj['source'] = record.source
        if hasattr(record, 'tokens'):
            log_obj['tokens'] = record.tokens
        if hasattr(record, 'query'):
            log_obj['query'] = record.query
        if hasattr(record, 'response_preview'):
            log_obj['response_preview'] = record.response_preview
        
        if record.exc_info:
            log_obj['exception'] = self.formatException(record.exc_info)
            
        return json.dumps(log_obj, ensure_ascii=False)

def setup_logger(name):
    """
    Setup logger with JSON formatting
    """
    logger = logging.getLogger(name)
    logger.setLevel(logging.INFO)
    
    if not logger.handlers:
        handler = logging.StreamHandler(sys.stdout)
        handler.setFormatter(JSONFormatter())
        logger.addHandler(handler)
    
    logger.propagate = False
    return logger