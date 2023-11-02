#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from datetime import datetime, timezone

from de.p1st.monitor.print_util import print_debug


def test():
    dt = datetime.now()

    print_debug('non UTC:')
    print_debug(dt)

    print_debug('\nUTC:')
    print_debug(now())
    print_debug(to_str(now()))
    print_debug(now_str())
    print_debug(from_str(to_str(now())))

    print_debug('\nlocalized:')
    print_debug(dt.tzinfo)
    dt = dt.replace(tzinfo=timezone.utc)
    print_debug(dt)


def now() -> datetime:
    return datetime.now(timezone.utc)


def now_str() -> str:
    return to_str(now())


def to_str(dt: datetime) -> str:
    return dt.strftime(fmt())


def from_str(dt_str: str) -> datetime:
    dt = datetime.strptime(dt_str, fmt())
    return dt.replace(tzinfo=timezone.utc)


def fmt() -> str:
    return '%Y%m%dT%H%M%S'


def fmt_len() -> int:
    return 13


if __name__ == '__main__':
    test()
