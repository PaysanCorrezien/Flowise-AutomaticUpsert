import os
import sys
import logging
from pathlib import Path
from dotenv import load_dotenv
from watcher.Documents import DocumentFinder
from data.FrontmatterProcess import FrontmatterProcessor
from api.FlowiseApi import FlowiseUpserter


def validate_env():
    """Validate required environment variables"""
    required_vars = {
        "WATCH_DIRECTORY": "Directory to watch for documents",
        "FLOWISE_API_URL": "Flowise API URL",
        "FLOWISE_API_KEY": "Flowise API Key",
        "DOCUMENT_STORE_ID": "Document Store ID",
    }

    missing = []
    for var, description in required_vars.items():
        if not os.getenv(var):
            missing.append(f"{var} ({description})")

    if missing:
        raise ValueError(
            f"Missing required environment variables:\n" + "\n".join(missing)
        )


def setup_logging():
    """Configure logging settings"""
    log_level = os.getenv("LOG_LEVEL", "INFO")
    log_file = os.getenv("LOG_FILE", "document_processor.log")

    level = getattr(logging, log_level.upper(), logging.INFO)

    logging.basicConfig(
        level=level,
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        handlers=[logging.FileHandler(log_file), logging.StreamHandler()],
    )


def main():
    try:
        # Load and validate environment variables
        load_dotenv()
        validate_env()

        # Setup logging
        setup_logging()
        logging.info("Starting document processing")

        # Get configuration from environment
        watch_directory = os.getenv("WATCH_DIRECTORY")
        if not watch_directory:
            raise ValueError("WATCH_DIRECTORY environment variable is required")

        file_patterns = os.getenv("FILE_PATTERNS", "*.md,*.docx,*.txt").split(",")
        hours_lookback = int(os.getenv("HOURS_LOOKBACK", "24"))
        exclude_patterns = os.getenv("EXCLUDE_PATTERNS", "*.tmp,~*").split(",")
        max_file_size = int(os.getenv("MAX_FILE_SIZE", "10485760"))  # 10MB default

        logging.info(f"Configuration loaded:")
        logging.info(f"Watch directory: {watch_directory}")
        logging.info(f"File patterns: {file_patterns}")
        logging.info(f"Exclude patterns: {exclude_patterns}")
        logging.info(f"Hours lookback: {hours_lookback}")
        logging.info(f"Max file size: {max_file_size} bytes")

        try:
            # Initialize components
            document_finder = DocumentFinder(
                watch_directory=watch_directory,
                file_patterns=file_patterns,
                exclude_patterns=exclude_patterns,
                max_file_size=max_file_size,
            )
            frontmatter_processor = FrontmatterProcessor()
            flowise_upserter = FlowiseUpserter()

            # Get recent files
            recent_files = document_finder.get_recent_files(hours_lookback)
            logging.info(
                f"Found {len(recent_files)} files modified in the last {hours_lookback} hours"
            )

            # Process each file
            for file_path in recent_files:
                try:
                    # Read file content
                    content = file_path.read_text(encoding="utf-8")
                    logging.debug(f"Processing file: {file_path}")

                    # Extract and process frontmatter
                    metadata, clean_content = frontmatter_processor.extract_frontmatter(
                        content
                    )
                    processed_metadata = frontmatter_processor.process_metadata(
                        metadata, file_path
                    )

                    # Upsert document
                    result = flowise_upserter.upsert_document(
                        file_path, clean_content, processed_metadata
                    )
                    logging.info(f"Successfully processed {file_path}")
                    logging.debug(f"Upsert result: {result}")

                except Exception as e:
                    logging.error(f"Error processing {file_path}: {str(e)}")
                    continue

        except Exception as e:
            logging.error(f"Error in document processing: {str(e)}")
            raise

    except Exception as e:
        logging.error(f"Critical error in main process: {str(e)}")
        sys.exit(1)


if __name__ == "__main__":
    main()
