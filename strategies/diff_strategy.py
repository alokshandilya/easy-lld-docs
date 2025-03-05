import difflib
from abc import ABC, abstractmethod


class DiffStrategy(ABC):
    @abstractmethod
    def calculate_diff(self, old_content: str, new_content: str) -> str:
        pass


class SimpleDiffStrategy(DiffStrategy):
    def calculate_diff(self, old_content: str, new_content: str) -> str:
        diff = difflib.unified_diff(
            old_content.splitlines(),
            new_content.splitlines(),
            lineterm="",
        )
        return "\n".join(diff)
