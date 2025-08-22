from logger_config import setup_logger

def test_logging():
    logger = setup_logger("TestLogger")
    
    logger.info("Basic log message")
    
    logger.info("Router decision", extra={
        "correlation_id": "test-123",
        "agent": "RouterAgent",
        "decision": "KnowledgeAgent",
        "confidence": 0.95,
        "execution_time_ms": 45
    })
    
    logger.warning("Performance warning", extra={
        "execution_time_ms": 5000,
        "query": "complex query"
    })
    
    logger.error("Error occurred", extra={
        "correlation_id": "test-456",
        "agent": "MathAgent"
    })
    
    print("\n✅ Logging test complete")

if __name__ == "__main__":
    test_logging()