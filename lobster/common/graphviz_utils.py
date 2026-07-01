#!/usr/bin/env python3
#
# LOBSTER - Lightweight Open BMW Software Traceability Evidence Report
# Copyright (C) 2025 Bayerische Motoren Werke Aktiengesellschaft (BMW AG)
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as
# published by the Free Software Foundation, either version 3 of the
# License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU
# Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public
# License along with this program. If not, see
# <https://www.gnu.org/licenses/>.
"""Shared Graphviz utilities for LOBSTER report tools."""

import subprocess
from typing import Optional


def is_dot_available(dot: Optional[str] = None) -> bool:
    """Return True if the ``dot`` executable (Graphviz) is on PATH.

    Args:
        dot: Optional explicit path to the ``dot`` binary.  When ``None``
            (default) the system PATH is searched.

    Returns:
        ``True`` if Graphviz ``dot`` is available, ``False`` otherwise.
    """
    try:
        subprocess.run(
            [dot if dot else "dot", "-V"],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            encoding="UTF-8",
            check=True,
            timeout=5,
        )
        return True
    except (FileNotFoundError, subprocess.TimeoutExpired,
            subprocess.CalledProcessError):
        return False
