from datetime import datetime


class DocumentVersion:
    """
    This class represents a version of a document.

    Attributes:
    - version_number (int): The version number of the document.
    - content (str): The content of the document.
    - timestamp (datetime): The timestamp when the version was created.
    """

    def __init__(self, version_number: int, content: str):
        self.version_number: int = version_number
        self.content: str = content
        self.timestamp: datetime = datetime.now()
