from __future__ import annotations

import logging
import time
from typing import Dict, List

from models import Action, Plan
from tools.base_tool import BaseTool
from tools.browser_tool import BrowserTool
from tools.chat_tool import ChatTool
from tools.clipboard_tool import ClipboardTool
from tools.file_tool import FileTool
from tools.folder_tool import FolderTool
from tools.input_tool import InputTool
from tools.media_tool import MediaTool
from tools.program_tool import ProgramTool
from tools.system_tool import SystemTool
from tools.window_tool import WindowTool

logger = logging.getLogger(__name__)

TOOLS: Dict[str, BaseTool] = {
    tool.name: tool
    for tool in [
        ProgramTool(), BrowserTool(), FileTool(), FolderTool(), MediaTool(),
        SystemTool(), ClipboardTool(), WindowTool(), InputTool(), ChatTool(),
    ]
}


def execute_plan(plan: Plan) -> List[str]:
    results: List[str] = []
    for step in plan.steps:
        results.append(execute_action(step))
        time.sleep(0.25)
    return results


def execute_action(step: Action) -> str:
    tool = TOOLS.get(step.tool)
    if tool is None:
        return f"ไม่รู้จัก tool '{step.tool}'"
    try:
        result = tool.run(step.action, step.target)
        logger.info("%s.%s(%r) -> %s", step.tool, step.action, step.target, result)
        return result
    except Exception as exc:
        logger.exception("Tool error: %s", exc)
        return f"ทำคำสั่งไม่สำเร็จ: {exc}"
