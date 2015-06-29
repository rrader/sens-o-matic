import asyncio
from rx.concurrency import AsyncIOScheduler
from rx.disposables import SingleAssignmentDisposable, CompositeDisposable, Disposable


class MyScheduler(AsyncIOScheduler):
    def schedule_periodic(self, period, action, state=None):
        """Schedules an action to be executed periodically.

        Keyword arguments:
        duetime -- {timedelta} Relative time after which to execute the action.
        action -- {Function} Action to be executed.

        Returns {Disposable} The disposable object used to cancel the scheduled
        action (best effort)."""

        scheduler = self
        seconds = self.to_relative(period)/1000.0
        if seconds == 0:
            return scheduler.schedule(action, state)

        disposable = SingleAssignmentDisposable()

        def interval():
            disposable.disposable = action(state)
            scheduler.schedule_periodic(period, action, state)

        handle = [self.loop.call_later(seconds, interval)]

        def dispose():
            # nonlocal handle
            handle[0].cancel()

        return CompositeDisposable(disposable, Disposable(dispose))

loop = asyncio.get_event_loop()
aio_scheduler = MyScheduler(loop=loop)
