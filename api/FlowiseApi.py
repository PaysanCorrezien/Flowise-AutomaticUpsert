import os
import json
from pathlib import Path
from typing import Dict
import requests
import logging


class FlowiseUpserter:
    """Handles document upserting to Flowise API"""

    def __init__(self):
        self.base_url = os.getenv("FLOWISE_API_URL")
        self.api_key = os.getenv("FLOWISE_API_KEY")
        self.document_store_id = os.getenv("DOCUMENT_STORE_ID")

        # Document processing settings
        self.chunk_size = int(os.getenv("CHUNK_SIZE", "2000"))
        self.chunk_overlap = int(os.getenv("CHUNK_OVERLAP", "400"))
        self.document_loader = os.getenv("DOCUMENT_LOADER", "plainText")
        self.text_splitter = os.getenv("TEXT_SPLITTER", "markdownTextSplitter")

        # Vector store and embedding settings
        self.vector_store_name = os.getenv("VECTOR_STORE_NAME", "pinecone")
        self.vector_store_namespace = os.getenv("VECTOR_STORE_NAMESPACE", "default")
        self.embedding_name = os.getenv("EMBEDDING_NAME", "openAIEmbeddings")
        self.record_manager_name = os.getenv(
            "RECORD_MANAGER_NAME", "postgresRecordManager"
        )

        if not all([self.base_url, self.api_key, self.document_store_id]):
            raise ValueError(
                "Missing required Flowise configuration in environment variables"
            )

        self.headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
        }

    def upsert_document(self, file_path: Path, content: str, metadata: Dict) -> Dict:
        try:
            # Use upsert endpoint for both new and existing documents
            url = f"{self.base_url}/document-store/upsert/{self.document_store_id}"

            config = {
                "loader": {"name": "plainText", "config": {"text": content}},
                "splitter": {"name": "recursiveCharacterTextSplitter", "config": {}},
                "embedding": {
                    "name": "openAIEmbeddings",
                    "config": {"openAIApiKey": os.getenv("OPENAI_API_KEY", "")},
                },
                "vectorStore": {"name": "pinecone", "config": {"namespace": "default"}},
                "recordManager": {"name": "postgresRecordManager", "config": {}},
                "metadata": metadata,
            }

            headers = {
                "Authorization": f"Bearer {self.api_key}",
                "Content-Type": "application/json",
            }

            logging.info(f"Request payload: {json.dumps(config, indent=2)}")
            response = requests.post(url, headers=headers, json=config)

            if response.status_code != 200:
                logging.error(f"Response content: {response.text}")
            response.raise_for_status()

            result = response.json()
            logging.info(f"Response result: {json.dumps(result, indent=2)}")

            return result

        except requests.RequestException as e:
            if e.response is not None:
                logging.error(f"Response content: {e.response.text}")
            raise

    def _clean_none_values(self, d: Dict) -> Dict:
        """Recursively remove None values from dictionaries"""
        if not isinstance(d, dict):
            return d
        return {k: self._clean_none_values(v) for k, v in d.items() if v is not None}
