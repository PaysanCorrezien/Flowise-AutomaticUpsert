from abc import ABC, abstractmethod
from typing import Dict, Any, Optional, List


class BaseTextSplitter(ABC):
    """Abstract base class for text splitters"""

    @abstractmethod
    def get_splitter_config(
        self, chunk_size: int, chunk_overlap: int
    ) -> Dict[str, Any]:
        """Return the splitter configuration for Flowise"""
        pass


class MarkdownTextSplitter(BaseTextSplitter):
    """Markdown-aware text splitter
    Tested and working with basic markdown documents"""

    def get_splitter_config(
        self, chunk_size: int, chunk_overlap: int
    ) -> Dict[str, Any]:
        return {
            "name": "markdownTextSplitter",
            "config": {"chunkSize": chunk_size, "chunkOverlap": chunk_overlap},
        }


class CharacterTextSplitter(BaseTextSplitter):
    """Basic character text splitter
    UNTESTED: Basic text splitting without special handling"""

    def get_splitter_config(
        self, chunk_size: int, chunk_overlap: int
    ) -> Dict[str, Any]:
        return {
            "name": "characterTextSplitter",
            "config": {"chunkSize": chunk_size, "chunkOverlap": chunk_overlap},
        }


class RecursiveCharacterSplitter(BaseTextSplitter):
    """Recursive character text splitter
    UNTESTED: Allows custom separators for more control over splitting"""

    def __init__(self, separators: Optional[List[str]] = None):
        self.separators = separators or ["\n\n", "\n", " ", ""]

    def get_splitter_config(
        self, chunk_size: int, chunk_overlap: int
    ) -> Dict[str, Any]:
        return {
            "name": "recursiveCharacterTextSplitter",
            "config": {
                "chunkSize": chunk_size,
                "chunkOverlap": chunk_overlap,
                "separators": self.separators,
            },
        }


class TokenTextSplitter(BaseTextSplitter):
    """Token-based text splitter
    UNTESTED: Uses specific tokenizer encodings for splitting"""

    def __init__(self, encoding_name: str = "gpt2"):
        """
        Args:
            encoding_name: Name of the tokenizer encoding
                         Options include: gpt2, r50k_base, p50k_base, etc.
        """
        self.encoding_name = encoding_name

    def get_splitter_config(
        self, chunk_size: int, chunk_overlap: int
    ) -> Dict[str, Any]:
        return {
            "name": "tokenTextSplitter",
            "config": {
                "chunkSize": chunk_size,
                "chunkOverlap": chunk_overlap,
                "encodingName": self.encoding_name,
            },
        }


class CodeTextSplitter(BaseTextSplitter):
    """Code-aware text splitter
    UNTESTED: Specifically for splitting code with language awareness"""

    def __init__(self, language: str = "python"):
        """
        Args:
            language: Programming language for splitting
                     Options include: python, javascript, java, cpp, etc.
        """
        self.language = language

    def get_splitter_config(
        self, chunk_size: int, chunk_overlap: int
    ) -> Dict[str, Any]:
        return {
            "name": "codeTextSplitter",
            "config": {
                "chunkSize": chunk_size,
                "chunkOverlap": chunk_overlap,
                "language": self.language,
            },
        }


class HtmlToMarkdownSplitter(BaseTextSplitter):
    """HTML to Markdown converter and splitter
    UNTESTED: Converts HTML to markdown before splitting"""

    def get_splitter_config(
        self, chunk_size: int, chunk_overlap: int
    ) -> Dict[str, Any]:
        return {
            "name": "htmlToMarkdownTextSplitter",
            "config": {"chunkSize": chunk_size, "chunkOverlap": chunk_overlap},
        }
