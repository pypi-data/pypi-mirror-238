import uuid

def uid(length: int = 6) -> str:
    """Generate uuid"""

    return str(uuid.uuid4()).replace('-', '')[:length]
