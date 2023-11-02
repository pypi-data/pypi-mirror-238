""" Dates and times """

from typing import Optional
import datetime
import time
from datetime import timedelta
import copy

from .constants import DT_FMT_DATE, DT_FMT_SEC, DT_FMT_US, TESTING, DT_STR_TEST_US



def get_dt_now() -> datetime.datetime:
    """Get current datetime"""
    if TESTING[0]:
        return datetime.datetime.strptime(DT_STR_TEST_US, DT_FMT_US)
    else:
        return datetime.datetime.fromtimestamp(time.time())

def get_ts_now_formatted(fmt: str,
                         offset: Optional[datetime.timedelta] = None) \
        -> str:
    """Get formatted current timestamp with an optional offset."""
    ts_now = get_dt_now()
    if offset is not None:
        return (ts_now + offset).strftime(fmt)
    else:
        return ts_now.strftime(fmt)

def get_ts_now_str(mode: str,
                   offset: Optional[datetime.timedelta] = None) \
        -> str:
    """Get current timestamp"""
    assert mode in ['date', 's', 'ms', 'us']

    # infer format
    if mode == 'date':
        fmt = DT_FMT_DATE
    elif mode == 's':
        fmt = DT_FMT_SEC
    elif mode in ['ms', 'us']:
        fmt = DT_FMT_US
    else:
        raise NotImplementedError

    # get string
    ts: str = get_ts_now_formatted(fmt, offset=offset)

    # finishing touches
    if mode == 'ms':
        ts = ts[:-3] # trim last 3 fractional digits

    return ts


class TimeLock():
    """
    Utility for managing timed events. TimeLock forces a waiting period until the next point in time an integer multiple
    of intervals ahead of an initial starting time. This allows for triggering events at strict intervals where missed
    intervals are skipped.
    """
    def __init__(self,
                 dt_start: datetime.datetime,
                 interval: int, # interval between lock releases
                 progress_dur: Optional[int] = None, # how often to print update on waiting period (seconds)
                 verbose: bool = False):
        assert (dt_start - get_dt_now()).total_seconds() > 0

        self._dt_target = dt_start
        self._interval = interval
        self._progress_dur = progress_dur
        self._verbose = verbose

    def _wait_until_target(self):
        """Wait until current time catches up to target time."""
        while (t_wait := (self._dt_target - get_dt_now()).total_seconds()) > 0:
            if self._verbose:
                print(f'TimeLock: Waiting {t_wait} seconds until {self._dt_target}.')
            if self._progress_dur is not None:
                t_wait = min(t_wait, self._progress_dur)
            time.sleep(t_wait)

    def _advance_target(self):
        """Advance target time beyond the current time by the minimum integer multiple of the interval."""
        dt_now = get_dt_now()
        dt_target_orig = copy.copy(self._dt_target)
        t_elapsed = (dt_now - self._dt_target).total_seconds()
        if t_elapsed <= 0:
            return
        num_intervals_advance = int(t_elapsed / self._interval) + 1
        self._dt_target += timedelta(seconds=num_intervals_advance * self._interval)
        if self._verbose:
            print(f'TimeLock: Advancing time lock target from {dt_target_orig} to {self._dt_target}.')

    def acquire(self):
        """Acquire lock (i.e. advance target time in preparation for next release)"""
        self._advance_target()
        self._wait_until_target()