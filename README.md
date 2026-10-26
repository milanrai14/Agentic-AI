# Agentic AI System

An AI-powered agentic system designed to solve complex tasks through reasoning, tool usage, multi-step workflows, and context-aware decision-making. Built with Python, LangChain, LangGraph, and locally hosted LLMs using Ollama.

## Overview

Unlike a traditional Generative AI application that primarily generates responses, an Agentic AI system can break tasks into steps, select appropriate tools, evaluate intermediate results, and determine what action to take next.

This project explores the development of an AI agent capable of executing structured workflows while maintaining state and handling conditional decisions.

## Key Features

- **LLM Integration:** Connect to locally hosted language models using Ollama.
- **Agentic Workflows:** Orchestrate multi-step tasks using LangGraph.
- **Tool Calling:** Enable agents to interact with custom tools and external APIs.
- **State Management:** Maintain context throughout workflow execution.
- **Conditional Routing:** Select the next action based on intermediate results.
- **Retrieval-Augmented Generation (RAG):** Retrieve relevant information from a knowledge base.
- **Corrective RAG (CRAG):** Evaluate retrieval relevance and retry or refine retrieval when necessary.
- **Modular Architecture:** Separate agent logic, tools, retrieval, and API layers.
- **Local Model Support:** Run supported LLMs locally to reduce dependence on paid model APIs.

*Features listed above describe the intended project scope; include only those implemented in your current version.*

## Tech Stack

| Category | Technology |
|---|---|
| Programming language | Python |
| LLM framework | LangChain |
| Agent orchestration | LangGraph |
| Local LLM runtime | Ollama |
| Language model | Llama 3.2 |
| Embeddings | Ollama Embeddings |
| Vector database | Chroma |
| Backend API | FastAPI |
| Configuration | Python-dotenv |
| Version control | Git and GitHub |

## Architecture

```text
User Request
     |
     v
Input Processing
     |
     v
LangGraph Workflow
     |
     +------> LLM Reasoning
     |
     +------> Tool Selection and Execution
     |
     +------> Knowledge Retrieval (RAG)
     |                 |
     |                 v
     |          Relevance Evaluation
     |                 |
     |          Retry if necessary
     |
     v
Result Verification
     |
     v
Final Response
```

LangChain provides model and tool integrations, while LangGraph manages workflow state, conditional routing, and multi-step execution.

## Project Structure

```text
agentic-ai-system/
├── app/
│   ├── agents/
│   │   ├── agent.py
│   │   └── graph.py
│   ├── tools/
│   │   └── custom_tools.py
│   ├── rag/
│   │   ├── retriever.py
│   │   └── ingestion.py
│   ├── api/
│   │   └── routes.py
│   ├── config.py
│   └── main.py
├── data/
├── tests/
├── .env.example
├── .gitignore
├── requirements.txt
└── README.md
```

## Getting Started

### 1. Clone the repository

```bash
git clone https://github.com/YOUR_USERNAME/agentic-ai-system.git
cd agentic-ai-system
```

### 2. Create a virtual environment

Windows:

```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
```

macOS/Linux:

```bash
python -m venv .venv
source .venv/bin/activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Install and configure Ollama

Install Ollama from [ollama.com](https://ollama.com/), then download the model:

```bash
ollama pull llama3.2
```

Ensure the Ollama service is running before executing the application.

### 5. Configure environment variables

Create a `.env` file based on `.env.example`.

```env
OLLAMA_MODEL=llama3.2
OLLAMA_BASE_URL=http://localhost:11434
```

Add other configuration values as required by the implemented features. Do not commit secrets or API keys.

### 6. Run the application

For a Python entry point:

```bash
python -m app.main
```

For a FastAPI application, if `app/main.py` exposes an object named `app`:

```bash
uvicorn app.main:app --reload
```

Use the command matching your actual application structure.

## Example Use Cases

- Research assistants that gather and organize information.
- Document question-answering systems using RAG.
- AI assistants that call tools and APIs.
- Workflow automation with conditional decisions.
- Corrective retrieval systems that retry when search results are inadequate.
- Multi-step task execution with human approval.

## Testing

Run automated tests using:

```bash
pytest
```

Tests should cover agent decisions, tool execution, retrieval relevance, workflow routing, error handling, and output quality.

## Future Improvements

- Add persistent checkpointing and conversation memory.
- Implement human-in-the-loop approval.
- Add structured logging and workflow tracing.
- Evaluate retrieval quality and answer groundedness.
- Add Docker support and cloud deployment.
- Implement authentication, rate limiting, and API security.
- Add evaluation datasets and regression tests.

## Security Considerations

- Validate user inputs and uploaded documents.
- Restrict agent tools to explicitly authorized actions.
- Require approval for sensitive or irreversible operations.
- Protect credentials and confidential data.
- Apply timeouts, retry limits, and resource limits.
- Treat retrieved documents and tool outputs as untrusted input.

## Learning Objectives

This project demonstrates practical experience with LLM application development, agent orchestration, retrieval-augmented generation, tool integration, workflow design, and production-oriented software engineering.

## License

This project is licensed under the MIT License. See the `LICENSE` file for details.

## Author

**Your Name**

- GitHub: [YOUR_USERNAME](https://github.com/YOUR_USERNAME)
- LinkedIn: [Your LinkedIn Profile](https://www.linkedin.com/)

---

*Built as a hands-on project to explore Agentic AI, RAG, and production-oriented AI engineering.*
