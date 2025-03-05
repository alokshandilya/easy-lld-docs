from models.document import Document
from models.user import User

owner = User(1, "Alok")
editor = User(2, "Aryan")
viewer = User(3, "Tridip")

print(owner.__dict__)
print(editor.__dict__)
print(viewer.__dict__)


doc = Document(1, 1, "Hello World")
print(doc.__dict__)
