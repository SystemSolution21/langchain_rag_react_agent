"""Tests for the RAG module."""

import json
from unittest.mock import MagicMock, patch

from langchain_core.documents.base import Document

from langchain_rag_react_agent.rag import (
    TableAwareTextSplitter,
    create_advanced_text_chunks,
    create_multimodal_embeddings,
    create_table_specific_chunks,
    detect_pdf_changes,
    extract_charts_and_graphs,
    extract_text_with_ocr,
    generate_sample_questions,
    load_pdf_documents_advanced,
    save_pdf_metadata,
)


class TestTableAwareTextSplitter:
    """Tests for TableAwareTextSplitter class."""

    def test_init(self):
        """Test TableAwareTextSplitter initialization."""
        splitter = TableAwareTextSplitter(chunk_size=500, chunk_overlap=100)
        assert splitter.chunk_size == 500
        assert splitter.chunk_overlap == 100
        assert splitter.base_splitter is not None

    def test_split_documents_with_table(self):
        """Test splitting documents containing tables."""
        splitter = TableAwareTextSplitter(chunk_size=100, chunk_overlap=20)
        docs = [
            Document(
                page_content="Table 1: Test Data\n| A | B |\n| 1 | 2 |",
                metadata={"source": "test.pdf"},
            )
        ]
        chunks = splitter.split_documents(docs)
        # Just verify it returns a list and doesn't crash
        assert isinstance(chunks, list)

    def test_split_documents_without_table(self):
        """Test splitting regular documents."""
        splitter = TableAwareTextSplitter(chunk_size=50, chunk_overlap=10)
        docs = [
            Document(
                page_content="This is a regular document without tables. " * 10,
                metadata={"source": "test.pdf"},
            )
        ]
        chunks = splitter.split_documents(docs)
        assert len(chunks) > 0


class TestCreateAdvancedTextChunks:
    """Tests for create_advanced_text_chunks function."""

    def test_create_chunks_from_documents(self, sample_documents):
        """Test creating chunks from sample documents."""
        chunks = create_advanced_text_chunks(
            documents=sample_documents, chunk_size=100, chunk_overlap=20
        )
        assert len(chunks) > 0
        assert all(isinstance(chunk, Document) for chunk in chunks)

    def test_create_chunks_preserves_metadata(self, sample_documents):
        """Test that chunking preserves document metadata."""
        chunks = create_advanced_text_chunks(
            documents=sample_documents, chunk_size=100, chunk_overlap=20
        )
        for chunk in chunks:
            assert "source" in chunk.metadata


class TestCreateTableSpecificChunks:
    """Tests for create_table_specific_chunks function."""

    def test_enhance_chunks_with_context(self):
        """Test enhancing chunks with content-type context."""
        docs = [
            Document(
                page_content="Regular text",
                metadata={"source": "test.pdf", "content_type": "text"},
            ),
            Document(
                page_content="Table data",
                metadata={"source": "test.pdf", "content_type": "table"},
            ),
        ]
        enhanced = create_table_specific_chunks(docs)
        assert len(enhanced) > 0
        assert all(isinstance(chunk, Document) for chunk in enhanced)


class TestCreateMultimodalEmbeddings:
    """Tests for create_multimodal_embeddings function."""

    @patch("langchain_rag_react_agent.rag.HuggingFaceEmbeddings")
    def test_creates_embeddings(self, mock_embeddings):
        """Test that embeddings are created."""
        mock_instance = MagicMock()
        mock_embeddings.return_value = mock_instance

        result = create_multimodal_embeddings()

        mock_embeddings.assert_called_once()
        assert result == mock_instance

    @patch("langchain_rag_react_agent.rag.HuggingFaceEmbeddings")
    def test_uses_correct_model(self, mock_embeddings):
        """Test that correct model is used."""
        create_multimodal_embeddings()

        call_kwargs = mock_embeddings.call_args[1]
        assert call_kwargs["model_name"] == "BAAI/bge-large-en-v1.5"
        assert call_kwargs["model_kwargs"]["device"] == "cpu"
        assert call_kwargs["encode_kwargs"]["normalize_embeddings"] is True


class TestLoadPdfDocumentsAdvanced:
    """Tests for load_pdf_documents_advanced function."""

    def test_load_from_empty_directory(self, mock_pdfs_dir):
        """Test loading from empty directory."""
        docs = load_pdf_documents_advanced(pdfs_dir=mock_pdfs_dir)
        assert docs == []

    def test_load_from_directory_with_pdf(self, create_test_pdf):
        """Test loading from directory with PDF files."""
        pdf_path = create_test_pdf("test.pdf")
        docs = load_pdf_documents_advanced(pdfs_dir=pdf_path.parent)
        # May return empty list if PDF parsing fails, but should not raise error
        assert isinstance(docs, list)

    def test_handles_nonexistent_directory(self, temp_dir):
        """Test handling of nonexistent directory."""
        nonexistent = temp_dir / "nonexistent"
        docs = load_pdf_documents_advanced(pdfs_dir=nonexistent)
        assert docs == []


class TestExtractTextWithOcr:
    """Tests for extract_text_with_ocr function."""

    @patch("langchain_rag_react_agent.rag.fitz")
    def test_extract_ocr_no_images(self, mock_fitz, create_test_pdf):
        """Test OCR extraction when PDF has no images."""
        pdf_path = create_test_pdf("test.pdf")

        # Mock PyMuPDF document with no images
        mock_doc = MagicMock()
        mock_page = MagicMock()
        mock_page.get_images.return_value = []
        mock_doc.__getitem__.return_value = mock_page
        mock_doc.page_count = 1
        mock_fitz.open.return_value = mock_doc

        docs = extract_text_with_ocr(pdf_path=str(pdf_path))

        assert isinstance(docs, list)
        assert len(docs) == 0  # No images, no OCR documents

    @patch("langchain_rag_react_agent.rag.fitz")
    def test_extract_ocr_handles_errors(self, mock_fitz):
        """Test that OCR extraction handles errors gracefully."""
        mock_fitz.open.side_effect = Exception("PDF error")

        docs = extract_text_with_ocr(pdf_path="nonexistent.pdf")

        assert isinstance(docs, list)
        assert len(docs) == 0


class TestExtractChartsAndGraphs:
    """Tests for extract_charts_and_graphs function."""

    @patch("langchain_rag_react_agent.rag.fitz")
    def test_extract_charts_basic(self, mock_fitz, create_test_pdf):
        """Test basic chart extraction."""
        pdf_path = create_test_pdf("test.pdf")

        # Mock PyMuPDF document
        mock_doc = MagicMock()
        mock_page = MagicMock()
        mock_page.get_images.return_value = []
        mock_doc.__getitem__.return_value = mock_page
        mock_doc.page_count = 1
        mock_fitz.open.return_value = mock_doc

        docs = extract_charts_and_graphs(pdf_path=str(pdf_path))

        assert isinstance(docs, list)

    @patch("langchain_rag_react_agent.rag.fitz")
    def test_extract_charts_handles_errors(self, mock_fitz):
        """Test that chart extraction handles errors gracefully."""
        mock_fitz.open.side_effect = Exception("PDF error")

        docs = extract_charts_and_graphs(pdf_path="nonexistent.pdf")

        assert isinstance(docs, list)


class TestPdfMetadata:
    """Tests for PDF metadata functions."""

    def test_save_and_load_pdf_metadata(self, mock_pdfs_dir, mock_db_dir, create_test_pdf):
        """Test saving and loading PDF metadata."""
        create_test_pdf("test.pdf")
        persistent_dir = mock_db_dir / "chroma_db"
        persistent_dir.mkdir(parents=True, exist_ok=True)

        save_pdf_metadata(pdfs_dir=mock_pdfs_dir, persistent_directory=persistent_dir)

        metadata_file = persistent_dir.parent / f"{persistent_dir.name}_metadata.json"
        assert metadata_file.exists()

        with open(metadata_file, "r") as f:
            metadata = json.load(f)
        assert isinstance(metadata, dict)
        assert "pdf_files" in metadata
        assert "test.pdf" in metadata["pdf_files"]

    def test_detect_pdf_changes_new_file(self, mock_pdfs_dir, mock_db_dir, create_test_pdf):
        """Test detecting new PDF file."""
        persistent_dir = mock_db_dir / "chroma_db"
        persistent_dir.mkdir(parents=True, exist_ok=True)

        # Save initial empty metadata
        save_pdf_metadata(pdfs_dir=mock_pdfs_dir, persistent_directory=persistent_dir)

        # Add a new file
        create_test_pdf("new.pdf")

        added, deleted = detect_pdf_changes(
            pdfs_dir=mock_pdfs_dir, persistent_directory=persistent_dir
        )

        assert "new.pdf" in added
        assert len(deleted) == 0

    def test_detect_pdf_changes_deleted_file(self, mock_pdfs_dir, mock_db_dir, create_test_pdf):
        """Test detecting deleted PDF file."""
        persistent_dir = mock_db_dir / "chroma_db"
        persistent_dir.mkdir(parents=True, exist_ok=True)

        # Create and save metadata with a file
        pdf_path = create_test_pdf("test.pdf")
        save_pdf_metadata(pdfs_dir=mock_pdfs_dir, persistent_directory=persistent_dir)

        # Delete the file
        pdf_path.unlink()

        added, deleted = detect_pdf_changes(
            pdfs_dir=mock_pdfs_dir, persistent_directory=persistent_dir
        )

        assert len(added) == 0
        assert "test.pdf" in deleted


class TestGenerateSampleQuestions:
    """Tests for generate_sample_questions function."""

    @patch("langchain_rag_react_agent.rag.Chroma")
    def test_generate_questions_basic(self, mock_chroma):
        """Test basic question generation."""
        # Mock Chroma instance
        mock_db = MagicMock()
        mock_db.similarity_search.return_value = [
            Document(
                page_content="Neural networks are a type of machine learning model.",
                metadata={"source": "test.pdf"},
            ),
            Document(
                page_content="Transformers use attention mechanisms.",
                metadata={"source": "test.pdf"},
            ),
        ]

        questions = generate_sample_questions(db=mock_db, num_questions=3)

        assert isinstance(questions, list)
        assert len(questions) == 3
        assert all(isinstance(q, str) for q in questions)

    @patch("langchain_rag_react_agent.rag.Chroma")
    def test_generate_questions_no_documents(self, mock_chroma):
        """Test question generation with no documents."""
        mock_db = MagicMock()
        mock_db.similarity_search.return_value = []

        questions = generate_sample_questions(db=mock_db, num_questions=5)

        assert isinstance(questions, list)
        assert len(questions) > 0  # Should return default questions

    @patch("langchain_rag_react_agent.rag.Chroma")
    def test_generate_questions_handles_errors(self, mock_chroma):
        """Test that question generation handles errors gracefully."""
        mock_db = MagicMock()
        mock_db.similarity_search.side_effect = Exception("DB error")

        questions = generate_sample_questions(db=mock_db, num_questions=3)

        assert isinstance(questions, list)
        assert len(questions) > 0  # Should return fallback questions
