#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import sys


# https://www.freedesktop.org/software/systemd/man/latest/sd-daemon.html
#
# define SD_EMERG   "<0>"  /* system is unusable */
# define SD_ALERT   "<1>"  /* action must be taken immediately */
# define SD_CRIT    "<2>"  /* critical conditions */
# define SD_ERR     "<3>"  /* error conditions */
# define SD_WARNING "<4>"  /* warning conditions */
# define SD_NOTICE  "<5>"  /* normal but significant condition */
# define SD_INFO    "<6>"  /* informational */
# define SD_DEBUG   "<7>"  /* debug-level messages */

def print_emerg(message: object):
    print(f'<0> {message}', file=sys.stderr)


def print_alert(message: object):
    print(f'<1> {message}', file=sys.stderr)


def print_crit(message: object):
    print(f'<2> {message}', file=sys.stderr)


def print_err(message: object):
    print(f'<3> {message}', file=sys.stderr)


def print_warning(message: object):
    print(f'<4> {message}', file=sys.stderr)


def print_notice(message: object):
    print(f'<5> {message}', file=sys.stdout)


def print_info(message: object):
    print(f'<6> {message}', file=sys.stdout)


def print_debug(message: object):
    print(f'<7> {message}', file=sys.stdout)
