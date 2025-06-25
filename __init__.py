"""
Dash Auto Save State Plugin

A Dash hook that automatically saves and restores component states to prevent data loss.
Supports localStorage persistence, cross-tab synchronization, and configurable exclusions.
"""

from .auto_save_state import AutoSaveState
from .hooks import auto_save_state_hook
