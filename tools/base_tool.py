from __future__ import annotations

from abc import ABC, abstractmethod
from typing import FrozenSet


class BaseTool(ABC):
    name: str
    actions: FrozenSet[str]

    @abstractmethod
    def run(self, action: str, target: str = "") -> str:
        raise NotImplementedError

    def validate(self, action: str) -> None:
        if action not in self.actions:
            raise ValueError(f"{self.name} ไม่รองรับ action '{action}'")
