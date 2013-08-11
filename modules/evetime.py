import datetime
import logging
import threading
import time

from kitnirc.modular import Module


_log = logging.getLogger(__name__)


class EveTimeModule(Module):
    """A KitnIRC module that reports EVE time to channel."""

    def __init__(self, *args, **kwargs):
        super(EveTimeModule, self).__init__(*args, **kwargs)
        # For now, we'll just report to all listed channels every hour,
        # on the hour. Later on we can add configurable intervals.
        self.channels = list(self.controller.config.items("evetime"))
        self.last_report = datetime.datetime.utcnow()
        self._stop = False
        self.thread = threading.Thread(target=self.loop, name="evetime")
        self.thread.daemon = True

    def start(self, *args, **kwargs):
        super(EveTimeModule, self).start(*args, **kwargs)
        self._stop = False
        self.thread.start()

    def stop(self, *args, **kwargs):
        super(EveTimeModule, self).stop(*args, **kwargs)
        self.stop = True
        self.thread.join(2.0)
        if self.thread.is_alive():
            _log.warning("Evetime thread alive 2s after shutdown request.")

    def loop(self):
        _log.info("EVE time reporter running.")
        while not self._stop:
            now = datetime.datetime.utcnow()
            if now.hour != self.last_report.hour:
                self.report(now)
                self.last_report = now
            time.sleep(1)

    def report(self, dt):
        msg = dt.strftime("-- %H%M EVE Time --")
        for channel in self.channels:
            self.controller.client.msg(channel, msg)


# vim: set ts=4 sts=4 sw=4 et:
