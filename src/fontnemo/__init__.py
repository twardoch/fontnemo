#!/usr/bin/env python3
# this_file: src/fontnemo/__init__.py
"""fontnemo - CLI tool for modifying font family names."""

try:
    from fontnemo._version import __version__
except ImportError:
    __version__ = "0.0.0+unknown"

__all__ = ["__version__"]
