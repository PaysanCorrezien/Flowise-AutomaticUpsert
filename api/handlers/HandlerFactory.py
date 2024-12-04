from pathlib import Path
import logging
from typing import Tuple
from .DocumentHandlers import (
    BaseDocumentHandler,
    MarkdownHandler,
    TextHandler,
    DocxHandler,
)
from .TextSplitters import (
    BaseTextSplitter,
    RecursiveCharacterSplitter,
    MarkdownSplitter,
)


class HandlerFactory:
    """Factory for creating appropriate document handlers and text splitters"""

    def __init__(self):
        # Initialize document handlers
        self.handlers = {}
        self._initialize_handlers()

        # Initialize text splitters with default configurations
        self.default_splitter = RecursiveCharacterSplitter()
        self.splitters = {
            ".md": MarkdownSplitter(),  # Use markdown splitter for .md files
            # Add more specific splitter mappings as needed
        }

    def _initialize_handlers(self):
        """Initialize all document handlers with their supported extensions"""
        handler_classes = [MarkdownHandler, TextHandler, DocxHandler]

        for handler_class in handler_classes:
            handler = handler_class()
            for extension in handler.supported_extensions():
                self.handlers[extension] = handler
            logging.debug(
                f"Initialized {handler_class.__name__} for extensions: {handler.supported_extensions()}"
            )

    def get_handlers(
        self, file_path: Path
    ) -> Tuple[BaseDocumentHandler, BaseTextSplitter]:
        """Get appropriate handlers for the file type"""
        extension = file_path.suffix.lower()

        # Find document handler
        document_handler = self.handlers.get(extension)
        if not document_handler:
            raise ValueError(
                f"No suitable document handler found for file type: {extension}"
            )

        logging.debug(f"Using {document_handler.__class__.__name__} for {file_path}")

        # Get text splitter (use specific if available, otherwise default)
        text_splitter = self.splitters.get(extension, self.default_splitter)
        logging.debug(f"Using {text_splitter.__class__.__name__} for {file_path}")

        return document_handler, text_splitter

    def get_supported_extensions(self) -> list[str]:
        """Get list of all supported file extensions"""
        return list(self.handlers.keys())
