# Local Development Setup (Python 3.13)

This guide helps you set up a local Python 3.13 environment for IDE support while using Docker for runtime.

## Prerequisites

- **Python 3.13+** installed
- **uv** package manager ([install guide](https://github.com/astral-sh/uv))
- **Docker & Docker Compose**
- **Ollama** (optional - can use containerized version)

---

## Step 1: Create Virtual Environment with uv

```bash
# Navigate to project directory
cd langchain_rag_react_agent

# Create virtual environment with Python 3.13
uv venv --python 3.13

# Activate virtual environment
# On Windows (PowerShell):
.venv\Scripts\Activate.ps1

# On Windows (CMD):
.venv\Scripts\activate.bat

# On Linux/Mac:
source .venv/bin/activate
```

---

## Step 2: Install Dependencies

```bash
# Install all dependencies in editable mode(changes reflect immediately)
uv pip install -e .
```

---

## Step 3: Choose Your Ollama Setup

### Option A: Use Local Ollama (Recommended for Active Development)

```bash
# 1. Install Ollama locally (if not already installed)
# Download from: https://ollama.ai

# 2. Pull the model
ollama pull llama3.2:3b

# 3. Verify Ollama is running
ollama list

# 4. Create .env file
cp .env.example .env

# 5. Update .env to use local Ollama
# Change this line:
OLLAMA_BASE_URL=http://host.docker.internal:11434

# 6. Start Docker app (without Ollama container)
docker-compose up -d --build
```

**Benefits:**

- ✅ Share models across projects
- ✅ Faster performance
- ✅ Use Ollama CLI for testing

### Option B: Use Containerized Ollama (Easier Setup)

```bash
# 1. Create .env file
cp .env.example .env

# 2. Keep default setting in .env:
OLLAMA_BASE_URL=http://ollama:11434

# 3. Start everything in Docker
docker-compose --profile local up -d --build

# 4. Pull model into container
docker exec langchain-ollama ollama pull llama3.2:3b
```

**Benefits:**

- ✅ No local Ollama installation needed
- ✅ Consistent with team members
- ✅ Easy cleanup

---

## Step 4: Verify Setup

### Test Local Environment

```bash
# Activate virtual environment (if not already)
.venv\Scripts\Activate.ps1  # Windows PowerShell

# Test imports
python -c "from langchain.agents import AgentExecutor; print('✅ LangChain imports work!')"

# Check LangChain version (should be 0.3.x)
python -c "import langchain; print(f'LangChain version: {langchain.__version__}')"
```

### Test Docker Environment

```bash
# Check containers are running
docker ps

# Test imports in container
docker exec langchain-rag-agent python -c "from langchain.agents import AgentExecutor; print('✅ Container imports work!')"

# Check LangChain version in container (should be 0.3.x)
docker exec langchain-rag-agent python -c "import langchain; print(f'LangChain version: {langchain.__version__}')"
```

---

## Step 5: Development Workflow

### Running the Application

```bash
# Option 1: Run in Docker (recommended - matches production)
docker-compose logs -f app

# Option 2: Run locally (for debugging)
python -m langchain_rag_react_agent.agent

# Or use the CLI command
langchain-rag-agent
```

### Making Code Changes

1. Edit code in `src/langchain_rag_react_agent/`
2. Changes are **immediately reflected** in Docker (source code is mounted)
3. No rebuild needed for code changes!
4. Only rebuild if you change dependencies in `pyproject.toml`

### Adding New Dependencies

```bash
# 1. Add to pyproject.toml manually, OR:
uv add <package-name>

# 2. Install locally
uv pip install -e .

# 3. Rebuild Docker
docker-compose build
docker-compose up -d
```

---

## Troubleshooting

### IDE shows import errors but code runs?

```bash
# Reinstall dependencies
uv pip install -e . --force-reinstall
```

### LangChain version mismatch?

```bash
# Check local version
python -c "import langchain; print(langchain.__version__)"

# Check Docker version
docker exec langchain-rag-agent python -c "import langchain; print(langchain.__version__)"

# Both should be 0.3.x (not 1.0.x)
```

### Container shows "AgentExecutor not found"?

```bash
# Rebuild with pinned dependencies
docker-compose build --no-cache
docker-compose up -d
```

---

## Python 3.11 vs 3.13 Compatibility

Your code is tested on Python 3.11 and should work on 3.13 with the same dependencies:

- ✅ LangChain 0.3.x supports both Python 3.11 and 3.13
- ✅ All dependencies are compatible
- ✅ No code changes needed

**Note:** If you encounter any Python 3.13-specific issues, you can use Python 3.11 locally while Docker uses 3.13 (or vice versa).

---

## Next Steps

1. ✅ Virtual environment created
2. ✅ Dependencies installed
3. ✅ Ollama configured
4. ✅ Docker containers running
5. 🚀 Start developing!

See [DEVELOPMENT.md](DEVELOPMENT.md) for team development workflow and best practices.
