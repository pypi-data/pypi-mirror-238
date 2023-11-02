#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from __future__ import annotations
from datetime import datetime
from enum import Enum
from functools import total_ordering

from de.p1st.monitor.print_util import print_warning, print_crit


# https://docs.python.org/3/library/functools.html#functools.total_ordering
@total_ordering
class WarnLevel(Enum):
    NONE = 0  # Not a warning. Everything is ok.
    LOW = 1
    NORMAL = 2
    HIGH = 3

    def __eq__(self, other):
        if isinstance(other, WarnLevel):
            return self.value == other.value
        return NotImplemented

    def __lt__(self, other):
        if isinstance(other, WarnLevel):
            return self.value < other.value
        return NotImplemented


class WarnMessage:
    def __init__(self, level: WarnLevel, date: datetime = None, message: str = None):
        """
        @param level:
        @param date: Required, except if `WarnLevel.NONE` given.
        @param message: Required, except if `WarnLevel.NONE` given.
        """
        self.level = level
        self.date = date
        self.message = message

        if self.level != WarnLevel.NONE:
            if self.date is None:
                raise ValueError()
            if self.message is None:
                raise ValueError()
        if self.level == WarnLevel.NONE:
            if self.date is not None:
                raise ValueError()
            if self.message is not None:
                raise ValueError()

    def is_warning(self) -> bool:
        return self.level > WarnLevel.NONE

    def print(self) -> WarnMessage:
        """
        return: self
        """
        if self.level == WarnLevel.NONE:
            pass
        elif self.level == WarnLevel.NORMAL:
            print_warning(self.formatted_message())
        elif self.level == WarnLevel.HIGH:
            print_crit(self.formatted_message())
        else:
            raise NotImplementedError()

        return self

    def formatted_message(self) -> str:
        return self.prefix() + self.message

    def prefix(self) -> str:
        if self.level == WarnLevel.NONE:
            raise ValueError()
        if self.level > WarnLevel.NORMAL:
            return f'[CRITICAL] {self.date}: '
        return f'{self.date}: '

