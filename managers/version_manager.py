from exceptions import DocumentNotFoundError
from models.version import DocumentVersion


class VersionManager:
    def __init__(self, diff_strategy):
        self.versions = {}
        self.diff_strategy = diff_strategy

    def save_version(self, doc_id: int, content: str):
        if doc_id not in self.versions:
            self.versions[doc_id] = []
        version_number = len(self.versions[doc_id]) + 1
        self.versions[doc_id].append(DocumentVersion(version_number, content))

    def get_versions(self, doc_id: int):
        if doc_id not in self.versions:
            raise DocumentNotFoundError(f"Document {doc_id} not found")
        return self.versions[doc_id]

    def get_version_diff(self, doc_id: int, v1: int, v2: int) -> str:
        versions = self.get_versions(doc_id)
        old = next(v.content for v in versions if v.version_number == v1)
        new = next(v.content for v in versions if v.version_number == v2)
        return self.diff_strategy.calculate_diff(old, new)

    def remove_document(self, doc_id: int):
        if doc_id in self.versions:
            del self.versions[doc_id]
