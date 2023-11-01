from __future__ import annotations
from datetime import datetime, timezone, timedelta
from pytimeparse import parse
from ..util import validate_duration
from ..log import log
from ..reddit import reddit
from ..Botling import Botling


# TBD:
# - What if the queue listing caps out (presumably at 1000)? What even happens?



class QueueAgeWatcher(Botling):
    """Sends a modmail warning when an item stays too long in the queue.
    This tracks all items in your modqueue to remember their age, so it may not work well for subs with very large modqueues."""

    default_settings = {
        "threshold": "1 month",  # The maximum age of a queue item before a warning should be sent.
        "period": "10 seconds",  # How frequently to check the modqueue

        # Usually, a warning is sent for each stale item.
        # In single warning mode, only one warning will be sent when an item first stales, and no more will be sent until that item is handled.
        "single_warning_mode": {
            "enabled": False,
            "grace_period": "1 day"  # We don't want to send a new warning as soon as the stale item is taken care of, since presumably the mod will take care of other stale items right after, so we give a grace period before checking resumes.
        }
    }

    def validate_settings(self) -> None:
        validate_duration(self.DR.settings.threshold, key="threshold", nonzero=True)
        validate_duration(self.DR.settings.period, key="period", nonzero=True)
        assert isinstance(self.DR.settings.single_warning_mode.enabled, bool)
        validate_duration(self.DR.settings.single_warning_mode.grace_period, key="single_warning_mode.grace_period")

    def setup(self) -> None:
        # Parse durations
        self.threshold = parse(self.DR.settings.threshold)
        self.period = parse(self.DR.settings.period)
        self.single_warning_mode_grace_period = parse(self.DR.settings.single_warning_mode.grace_period)

        # Initialize storage
        self.DR.storage["ages"] = {}  # Ages for all items we've seen.
        self.DR.storage["last_alerted"] = None  # Time of the last alert, for single warning mode

        # Schedule periodic scan
        self.DR.scheduler.every(self.period).seconds.do(self.scan)

    def scan(self) -> None:
        # If we're in a grace period, don't bother pinging reddit
        if self.DR.storage["last_alerted"] and datetime.now(timezone.utc) - self.DR.storage["last_alerted"] < timedelta(seconds=self.single_warning_mode_grace_period):
            log.debug(f"Skipping sending an alert because we're in a grace period.")
            return

        # Iterate over the queue
        new_ages = {}
        for item in reddit.sub.mod.modqueue(limit=None):
            # If it's new, log the age

            # If it's old, copy its age and check if it's stale
            if False:
                new_ages[item.fullname] = self.DR.storage["ages"][item.fullname]
        
        # All items in ages that weren't seen during iteration won't be copied
            

        # If the queue size is healthy, mark that there's no active alert and quit
        if queue_size <= self.DR.settings.threshold:
            self.DR.storage["active_alert"] = False
            return

        # If there's already an active alert and allow_repeated_alerts is off, quit
        if not self.DR.settings.allow_repeated_alerts and self.DR.storage["active_alert"]:
            log.debug("Skipping sending an alert because there's already an active one.")
            return

        # The queue is unhealthy, so send an alert.
        log.info(f"The queue size is {queue_size}, which is above the threshold ({self.DR.settings.threshold}). Alerting mods.")

        # Send modmail
        reddit.DR.send_modmail(subject=f"The modqueue size has reached {queue_size}",
                               body=f"""The modqueue size has reached {queue_size}, which is more than the threshold of {self.DR.settings.threshold} allowed by your settings. Please tend to the queue.""")

        # Update storage
        self.DR.storage["active_alert"] = True
        self.DR.storage["last_alerted"] = datetime.now(timezone.utc)
