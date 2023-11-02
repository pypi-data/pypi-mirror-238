"""

A pybind11 binding for Aria Synthetic Environment calibration module
"""
from __future__ import annotations
from projectaria_tools.project.ase import get_ase_rgb_calibration
from . import interpreter
from . import readers
__all__ = ['get_ase_rgb_calibration', 'interpreter', 'readers']
