from dataclasses import dataclass
from typing import Optional, List


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
    import_query: str
    verify_ssl: bool
    page_size: int
    schema: str
    timeout: int
    out: str
    cb_auth_conf: AuthenticationConfig

    @property
    def base(self) -> str:
        return f"{self.cb_auth_conf.root}/api/v3"
