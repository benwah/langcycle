#!/bin/env python

import os
import logging
import sys


logging.basicConfig(level=logging.INFO)


def cycle_layout(layouts):
    layout = os. \
        popen("setxkbmap -query | grep layout | awk '{ print $2 }'"). \
        read(). \
        strip('\n')
    variant = os. \
        popen("setxkbmap -query | grep variant | awk '{ print $2 }'"). \
        read(). \
        strip('\n')
    variant = None if variant == '' else variant

    layout_variant = [layout, variant] if variant else [layout]
    next_layout_index = 0

    if layout_variant in layouts:
        next_layout_index = layouts.index(layout_variant) + 1
        if next_layout_index == len(layouts):
            next_layout_index = 0

    next_layout = layouts[next_layout_index]

    command = "setxkbmap %s" % next_layout[0]
    if len(next_layout) > 1:
        command = "%s %s" % (command, next_layout[1])

    change_layout_result = os.system(command)

    if change_layout_result != 0:
        logging.error('Failed to cycle keyboard layout using: %s' % command)
    else:
        logging.info('Successfully cycled keyboard layout using: %s' % command)


def help():
    print("""Usage: langycycle.py LAYOUT[:VARIANT] [LAYOUT[:VARIANT]]...

Cycles through keyboard layouts and variants using setxkbmap.

example: langycycle.py us fr ca:eng ca:fr ca:multi""")


def main():
    if len(sys.argv[1:]) == 0 or sys.argv[1] in ('help', '-h', '--help'):
        help()
        sys.exit()

    layouts = map(
        lambda x: x.split(':'),
        sys.argv[1:]
    )

    cycle_layout(list(layouts))

if __name__ == '__main__':
    main()
