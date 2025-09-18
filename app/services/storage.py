import os
from pathlib import Path
from datetime import datetime, timezone

class LocalStorage:
    def __init__(self, base_dir: str):
        self.base_dir = base_dir
        os.makedirs(self.base_dir, exist_ok=True)

    # generate unique filename to avoid collisions
    # use upload time as distinction
    # todo maybe change to id instead
    def save_file(self, file, filename: str) -> str:
        name, extention = filename.rsplit('.', 1)
        ts = datetime.now(timezone.utc).strftime("%Y%m%d%H%M%S%f")
        unique_name = f"{name}-{ts}.{extention}"
        file_path = Path(self.base_dir) / unique_name

        with open(file_path, "wb") as f:
            f.write(file.read())

        return file_path.as_posix()

# saving logic separeted to a "service":
# 1. can be reused in other saving file needs in the future
# 2. can be swapped from local store to S3Storage with same save_file interface,
#    seamless change with minimal changes to main app logic code