from datetime import datetime


class User:
    def __init__(self, user_id: int, name: str):
        self.user_id = user_id
        self.name = name


# Create users
owner = User(1, "Alok")
editor = User(2, "Lalit")
viewer = User(3, "Tridip")

print(owner.__dict__)
print(editor.__dict__)
print(viewer.__dict__)


class Document:
    def __init__(self, doc_id: int, owner_id: int, content: str):
        self.doc_id = doc_id
        self.owner_id = owner_id
        self.content = content
        self.created_at = datetime.now()


doc = Document(1, 1, "Hello World")
print(doc.__dict__)
