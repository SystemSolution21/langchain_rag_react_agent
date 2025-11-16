# Quick Reference Guide

## 🚀 Common Commands

### Local Development Setup

```bash
# Create virtual environment (Python 3.13)
uv venv --python 3.13

# Activate virtual environment
.venv\Scripts\Activate.ps1  # Windows PowerShell
source .venv/bin/activate    # Linux/Mac

# Install dependencies
uv pip install -e .
```

---

### Docker Commands

#### With Containerized Ollama (New Team Members)

```bash
# Build and start everything
docker-compose --profile local up -d --build

# Pull LLM model (first time only)
docker exec langchain-ollama ollama pull llama3.2:3b

# View logs
docker-compose logs -f app

# Stop containers
docker-compose --profile local down
```

#### With Local Ollama (Active Developers)

```bash
# Make sure Ollama is running locally
ollama list

# Update .env file
OLLAMA_BASE_URL=http://host.docker.internal:11434

# Build and start app only
docker-compose up -d --build

# View logs
docker-compose logs -f app

# Stop containers
docker-compose down
```

---

### Ollama Commands

```bash
# Pull a model
ollama pull llama3.2:3b

# List installed models
ollama list

# Run a model (test)
ollama run llama3.2:3b

# Remove a model
ollama rm llama3.2:3b

# Check Ollama version
ollama --version
```

---

### Development Workflow

```bash
# 1. Make code changes in src/

# 2. Changes are automatically reflected in Docker (no rebuild needed!)

# 3. View logs to see changes
docker-compose logs -f app

# 4. If you changed dependencies in pyproject.toml:
docker-compose build
docker-compose up -d
```

---

### Debugging

```bash
# Access container shell
docker exec -it langchain-rag-agent bash

# Run Python in container
docker exec -it langchain-rag-agent python

# Test imports in container
docker exec langchain-rag-agent python -c "from langchain.agents import AgentExecutor; print('OK')"

# Check LangChain version in container
docker exec langchain-rag-agent python -c "import langchain; print(langchain.__version__)"

# Check installed packages in container
docker exec langchain-rag-agent pip list | grep langchain
```

---

### Troubleshooting

```bash
# Rebuild from scratch (no cache)
docker-compose build --no-cache
docker-compose up -d

# Remove all containers and volumes
docker-compose down -v

# Check container status
docker ps -a

# View all logs
docker-compose logs

# Follow specific service logs
docker-compose logs -f ollama
docker-compose logs -f app
```

---

### Adding Dependencies

```bash
# 1. Add to pyproject.toml or use uv
uv add <package-name>

# 2. Install locally
uv pip install -e .

# 3. Rebuild Docker
docker-compose build
docker-compose up -d
```

---

### Running Tests

```bash
# Run tests in container (recommended)
docker exec langchain-rag-agent pytest

# Run tests locally
pytest

# Run specific test file
pytest tests/test_agent.py

# Run with verbose output
pytest -v
```

---

## 📁 Important Files

| File | Purpose |
|------|---------|
| `pyproject.toml` | Dependencies and project config |
| `.env` | Environment variables (create from `.env.example`) |
| `docker-compose.yml` | Docker services configuration |
| `Dockerfile` | Container build instructions |
| `src/langchain_rag_react_agent/agent.py` | Main application |
| `src/langchain_rag_react_agent/rag.py` | RAG logic |

---

## 🔧 Configuration

### .env File Quick Setup

```bash
# Copy example
cp .env.example .env

# For containerized Ollama
OLLAMA_BASE_URL=http://ollama:11434

# For local Ollama
OLLAMA_BASE_URL=http://host.docker.internal:11434

# Choose model
OLLAMA_LLM=llama3.2:3b
```

---

## 🆘 Common Issues

### "Port 11434 already in use"
```bash
# Option 1: Stop local Ollama (quit from system tray)
# Option 2: Use local Ollama (update .env and run without --profile local)
```

### "Module not found" in container
```bash
docker-compose build --no-cache
docker-compose up -d
```

### "Import errors" in IDE
```bash
# Reinstall local dependencies
uv pip install -e . --force-reinstall
```

### "AgentExecutor not found"
```bash
# Check LangChain version (should be 0.3.x, not 1.0.x)
docker exec langchain-rag-agent python -c "import langchain; print(langchain.__version__)"

# If 1.0.x, rebuild with pinned dependencies
docker-compose build --no-cache
```

---

## 📚 Documentation

- [LOCAL_SETUP.md](LOCAL_SETUP.md) - Detailed local development setup
- [DEVELOPMENT.md](DEVELOPMENT.md) - Team development workflow
- [README.md](README.md) - Project overview and features

