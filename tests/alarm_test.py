from typing import Any
import decky # type: ignore
import asyncio
import sys
import os
import test_utils as test_utils
import datetime
import pytest

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import main

@pytest.mark.asyncio
async def test_notification_ringer():
    test_message = "test message"
    plugin = main.Plugin()
    await plugin._main()
    events: list[test_utils.Emit] = []
    def callback(event: str, args: Any, events: list[str]=events):
        events.append(test_utils.Emit(event, args))
    test_utils.emit_callback = callback

    alarm_time: datetime = datetime.datetime.now() + datetime.timedelta(seconds=0.001)
    await plugin.set_alarm(alarm_time.time().isoformat(), test_message)
    assert len(events) == 0
    await asyncio.sleep(0.001)
    assert len(events) == 1
    assert events[0].event == main.NotificationRinger.EVENT_TYPE
    assert events[0].args[0] == test_message

@pytest.mark.asyncio
async def test_timer():
    test_message = "timer test"
    plugin = main.Plugin()
    await plugin._main()
    events: list[test_utils.Emit] = []
    def callback(event: str, args: Any, events: list[str]=events):
        events.append(test_utils.Emit(event, args))
    test_utils.emit_callback = callback

    await plugin.set_timer(0, 1, test_message)
    assert len(events) == 0
    await asyncio.sleep(1)
    assert len(events) == 1
    assert events[0].event == main.NotificationRinger.EVENT_TYPE
    assert events[0].args[0] == test_message

