import re
import os
from dotenv import load_dotenv
import google.generativeai as genai
from rag import query_rag

load_dotenv()
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

load_dotenv()

class AgentRouter:
    """Routes user queries to the appropriate agent"""
    
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
        
        # Knowledge patterns to ensure math doesn't override
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
    
    def classify_query(self, query: str) -> str:
        """Classify if query is math or knowledge-based"""
        query_lower = query.lower()
        
        # First check if it's clearly about InfinitePay/business
        for pattern in self.knowledge_patterns:
            if re.search(pattern, query_lower):
                return "knowledge"
        
        # Then check for math patterns
        for pattern in self.math_patterns:
            if re.search(pattern, query_lower):
                return "math"
        
        # Default to knowledge agent
        return "knowledge"

# Test function
def test_classification():
    """Test the classification system"""
    router = AgentRouter()
    
    test_cases = [
        ("O que é a maquininha Smart?", "knowledge"),
        ("Quanto é 25 + 37?", "math"),
        ("Como funciona o InfiniteTap?", "knowledge"),
        ("Calcule 15% de 200", "math"),
    ]
    
    print("=== Testing Agent Classification ===")
    for query, expected in test_cases:
        predicted = router.classify_query(query)
        status = "✅" if predicted == expected else "❌"
        print(f"{status} '{query}' -> {predicted} (expected: {expected})")

if __name__ == "__main__":
    test_classification()


class KnowledgeAgent:
    """Handles questions about InfinitePay using RAG"""
    
    def process(self, query: str, session_id: str) -> str:
        """Process knowledge-based query"""
        # Get relevant context from your documents
        context = query_rag(query, "infinitepay-context")
        
        if not context:
            return "Desculpe, não encontrei informações sobre isso na base de conhecimento da InfinitePay."
        
        # Create prompt with context
        prompt = f"""
Você é um assistente da InfinitePay. Use APENAS as informações do contexto para responder.

CONTEXTO:
{context}

PERGUNTA: {query}

Responda de forma clara e útil baseado apenas no contexto fornecido.
"""
        
        try:
            model = genai.GenerativeModel('gemini-1.5-flash')
            response = model.generate_content(prompt)
            return response.text
        except Exception as e:
            return f"Erro ao processar sua pergunta: {str(e)}"

class MathAgent:
    """Simple math using Gemini with strict formatting"""
    
    def process(self, query: str, session_id: str) -> str:
        """Process mathematical query using Gemini"""
        
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
            return response.text.strip()
        except Exception as e:
            return f"Erro no cálculo: {str(e)}"