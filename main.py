import os

# The decky plugin module is located at decky-loader/plugin
# For easy intellisense checkout the decky-loader code repo
# and add the `decky-loader/plugin/imports` path to `python.analysis.extraPaths` in `.vscode/settings.json`
import decky # type: ignore
import asyncio
import datetime
from enum import Enum, auto
import abc

logger = decky.logger.getChild("decky-alarm")

class Ringer(abc.ABC):
    @abc.abstractmethod
    async def ring(self) -> None:
        raise NotImplemented()

class NotificationRinger(Ringer):
    EVENT_TYPE = "notification_ringer"

    def __init__(self, message: str) -> None:
        super().__init__()
        self.message = message

    async def ring(self) -> None:
        logger.debug("Notification ringer with message %s is rinning", self.message)
        await decky.emit(self.EVENT_TYPE, self.message)
 

class Alarm:
    class Repeat(Enum):
        NO=auto()
        ONCE=auto()
        CONTINIOUSLY=auto()
        CUSTOM=auto()

        def custom_repeat(self, count=int) -> None:
            self.repeat_count=count

    def __init__(self, alarm_time: datetime.datetime, ringer: Ringer, repeat: Repeat) -> None:
        self.alarm_time = alarm_time
        self.ringer = ringer
        self.repeat = repeat

    async def start_alarm(self) -> None:
        sleep_time: datetime.timedelta = self.alarm_time - datetime.datetime.now()
        logger.info("Setting alarm for %s, in %s", self.alarm_time, sleep_time)
        await asyncio.sleep(float(sleep_time.seconds))
        await self.ringer.ring()
        #TODO implement repeats


class Plugin:
    # A normal method. It can be called from the TypeScript side using @decky/api.
    async def add(self, left: int, right: int) -> int:
        return left + right

    async def long_running(self):
        await asyncio.sleep(15)
        # Passing through a bunch of random data, just as an example
        await decky.emit("test_event", "Hello from the backend!", True, 2)

    # Asyncio-compatible long-running code, executed in a task when the plugin is loaded
    async def _main(self):
        decky.logger.info("Decky alarm loaded")
        self.loop = asyncio.get_event_loop()

    # Function called first during the unload process, utilize this to handle your plugin being stopped, but not
    # completely removed
    async def _unload(self):
        decky.logger.info("Decky alarm unloaded")

    # Function called after `_unload` during uninstall, utilize this to clean up processes and other remnants of your
    # plugin that may remain on the system
    async def _uninstall(self):
        decky.logger.info("Decky alarm uninstalled")

    async def start_timer(self):
        self.loop.create_task(self.long_running())


    def time_as_datetime(self, time: datetime.time) -> datetime.datetime:
        date: datetime.date = datetime.date.today()
        if time < datetime.datetime.now().time():
            date += datetime.timedelta(days=1)
        return datetime.datetime.combine(date, time)

    async def set_alarm(self, time: str, message: str = None) -> None:
        logger.debug("Setting alarm for %s", time)
        alarm = Alarm(self.time_as_datetime(datetime.time.fromisoformat(time)), NotificationRinger(message), Alarm.Repeat.NO)
        self.loop.create_task(alarm.start_alarm())

    async def test_function(self) -> None:
        decky.logger.info("Test function called")
        await self.set_alarm("22:00", "Bedtime")