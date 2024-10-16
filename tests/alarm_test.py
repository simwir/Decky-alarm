from typing import Any
import decky # type: ignore
import asyncio
import sys
import os
import setup
import datetime
import pytest

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import main


def test_call_test_function():
    plugin = main.Plugin()
    asyncio.run(plugin.test_function(), debug=True)

@pytest.mark.asyncio
async def test_notification_ringer():
    plugin = main.Plugin()
    await plugin._main()
    events = []
    def callback(event: str, *args: Any, events: list[str]=events):
        events.append(event)
    setup.emit_callback = callback
    alarm_time: datetime = datetime.datetime.now() + datetime.timedelta(seconds=0.5)
    await plugin.set_alarm(alarm_time.time().isoformat())
    await asyncio.sleep(1)
    assert len(events) == 1
    assert events[0] == main.NotificationRinger.EVENT_TYPE
