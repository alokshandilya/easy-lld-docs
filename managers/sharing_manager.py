class SharingManager:
    def __init__(self):
        self.shared_with = {}

    def share_document(self, doc_id: int, user_id: int, role: str):
        if doc_id not in self.shared_with:
            self.shared_with[doc_id] = {}
        self.shared_with[doc_id][user_id] = role

    def get_role(self, doc_id: int, user_id: int) -> str:
        return self.shared_with.get(doc_id, {}).get(user_id, None)

    def remove_document(self, doc_id: int):
        if doc_id in self.shared_with:
            del self.shared_with[doc_id]
