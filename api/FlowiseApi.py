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
        """Upsert a single document to Flowise"""
        try:
            url = f"{self.base_url}/document-store/upsert/{self.document_store_id}"

            # Prepare the complete payload with all required configurations
            payload = {
                "loader": {"name": self.document_loader, "config": {"text": content}},
                "splitter": {
                    "name": self.text_splitter,
                    "config": {
                        "chunkSize": self.chunk_size,
                        "chunkOverlap": self.chunk_overlap,
                        "separators": (
                            ["\n\n", "\n", " ", ""]
                            if self.text_splitter == "recursiveCharacterTextSplitter"
                            else None
                        ),
                    },
                },
                "embedding": {"name": self.embedding_name, "config": {}},
                "vectorStore": {
                    "name": self.vector_store_name,
                    "config": {"namespace": self.vector_store_namespace},
                },
                "recordManager": {"name": self.record_manager_name, "config": {}},
                "metadata": metadata,
            }

            # Clean up None values from config
            payload = self._clean_none_values(payload)

            # Debug logging
            logging.info("==== Request Details ====")
            logging.info(f"URL: {url}")
            logging.info(
                f"Headers: {json.dumps({k: '' if k == 'Authorization' else v for k, v in self.headers.items()})}"
            )
            logging.info(
                f"Payload: {json.dumps({k: v if k not in ['content', 'text'] else '...' for k, v in payload.items()}, indent=2)}"
            )
            logging.info("=====================")

            # Make the request
            response = requests.post(url, headers=self.headers, json=payload)
            response.raise_for_status()

            result = response.json()
            logging.info(f"Successfully upserted document: {file_path.name}")
            return result

        except requests.RequestException as e:
            logging.error(f"HTTP Error upserting document {file_path}: {str(e)}")
            if e.response is not None:
                logging.error(f"Response content: {e.response.text}")
            raise

    def _clean_none_values(self, d: Dict) -> Dict:
        """Recursively remove None values from dictionaries"""
        if not isinstance(d, dict):
            return d
        return {k: self._clean_none_values(v) for k, v in d.items() if v is not None}
