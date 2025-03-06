from typing import Dict

from exceptions import PermissionDeniedError
from managers.document_manager import DocumentManager
from managers.sharing_manager import SharingManager
from managers.version_manager import VersionManager
from models.user import User
from strategies.diff_strategy import SimpleDiffStrategy
from utils.display_utils import print_collaborators, print_versions


def main() -> None:
    diff_strategy: SimpleDiffStrategy = SimpleDiffStrategy()
    version_manager: VersionManager = VersionManager(diff_strategy)
    doc_manager: DocumentManager = DocumentManager(None, version_manager)
    sharing_manager: SharingManager = SharingManager(doc_manager)

    doc_manager.sharing_manager = sharing_manager

    # Create users
    users: Dict[int, User] = {
        1: User(1, "Alok"),
        2: User(2, "Aryan"),
        3: User(3, "Tridip"),
        4: User(4, "Vivek"),
    }
    owner = users[1]
    editor = users[2]
    viewer = users[3]
    stranger = users[4]

    # Create document
    doc = doc_manager.create_document(owner, "Initial content")
    doc_id = doc.doc_id
    print(f"Document created with ID: {doc_id}")

    # Share document with valid roles
    try:
        sharing_manager.share_document(doc_id, editor.user_id, "editor")
        sharing_manager.share_document(doc_id, viewer.user_id, "viewer")
        print("Sharing successful!")
    except ValueError as e:
        print(f"Sharing failed: {e}")

    # Test 1: List collaborators before removal
    print("\n--- Collaborators Before Removal ---")
    print_collaborators(doc_manager, sharing_manager, users, doc_id)

    # # Test 2: Owner removes editor role
    # print("\n--- Removing Editor Role ---")
    # try:
    #     sharing_manager.remove_role(doc_id, owner.user_id, editor.user_id)
    # except PermissionDeniedError as e:
    #     print(f"Error: {e}")

    # Test 3: List collaborators after removal
    print("\n--- Collaborators After Removal ---")
    print_collaborators(doc_manager, sharing_manager, users, doc_id)

    # Test 4: Stranger tries to remove role (should fail)
    print("\n--- Stranger Attempts to Remove Role ---")
    try:
        sharing_manager.remove_role(doc_id, stranger.user_id, viewer.user_id)
    except PermissionDeniedError as e:
        print(f"Error: {e}")

    # # Test 5: Owner removes viewer role
    # print("\n--- Removing Viewer Role ---")
    # try:
    #     sharing_manager.remove_role(doc_id, owner.user_id, viewer.user_id)
    # except PermissionDeniedError as e:
    #     print(f"Error: {e}")

    # Test 6: List collaborators after final removal
    print("\n--- Collaborators After Final Removal ---")
    print_collaborators(doc_manager, sharing_manager, users, doc_id)

    # Test 7: Version history and diffs
    print("\n--- Editing Process ---")

    editor_content: str = """
    Hello, I am Editor. I am editing this document.
    this is only for testing the version history and diffs.

    Nothing serious here.
    """

    owner_content: str = """
    Hello, I am Owner. I am editing this document.

    This is only for testing the version history and diffs.
    Remember, I am the owner of this document.
    """

    try:
        doc_manager.edit_document(editor, doc_id, editor_content)
        doc_manager.edit_document(owner, doc_id, owner_content)
        doc_manager.edit_document(viewer, doc_id, "Viewe edited content v4")
    except PermissionDeniedError as e:
        print(f"Edit attempt failed: {e}")

    print_versions(version_manager, doc_id)

    # Test 8: Permission tests
    print("\n--- Permission Tests ---")

    # Stranger tries to edit
    try:
        doc_manager.edit_document(stranger, doc_id, "Malicious edit")
    except PermissionDeniedError as e:
        print(f"Stranger edit attempt: {e}")

    # Viewer tries to edit
    try:
        doc_manager.edit_document(viewer, doc_id, "Viewer edit")
    except PermissionDeniedError as e:
        print(f"Viewer edit attempt: {e}")

    # Editor successfully edits
    try:
        doc_manager.edit_document(editor, doc_id, "Editor approved")
        print("Editor edit successful!")
    except PermissionDeniedError as e:
        print(f"Editor edit failed: {e}")

    # Owner successfully edits
    try:
        doc_manager.edit_document(owner, doc_id, "Owner approved")
        print("Owner edit successful!")
    except PermissionDeniedError as e:
        print(f"Owner edit failed: {e}")

    # Delete test
    print("\n--- Delete Test ---")
    try:
        doc_manager.delete_document(viewer, doc_id)
    except PermissionDeniedError as e:
        print(f"Viewer delete attempt: {e}")

    try:
        doc_manager.delete_document(editor, doc_id)
    except PermissionDeniedError as e:
        print(f"Editor delete attempt: {e}")

    try:
        doc_manager.delete_document(owner, doc_id)
        print("Owner successfully deleted document")
    except PermissionDeniedError as e:
        print(f"Owner delete failed: {e}")


if __name__ == "__main__":
    main()
