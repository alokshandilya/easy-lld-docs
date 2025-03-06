from typing import TYPE_CHECKING, Any, Dict

from exceptions import DocumentNotFoundError
from models.user import User

if TYPE_CHECKING:
    from managers.document_manager import DocumentManager
    from managers.sharing_manager import SharingManager


def print_collaborators(
    doc_manager: "DocumentManager",
    sharing_manager: "SharingManager",
    users: Dict[int, "User"],
    doc_id: int,
) -> None:
    try:
        doc = doc_manager.get_document(doc_id)
        owner = users[doc.owner_id]
        shared = sharing_manager.shared_with.get(doc_id, {})

        print("\nDocument Collaborators:")
        print(f"- {owner.name} (Owner)")
        for user_id, role in shared.items():
            user = users[user_id]
            print(f"- {user.name} ({role.capitalize()})")

    except DocumentNotFoundError as e:
        print(f"Error: {e}")


def print_versions(version_manager: Any, doc_id: int) -> None:
    try:
        versions = version_manager.get_versions(doc_id)
        print(f"\nVersions for Document {doc_id}:")
        for version in versions:
            print(f"Version {version.version_number} ({version.timestamp})")

        # diffs between consecutive versions
        for i in range(1, len(versions)):
            diff = version_manager.get_version_diff(doc_id, i, i + 1)
            print(f"\nDiff between v{i} and v{i+1}:")
            print(diff or "No changes")

    except DocumentNotFoundError as e:
        print(f"Error: {e}")
