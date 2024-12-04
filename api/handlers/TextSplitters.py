from abc import ABC, abstractmethod
from typing import Dict, Any


class BaseTextSplitter(ABC):
    """Abstract base class for text splitters"""

    @abstractmethod
    def get_splitter_config(
        self, chunk_size: int, chunk_overlap: int
    ) -> Dict[str, Any]:
        """Return the splitter configuration for Flowise"""
        pass


class MarkdownTextSplitter(BaseTextSplitter):
    """Markdown-aware text splitter"""

    def get_splitter_config(
        self, chunk_size: int, chunk_overlap: int
    ) -> Dict[str, Any]:
        return {
            "name": "markdownTextSplitter",
            "config": {"chunkSize": chunk_size, "chunkOverlap": chunk_overlap},
        }


class CharacterTextSplitter(BaseTextSplitter):
    """Basic character text splitter"""

    def get_splitter_config(
        self, chunk_size: int, chunk_overlap: int
    ) -> Dict[str, Any]:
        return {
            "name": "characterTextSplitter",
            "config": {"chunkSize": chunk_size, "chunkOverlap": chunk_overlap},
        }


class RecursiveCharacterSplitter(BaseTextSplitter):
    """Recursive character text splitter"""

    def get_splitter_config(
        self, chunk_size: int, chunk_overlap: int
    ) -> Dict[str, Any]:
        return {
            "name": "recursiveCharacterTextSplitter",
            "config": {
                "chunkSize": chunk_size,
                "chunkOverlap": chunk_overlap,
                "separators": ["\n\n", "\n", " ", ""],
            },
        }


class TokenTextSplitter(BaseTextSplitter):
    """Token-based text splitter"""

    def get_splitter_config(
        self, chunk_size: int, chunk_overlap: int
    ) -> Dict[str, Any]:
        return {
            "name": "tokenTextSplitter",
            "config": {"chunkSize": chunk_size, "chunkOverlap": chunk_overlap},
        }


class HtmlToMarkdownSplitter(BaseTextSplitter):
    """HTML to Markdown converter and splitter"""

    def get_splitter_config(
        self, chunk_size: int, chunk_overlap: int
    ) -> Dict[str, Any]:
        return {
            "name": "htmlToMarkdownTextSplitter",
            "config": {"chunkSize": chunk_size, "chunkOverlap": chunk_overlap},
        }


class CodeTextSplitter(BaseTextSplitter):
    """Code-aware text splitter"""

    def get_splitter_config(
        self, chunk_size: int, chunk_overlap: int
    ) -> Dict[str, Any]:
        return {
            "name": "codeTextSplitter",
            "config": {"chunkSize": chunk_size, "chunkOverlap": chunk_overlap},
        }
