from datetime import datetime, date
from pathlib import Path
from typing import Dict, Tuple
import yaml
import logging
import urllib.parse


class FrontmatterProcessor:
    """Handles extraction and processing of document frontmatter"""

    EXPECTED_FIELDS = {
        "referent": str,
        "titre": str,
        "categorie": str,
        "date_modification": (str, datetime, date),
        "date_creation": (str, datetime, date),
        "complexite": str,
        "version": (int, str),
        "lien": list,
        "url": str,
        "permission": str,
        "doc_id": str,
    }

    @staticmethod
    def extract_frontmatter(content: str) -> Tuple[Dict, str]:
        """Extract YAML frontmatter from document content"""
        if content.startswith("---"):
            parts = content.split("---", 2)[1:]
            if len(parts) >= 2:
                try:
                    metadata = yaml.safe_load(parts[0])
                    content = parts[1].strip()
                    logging.debug("Successfully extracted frontmatter")
                    return metadata, content
                except yaml.YAMLError as e:
                    logging.error(f"Error parsing frontmatter: {e}")
        return {}, content

    @staticmethod
    def normalize_windows_path(path: str) -> str:
        """Convert any path to Windows-style path"""
        normalized = path.replace("/", "\\")
        if normalized.startswith("\\\\"):
            normalized = "\\\\" + normalized.lstrip("\\")
        logging.debug(f"Normalized path: {path} -> {normalized}")
        return normalized

    def prepare_source_metadata(self, url: str, file_path: Path) -> Dict:
        """Prepare source metadata in Flowise format"""
        normalized_url = self.normalize_windows_path(url)
        source_url = urllib.parse.quote(normalized_url, safe="/:")

        return {
            "sourceDocument": {
                "pageContent": "",
                "metadata": {
                    "source": source_url,
                    "filename": file_path.name,
                    "filePath": self.normalize_windows_path(str(file_path.absolute())),
                    "loc": {"lines": {"from": 1, "to": 1}},
                },
            }
        }

    def validate_frontmatter(self, metadata: Dict) -> Dict[str, str]:
        """Validate and standardize frontmatter fields"""
        validated = {}

        for field, expected_type in self.EXPECTED_FIELDS.items():
            value = metadata.get(field)
            if value is not None:
                if isinstance(expected_type, tuple):
                    if not isinstance(value, expected_type):
                        logging.warning(
                            f"{field} has unexpected type {type(value)}, expected one of {expected_type}"
                        )
                        value = str(value)
                elif not isinstance(value, expected_type):
                    logging.warning(
                        f"{field} has unexpected type {type(value)}, expected {expected_type}"
                    )
                    if expected_type == str:
                        value = str(value)
                    elif expected_type == list and value == "[]":
                        value = []
            else:
                logging.warning(f"Missing expected field: {field}")

            validated[field] = value

        return validated

    def process_metadata(self, metadata: Dict, file_path: Path) -> Dict:
        """Process and enhance metadata with file information"""
        validated_metadata = self.validate_frontmatter(metadata)

        # Process dates
        for date_field in ["date_modification", "date_creation"]:
            if validated_metadata.get(date_field):
                try:
                    value = validated_metadata[date_field]
                    if isinstance(value, datetime):
                        validated_metadata[date_field] = value.date().isoformat()
                    elif isinstance(value, date):
                        validated_metadata[date_field] = value.isoformat()
                    else:  # It's a string
                        parsed_date = datetime.strptime(value, "%Y-%m-%d").date()
                        validated_metadata[date_field] = parsed_date.isoformat()
                except ValueError as e:
                    logging.error(f"Could not parse {date_field}: {e}")

        # Extract source from URL if present
        if validated_metadata.get("url"):
            processed_metadata = {
                "source": validated_metadata.pop("url")  # Remove url and use as source
            }
        else:
            processed_metadata = {}

        # Add all other metadata fields directly
        processed_metadata.update(validated_metadata)

        return processed_metadata
