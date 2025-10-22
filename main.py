# Step 1: Install packages if not done
# pip install langgraph langchain openai faiss-cpu

from langgraph.graph import StateGraph, END
from langchain_community.vectorstores import FAISS
from langchain_openai import OpenAIEmbeddings, ChatOpenAI
import random
from typing import TypedDict

# -----------------------------
# Simulated Banking APIs
# -----------------------------
def get_account_balance(account_id):
    balances = {"12345": 5000.50, "67890": 12000.00}
    return balances.get(account_id, 0.0)

def apply_loan(account_id, amount):
    credit_score = random.randint(300, 850)
    approved = credit_score > 600
    return {"approved": approved, "amount": amount if approved else 0, "score": credit_score}

def transaction_history(account_id):
    history = {
        "12345": ["Deposit $1000", "Withdrawal $200", "Transfer $500"],
        "67890": ["Deposit $5000", "Withdrawal $300"]
    }
    return history.get(account_id, [])

# -----------------------------
# Initialize LLM + RAG (Banking Knowledge)
# -----------------------------
# Note: Set OPENAI_API_KEY environment variable or create .env file
try:
    llm = ChatOpenAI(model="gpt-4")
    docs = [
        "Customer can check account balance, transfer funds, apply for loans.",
        "Loan eligibility is based on income, credit score, and account history.",
        "Banking regulations must be followed for KYC and compliance."
    ]
    embeddings = OpenAIEmbeddings()
    vectorstore = FAISS.from_texts(docs, embeddings)
    rag_available = True
except Exception as e:
    print(f"OpenAI not configured: {e}")
    print("Please set OPENAI_API_KEY environment variable or create .env file")
    rag_available = False

def rag_response(query):
    """Simple RAG response using vectorstore"""
    if not rag_available:
        return "I can help you with banking services like checking balances, applying for loans, and viewing transaction history."
    
    docs = vectorstore.similarity_search(query, k=1)
    if docs:
        return docs[0].page_content
    return "I can help you with banking services like checking balances, applying for loans, and viewing transaction history."

# -----------------------------
# Define State for LangGraph
# -----------------------------
class BankingState(TypedDict):
    query: str
    account_id: str
    next_step: str
    response: str
    status: str

# -----------------------------
# Agent Functions
# -----------------------------
def query_agent(state: BankingState) -> BankingState:
    """Understand customer query"""
    query = state["query"].lower()
    return {
        **state,
        "status": "query_understood"
    }

def planner_agent(state: BankingState) -> BankingState:
    """Decide next steps"""
    query = state["query"].lower()
    if "balance" in query:
        next_step = "check_balance"
    elif "loan" in query:
        next_step = "loan_application"
    elif "history" in query or "transaction" in query:
        next_step = "transactions"
    else:
        next_step = "rag_response"
    
    return {
        **state,
        "next_step": next_step,
        "status": "planned"
    }

def response_agent(state: BankingState) -> BankingState:
    """Generate answer using RAG + Banking APIs"""
    account_id = state["account_id"]
    next_step = state["next_step"]
    
    try:
        if next_step == "check_balance":
            result = f"Your account balance is ${get_account_balance(account_id):,.2f}"
        elif next_step == "loan_application":
            loan_result = apply_loan(account_id, 10000)
            if loan_result['approved']:
                result = f"Loan approved for ${loan_result['amount']}, credit score: {loan_result['score']}"
            else:
                result = f"Loan rejected, credit score: {loan_result['score']}"
        elif next_step == "transactions":
            tx_history = transaction_history(account_id)
            result = "Recent transactions: " + ", ".join(tx_history)
        else:
            # fallback to RAG
            result = rag_response(state["query"])
        
        return {
            **state,
            "response": result,
            "status": "completed"
        }
    except Exception as e:
        return {
            **state,
            "response": "Sorry, unable to fetch info at the moment.",
            "status": "failed"
        }

def qa_agent(state: BankingState) -> BankingState:
    """Check response correctness"""
    response = state.get("response", "No response")
    status = "passed" if response != "No response" else "failed"
    return {
        **state,
        "status": status
    }

# -----------------------------
# Build Graph
# -----------------------------
workflow = StateGraph(BankingState)

# Add nodes
workflow.add_node("query", query_agent)
workflow.add_node("planner", planner_agent)
workflow.add_node("response", response_agent)
workflow.add_node("qa", qa_agent)

# Add edges
workflow.add_edge("query", "planner")
workflow.add_edge("planner", "response")
workflow.add_edge("response", "qa")
workflow.add_edge("qa", END)

# Set entry point
workflow.set_entry_point("query")

# Compile the graph
app = workflow.compile()

# -----------------------------
# Run Multi-Layer Banking Workflow
# -----------------------------
customer_query = "Can I check my account balance and apply for a loan?"
initial_state = {
    "query": customer_query,
    "account_id": "12345",
    "next_step": "",
    "response": "",
    "status": "idle"
}

result = app.invoke(initial_state)

# -----------------------------
# Output Results
# -----------------------------
print("Customer Query:", customer_query)
print("Response:", result["response"])
print("QA Status:", result["status"])
