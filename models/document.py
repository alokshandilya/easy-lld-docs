from datetime import datetime


class Document:
    """
    This class represents a document.

    Attributes:
    - doc_id (int): The unique id of the document.
    - owner_id (int): The user id of the owner of the document.
    - content (str): The content of the document.
    """

    def __init__(self, doc_id: int, owner_id: int, content: str):
        self.doc_id: int = doc_id
        self.owner_id: int = owner_id
        self.content: str = content
        self.created_at: datetime = datetime.now()
