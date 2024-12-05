from enum import Enum
from typing import Dict, Any


class VectorStoreType(Enum):
    """Available vector store types in Flowise"""

    PINECONE = "pinecone"
    QDRANT = "qdrant"
    CHROMA = "chroma"
    WEAVIATE = "weaviate"
    MILVUS = "milvus"
    REDIS = "redis"
    FAISS = "faiss"


# TODO: all all


class VectorStoreManager:
    """Manages vector store configurations"""

    def __init__(self, store_type: VectorStoreType, config: Dict[str, Any] = None):
        """
        Args:
            store_type: Type of vector store to use
            config: Configuration parameters for the vector store
        """
        self.store_type = store_type
        self.config = config or {"namespace": "default"}

    def get_config(self) -> Dict[str, Any]:
        """Get the vector store configuration for Flowise"""
        return {"name": self.store_type.value, "config": self.config}
