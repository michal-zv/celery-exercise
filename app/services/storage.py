import os
from pathlib import Path
import re
from uuid import UUID
import logging

logger = logging.getLogger(__name__)

class LocalStorage:
    def __init__(self, base_dir: str):
        self.base_dir = base_dir
        os.makedirs(self.base_dir, exist_ok=True)

    # create unique filename to avoid collisions 
    # use file_id to be recognizable in filesystem or on debug
    def save_file(self, file, filename: str, file_id: UUID) -> str:
        clean_name = re.sub(r"[^\w\-_\.]", "_", filename)
        unique_name = f"{file_id}-{clean_name}"
        file_path = Path(self.base_dir) / unique_name

        try:
            with open(file_path, "wb") as f:
                data = file.read()
                f.write(file.read())
            logger.debug(f"Saved file {file_path} ({len(data)} bytes)")
            return file_path.as_posix()
        
        except Exception as e:
            logger.error(f"Failed to save file {file_path}: {e}")
            raise

# saving logic separeted to a "service":
# 1. can be reused in other saving file needs in the future
# 2. can be swapped from local store to S3Storage with same save_file interface,
#    seamless change with minimal changes to main app logic code