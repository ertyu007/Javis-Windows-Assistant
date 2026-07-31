from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Dict, List


@dataclass
class Action:
    tool: str
    action: str
    target: str = ""

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "Action":
        return cls(
            tool=str(data.get("tool", "chat")).strip().lower(),
            action=str(data.get("action", "answer")).strip().lower(),
            target=str(data.get("target", "")).strip(),
        )


@dataclass
class Plan:
    reply: str = ""
    steps: List[Action] = field(default_factory=list)
    requires_confirmation: bool = False

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "Plan":
        raw_steps = data.get("steps")
        if not isinstance(raw_steps, list):
            raw_steps = [data] if data.get("tool") else []

        steps = [Action.from_dict(item) for item in raw_steps if isinstance(item, dict)]
        return cls(
            reply=str(data.get("reply", "")).strip(),
            steps=steps,
            requires_confirmation=bool(data.get("requires_confirmation", False)),
        )
