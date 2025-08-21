import re
import os
import time
import json
from datetime import datetime
from dotenv import load_dotenv
import google.generativeai as genai
from rag import query_rag

load_dotenv()
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

class AgentRouter:
    """Routes user queries to the appropriate agent with structured logging"""
    
    def __init__(self):
        self.math_patterns = [
            r'\d+\s*[+\-*/÷×]\s*\d+',
            r'calcul|calculadora',
            r'quanto\s+(é|eh|e)\s+',
            r'qual\s+(é|eh|e)\s+o\s+resultado',
            r'somar|subtrair|multiplicar|dividir',
            r'soma|subtração|multiplicação|divisão',
            r'\+|\-|\*|\/|=',
            r'porcentagem|%',
            r'\d+\s*%',
            r'vezes|vez',
            r'mais|menos',
            r'dividido\s+por',
            r'elevado\s+a',
            r'ao\s+quadrado|ao\s+cubo',
            r'raiz\s+quadrada|raiz\s+de',
            r'fatorial',
            r'exponencial',
            r'\d+\s*\^\s*\d+',
        ]
        
        self.knowledge_patterns = [
            r'o\s+que\s+(é|eh|e)',
            r'como\s+funciona',
            r'quais\s+são',
            r'infinitepay|maquininha|app|pix|taxa',
            r'conta\s+inteligente',
            r'empréstimo',
            r'cartão\s+virtual',
            r'nitro|receba\s+na\s+hora',
        ]
    
    def classify_query(self, query: str) -> tuple[str, dict]:
        """
        Classify if query is math or knowledge-based and return decision details
        Returns: (agent_type, decision_log)
        """
        query_lower = query.lower()
        decision_time = datetime.utcnow().isoformat()
        
        # Check for knowledge patterns
        for pattern in self.knowledge_patterns:
            if re.search(pattern, query_lower):
                decision_log = {
                    "timestamp": decision_time,
                    "router": "AgentRouter",
                    "query": query,
                    "decision": "knowledge",
                    "reason": f"Matched knowledge pattern: {pattern}",
                    "confidence": 0.95
                }
                print(f"[ROUTER LOG] {json.dumps(decision_log, ensure_ascii=False)}")
                return "knowledge", decision_log
        
        # Check for math patterns
        for pattern in self.math_patterns:
            if re.search(pattern, query_lower):
                decision_log = {
                    "timestamp": decision_time,
                    "router": "AgentRouter",
                    "query": query,
                    "decision": "math",
                    "reason": f"Matched math pattern: {pattern}",
                    "confidence": 0.95
                }
                print(f"[ROUTER LOG] {json.dumps(decision_log, ensure_ascii=False)}")
                return "math", decision_log
        
        # Default to knowledge
        decision_log = {
            "timestamp": decision_time,
            "router": "AgentRouter",
            "query": query,
            "decision": "knowledge",
            "reason": "No specific pattern matched, defaulting to knowledge",
            "confidence": 0.5
        }
        print(f"[ROUTER LOG] {json.dumps(decision_log, ensure_ascii=False)}")
        return "knowledge", decision_log


class KnowledgeAgent:
    """Handles questions about InfinitePay using RAG with execution logging"""
    
    def process(self, query: str, session_id: str) -> tuple[str, dict]:
        """
        Process knowledge-based query with logging
        Returns: (response, execution_log)
        """
        start_time = time.time()
        log_data = {
            "agent": "KnowledgeAgent",
            "query": query,
            "session_id": session_id,
            "timestamp": datetime.utcnow().isoformat()
        }
        
        try:
            # Get relevant context from RAG
            context = query_rag(query, "infinitepay-context")
            
            if not context:
                execution_time = time.time() - start_time
                log_data.update({
                    "source": "No context found",
                    "execution_time": f"{execution_time:.3f}s",
                    "status": "no_context"
                })
                print(f"[KNOWLEDGE LOG] {json.dumps(log_data, ensure_ascii=False)}")
                return "Desculpe, não encontrei informações sobre isso na base de conhecimento da InfinitePay.", log_data
            
            # Log the source
            log_data["source"] = f"RAG context (InfinitePay docs) - {len(context)} chars"
            
            # Create prompt with context
            prompt = f"""
Você é um assistente da InfinitePay. Use APENAS as informações do contexto para responder.

CONTEXTO:
{context}

PERGUNTA: {query}

Responda de forma clara e útil baseado apenas no contexto fornecido.
"""
            
            # Generate response
            model = genai.GenerativeModel('gemini-1.5-flash')
            response = model.generate_content(prompt)
            
            execution_time = time.time() - start_time
            log_data.update({
                "execution_time": f"{execution_time:.3f}s",
                "status": "success",
                "response_length": len(response.text)
            })
            
            print(f"[KNOWLEDGE LOG] {json.dumps(log_data, ensure_ascii=False)}")
            return response.text, log_data
            
        except Exception as e:
            execution_time = time.time() - start_time
            log_data.update({
                "execution_time": f"{execution_time:.3f}s",
                "status": "error",
                "error": str(e)
            })
            print(f"[KNOWLEDGE LOG] {json.dumps(log_data, ensure_ascii=False)}")
            return f"Erro ao processar sua pergunta: {str(e)}", log_data


class MathAgent:
    """Simple math using Gemini with execution logging"""
    
    def process(self, query: str, session_id: str) -> tuple[str, dict]:
        """
        Process mathematical query with logging
        Returns: (response, execution_log)
        """
        start_time = time.time()
        log_data = {
            "agent": "MathAgent",
            "query": query,
            "session_id": session_id,
            "timestamp": datetime.utcnow().isoformat()
        }
        
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
            model = genai.GenerativeModel('gemini-1.5-flash')
            response = model.generate_content(prompt)
            
            execution_time = time.time() - start_time
            log_data.update({
                "execution_time": f"{execution_time:.3f}s",
                "status": "success",
                "llm_used": "gemini-1.5-flash"
            })
            
            print(f"[MATH LOG] {json.dumps(log_data, ensure_ascii=False)}")
            return response.text.strip(), log_data
            
        except Exception as e:
            execution_time = time.time() - start_time
            log_data.update({
                "execution_time": f"{execution_time:.3f}s",
                "status": "error",
                "error": str(e)
            })
            print(f"[MATH LOG] {json.dumps(log_data, ensure_ascii=False)}")
            return f"Erro no cálculo: {str(e)}", log_data


# Test the logging system
if __name__ == "__main__":
    router = AgentRouter()
    knowledge_agent = KnowledgeAgent()
    math_agent = MathAgent()
    
    test_queries = [
        "O que é a maquininha Smart?",
        "Quanto é 25 + 37?",
        "Como funciona o InfiniteTap?",
        "Calcule 15% de 200"
    ]
    
    print("=== Testing Agent System with Logging ===\n")
    for query in test_queries:
        print(f"Query: {query}")
        agent_type, router_log = router.classify_query(query)
        
        if agent_type == "math":
            response, agent_log = math_agent.process(query, "test-session")
        else:
            response, agent_log = knowledge_agent.process(query, "test-session")
        
        print(f"Response: {response[:100]}..." if len(response) > 100 else f"Response: {response}")
        print("-" * 80 + "\n")