from exceptions import DocumentNotFoundError, PermissionDeniedError
from models.document import Document


class DocumentManager:
    def __init__(self, sharing_manager, version_manager):
        self.documents = {}
        self.sharing_manager = sharing_manager
        self.version_manager = version_manager
        self.next_doc_id = 1

    def create_document(self, owner, content: str) -> Document:
        doc_id = self.next_doc_id
        self.next_doc_id += 1
        doc = Document(doc_id, owner.user_id, content)
        self.documents[doc_id] = doc
        self.version_manager.save_version(doc_id, content)
        return doc

    def edit_document(self, user, doc_id: int, new_content: str):
        if doc_id not in self.documents:
            raise DocumentNotFoundError(f"Document {doc_id} not found")

        doc = self.documents[doc_id]
        if user.user_id != doc.owner_id:
            role = self.sharing_manager.get_role(doc_id, user.user_id)
            if role != "editor":
                raise PermissionDeniedError("Edit permission denied")

        doc.content = new_content
        self.version_manager.save_version(doc_id, new_content)

    def delete_document(self, user, doc_id: int):
        if doc_id not in self.documents:
            raise DocumentNotFoundError(f"Document {doc_id} not found")

        if user.user_id != self.documents[doc_id].owner_id:
            raise PermissionDeniedError("Delete permission denied")

        del self.documents[doc_id]
        self.sharing_manager.remove_document(doc_id)
        self.version_manager.remove_document(doc_id)

    def get_document_versions(self, user, doc_id: int):
        if doc_id not in self.documents:
            raise DocumentNotFoundError(f"Document {doc_id} not found")

        doc = self.documents[doc_id]
        role = self.sharing_manager.get_role(doc_id, user.user_id)

        if user.user_id != doc.owner_id and not role:
            raise PermissionDeniedError("View permission denied")

        versions = self.version_manager.get_versions(doc_id)
        return [versions[-1]] if role == "viewer" else versions

    def get_document(self, doc_id: int) -> Document:
        if doc_id not in self.documents:
            raise DocumentNotFoundError(f"Document {doc_id} not found")
        return self.documents[doc_id]
