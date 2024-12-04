from pathlib import Path
import time
from typing import List, Optional
import logging


class DocumentFinder:
    """Handles document discovery and filtering based on modification time"""

    def __init__(
        self,
        watch_directory: str,
        file_patterns: List[str],
        exclude_patterns: Optional[List[str]] = None,
        max_file_size: Optional[int] = None,
    ):
        self.watch_directory = Path(watch_directory)
        self.file_patterns = file_patterns
        self.exclude_patterns = exclude_patterns or []
        self.max_file_size = max_file_size

        if not self.watch_directory.exists():
            raise ValueError(f"Watch directory does not exist: {watch_directory}")

        logging.info(f"Initialized DocumentFinder:")
        logging.info(f"- Watch directory: {watch_directory}")
        logging.info(f"- File patterns: {file_patterns}")
        logging.info(f"- Exclude patterns: {exclude_patterns}")
        logging.info(f"- Max file size: {max_file_size} bytes")

    def should_process_file(self, file_path: Path) -> bool:
        """Check if a file should be processed based on exclusion rules and size"""
        # Check exclusion patterns
        for pattern in self.exclude_patterns:
            if file_path.match(pattern):
                logging.debug(f"Skipping excluded file: {file_path}")
                return False

        # Check file size
        if self.max_file_size and file_path.stat().st_size > self.max_file_size:
            logging.warning(f"Skipping file exceeding size limit: {file_path}")
            return False

        return True

    def get_recent_files(self, hours: int = 24) -> List[Path]:
        """Get files modified within the specified hours"""
        cutoff_time = time.time() - (hours * 3600)
        recent_files = []

        for pattern in self.file_patterns:
            for file_path in self.watch_directory.rglob(pattern):
                try:
                    if (
                        file_path.is_file()
                        and file_path.stat().st_mtime > cutoff_time
                        and self.should_process_file(file_path)
                    ):

                        recent_files.append(file_path)
                        logging.debug(f"Found recent file: {file_path}")
                except Exception as e:
                    logging.error(f"Error accessing file {file_path}: {str(e)}")
                    continue

        logging.info(f"Found {len(recent_files)} recent files")
        return recent_files
