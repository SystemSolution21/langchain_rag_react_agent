# Development Guide

## Setup for Team Development

This project uses a **hybrid approach**: local IDE support + containerized runtime for consistency.

### Prerequisites

- **Docker & Docker Compose** (required)
- **Python 3.13+** (optional - for local IDE support only)
- **[uv](https://github.com/astral-sh/uv)** package manager (optional - recommended) or pip

**Note:** You do NOT need to install Ollama locally! It runs in a Docker container.

---

## Quick Start

### New Team Member Onboarding (5 minutes)

**Minimum requirements:** Just Docker! Everything else is optional.

```bash
# 1. Clone the repository
git clone <repo-url>
cd langchain_rag_react_agent

# 2. Create .env file (copy from .env.example if available)
# Add any required API keys

# 3. Start everything in Docker
docker-compose --profile local up -d --build

# 4. Pull the LLM model (one-time, ~2GB download)
docker exec langchain-ollama ollama pull llama3.2:3b

# 5. Done! Check logs to see it running
docker-compose logs -f app
```

That's it! No Python, no Ollama, no dependencies to install locally.

---

### 1. Clone and Setup Local Environment (Optional - for IDE support)

**For detailed local setup with Python 3.13, see [LOCAL_SETUP.md](LOCAL_SETUP.md)**

```bash
# Quick setup (for IDE autocomplete, linting, type checking)
# Create virtual environment
uv venv --python 3.13

# Activate (Windows PowerShell)
.venv\Scripts\Activate.ps1

# Install dependencies
uv pip install -e .
```

**Why?** This allows your IDE to resolve imports, provide autocomplete, and catch errors while coding.

**Can I skip this?** Yes! You can develop entirely in containers. But IDE support is much better with local dependencies.

### 2. Start Docker Containers

```bash
# Build and start containers (with local Ollama)
docker-compose --profile local up -d --build

# Pull the LLM model into the container
docker exec langchain-ollama ollama pull llama3.2:3b
```

### 3. Develop with Live Reload

- Edit code in `src/` directory
- Changes are **immediately reflected** in the container (no rebuild needed!)
- Container uses the mounted source code from your local filesystem

### 4. View Logs

```bash
# View application logs
docker-compose logs -f app

# View Ollama logs
docker-compose logs -f ollama
```

---

## Team Consistency Guarantees

### ✅ What Ensures Consistency Across Team?

1. **`pyproject.toml`** - Single source of truth for dependencies
2. **`Dockerfile`** - Exact same build process for everyone
3. **`docker-compose.yml`** - Identical runtime environment
4. **CI/CD runs in containers** - Production matches development

### ✅ What's Different Locally?

- **Only the IDE environment** (for autocomplete/linting)
- **Actual code execution happens in containers** (consistent for everyone)

### ⚠️ Important Rules

1. **Never commit local virtual environments** (`.venv/`, `venv/`)
2. **Always test in containers** before pushing
3. **Update `pyproject.toml`** when adding dependencies (not just local pip install)

---

## Workflow

### Adding a New Dependency

```bash
# 1. Add to pyproject.toml manually, OR use uv:
uv add <package-name>

# 2. Install locally for IDE support
uv pip install -e .

# 3. Rebuild container to install in Docker
docker-compose --profile local build
docker-compose --profile local up -d
```

### Running Tests

```bash
# Run tests in container (recommended)
docker exec langchain-rag-agent pytest

# Run tests locally (for quick iteration)
pytest
```

### Debugging

```bash
# Access container shell
docker exec -it langchain-rag-agent bash

# Check installed packages in container
docker exec langchain-rag-agent pip list

# Test imports in container
docker exec langchain-rag-agent python -c "from langchain_classic.agents import AgentExecutor; print('OK')"
```

---

## Troubleshooting

### Import errors in IDE but code runs in container?

```bash
# Reinstall local dependencies
uv pip install -e .
```

### Import errors in container but works locally?

```bash
# Rebuild container
docker-compose --profile local build --no-cache
docker-compose --profile local up -d
```

### Port conflicts (Ollama already running)?

**If you have Ollama installed locally and it's using port 11434:**

```bash
# Option 1: Use your local Ollama (RECOMMENDED for active developers)
# Update .env file:
OLLAMA_BASE_URL=http://host.docker.internal:11434
# Then start without Ollama container:
docker-compose up -d  # Without --profile local

# Option 2: Stop local Ollama and use containerized version
# Quit Ollama from system tray (Windows/Mac)
# Then use containerized Ollama:
docker-compose --profile local up -d
```

**Real-world recommendation:**

- **Active developers**: Use local Ollama (Option 1) - faster, share models across projects
- **New team members**: Use containerized Ollama (Option 2) - easier onboarding
- **CI/CD**: Always use containerized Ollama (Option 2) - reproducible builds

---

## 🤔 Should I Use Local or Containerized Ollama?

### Comparison Table

| Aspect | Local Ollama | Containerized Ollama |
|--------|--------------|---------------------|
| **Setup Time** | 5 min (install once) | 2 min (docker-compose) |
| **Disk Space** | Shared across projects | Separate per project |
| **Speed** | Faster (native) | Slightly slower (container overhead) |
| **GPU Access** | Better (native drivers) | Requires Docker GPU setup |
| **Team Consistency** | ⚠️ Version may differ | ✅ Same version for all |
| **CI/CD** | ❌ Hard to setup | ✅ Easy to integrate |
| **Multi-project** | ✅ Share models | ❌ Duplicate models |
| **Onboarding** | Need to install Ollama | Just need Docker |

### Real-World Usage Patterns

**🏢 Startup/Small Team (2-5 developers):**

```bash
# Most common: Developers use local Ollama
- Install Ollama locally once
- Share models across projects
- Use containerized Ollama only for CI/CD
```

**🏭 Medium/Large Team (5+ developers):**

```bash
# Mixed approach:
- Senior devs: Local Ollama (faster iteration)
- New devs: Containerized Ollama (easier onboarding)
- CI/CD: Always containerized
- Production: Kubernetes with Ollama containers
```

**☁️ Production Deployment:**

```bash
# Always containerized:
- Docker Compose for simple deployments
- Kubernetes for scale
- Specific model versions locked
```

### Our Recommendation

**For this project:**

1. **If you're actively developing AI features:**
   - Install Ollama locally
   - Use `docker-compose up -d` (without `--profile local`)
   - Set `OLLAMA_BASE_URL=http://host.docker.internal:11434` in `.env`

2. **If you're new or just testing:**
   - Use containerized Ollama
   - Use `docker-compose --profile local up -d`
   - Everything works out of the box

3. **For CI/CD pipelines:**
   - Always use `--profile local` (containerized)
   - Ensures reproducible builds

---

## Architecture

```
Local Machine                    Docker Container
┌─────────────────┐             ┌──────────────────┐
│ IDE (VSCode)    │             │ Python Runtime   │
│ - Autocomplete  │             │ - Executes code  │
│ - Linting       │             │ - Dependencies   │
│ - Type checking │             │ - Ollama LLM     │
└─────────────────┘             └──────────────────┘
        │                                │
        └────── src/ (mounted) ──────────┘
              (shared filesystem)
```

**Key Point:** You edit locally, code runs in container!
