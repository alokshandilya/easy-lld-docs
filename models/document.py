from datetime import datetime


class Document:
    def __init__(self, doc_id: int, owner_id: int, content: str):
        self.doc_id = doc_id
        self.owner_id = owner_id
        self.content = content
        self.created_at = datetime.now()
