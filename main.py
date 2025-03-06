from exceptions import PermissionDeniedError
from managers.document_manager import DocumentManager
from managers.sharing_manager import SharingManager
from managers.version_manager import VersionManager
from models.user import User
from strategies.diff_strategy import SimpleDiffStrategy
from utils.display_utils import print_collaborators, print_versions


def main():
    # Initialize components
    diff_strategy = SimpleDiffStrategy()
    version_manager = VersionManager(diff_strategy)
    sharing_manager = SharingManager()
    doc_manager = DocumentManager(sharing_manager, version_manager)

    # Create users
    users = {
        1: User(1, "Alok"),
        2: User(2, "Aryan"),
        3: User(3, "Tridip"),
        4: User(4, "Chaya"),
    }
    owner = users[1]
    editor = users[2]
    viewer = users[3]
    stranger = users[4]

    # Create document
    doc = doc_manager.create_document(owner, "Initial content")
    doc_id = doc.doc_id
    print(f"Document created with ID: {doc_id}")

    # Share document
    sharing_manager.share_document(doc_id, editor.user_id, "editor")
    sharing_manager.share_document(doc_id, viewer.user_id, "viewer")

    # Test 1: List collaborators
    print_collaborators(doc_manager, sharing_manager, users, doc_id)

    # Test 2: Version history and diffs
    print("\n--- Editing Process ---")
    try:
        doc_manager.edit_document(editor, doc_id, "Editor edited content v2")
        doc_manager.edit_document(owner, doc_id, "Owner edited content v3")
        doc_manager.edit_document(viewer, doc_id, "Viewe edited content v4")
    except PermissionDeniedError as e:
        print(f"Edit attempt failed: {e}")

    print_versions(version_manager, doc_id)

    # Test 3: Permission tests
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
