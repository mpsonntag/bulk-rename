"""
Copyright (c) 2017, Michael Sonntag (sonntag@bio.lmu.de)

All rights reserved.

Redistribution and use in source and binary forms, with or without
modification, are permitted under the terms of the BSD License. See
LICENSE file in the root of the project.
"""

import unittest


class DependencyTest(unittest.TestCase):
    """
    This class checks for non python gtk3 dependencies.

    This Class will be removed, it is testing how travis and conda
    can play nice with gtk3.
    """
    def test_gi_dependency(self):
        has_error = False
        try:
            import gi
        except (ImportError, ValueError) as _:
            has_error = True

        self.assertFalse(has_error)

    def test_pygtkcompat(self):
        has_error = False
        try:
            import gi
            import pygtkcompat
            pygtkcompat.enable()
            pygtkcompat.enable_gtk(version='3.0')
        except (ImportError, ValueError) as _:
            has_error = True

        self.assertFalse(has_error)

    def test_gtk(self):
        has_error = False
        try:
            import gi
            import pygtkcompat
            pygtkcompat.enable()
            pygtkcompat.enable_gtk(version='3.0')
            import gtk
        except (ImportError, ValueError) as _:
            has_error = True

        self.assertFalse(has_error)

    def test_gobject(self):
        has_error = False
        try:
            import gi
            import pygtkcompat
            pygtkcompat.enable()
            pygtkcompat.enable_gtk(version='3.0')
            import gtk
            import gobject
        except (ImportError, ValueError) as _:
            has_error = True

        self.assertFalse(has_error)
