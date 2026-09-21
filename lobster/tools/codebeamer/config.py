# LOBSTER - Lightweight Open BMW Software Traceability Evidence Report
# Copyright (C) 2025-2026 Bayerische Motoren Werke Aktiengesellschaft (BMW AG)
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

from dataclasses import dataclass
from typing import Callable, Optional, List, Union


@dataclass
class AuthenticationConfig:
    token: Optional[str]
    user: Optional[str]
    password: Optional[str]
    root: str


@dataclass
class Config:
    num_request_retry: int
    retry_error_codes: List
    references: dict
    import_tagged: str
    import_query: Union[str, int]
    baseline_id: Optional[int]
    verify_ssl: bool
    page_size: int
    schema: str
    timeout: int
    out: str
    cb_auth_conf: AuthenticationConfig
    item_to_text: Optional[Callable[[dict], Optional[str]]] = None

    @property
    def base(self) -> str:
        return f"{self.cb_auth_conf.root}/api/v3"
