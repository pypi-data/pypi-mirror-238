from __future__ import annotations
from datetime import datetime, timezone, timedelta
from praw.models import Submission
from ..reddit import reddit
from .TimeGuardedStream import TimeGuardedStream

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from typing import Iterable


class TimeDelayPostStream(TimeGuardedStream[Submission]):
    """A stream of posts with a time delay."""

    def get_items_raw(self) -> Iterable[Submission]:
        return reddit.sub.new(limit=None)

    def id(self, item: Submission) -> str:
        return item.id

    def timestamp(self, item: Submission) -> datetime:
        return datetime.fromtimestamp(item.created_utc, timezone.utc)

    def get_latest_item(self) -> Submission | None:
        return next(reddit.sub.new(limit=1), None)


        from datetime import datetime, timezone, timedelta
        curtime = datetime.now(timezone.utc)

        for item in reddit.sub.new(limit=None):
            if abs(curtime - datetime.fromtimestamp(item.created_utc, timezone.utc)) >= timedelta(days=3):
                last_expired = item
                break
            log.warning((item.fullname, datetime.fromtimestamp(item.created_utc, timezone.utc).isoformat()))

        log.info("\n")
        log.warning((last_expired.fullname, datetime.fromtimestamp(last_expired.created_utc, timezone.utc).isoformat()))
        log.info("\n")

        curtime += timedelta(days=1)
        for item in reddit.sub.new(limit=None, params={"before": last_expired.fullname}):
            if abs(curtime - datetime.fromtimestamp(item.created_utc, timezone.utc)) >= timedelta(days=3):
                last_expired = item
                break
            log.warning((item.fullname, datetime.fromtimestamp(item.created_utc, timezone.utc).isoformat()))

        log.info("\n")
        log.warning((last_expired.fullname, datetime.fromtimestamp(last_expired.created_utc, timezone.utc).isoformat()))