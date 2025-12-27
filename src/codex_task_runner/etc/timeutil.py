from __future__ import annotations

import datetime as dt


def utc_stamp() -> str:
    now = dt.datetime.now(tz=dt.timezone.utc)
    return now.strftime("%Y%m%dT%H%M%SZ")
