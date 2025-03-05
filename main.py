from models.document import Document
from models.user import User
from models.version import DocumentVersion

owner = User(1, "Alok")
editor = User(2, "Aryan")
viewer = User(3, "Tridip")

print(owner.__dict__)
print(editor.__dict__)
print(viewer.__dict__)


doc = Document(1, 1, "Hello World")
print(doc.__dict__)

v1 = DocumentVersion(1, "Namaste World")
print(v1.__dict__)
