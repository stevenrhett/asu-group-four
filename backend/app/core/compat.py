"""
Runtime compatibility helpers.

Currently suppresses known third-party deprecation warnings emitted by lazy_model
until upstream releases an official fix compatible with Pydantic v3.
"""

from __future__ import annotations

import warnings

from pydantic.warnings import PydanticDeprecatedSince211

warnings.simplefilter("ignore", PydanticDeprecatedSince211)
