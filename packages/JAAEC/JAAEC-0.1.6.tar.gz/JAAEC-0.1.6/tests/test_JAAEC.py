#!/usr/bin/env python

"""Tests for `JAAEC` package."""


import unittest

from JAAEC import JAAEC


class TestJaaec(unittest.TestCase):
    """Tests for `JAAEC` package."""

    def testImport(self):
        try:
            from JAAEC import JAAEC
        except ImportError:
            self.fail("Was not able to import JAAEC.")

    def testJAAEC(self):
        try:
            from JAAEC import JAAEC
            JAAEC.AmazingAutoEncoder((1, 10_000, 8), (1, 32), 1e-6)
        except ImportError:
            self.fail("Was not able to import JAAEC.")
        except:
            self.fail("Was not able to instantiate Amazing Autoencoder.")
