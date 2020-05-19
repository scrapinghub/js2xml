#!/usr/bin/env python
import sys
from argparse import ArgumentParser

import six

import js2xml


def main():
    ap = ArgumentParser()
    ap.add_argument('--debug', action='store_true')
    ap.add_argument('filenames', nargs='*', default=['-'])
    args = ap.parse_args()

    mode = 'rU' if six.PY2 else 'r'

    for fn in args.filenames:
        fo = sys.stdin if fn == '-' else open(fn, mode)
        parsed = js2xml.parse(fo.read())
        print(js2xml.pretty_print(parsed))


if __name__ == '__main__':
    sys.exit(main())
