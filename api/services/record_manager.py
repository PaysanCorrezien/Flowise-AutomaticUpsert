from enum import Enum
from typing import Dict, Any


class RecordManagerType(Enum):
    """Available record manager types in Flowise"""

    POSTGRES = "postgresRecordManager"
    REDIS = "redisRecordManager"
    MEMORY = "inMemoryRecordManager"
    FILE = "fileRecordManager"


class RecordManagerManager:
    """Manages record manager configurations"""

    def __init__(self, manager_type: RecordManagerType, config: Dict[str, Any] = None):
        """
        Args:
            manager_type: Type of record manager to use
            config: Configuration parameters for the record manager
        """
        self.manager_type = manager_type
        self.config = config or {}

    def get_config(self) -> Dict[str, Any]:
        """Get the record manager configuration for Flowise"""
        return {"name": self.manager_type.value, "config": self.config}
