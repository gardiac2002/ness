#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
test_ness
----------------------------------

Tests for `ness` module.
"""

import pytest


import ness


def test_parse_report():
    report = ness.from_file('sample.nessus')
    assert len(report.get('hosts')) == 1
    print(report)


def test_parse_from_file():
    with pytest.raises(FileNotFoundError):
        ness.from_file('not-existant-path')


