
from typing import TypedDict

from langchain_ollama import ChatOllama
from langgraph.graph import StateGraph, START, END


# 1. Initialize the LangChain LLM
llm = ChatOllama(
    model="llama3.2",
    temperature=0
)


# 2. Create a small knowledge base
KNOWLEDGE_BASE = [
    {
        "topic": "LangChain",
        "content": (
            "LangChain is a framework for building "
            "applications powered by language models. "
            "It provides integrations, prompts, tools, "
            "and retrieval components."
        ),
    },
    {
        "topic": "LangGraph",
        "content": (
            "LangGraph is a framework for building "
            "stateful workflows and AI agents. "
            "It uses nodes, edges, shared state, "
            "conditional routing, and loops."
        ),
    },
    {
        "topic": "RAG",
        "content": (
            "Retrieval-Augmented Generation, or RAG, "
            "retrieves relevant information from a "
            "knowledge source and supplies it to an "
            "LLM to help generate grounded answers."
        ),
    },
    {
        "topic": "Agentic AI",
        "content": (
            "Agentic AI systems pursue goals by "
            "making decisions, planning steps, and "
            "using tools or actions when appropriate."
        ),
    },
]


# 3. Define shared workflow state
class ResearchState(TypedDict):
    question: str
    context: str
    answer: str


# 4. Retrieve relevant information
def retrieve_context(state: ResearchState) -> dict:
    question_words = set(
        state["question"].lower().split()
    )

    matches = []

    for document in KNOWLEDGE_BASE:
        searchable_text = (
            document["topic"] + " " + document["content"]
        ).lower()

        document_words = set(searchable_text.split())
        score = len(question_words & document_words)

        if score > 0:
            matches.append((score, document))

    # Keep the highest-scoring documents
    matches.sort(key=lambda item: item[0], reverse=True)

    context = "\n".join(
        f"{doc['topic']}: {doc['content']}"
        for _, doc in matches[:2]
    )

    print("\n[Retriever] Knowledge retrieved.")

    return {"context": context}


# 5. Decide which node runs next
def route_question(state: ResearchState) -> str:
    if state["context"].strip():
        return "generate"

    return "fallback"


# 6. Generate an answer using LangChain
def generate_answer(state: ResearchState) -> dict:
    prompt = f"""
You are a helpful AI research assistant.

Answer the question using ONLY the context below.
If the context does not contain enough information,
say that the available knowledge is insufficient.

Context:
{state["context"]}

Question:
{state["question"]}

Answer:
"""

    response = llm.invoke(prompt)

    print("[LLM] Answer generated.")

    return {"answer": response.content}


# 7. Handle questions with no matching information
def fallback_answer(state: ResearchState) -> dict:
    return {
        "answer": (
            "I could not find relevant information "
            "in the knowledge base. Try asking about "
            "LangChain, LangGraph, RAG, or Agentic AI."
        )
    }


# 8. Build the LangGraph workflow
builder = StateGraph(ResearchState)

builder.add_node("retrieve", retrieve_context)
builder.add_node("generate", generate_answer)
builder.add_node("fallback", fallback_answer)

builder.add_edge(START, "retrieve")

builder.add_conditional_edges(
    "retrieve",
    route_question,
    {
        "generate": "generate",
        "fallback": "fallback",
    },
)

builder.add_edge("generate", END)
builder.add_edge("fallback", END)

# Compile the graph
research_graph = builder.compile()


# 9. Run the application
def main():
    print("=== LangGraph Research Assistant ===")
    print("Ask about LangChain, LangGraph, RAG,")
    print("or Agentic AI. Type 'exit' to quit.")

    while True:
        question = input("\nYou: ").strip()

        if question.lower() in {"exit", "quit"}:
            print("Goodbye!")
            break

        if not question:
            print("Please enter a question.")
            continue

        result = research_graph.invoke(
            {
                "question": question,
                "context": "",
                "answer": "",
            }
        )

        print("\nAssistant:", result["answer"])


if __name__ == "__main__":
    main()
