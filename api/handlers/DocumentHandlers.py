from abc import ABC, abstractmethod
from pathlib import Path
from typing import Dict, Any


class BaseDocumentHandler(ABC):
    """Abstract base class for document type handlers"""

    @abstractmethod
    def get_loader_config(self, content: str) -> Dict[str, Any]:
        """Return the loader configuration with content for Flowise"""
        pass

    @abstractmethod
    def supported_extensions(self) -> list[str]:
        """Return list of supported file extensions"""
        pass


class MarkdownHandler(BaseDocumentHandler):
    """Handles Markdown documents"""

    def get_loader_config(self, content: str) -> Dict[str, Any]:
        return {"name": "plainText", "config": {"text": content}}

    def supported_extensions(self) -> list[str]:
        return [".md"]


class TextHandler(BaseDocumentHandler):
    """Handles plain text documents"""

    def get_loader_config(self, content: str) -> Dict[str, Any]:
        return {"name": "plainText", "config": {"text": content}}

    def supported_extensions(self) -> list[str]:
        return [".txt"]
