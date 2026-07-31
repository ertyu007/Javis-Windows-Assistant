from __future__ import annotations

from models import Plan

DANGEROUS = {
    ("system", "shutdown"),
    ("system", "restart"),
    ("system", "sleep"),
}


def needs_confirmation(plan: Plan) -> bool:
    if plan.requires_confirmation:
        return True
    return any((step.tool, step.action) in DANGEROUS for step in plan.steps)
