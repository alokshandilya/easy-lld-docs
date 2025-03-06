from typing import TYPE_CHECKING, Dict, Optional

from exceptions import DocumentNotFoundError, PermissionDeniedError

if TYPE_CHECKING:
    from managers.document_manager import DocumentManager


class SharingManager:
    def __init__(self, doc_manager: "DocumentManager"):
        self.shared_with: Dict[int, Dict[int, str]] = {}
        self.doc_manager: DocumentManager = doc_manager

    def share_document(self, doc_id: int, user_id: int, role: str) -> None:
        """
        Share a document with a user, assigning them a specific role.
        Valid roles are 'viewer' and 'editor'.
        """
        if role not in ["viewer", "editor"]:
            raise ValueError(f"Invalid role: {role}. Choose 'viewer' or 'editor'")

        if doc_id not in self.shared_with:
            self.shared_with[doc_id] = {}
        self.shared_with[doc_id][user_id] = role

    def remove_role(self, doc_id: int, owner_id: int, user_id: int) -> None:
        """
        Remove a user's role for a document. Only the owner can perform this action.
        """
        if doc_id not in self.shared_with:
            raise DocumentNotFoundError(f"Document {doc_id} not found")

        # check if the requester is the owner
        doc = self.doc_manager.get_document(doc_id)
        if owner_id != doc.owner_id:
            raise PermissionDeniedError("Only the owner can remove roles.")

        # remove user from the shared list
        if user_id in self.shared_with[doc_id]:
            del self.shared_with[doc_id][user_id]
            print(f"Role removed for user {user_id} in document {doc_id}.")
        else:
            print(f"User {user_id} is not shared with document {doc_id}.")

    def get_role(self, doc_id: int, user_id: int) -> Optional[str]:
        return self.shared_with.get(doc_id, {}).get(user_id, None)

    def remove_document(self, doc_id: int) -> None:
        if doc_id in self.shared_with:
            del self.shared_with[doc_id]
