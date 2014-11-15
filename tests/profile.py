#!/usr/bin/env python
# -*- coding: utf-8 -*-

import js2xml
import os

TEST_DIR = os.path.dirname(__file__)

files = [
    os.path.join(TEST_DIR, 'samples/fullcalendar.js'),
    os.path.join(TEST_DIR, 'samples/fullcalendar.min.js'),
    os.path.join(TEST_DIR, 'samples/jquery.min.js'),
]
for filename in files:
    with open(filename) as f:
        jscode = f.read()

tree = js2xml.parse(jscode)
