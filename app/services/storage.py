import os
from uuid import uuid4
from app.config import settings

class LocalStorage:
    def __init__(self, base_dir: str):
        self.base_dir = base_dir
        os.makedirs(self.base_dir, exist_ok=True)

    # generate unique filename to avoid collisions
    # todo maybe change to id instead
    def save_file(self, file, filename: str) -> str:
        extention = os.path.splitext(filename)[1]
        unique_name = f"{uuid4()}{extention}"
        file_path = os.path.join(self.base_dir, unique_name)

        with open(file_path, "wb") as f:
            f.write(file.read())

        return file_path

# saving logic separeted to a "service":
# 1. can be reused in other saving file needs in the future
# 2. can be swapped from local store to S3Storage with same save_file interface,
#    seamless change with minimal changes to main app logic code