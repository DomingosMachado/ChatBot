import re
import os
import time
import json
from datetime import datetime
from dotenv import load_dotenv
import google.generativeai as genai
from rag import query_rag
import hashlib
from logger_config import setup_logger

load_dotenv()
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

router_logger = setup_logger("AgentRouter")
knowledge_logger = setup_logger("KnowledgeAgent")
math_logger = setup_logger("MathAgent")

class AgentRouter:
    """
    Routes user queries to the appropriate agent with structured logging
    """
    
    def __init__(self):
        self.math_patterns = [
            (r'\d+\s*[+\-*/÷×]\s*\d+', 'arithmetic_operation'),
            (r'calcul|calculadora', 'calculator_keyword'),
            (r'quanto\s+(é|eh|e)\s+', 'how_much_question'),
            (r'qual\s+(é|eh|e)\s+o\s+resultado', 'result_question'),
            (r'somar|subtrair|multiplicar|dividir', 'math_verbs'),
            (r'soma|subtração|multiplicação|divisão', 'math_nouns'),
            (r'\+|\-|\*|\/|=', 'math_symbols'),
            (r'porcentagem|%', 'percentage'),
            (r'\d+\s*%', 'percentage_value'),
            (r'vezes|vez', 'multiplication_keyword'),
            (r'mais|menos', 'addition_subtraction'),
            (r'dividido\s+por', 'division_keyword'),
            (r'elevado\s+a', 'exponentiation'),
            (r'ao\s+quadrado|ao\s+cubo', 'power_keywords'),
            (r'raiz\s+quadrada|raiz\s+de', 'square_root'),
            (r'fatorial', 'factorial'),
            (r'exponencial', 'exponential'),
            (r'\d+\s*\^\s*\d+', 'power_notation'),
        ]
        
        self.knowledge_patterns = [
            (r'o\s+que\s+(é|eh|e)', 'what_is_question'),
            (r'como\s+funciona', 'how_works_question'),
            (r'quais\s+são', 'which_are_question'),
            (r'infinitepay|maquininha|app|pix|taxa', 'infinitepay_keywords'),
            (r'conta\s+inteligente', 'smart_account'),
            (r'empréstimo', 'loan'),
            (r'cartão\s+virtual', 'virtual_card'),
            (r'nitro|receba\s+na\s+hora', 'instant_payment'),
        ]
    
    def classify_query(self, query: str) -> tuple[str, dict]:
        """
        Classify if query is math or knowledge-based and return decision details
        """
        start_time = time.time()
        query_lower = query.lower()
        query_length = len(query)
        word_count = len(query.split())
        query_hash = hashlib.md5(query.encode()).hexdigest()[:8]
        
        decision_log = {
            "timestamp": datetime.utcnow().isoformat() + "Z",
            "router": "AgentRouter",
            "version": "1.0.0",
            "query_metadata": {
                "original": query,
                "normalized": query_lower,
                "length": query_length,
                "word_count": word_count,
                "query_hash": query_hash
            },
            "patterns_checked": {
                "knowledge": 0,
                "math": 0
            },
            "matches": []
        }
        
        for pattern, pattern_name in self.knowledge_patterns:
            decision_log["patterns_checked"]["knowledge"] += 1
            if re.search(pattern, query_lower):
                decision_log["matches"].append({
                    "type": "knowledge",
                    "pattern": pattern_name,
                    "matched_text": re.search(pattern, query_lower).group()
                })
                decision_log["decision"] = "knowledge"
                decision_log["reason"] = f"Matched knowledge pattern: {pattern_name}"
                decision_log["confidence"] = min(0.95, 0.7 + (0.1 * len(decision_log["matches"])))
                decision_log["processing_time_ms"] = round((time.time() - start_time) * 1000, 2)
                
                router_logger.info("Query routed to KnowledgeAgent", extra={
                    "correlation_id": query_hash,
                    "decision": "knowledge",
                    "confidence": decision_log["confidence"],
                    "execution_time_ms": decision_log["processing_time_ms"],
                    "query": query[:50]
                })
                
                return "knowledge", decision_log
        
        for pattern, pattern_name in self.math_patterns:
            decision_log["patterns_checked"]["math"] += 1
            if re.search(pattern, query_lower):
                decision_log["matches"].append({
                    "type": "math",
                    "pattern": pattern_name,
                    "matched_text": re.search(pattern, query_lower).group()
                })
                decision_log["decision"] = "math"
                decision_log["reason"] = f"Matched math pattern: {pattern_name}"
                decision_log["confidence"] = min(0.95, 0.7 + (0.1 * len(decision_log["matches"])))
                decision_log["processing_time_ms"] = round((time.time() - start_time) * 1000, 2)
                
                router_logger.info("Query routed to MathAgent", extra={
                    "correlation_id": query_hash,
                    "decision": "math",
                    "confidence": decision_log["confidence"],
                    "execution_time_ms": decision_log["processing_time_ms"],
                    "query": query[:50]
                })
                
                return "math", decision_log
        
        decision_log["decision"] = "knowledge"
        decision_log["reason"] = "No specific pattern matched, defaulting to knowledge base"
        decision_log["confidence"] = 0.3
        decision_log["processing_time_ms"] = round((time.time() - start_time) * 1000, 2)
        
        router_logger.warning("Default routing to KnowledgeAgent", extra={
            "correlation_id": query_hash,
            "decision": "knowledge",
            "confidence": decision_log["confidence"],
            "execution_time_ms": decision_log["processing_time_ms"],
            "query": query[:50]
        })
        
        return "knowledge", decision_log


class KnowledgeAgent:
    """
    Handles questions about InfinitePay using RAG with execution logging
    """
    
    def __init__(self):
        self.version = "1.0.0"
        self.model = "gemini-1.5-flash"
    
    def process(self, query: str, session_id: str) -> tuple[str, dict]:
        """
        Process knowledge-based query with logging
        """
        start_time = time.time()
        
        log_data = {
            "agent": "KnowledgeAgent",
            "version": self.version,
            "model": self.model,
            "query": query,
            "session_id": session_id,
            "timestamp": datetime.utcnow().isoformat() + "Z",
            "metrics": {
                "start_time": start_time,
                "rag_retrieval_time": None,
                "llm_generation_time": None,
                "total_execution_time": None
            }
        }
        
        try:
            knowledge_logger.info("Starting knowledge query processing", extra={
                "correlation_id": session_id,
                "query": query[:50]
            })
            
            rag_start = time.time()
            context = query_rag(query, "infinitepay-context")
            rag_end = time.time()
            rag_time_ms = (rag_end - rag_start) * 1000
            log_data["metrics"]["rag_retrieval_time"] = f"{(rag_end - rag_start):.3f}s"
            
            knowledge_logger.info("RAG retrieval completed", extra={
                "correlation_id": session_id,
                "execution_time_ms": rag_time_ms,
                "source": "infinitepay-context"
            })
            
            if not context:
                execution_time = time.time() - start_time
                log_data.update({
                    "source": {
                        "type": "none",
                        "message": "No relevant context found in knowledge base"
                    },
                    "metrics": {
                        **log_data["metrics"],
                        "total_execution_time": f"{execution_time:.3f}s"
                    },
                    "status": "no_context",
                    "status_code": 204
                })
                
                knowledge_logger.warning("No context found", extra={
                    "correlation_id": session_id,
                    "execution_time_ms": execution_time * 1000
                })
                
                return "Desculpe, não encontrei informações sobre isso na base de conhecimento da InfinitePay.", log_data
            
            log_data["source"] = {
                "type": "rag",
                "database": "infinitepay-context",
                "context_length": len(context),
                "context_preview": context[:100] + "..." if len(context) > 100 else context,
                "chunks_retrieved": 3
            }
            
            prompt = f"""
Você é um assistente da InfinitePay. Use APENAS as informações do contexto para responder.

CONTEXTO:
{context}

PERGUNTA: {query}

Responda de forma clara e útil baseado apenas no contexto fornecido.
"""
            
            llm_start = time.time()
            model = genai.GenerativeModel(self.model)
            response = model.generate_content(prompt)
            llm_end = time.time()
            llm_time_ms = (llm_end - llm_start) * 1000
            log_data["metrics"]["llm_generation_time"] = f"{(llm_end - llm_start):.3f}s"
            
            execution_time = time.time() - start_time
            log_data.update({
                "metrics": {
                    **log_data["metrics"],
                    "total_execution_time": f"{execution_time:.3f}s"
                },
                "response_metadata": {
                    "length": len(response.text),
                    "language": "pt-BR",
                    "tokens_estimated": len(response.text.split())
                },
                "status": "success",
                "status_code": 200
            })
            
            knowledge_logger.info("Knowledge query processed successfully", extra={
                "correlation_id": session_id,
                "execution_time_ms": execution_time * 1000,
                "tokens": len(response.text.split()),
                "response_preview": response.text[:50]
            })
            
            return response.text, log_data
            
        except Exception as e:
            execution_time = time.time() - start_time
            log_data.update({
                "metrics": {
                    **log_data["metrics"],
                    "total_execution_time": f"{execution_time:.3f}s"
                },
                "status": "error",
                "status_code": 500,
                "error": {
                    "type": type(e).__name__,
                    "message": str(e),
                    "traceback": None
                }
            })
            
            knowledge_logger.error("Knowledge query processing failed", extra={
                "correlation_id": session_id,
                "execution_time_ms": execution_time * 1000,
                "error": str(e)
            }, exc_info=True)
            
            return f"Erro ao processar sua pergunta: {str(e)}", log_data


class MathAgent:
    """
    Simple math using Gemini with execution logging
    """
    
    def __init__(self):
        self.version = "1.0.0"
        self.model = "gemini-1.5-flash"
    
    def process(self, query: str, session_id: str) -> tuple[str, dict]:
        """
        Process mathematical query with logging
        """
        start_time = time.time()
        math_expression = self._extract_math_expression(query)
        
        log_data = {
            "agent": "MathAgent",
            "version": self.version,
            "model": self.model,
            "query": query,
            "session_id": session_id,
            "timestamp": datetime.utcnow().isoformat() + "Z",
            "math_metadata": {
                "extracted_expression": math_expression,
                "operation_type": self._identify_operation(query)
            },
            "metrics": {
                "start_time": start_time
            }
        }
        
        math_logger.info("Starting math calculation", extra={
            "correlation_id": session_id,
            "query": query[:50]
        })
        
        prompt = f"""
Você é uma calculadora. Responda APENAS com o cálculo e resultado final.

Exemplos:
- "Quanto é 25 + 37?" → "25 + 37 = 62"
- "10 vezes 47" → "10 × 47 = 470" 
- "15% de 200" → "15% de 200 = 30"

Pergunta: {query}

Resposta (APENAS o cálculo e resultado):
"""
        
        try:
            llm_start = time.time()
            model = genai.GenerativeModel(self.model)
            response = model.generate_content(prompt)
            llm_end = time.time()
            llm_time_ms = (llm_end - llm_start) * 1000
            
            execution_time = time.time() - start_time
            log_data.update({
                "metrics": {
                    **log_data["metrics"],
                    "llm_generation_time": f"{(llm_end - llm_start):.3f}s",
                    "total_execution_time": f"{execution_time:.3f}s"
                },
                "response_metadata": {
                    "result": response.text.strip(),
                    "format": "calculation_result"
                },
                "status": "success",
                "status_code": 200
            })
            
            math_logger.info("Math calculation completed", extra={
                "correlation_id": session_id,
                "execution_time_ms": execution_time * 1000,
                "response_preview": response.text.strip()[:50]
            })
            
            return response.text.strip(), log_data
            
        except Exception as e:
            execution_time = time.time() - start_time
            log_data.update({
                "metrics": {
                    **log_data["metrics"],
                    "total_execution_time": f"{execution_time:.3f}s"
                },
                "status": "error",
                "status_code": 500,
                "error": {
                    "type": type(e).__name__,
                    "message": str(e)
                }
            })
            
            math_logger.error("Math calculation failed", extra={
                "correlation_id": session_id,
                "execution_time_ms": execution_time * 1000,
                "error": str(e)
            }, exc_info=True)
            
            return f"Erro no cálculo: {str(e)}", log_data
    
    def _extract_math_expression(self, query: str) -> str:
        """
        Extract mathematical expression from query
        """
        patterns = [
            r'\d+\s*[+\-*/÷×]\s*\d+',
            r'\d+\s*%\s*de\s*\d+',
            r'\(\s*\d+\s*[+\-*/]\s*\d+\s*\)\s*[+\-*/]\s*\d+'
        ]
        for pattern in patterns:
            match = re.search(pattern, query)
            if match:
                return match.group()
        return query
    
    def _identify_operation(self, query: str) -> str:
        """
        Identify the type of mathematical operation
        """
        query_lower = query.lower()
        if any(op in query_lower for op in ['+', 'mais', 'somar', 'soma']):
            return "addition"
        elif any(op in query_lower for op in ['-', 'menos', 'subtrair']):
            return "subtraction"
        elif any(op in query_lower for op in ['*', '×', 'x', 'vezes', 'multiplicar']):
            return "multiplication"
        elif any(op in query_lower for op in ['/', '÷', 'dividir', 'dividido']):
            return "division"
        elif '%' in query_lower or 'porcentagem' in query_lower:
            return "percentage"
        elif '^' in query_lower or 'elevado' in query_lower:
            return "exponentiation"
        return "complex"


if __name__ == "__main__":
    router = AgentRouter()
    knowledge_agent = KnowledgeAgent()
    math_agent = MathAgent()
    
    test_queries = [
        "O que é a maquininha Smart?",
        "Quanto é 25 + 37?",
        "Como funciona o InfiniteTap?",
        "(42 * 2) / 6"
    ]
    
    print("=== Testing Agent System with Professional Logging ===\n")
    for query in test_queries:
        print(f"Query: {query}")
        agent_type, router_log = router.classify_query(query)
        
        if agent_type == "math":
            response, agent_log = math_agent.process(query, "test-session")
        else:
            response, agent_log = knowledge_agent.process(query, "test-session")
        
        print(f"Response: {response[:100]}..." if len(response) > 100 else f"Response: {response}")
        print("-" * 80 + "\n")