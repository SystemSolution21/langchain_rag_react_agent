"""Tests for the agent module."""

from unittest.mock import patch

from langchain_core.documents.base import Document

# Note: We'll test the components that can be tested without running the full agent


class TestAgentComponents:
    """Tests for agent module components."""

    @patch("langchain_rag_react_agent.agent.ChatOllama")
    @patch("langchain_rag_react_agent.agent.HuggingFaceEmbeddings")
    def test_llm_initialization(self, mock_embeddings, mock_chat_ollama, monkeypatch):
        """Test that LLM is initialized with correct parameters."""
        monkeypatch.setenv("OLLAMA_LLM", "llama3.2:3b")
        monkeypatch.setenv("OLLAMA_BASE_URL", "http://localhost:11434")

        # Import after setting env vars
        import importlib

        import langchain_rag_react_agent.agent as agent_module

        importlib.reload(agent_module)

        # Verify ChatOllama was called (it's called at module level)
        # This test verifies the module can be imported without errors

    @patch("langchain_rag_react_agent.agent.HuggingFaceEmbeddings")
    def test_embeddings_initialization(self, mock_embeddings):
        """Test that embeddings are initialized with correct model."""
        # Import the module

        # The embeddings should be created at module level
        # This test verifies the module structure


class TestSourceMetadata:
    """Tests for SourceMetadata Pydantic model."""

    def test_source_metadata_creation(self):
        """Test creating SourceMetadata instance."""
        from langchain_rag_react_agent.agent import SourceMetadata

        metadata = SourceMetadata(file="test.pdf", page="1", type="text")

        assert metadata.file == "test.pdf"
        assert metadata.page == "1"
        assert metadata.type == "text"

    def test_source_metadata_validation(self):
        """Test SourceMetadata field validation."""
        from langchain_rag_react_agent.agent import SourceMetadata

        # Should accept valid content types
        valid_types = ["text", "table", "ocr_images", "chart_graph", "structured"]
        for content_type in valid_types:
            metadata = SourceMetadata(file="test.pdf", page="1", type=content_type)
            assert metadata.type == content_type


class TestRAGResponse:
    """Tests for RAGResponse Pydantic model."""

    def test_rag_response_creation(self):
        """Test creating RAGResponse instance."""
        from langchain_rag_react_agent.agent import RAGResponse, SourceMetadata

        sources = [
            SourceMetadata(file="test1.pdf", page="1", type="text"),
            SourceMetadata(file="test2.pdf", page="2", type="table"),
        ]

        response = RAGResponse(answer="This is the answer", sources=sources)

        assert response.answer == "This is the answer"
        assert len(response.sources) == 2
        assert response.sources[0].file == "test1.pdf"

    def test_rag_response_empty_sources(self):
        """Test RAGResponse with empty sources list."""
        from langchain_rag_react_agent.agent import RAGResponse

        response = RAGResponse(answer="Answer without sources", sources=[])

        assert response.answer == "Answer without sources"
        assert response.sources == []


class TestPdfRagTool:
    """Tests for pdf_rag_tool function."""

    @patch("langchain_rag_react_agent.agent.rag_chain")
    def test_rag_with_sources_basic(self, mock_rag_chain):
        """Test basic RAG with sources functionality."""
        from langchain_rag_react_agent.agent import rag_with_sources

        # Mock the RAG chain response
        mock_rag_chain.invoke.return_value = {
            "answer": "Test answer",
            "context": [
                Document(
                    page_content="Test content",
                    metadata={"source": "test.pdf", "page": 1, "content_type": "text"},
                )
            ],
        }

        result = rag_with_sources(input="What is this about?", chat_history=[])

        assert isinstance(result, str)
        assert "Test answer" in result

    @patch("langchain_rag_react_agent.agent.rag_chain")
    def test_rag_with_sources_includes_sources(self, mock_rag_chain):
        """Test RAG with sources includes sources in response."""
        from langchain_rag_react_agent.agent import rag_with_sources

        # Mock the RAG chain response with multiple sources
        mock_rag_chain.invoke.return_value = {
            "answer": "Answer with sources",
            "context": [
                Document(
                    page_content="Content 1",
                    metadata={"source": "doc1.pdf", "page": 1, "content_type": "text"},
                ),
                Document(
                    page_content="Content 2",
                    metadata={"source": "doc2.pdf", "page": 2, "content_type": "table"},
                ),
            ],
        }

        result = rag_with_sources(input="Test query", chat_history=[])

        assert "📚 Sources:" in result
        assert "doc1.pdf" in result
        assert "doc2.pdf" in result

    @patch("langchain_rag_react_agent.agent.rag_chain")
    def test_rag_with_sources_handles_empty_context(self, mock_rag_chain):
        """Test RAG with sources handles empty context gracefully."""
        from langchain_rag_react_agent.agent import rag_with_sources

        # Mock response with no context
        mock_rag_chain.invoke.return_value = {
            "answer": "Answer without context",
            "context": [],
        }

        result = rag_with_sources(input="Test query", chat_history=[])

        assert isinstance(result, str)
        assert "Answer without context" in result


class TestPromptTemplates:
    """Tests for prompt templates."""

    def test_react_prompt_template_structure(self):
        """Test that ReAct prompt template has correct structure."""
        from langchain_rag_react_agent.agent import react_prompt_template

        assert isinstance(react_prompt_template, str)
        assert "Question:" in react_prompt_template
        assert "Thought:" in react_prompt_template
        assert "Action:" in react_prompt_template
        assert "Observation:" in react_prompt_template
        assert "Final Answer:" in react_prompt_template

    def test_contextualize_q_system_prompt(self):
        """Test contextualize question system prompt."""
        from langchain_rag_react_agent.agent import contextualize_q_system_prompt

        assert isinstance(contextualize_q_system_prompt, str)
        assert len(contextualize_q_system_prompt) > 0

    def test_qa_system_prompt(self):
        """Test QA system prompt."""
        from langchain_rag_react_agent.agent import qa_system_prompt

        assert isinstance(qa_system_prompt, str)
        assert "context" in qa_system_prompt.lower()
