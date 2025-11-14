# 🚀 Quick Start Guide

Get up and running with LangChain RAG React Agent in 5 minutes!

## 📦 What You'll Need

- Docker & Docker Compose installed
- 4GB+ RAM available
- 10GB+ disk space

## 🎯 Fastest Path: Docker Compose with Local Ollama

### Step 1: Navigate to Project

```bash
cd C:\Users\rs258\MyAI\LangChain\langchain_rag_react_agent
```

### Step 2: Configure Environment

```bash
# Copy the example environment file
copy .env.example .env

# Edit .env if needed (optional - defaults work fine)
notepad .env
```

### Step 3: Start Services

```bash
# Start both app and Ollama
docker-compose --profile local up -d

# Check services are running
docker-compose ps
```

### Step 4: Download Ollama Model (First Time Only)

```bash
# Pull the default model (llama3.2:3b - ~2GB)
docker exec langchain-ollama ollama pull llama3.2:3b

# Or use a smaller model for testing
docker exec langchain-ollama ollama pull llama3.2:1b
```

### Step 5: Run the Agent

```bash
# Interactive mode
docker-compose exec app python -m langchain_rag_react_agent.agent

# You should see:
# Start ReAct Agent with PDF RAG context chatting!
# You: [Type your question here]
```

### Step 6: Ask Questions

```　Example Conversation:
You: What are the main topics in the Recurrent Neural Network PDF?
AI: Based on the PDF document, the main topics include...

You: Explain the LSTM architecture
AI: LSTM (Long Short-Term Memory) is...

You: exit
```

## 🎨 Alternative: Use External Ollama

If you already have Ollama running on your machine:

### Step 1: Update .env

```env
OLLAMA_BASE_URL=http://host.docker.internal:11434
```

### Step 2: Start App Only

```bash
docker-compose up -d
```

### Step 3: Run

```bash
docker-compose exec app python -m langchain_rag_react_agent.agent
```

## 💻 Alternative: Local Development (No Docker)

### Step 1: Install Dependencies

```bash
# Install uv if not already installed
pip install uv

# Install project dependencies
uv sync
```

### Step 2: Install System Dependencies

```bash
# Windows (using Chocolatey)
choco install tesseract poppler

# Or download manually:
# - Tesseract: https://github.com/UB-Mannheim/tesseract/wiki
# - Poppler: https://github.com/oschwartz10612/poppler-windows/releases
```

### Step 3: Pre-download Models (Recommended)

```bash
python scripts/setup_models.py
```

### Step 4: Configure Environment

```bash
copy .env.example .env
# Edit OLLAMA_BASE_URL=http://localhost:11434
```

### Step 5: Run

```bash
python -m langchain_rag_react_agent.agent
```

## 📚 Adding Your Own PDFs

```bash
# Copy PDFs to the pdfs directory
copy "C:\path\to\your\document.pdf" pdfs\

# The agent will automatically process them on next run
```

## 🔧 Useful Commands

### Docker Management

```bash
# View logs
docker-compose logs -f app

# Restart services
docker-compose restart

# Stop services
docker-compose down

# Rebuild after code changes
docker-compose build
```

### Ollama Management

```bash
# List available models
docker exec langchain-ollama ollama list

# Pull different model
docker exec langchain-ollama ollama pull gemma2:2b

# Update .env to use new model
# OLLAMA_LLM=gemma2:2b
```

## ❓ Troubleshooting

### "Connection refused" to Ollama

```bash
# Check Ollama is running
docker ps | grep ollama

# Restart Ollama
docker-compose restart ollama
```

### Out of Memory

```bash
# Use smaller model
docker exec langchain-ollama ollama pull llama3.2:1b

# Update .env
# OLLAMA_LLM=llama3.2:1b
```

### PDF Not Processing

- Check PDF is in `pdfs/` directory
- Ensure PDF is not password-protected
- Check logs: `docker-compose logs app`

## 🎉 Next Steps

- Read the full [README.md](README.md) for advanced features
- Explore different Ollama models
- Try cloud LLMs (OpenAI, Anthropic) for production
- Customize the agent prompts in `src/langchain_rag_react_agent/agent.py`

---
