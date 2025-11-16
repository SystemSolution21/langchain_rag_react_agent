# 🤖 LangChain RAG React Agent

Advanced RAG-based ReAct Agent with PDF processing, OCR, table extraction, and multimodal support.

## ✨ Features

- **🔍 Advanced PDF Processing**: Tables, charts, images, and OCR support
- **🧠 ReAct Agent**: Reasoning and acting with LangChain agents
- **📚 Vector Store**: Persistent Chroma DB with semantic search
- **🎯 Multimodal RAG**: Text, tables, charts, and image extraction
- **🐳 Docker Ready**: Containerized deployment with Docker Compose
- **🔄 Flexible LLM Support**: Ollama (local) or cloud providers (OpenAI, Anthropic)
- **📊 Rich Output**: Markdown formatting with source citations

## 🏗️ Architecture

```project
langchain_rag_react_agent/
├── src/langchain_rag_react_agent/  # Main package
│   ├── agent.py                     # ReAct agent application
│   ├── rag.py                       # RAG processing logic
│   ├── config.py                    # Configuration management
│   └── utils/                       # Utility modules
│       └── logger.py                # Logging configuration
├── scripts/                         # Helper scripts
│   └── setup_models.py              # Pre-download AI models
├── pdfs/                            # PDF documents directory
├── db/                              # Vector store database
├── logs/                            # Application logs
├── Dockerfile                       # Container definition
├── docker-compose.yml               # Multi-service orchestration
└── pyproject.toml                   # Project dependencies
```

## 🚀 Quick Start

### Option 1: Docker Compose (Recommended)

#### With Local Ollama (Full Stack)

```bash
# 1. Clone and navigate
cd langchain_rag_react_agent

# 2. Create environment file
cp .env.example .env

# 3. Add your PDFs
cp your_document.pdf pdfs/

# 4. Start services (includes Ollama)
docker-compose --profile local up -d

# 5. Pull Ollama model (first time only)
docker exec langchain-ollama ollama pull llama3.2:3b

# 6. Run the agent
docker-compose exec app python -m langchain_rag_react_agent.agent
```

#### With External Ollama or Cloud LLM

```bash
# 1. Configure .env for external service
# Set OLLAMA_BASE_URL=http://host.docker.internal:11434
# Or set OPENAI_API_KEY for OpenAI

# 2. Start app only
docker-compose up -d

# 3. Run the agent
docker-compose exec app python -m langchain_rag_react_agent.agent
```

### Option 2: Local Development

```bash
# 1. Install dependencies with uv
uv sync

# 2. Pre-download models (recommended)
python scripts/setup_models.py

# 3. Create .env file
cp .env.example .env

# 4. Add PDFs to pdfs/ directory
cp your_document.pdf pdfs/

# 5. Run the agent
python -m langchain_rag_react_agent.agent
# Or use the CLI command
langchain-rag-agent
```

## 📋 Prerequisites

### For Docker (Recommended for Teams)

- **Docker Engine 20.10+** and **Docker Compose**
- **That's it!** No need to install Python, Ollama, or any dependencies locally
- See [DEVELOPMENT.md](DEVELOPMENT.md) for team development workflow

### For Docker

- Docker Engine 20.10+
- Docker Compose 2.0+
- 4GB+ RAM (8GB+ recommended for Ollama)
- 10GB+ disk space

### For Local Development

- Python 3.13+
- uv package manager
- Tesseract OCR
- Poppler (for PDF processing)
- Git

## 🔧 Configuration

### Environment Variables

See `.env.example` for all available options. Key variables:

| Variable | Description | Default |
|----------|-------------|---------|
| `OLLAMA_BASE_URL` | Ollama server URL | `http://ollama:11434` |
| `OLLAMA_LLM` | Ollama model name | `llama3.2:3b` |
| `OPENAI_API_KEY` | OpenAI API key (optional) | - |
| `PROJECT_ROOT` | Project root directory | `/app` (Docker) |

### Docker Profiles

- **`local`**: Full stack with Ollama included
- **default**: App only, connects to external LLM

## 📚 Usage

### Interactive Chat

```bash
# Start the agent
langchain-rag-agent

# Ask questions about your PDFs
You: What are the main topics in the document?
AI: Based on the PDF documents, the main topics are...
```

### Pre-download Models

```bash
# Download HuggingFace embeddings (~1.34 GB)
setup-models
```

## 🛠️ Development

### Install Development Dependencies

```bash
uv sync --group dev
```

### Run Tests

```bash
pytest
```

### Code Formatting

```bash
# Format code
black src/

# Lint code
ruff check src/
```

## 🐳 Docker Commands

### Build and Run

```bash
# Build image
docker-compose build

# Start services (with Ollama)
docker-compose --profile local up -d

# Start app only
docker-compose up -d

# View logs
docker-compose logs -f app

# Stop services
docker-compose down
```

### Manage Ollama Models

```bash
# List models
docker exec langchain-ollama ollama list

# Pull a model
docker exec langchain-ollama ollama pull llama3.2:3b

# Remove a model
docker exec langchain-ollama ollama rm llama3.2:3b
```

## 📖 Advanced Features

### Supported PDF Content Types

- ✅ Plain text
- ✅ Tables (structured extraction)
- ✅ Charts and graphs (OCR + analysis)
- ✅ Images with text (OCR)
- ✅ Complex layouts
- ✅ Multi-column documents

### Vector Store Features

- Persistent Chroma DB
- Automatic PDF change detection
- Incremental updates
- Source metadata tracking
- Semantic similarity search

## 🔍 Troubleshooting

### Ollama Connection Issues

```bash
# Check Ollama is running
docker ps | grep ollama

# Test Ollama API
curl http://localhost:11434/api/tags
```

### PDF Processing Errors

- Ensure Tesseract is installed
- Check PDF file permissions
- Verify PDF is not encrypted

### Memory Issues

- Reduce `RETRIEVAL_K` in .env
- Use smaller Ollama models (e.g., `llama3.2:1b`)
- Increase Docker memory limit

## 📝 License

MIT License - see LICENSE file for details

## 🤝 Contributing

Contributions welcome! Please open an issue or submit a pull request.

## 📧 Support

For issues and questions, please open a GitHub issue.

---

**Built with** ❤️ **using LangChain, Ollama, and Docker**
