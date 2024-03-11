from datetime import datetime
from hashlib import sha256


def create_unique_id(file_name: str, file_owner: str, file_owner_id: int) -> str:
    return str(hex(int(datetime.now().timestamp())))[2:] + sha256(f"{file_name}{file_owner}{file_owner_id}".encode(encoding="utf-8")).hexdigest()
    