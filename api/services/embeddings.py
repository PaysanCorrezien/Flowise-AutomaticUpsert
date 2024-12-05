from enum import Enum, auto
from typing import Dict, Any


class EmbeddingType(Enum):
    """Available embedding types in Flowise"""

    OPENAI = "openAIEmbeddings"
    HUGGINGFACE = "huggingFaceEmbeddings"
    COHERE = "cohereEmbeddings"
    AZURE_OPENAI = "azureOpenAIEmbeddings"
    GOOGLE_VERTEX = "googleVertexEmbeddings"
    # TODO: Add more embedding types as needed


class EmbeddingManager:
    """Manages embedding configurations"""

    def __init__(self, embedding_type: EmbeddingType, config: Dict[str, Any] = None):
        """
        Args:
            embedding_type: Type of embedding to use
            config: Configuration parameters for the embedding
        """
        self.embedding_type = embedding_type
        self.config = config or {}

    def get_config(self) -> Dict[str, Any]:
        """Get the embedding configuration for Flowise"""
        return {"name": self.embedding_type.value, "config": self.config}
