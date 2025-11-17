"""
Runtime compatibility helpers.

Currently suppresses known third-party deprecation warnings emitted by lazy_model
until upstream releases an official fix compatible with Pydantic v3.
"""

from __future__ import annotations

import warnings

try:
    from pydantic.warnings import PydanticDeprecatedSince211
    warnings.simplefilter("ignore", PydanticDeprecatedSince211)
except ImportError:
    # PydanticDeprecatedSince211 may not exist in all Pydantic versions
    # This is fine - we'll just skip the warning suppression
    pass
