from quick_commands import quick_plan


def test_open_youtube():
    plan = quick_plan("เปิด YouTube")
    assert plan is not None
    assert plan.steps[0].tool == "browser"


def test_shutdown_requires_confirmation():
    plan = quick_plan("ปิดเครื่อง")
    assert plan is not None
    assert plan.requires_confirmation is True


def test_hotkey():
    plan = quick_plan("กด ctrl+s")
    assert plan is not None
    assert plan.steps[0].action == "hotkey"
