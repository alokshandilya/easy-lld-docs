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
        self.doc_id = doc_id
        self.owner_id = owner_id
        self.content = content
        self.created_at = datetime.now()
