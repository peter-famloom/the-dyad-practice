#!/usr/bin/env python3
"""Tests for regen_directory_index — peak extraction + idempotent splice. Runnable standalone."""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from regen_directory_index import HEADING, peak, render, splice  # noqa: E402


def test_peak_em_dash():
    assert peak("keeping the bond covalent — every +1 enters by survival") == \
        "keeping the bond covalent"


def test_peak_colon():
    assert peak("Wu-wei Cognitive Offloading: Safely pushed the tenet") == \
        "Wu-wei Cognitive Offloading"


def test_peak_first_delim_wins():
    # an em-dash earlier than a later colon → split on the em-dash, not the colon
    assert peak("raising self-healing efficacy — resuscitation: toward rarely-needed") == \
        "raising self-healing efficacy"


def test_peak_plain_passthrough():
    assert peak("Swing trading strategy backtesting") == "Swing trading strategy backtesting"


def test_peak_collapses_whitespace_and_trailing_dot():
    assert peak("commons process-integrity.") == "commons process-integrity"


def test_peak_truncates_to_max():
    out = peak("x" * 200)
    assert len(out) == 100 and out.endswith("…")


def test_splice_is_idempotent():
    section = render()
    once = splice("# Title\n\nintro\n\n" + section, section)
    twice = splice(once, section)
    assert once == twice
    assert HEADING in once


def test_splice_appends_when_heading_absent():
    out = splice("# Title\n\nno section here\n", "## Registered Dyads\n\nbody")
    assert out.count("## Registered Dyads") == 1
    assert out.rstrip().endswith("body")


if __name__ == "__main__":
    tests = [v for k, v in sorted(globals().items()) if k.startswith("test_")]
    for fn in tests:
        fn()
        print("PASS %s" % fn.__name__)
    print("All %d tests passed." % len(tests))
