from datetime import datetime, date
from pathlib import Path
from typing import Dict, Tuple
import yaml
import logging


class FrontmatterProcessor:
    """Handles extraction and processing of document frontmatter"""

    EXPECTED_FIELDS = {
        "referent": str,
        "titre": str,
        "categorie": str,
        "date_modification": (str, datetime, date),  # Accept string or date objects
        "date_creation": (str, datetime, date),  # Accept string or date objects
        "complexite": str,
        "version": (int, str),
        "lien": list,
        "url": str,
        "permission": str,
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
                    # Handle different date types
                    if isinstance(validated_metadata[date_field], (datetime, date)):
                        date_value = validated_metadata[date_field]
                    else:
                        date_value = datetime.strptime(
                            validated_metadata[date_field], "%Y-%m-%d"
                        )

                    # Convert to ISO format string
                    if isinstance(date_value, datetime):
                        validated_metadata[date_field] = date_value.date().isoformat()
                    else:  # date object
                        validated_metadata[date_field] = date_value.isoformat()

                except ValueError as e:
                    logging.error(f"Could not parse {date_field}: {e}")

        # Handle paths
        if validated_metadata.get("url"):
            validated_metadata["url"] = self.normalize_windows_path(
                validated_metadata["url"]
            )

        # Add system metadata
        validated_metadata.update(
            {
                "source_file": file_path.name,
                "file_path": self.normalize_windows_path(str(file_path.absolute())),
                "processing_date": datetime.now().isoformat(),
            }
        )

        logging.info(f"Processed metadata for {file_path.name}")
        return validated_metadata
